import json
import operator
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from typing import Callable

OPERATOR_MAP = {
    '<': operator.lt,
    '>': operator.gt,
    '<=': operator.le,
    '>=': operator.ge,
    '==': operator.eq,
}

@dataclass
class PackageSpec():
    name: str
    version_comparator: str
    version_string: str

    def __str__(self):
        if self.version_comparator or self.version_string:
            return f"{self.name}{self.version_comparator}{self.version_string}"
        else:
            return self.name


@dataclass(frozen=True)
class Requirement():

    # The package_name, according to pip. Can optionally include a version
    # as in "somepackage==3.2.1" or "somepackage>=3.2.1"
    package_spec: str
    # A callable that takes the package name and raises an exception if the
    # package isn't installed. Often the module has the same name as the
    # package, and you can just use `__import__`. If this isn't provided, we'll
    # try using `pip show [packagename]` to find out if the package is
    # installed.
    import_checker: Callable[[str], None] = None

    @property
    def package_spec_regex(self):
        try:
            return self.__class__._package_spec_regex
        except AttributeError:
            # TODO: Make sure regex is robust in the face of weird package names / versions
            r = re.compile(
                r'^(?P<name>[\w-]+)(?:(?P<comparator>(?:<)|(?:>)|(?:<=)|(?:>=)|(?:==))(?P<version_string>[\w.-]+))?$'
            )
            self.__class__._package_spec_regex = r
            return r

    def parsed_package_spec(self) -> PackageSpec:
        """Parse a package spec like "somepackage>=3.2.1" into a PackageSpec
        containing the name, comparator and version string"""
        m = self.package_spec_regex.match(self.package_spec)
        if not m:
            raise RuntimeError(f"Could not parse package spec {self.package_spec}")
        return PackageSpec(
            name=m.group('name'),
            version_comparator=m.group('comparator'),
            version_string=m.group('version_string')
        )


class PythonRequirements():
    _pip_is_set_up = False
    _requirements_are_ok = False

    def __init__(self, packages):
        """packages should be a list or other iterable, whose items are either
        package names, or tuples of package names and (optionally) version
        specs and module names"""
        self._requirements = []
        for p in packages:
            if isinstance(p, str):
                self._requirements.append(
                    Requirement(p)
                )
            elif isinstance(p, tuple):
                self._requirements.append(
                    Requirement(*p)
                )
            else:
                raise RuntimeError("Specified package has invalid type")

    @property
    def version_parser(self):
        """Return a parser that can be used to convert version strings into
        objects that can be usefully compared. This is fairly dubious as it
        imports pip's vendored version of version, but it's working here so
        let's run with it for now."""
        try:
            return self._version_parser
        except AttributeError:
            if not self._pip_is_set_up:
                self.setup_pip()
            from pip._vendor.packaging.version import Version
            self.__class__._version_parser = Version
            return self._version_parser
    
    def setup_pip(self):
        global Version
        if self._pip_is_set_up:
            print("Pip already set up")
            return
        try:
            # Check if pip is already installed
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "pip",
                    "--version"
                ],
                check=True
            )
        except subprocess.CalledProcessError:
            # Conceivably we might not have either pip or ensurepip, but let's
            # assume we do as otherwise it's game over.
            print("Bootstrapping pip...")
            import ensurepip
            ensurepip.bootstrap()
            os.environ.pop("PIP_REQ_TRACKER", None)
        self.__class__._pip_is_set_up = True

    @property
    def requirements_installed(self):
        return not self.find_missing_requirements()

    def find_missing_requirements(self):
        if self._requirements_are_ok:
            # Let's assume if there were no missing requirements before, there
            # probably still aren't.
            return []

        self.setup_pip()

        requirements_to_check_by_pip = set()
        missing_requirements = set()
        for r in self._requirements:
            if r.import_checker:
                try:
                    requirement_ok = r.import_checker(r.parsed_package_spec().name)
                except Exception as e:
                    requirement_ok = False
                    print(
                        f"Import check for package {r} "
                        f"raised the following error:\n{e}"
                    )
                else:
                    if not requirement_ok:
                        print(
                            f"Import check for package {r} "
                            f"returned False"
                        )
                if not requirement_ok:
                    missing_requirements.add(r)
            else:
                requirements_to_check_by_pip.add(r)

        if requirements_to_check_by_pip:
            print("Checking for the following package names using pip:")
            print(", ".join([
                r.package_spec for r in requirements_to_check_by_pip
            ]))
            print(
                "You could avoid this step by adding import checkers for "
                "these packages.\n"
            )
            result = subprocess.run(
                [
                    sys.executable,
                    '-m',
                    'pip',
                    'list',
                    '--format',
                    'json',
                ],
                check=True,
                capture_output=True
            )
            found_packages = {
                p['name']: p['version']
                for p in json.loads(result.stdout.decode())
            }
            for requirement in requirements_to_check_by_pip:
                package_spec = requirement.parsed_package_spec()
                if package_spec.name in found_packages:
                    found_version = found_packages[package_spec.name]
                    if package_spec.version_string:
                        op = OPERATOR_MAP[package_spec.version_comparator]
                        version_is_ok = op(
                            self.version_parser(found_version),
                            self.version_parser(package_spec.version_string)
                        )
                    else:
                        version_is_ok = True
                    if version_is_ok:
                        print(
                            f"Found installed {package_spec.name}=={found_version}, "
                            f"which satisfies requirement {package_spec}"
                        )
                    else:
                        print(
                            f"Found installed {package_spec.name}=={found_version}, "
                            f"but we need {package_spec}"
                        )
                        missing_requirements.add(requirement)
                else:
                    print(f"Did not find any installed {package_spec.name}")
                    missing_requirements.add(requirement)

        if not missing_requirements:
            self.__class__._requirements_are_ok = True
        return missing_requirements

    def install_requirements(self):
        print("Bootstrapping dependencies (may take a long time)...")
        missing_requirements = self.find_missing_requirements()
        # preserve original ordering:
        for requirement in self._requirements:
            if requirement in missing_requirements:
                print(f"Installing package {requirement.package_spec}")
                result = subprocess.Popen(
                    [
                        sys.executable,
                        '-m',
                        'pip',
                        'install',
                        '--prefer-binary',
                        requirement.package_spec
                    ],
                    stderr=subprocess.STDOUT,
                    stdout=subprocess.PIPE,
                )
                for line in iter(result.stdout.readline, b''):
                    print(line.rstrip().decode())
                if result.returncode:
                    print("=="*40)
                    print("!!!INSTALLATION FAILED!!!")
                    print("=="*40)
                else:
                    print("Installation successful")
