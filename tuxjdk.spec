#
# spec file for package tuxjdk
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

%global hgtag   jdk8u60-b27
%global update  60
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
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  time
BuildRequires:  zip
BuildRequires:  unzip
BuildRequires:  freetype2-devel
BuildRequires:  fontconfig-devel
BuildRequires:  alsa-devel
BuildRequires:  cups-devel
BuildRequires:  libpng-devel
BuildRequires:  libjpeg-devel
BuildRequires:  giflib-devel
BuildRequires:  gtk2-devel
BuildRequires:  libX11-devel
BuildRequires:  libXi-devel
BuildRequires:  libXinerama-devel
BuildRequires:  libXt-devel
BuildRequires:  libXtst-devel
BuildRequires:  java-devel
BuildRequires:  quilt
BuildRequires:  fdupes
Source0:        %{name}-%{version}.tar.xz
Source1:        %{hgtag}.tar.xz
Source2:        launcher.sh
Source13:       %{name}-rpmlintrc

%description
Enhanced Open Java Development Kit for developers on Linux. Contains series of
patched to OpenJDK to enhance user experience with Java-based and Swing-based
tools (NetBeans, Idea, Android Studio, etc).

%package        launchers
Summary:        Path launchers for TuxJdk
Group:          Development/Languages
Requires:       tuxjdk
BuildArch:      noarch

%description    launchers
Launch scripts for TuxJdk, located under /usr/local/bin, to be the first
in path but not to conflict with existing jpackage-based packages.

%prep
%setup -q
%setup -q -T -D -a 1
( cd %{hgtag}/jdk/src/share/native/sun/awt && rm -rf giflib )
( cd %{hgtag}/jdk/src/share/native/java/util/zip && rm -rf zlib-1.2.8 )
( cd %{hgtag} && bash ../applyTuxjdk.sh )

%build
pushd %{hgtag}
bash ./common/autoconf/autogen.sh
bash ../configureBuildOpenjdk.sh
popd

%install
# we are building release build,
# so there should be only minimal debug info,
# and probably for a good reason:
export NO_BRP_STRIP_DEBUG='true'
# creating main dir:
install -dm 755 %{buildroot}/opt/%{vendor}/%{name}
# processing the image:
pushd %{hgtag}/build/images/j2sdk-image
# deleting useless files:
rm -rf 'demo' 'sample'
# copy everything to /opt:
cp -R * %{buildroot}/opt/%{vendor}/%{name}/
popd
# hardlinks instead of duplicates:
%fdupes %{buildroot}/opt/%{vendor}/%{name}/
# copy launchers to /usr/local/bin:
install -Dm 755 %{SOURCE2} %{buildroot}/usr/local/bin/java
install -Dm 755 %{SOURCE2} %{buildroot}/usr/local/bin/javac
install -Dm 755 %{SOURCE2} %{buildroot}/usr/local/bin/javap
install -Dm 755 %{SOURCE2} %{buildroot}/usr/local/bin/javah
# hadlink launchers as well:
%fdupes %{buildroot}/usr/local/bin/
# default font size and antialiasing mode:
# TODO maybe find a better way to do that?
cp default_swing.properties %{buildroot}/opt/%{vendor}/%{name}/jre/lib/swing.properties

%files
%defattr(644,root,root,755)
%dir /opt/%{vendor}
/opt/%{vendor}/%{name}
%attr(755,root,root) /opt/%{vendor}/%{name}/bin/*
%attr(755,root,root) /opt/%{vendor}/%{name}/jre/bin/*

%files launchers
%defattr(755,root,root,755)
/usr/local/bin/*

%changelog
* Fri Aug 21 2015 baiduzhyi.devel@gmail.com
- Refreshing for 8u60.
- Dropping giflib5 and gcc5 patches.
* Wed Jul 15 2015 baiduzhyi.devel@gmail.com
- Refreshing for 8u51.
* Tue Jul 14 2015 - baiduzhyi.devel@gmail.com
- Moving under vendor-specific dir.
* Wed Jun 10 2015 baiduzhyi.devel@gmail.com
- Version 03 of tuxjdk:
  * configurable default font size;
  * configurable default text antialiasing;
  * disabling some gcc warnings;
  * compressing the jars;
  * adding default swing.properties file;
  * fixing binaries strip.
* Fri May 29 2015 baiduzhyi.devel@gmail.com
- Do not merge jre into jdk image.
* Tue May 26 2015 baiduzhyi.devel@gmail.com
- Version 02 of tuxjdk:
  * spec file uses script for build;
  * added launcher scripts under /usr/local/bin/ ;
  * dropped verbosity fix patch;
  * merging jre and jdk into single dir;
  * adding rpmlint config;
  * checking support for other distributions;
* Fri Apr  3 2015 baiduzhyi.devel@gmail.com
- Working spec file based on tuxjdk 8.40.0.
* Thu Apr  2 2015 baiduzhyi.devel@gmail.com
- Initial attempt to build normal openJDK source code.
