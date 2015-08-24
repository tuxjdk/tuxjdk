This project contains series of patched to OpenJDK to enhance user experience with Java-based and Swing-based tools (NetBeans, Idea, Android Studio, etc)

# Download
Download latest build of tuxjdk for different distributions here:
[OBS repository](http://download.opensuse.org/repositories/home:/tuxjdk/)<br/>
It will be installed under `/opt/tuxjdk` and will not touch the alternatives and
any other java binaries you might have in path.

# Quickstart (for packagers and developers)

TuxJdk uses [Quilt](http://en.wikipedia.org/wiki/Quilt_(software)) to manage patches, and [here](http://www.suse.de/~agruen/quilt.pdf) is a good tutorial on using Quilt.<br/>
Additionally, project contains number of helper scripts to automate most common tasks.<br/>
To apply tuxjdk, do the following steps:

```bash
# clone tuxjdk:
git clone 'https://github.com/tuxjdk/tuxjdk.git'
# clone openjdk:
HGTAG='jdk8u51-b16'
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
# Versioning
Verion of tuxjdk is a desperate attempt to put some sense into current java versioning scheme.
First two numbers reflects major and update version of java for which current patches are adapted.
Third number is the version of tuxjdk itself, padded with 0 to have a natural sorting.

# Distribution packagers

* Source package files for Ubuntu/Arch/others are appreciated.
* Project is organized into series of patches, they should not be dependent. Feel free to use them selectively and report any issues.

# Patches list
* **backport** contains patches that may be included in next version of openjdk or those that should but probably will not.
 * **compare-pointer-with-literal** fixes a mistake in C code, detected by OBS.
 * **less-warnings** disable some most noisy warnings during the compilation.
 * **opensuse-link-zlib-as-needed** fixes the linking against system zlib.
* **tune** contains patches to tune the openjdk default settings or distribution package.
 * **default-gc** changes the default garbage collector to *ConcMarkSwee*, it greatly lowers the footprint and boosts the performance of NetBeans.
 * **empty-ctsym** makes the *ct.sym* file completely empty.
 * **full-srczip** forces the openjdk to pack all the existing sources into *src.zip* file, even from *com.sun* and *sun* packages.
* **tuxjdk** contains tuxjdk-specific changes, mostly fonts related.
 * **change-vendor** changes the system properties to identify tuxjdk as vendor.
 * **add-fontconfig-support** forces reading of system fontconfig settings and rendering the fonts similarly to native toolkits such as Qt and GTK, instead of using hardcoded rendering path.
 * **configurable-ui-fonts** fixes the typographical point size (upstream openjdk completely ignores the 1/72" standard), adds a possibility to configure defaut font size (hardcoded to 12 in most locations and to 11 in some locations in upstream) and allows to specify desired default font antialiasing if the are any problems detecting one from system (upstream defaults behaviour is not well-defined, and needs constant attention from developers not to forget to set proper RenderingHints).

# Planned features, tasks backlog
## 8.60.04
* [x] change logic of 'awt.useSystemAAFontSettings'.
* [ ] add possibility to specify antialiasing 'grayscale.'
* [ ] change antialiasing 'on' to autodetect between grayscale and lcd.
* [ ] font size scaling: configure font size to 12 but render as 9, for badly-written apps like jedit.
* [ ] split single huge patch into series of smaller patches.
* [ ] check fontconfig support for memory leaks.

## General tasks
* [ ] add default settings autudetection app.
* [ ] Ubuntu packages
* [ ] document font size settings
* [ ] document font antialiasing settings
* [ ] document font scaling settings
* [ ] document default GC change
