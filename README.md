# FacialMotionCapture_v2 (add-on edition)

This is a fork of jkirsons' https://github.com/jkirsons/FacialMotionCapture_v2.
See also https://www.youtube.com/watch?v=9FBMoUo6vhY and the related videos on
the channel.

The idea is to make it installable as an add-on. I got a bit distracted so it's
not really finished yet. However if you're lucky you might get it to work as
follows:

* Copy the FacialMotionCapture_v2 folder to your add-ons folder (or symlink, or
  use a zip file, or whatever).
* Download trained model (lbfmodel.yaml) to your home directory:
  https://raw.githubusercontent.com/kurnianggoro/GSOC2017/master/data/lbfmodel.yaml.
  The licensing of this file is a bit unclear, see
  https://github.com/kurnianggoro/GSOC2017/issues/3. Seems like you're not
  supposed to use it for commercial purposes, although I doubt anybody is
  checking.
* Download "Vincent" blend file from https://cloud.blender.org/p/characters.
  Apparently characters rigged with the free Blenrig add-on should work too,
  but Vincent is tried and tested.
* Open "Vincent" in Blender. I recommend starting Blender in a terminal so you
  see what's going on better.
* Go to Preferences, search for Facial Mocap v2.
* Enable the add-on. This will cause the add-on's Python requirements to be
  automatically downloaded and installed. Note that this could take some time,
  and frankly might fail.

I've tested it in Ubuntu 20.10 with Blender 2.9.1. It seems to work for me, so
maybe it'll work for you too. On Windows you might need to run Blender as
Administrator when installing the add-on.

TODO
====

* Requirements are currently automatically installed on registration. This
  ought to be optionally initiated by the user.
* Output of install command is only shown on failure, which means blender
  kind of looks like it's hung during installation.