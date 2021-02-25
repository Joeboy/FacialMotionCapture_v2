# FacialMotionCapture_v2 (add-on edition)

This is a fork of jkirsons' https://github.com/jkirsons/FacialMotionCapture_v2.
See also https://www.youtube.com/watch?v=9FBMoUo6vhY and the related videos on
the channel.

The idea is to make it installable as an add-on. I got a bit distracted so it's
not really finished yet. However if you're lucky you might get it to work as
follows:

* Copy the FacialMotionCapture_v2 folder to your add-ons folder (or symlink, or
  use a zip file, or whatever).
* Download the code as a zip file from github (the green "Code" button, followed by
  "Download ZIP")
* Download trained model to your home directory:
  https://raw.githubusercontent.com/kurnianggoro/GSOC2017/master/data/lbfmodel.yaml.
  The licensing of this file is a bit unclear, see
  https://github.com/kurnianggoro/GSOC2017/issues/3. Seems like you're not
  supposed to use it for commercial purposes, although I doubt anybody is
  checking.
* Run Blender. I recommend starting Blender in a terminal so you can see what's
  going on better. On Windows, you'll need to run it as administrator.
* Go to Preferences, install the add-on from the zip file you downloaded earlier,
  and enable it. This will cause the add-on's Python requirements to be
  automatically downloaded and installed. Note that this requires an internet
  connection, and could take some time.
* (Windows only) There's no need to be running as administrator anymore, so you
  might want to close Blender and re-open it as normal.
* Download "Vincent" blend file from https://cloud.blender.org/p/characters.
  Apparently characters rigged with the free BlenRig add-on should work too,
  but Vincent is tried and tested.
* Open the "Vincent" file in Blender.
* As per the original youtube vid, click on the "OpenCV Animation" tool, then
  "Capture".

The install worked for me in Ubuntu 20.10 and on Windows 10. I had to run
Blender as administrator on Windows.


TODO
====

* Requirements are currently automatically installed when the add-on is
  enabled. This ought to be optionally initiated by the user.

Issues
======

* This is just a repackaging of the original code as an add-on for easy
  installation. It seems like some people find the code needs tweaking for
  their hardware or whatever, and I've made no attempt to make it more
  reliable. You can still modify the python files in your `addons` folder
  after installation if you need to.