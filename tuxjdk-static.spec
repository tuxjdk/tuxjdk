#
# spec file to use opensuse build command to produce a static image of
# tuxjdk.
#
# Copyright (c) 2015 Stanislav Baiduzhyi <baiduzhyi.devel@gmail.com>
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

%global vendor  tuxjdk
%global product TuxJdk

%global hgtag   jdk8u66-b17
%global update  66
%global minor   03

# openjdk build system is different,
# we are building release so there is no useful debuginfo,
# so disabling debuginfo package creation:
%global debug_package %{nil}
# no one should touch our jars, we know better:
%define __jar_repack %{nil}


Name:           tuxjdk
Version:        8.%{update}.%{minor}
Release:        0
URL:            https://github.com/tuxjdk/tuxjdk
Summary:        Enhanced Open Java Development Kit for developers on Linux
#License:        GNU General Public License, version 2, with the Classpath Exception
License:        GPL-2.0+
Group:          Development/Languages
BuildRequires:  bash
BuildRequires:  make
BuildRequires:  gcc5
BuildRequires:  gcc5-c++
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  time
BuildRequires:  zip
BuildRequires:  unzip
BuildRequires:  freetype2-devel
BuildRequires:  fontconfig-devel
BuildRequires:  alsa-devel
BuildRequires:  cups-devel
BuildRequires:  gtk2-devel
BuildRequires:  libX11-devel
BuildRequires:  libXi-devel
BuildRequires:  libXinerama-devel
BuildRequires:  libXt-devel
BuildRequires:  libXtst-devel
BuildRequires:  java-devel
BuildRequires:  ca-certificates
BuildRequires:  ca-certificates-mozilla
BuildRequires:  ca-certificates-cacert
BuildRequires:  quilt
BuildRequires:  fdupes
Source0:        %{name}-%{version}.tar.xz
Source1:        %{hgtag}.tar.xz

%description
Enhanced Open Java Development Kit for developers on Linux. Contains series of
patched to OpenJDK to enhance user experience with Java-based and Swing-based
tools (NetBeans, Idea, Android Studio, etc).

%prep
## fail on unsupported hosts:
%if 0%{?is_opensuse}
  %if 0%{?suse_version} == 1315
    echo 'openSUSE Leap 42.1 is detected, we can continue.'
  %else
    echo 'wrong openSUSE version detected, this file was designed for Leap 42.1 only' >&2
    exit 1
  %endif
%else
  echo 'wrong distribution detected, this file was designed for Leap 42.1 only' >&2
  exit 1
%endif
%setup -q
%setup -q -T -D -a 1
( cd %{hgtag} && bash ../applyTuxjdk.sh )

%build
pushd %{hgtag}
bash ./common/autoconf/autogen.sh
## using gcc5 from Leap 42.1:
export CC=gcc-5
export CXX=g++-5
## jdk8u45 still does not support linux 4.0 officially,
## so we have to disable os version check because
## tumbleweed already has 4.0-based kernel:
export DISABLE_HOTSPOT_OS_VERSION_CHECK=ok

rm -rf 'build'
mkdir 'build'
pushd 'build'

bash ../configure \
    --disable-debug-symbols \
    --disable-zip-debug-info \
    --with-debug-level=release \
    --with-stdc++lib=static \
    --with-milestone='fcs' \
    --with-update-version=%{update} \
    --with-user-release-suffix=%{vendor} \
    --with-build-number=%{minor} \
    --enable-unlimited-crypto \
    --with-boot-jdk='/usr/lib64/jvm/java'

make \
    JAVAC_FLAGS=-g \
    COMPRESS_JARS=false \
    LAUNCHER_NAME=%{vendor} \
    PRODUCT_NAME=%{product} \
    JDK_UPDATE_VERSION=%{update} \
    HOTSPOT_VM_DISTRO=%{product} \
    HOTSPOT_BUILD_VERSION=tuxjdk-%{minor} \
    images

popd
popd

%install
# we are building release build,
# so there should be only minimal debug info,
# and probably for a good reason:
export NO_BRP_STRIP_DEBUG='true'
#
# default font size and antialiasing mode:
cp default_swing.properties %{hgtag}/build/images/j2sdk-image/jre/lib/swing.properties
#
# certificates:
pushd %{hgtag}/build/images/j2sdk-image/jre/lib/security
mv cacerts cacerts.orig
cp /var/lib/ca-certificates/java-cacerts ./cacerts
popd
#
# processing the image:
pushd %{hgtag}/build/images/j2sdk-image
# deleting useless files:
rm -rf 'demo' 'sample'
# fix permissions for files and dirs:
chmod -R a-w .
chmod -R a+r .
find "$(pwd)" -type d -exec chmod a+x {} +
chmod a+x bin/*
chmod a+x jre/bin/*
popd
#
# packing the image:
pushd %{hgtag}/build/images/
mv j2sdk-image %{name}-static-%{version}
tar -cJf %{buildroot}/%{name}-static-%{version}.tar.xz %{name}-static-%{version}
popd

%files
%defattr(644,root,root,755)
/%{name}-static-%{version}.tar.xz

%changelog
* Fri Nov 13 2015 baiduzhyi.devel@gmail.com
- Initial version of static build spec file.
