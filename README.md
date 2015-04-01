This project contains series of patched to OpenJDK to enhance user experience with Java-based and Swing-based tools (NetBeans, Idea, Android Studio, etc)

# WARNING
The project is in the process of migrating from google-code, so some things may not work as intended.

# Download
Download latest build of tuxjdk for openSUSE here:
[jdk-8u25-tuxjdk-b01.tar.xz](https://googledrive.com/host/0B68yuEpDuq6waUl5UjNTUWRlYTQ/jdk-8u25-tuxjdk-b01.tar.xz)

# Quickstart (for packagers and developers)

TuxJdk users [Quilt](http://en.wikipedia.org/wiki/Quilt_(software)) to manage patches, and [here](http://www.suse.de/~agruen/quilt.pdf) is a good tutorial on using Quilt.
Additionally, project contains number of helper scripts to automate most common tasks.
To build tuxjdk, do the following steps:

```bash
# clone tuxjdk:
git clone 'https://github.com/TheIndifferent/tuxjdk.git'
# clone openjdk:
hg clone 'http://hg.openjdk.java.net/jdk8u/jdk8u' jdk8-tuxjdk
cd jdk8-tuxjdk
bash get_source.sh
# run helper script to apply tuxjdk onto openjdk sources:
../tuxjdk/applyTuxjdk.sh
# tuxjdk applied, now we can create external build folder:
cd ..
mkdir build
cd build
# and run helper script to configure and make tuxjdk images,
# script takes 3 arguments: openjdk source folder, bootstrap jdk and build number:
../tuxjdk/configureBuildOpenjdk.sh ../jdk8-tuxjdk /opt/jdk1.7.0_51 b00
# now wait until the build is complete, and go see the images:
ls images/j2sdk-image
ls images/j2re-image
```

# Patches list
```
TODO
```
