This project contains series of patched to OpenJDK to enhance user experience with Java-based and Swing-based tools (NetBeans, Idea, Android Studio, etc)

# Download
Download latest build of tuxjdk for openSUSE and Fedora here:
[OBS repository](http://download.opensuse.org/repositories/home:/TheIndifferent:/tuxjdk/)

It will be installed under `/opt/tuxjdk` and will not touch the alternatives and
any other java binaries you might have in path.

# Quickstart (for packagers and developers)

TuxJdk uses [Quilt](http://en.wikipedia.org/wiki/Quilt_(software)) to manage patches, and [here](http://www.suse.de/~agruen/quilt.pdf) is a good tutorial on using Quilt.<br/>
Additionally, project contains number of helper scripts to automate most common tasks.<br/>
To apply tuxjdk, do the following steps:

```bash
# clone tuxjdk:
git clone 'https://github.com/TheIndifferent/tuxjdk.git'
# clone openjdk:
HGTAG='jdk8u45-b14'
hg clone 'http://hg.openjdk.java.net/jdk8u/jdk8u' $HGTAG
cd $HGTAG
bash ./get_source.sh
bash ./common/bin/hgforest.sh checkout $HGTAG
# run helper script to apply tuxjdk onto openjdk sources:
../tuxjdk/applyTuxjdk.sh
# tuxjdk applied, now we can create external build folder:
mkdir ../build
cd ../build
# and run configure script with your favourite options:
bash ../$HGTAG/configure <your options here>
# then make images:
make JAVAC_FLAGS=-g images
# now wait until the build is complete, and go see the images:
ls images/j2sdk-image
ls images/j2re-image
```

# Patches list
```
TODO
```
