#!/bin/bash

if [ "$#" -ne 2 ] ; then
    echo "expected 2 arguments:"
    echo " * folder to use as chroot for build"
    echo " * build number"
    exit 1;
fi

# input parameters:
ROOT=$1
BUILDNUM=$2

# exit on any fail:
set -e

# our chroot:

# installing everything we need:
zypper -n --no-gpg-checks --root $ROOT ar http://download.opensuse.org/distribution/openSUSE-current/repo/oss/ repo-oss
zypper -n --no-gpg-checks --root $ROOT ar http://download.opensuse.org/update/openSUSE-current/ repo-update
zypper -n --no-gpg-checks --root $ROOT refresh
zypper -n --no-gpg-checks --root $ROOT install --no-recommends gcc gcc-c++ make autoconf automake freetype2-devel fontconfig-devel xorg-x11-devel gawk grep zip zlib-devel procps alsa-devel cups-devel unzip findutils tar bzip2 gzip cpio xz which libjpeg62-devel giflib-devel

# install some developer tools:
zypper -n --no-gpg-checks --root $ROOT install mercurial quilt wget

# needed for dns lookup:
cp /etc/resolv.conf $ROOT/etc/resolv.conf

function umountExitHook() {
  set +e
  echo -n "unmounting $ROOT/dev..."
  umount $ROOT/dev
  echo "done."
  echo -n "unmounting $ROOT/proc..."
  umount $ROOT/proc
  echo "done."
}

# bind special folders from host:
echo ""
echo -n "mounting proc and dev..."
trap umountExitHook EXIT
mount --bind /dev $ROOT/dev
mount -t proc proc $ROOT/proc
echo "done."

# starting the process:
echo -n "creating build script..."
mkdir $ROOT/usr/src/tuxjdk
cat <<EOF > $ROOT/usr/src/tuxjdk/cloneBuildTuxJdk.sh
#!/bin/bash
# edit on first fail:
set -e
# bootstrap jdk:
cd /opt
wget -4 --no-http-keep-alive --no-check-certificate https://googledrive.com/host/0B68yuEpDuq6waUl5UjNTUWRlYTQ/jdk-8u0-openjdk-vanilla.tar.xz
tar -xJf jdk-8u0-openjdk-vanilla.tar.xz
# now preparing tuxjdk for build:
cd /usr/src/tuxjdk
hg clone https://code.google.com/p/tuxjdk/ tuxjdk
hg clone http://hg.openjdk.java.net/jdk8/jdk8/ jdk-8u0-tuxjdk-$BUILDNUM
cd jdk-8u0-tuxjdk-$BUILDNUM
bash get_source.sh
bash ../tuxjdk/applyTuxjdk.sh
# preparation done, starting actual build:
cd ..
mkdir build
cd build
bash ../jdk-8u0-tuxjdk-$BUILDNUM/configure --with-zlib=system --disable-debug-symbols --disable-zip-debug-info --with-boot-jdk=/opt/jdk-8u0-openjdk-vanilla --with-milestone=tuxjdk --with-build-number=$BUILDNUM --with-jvm-variants=client
make images
EOF
chmod a+x $ROOT/usr/src/tuxjdk/cloneBuildTuxJdk.sh
echo "done."
echo ""
echo "running the build in chroot..."
echo ""
chroot $ROOT /usr/src/tuxjdk/cloneBuildTuxJdk.sh

# build should be complete by now, packing distribution:
mv $ROOT/usr/src/tuxjdk/build/images/j2sdk-image jdk-8u0-tuxjdk-$BUILDNUM
tar -cJf jdk-8u0-tuxjdk-$BUILDNUM.tar.xz jdk-8u0-tuxjdk-$BUILDNUM
