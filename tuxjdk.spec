%global hgtag   jdk8u40-b25
%global update  40
%global minor   00

%_buildshell    /bin/bash

Name:           tuxjdk
Version:        8.%{update}.%{minor}
Release:        0
Summary:        Enhanced Open Java Development Kit for developers on Linux
License:        GNU General Public License, version 2, with the Classpath Exception
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
Source0:        %{name}-%{version}.tar.xz
Source1:        %{hgtag}.tar.xz

%description
Enhanced Open Java Development Kit for developers on Linux. Contains series of
patched to OpenJDK to enhance user experience with Java-based and Swing-based
tools (NetBeans, Idea, Android Studio, etc).

%prep
%setup -q
%setup -q -T -D -a 1
( cd %{hgtag}/jdk/src/share/native/sun/awt && rm -rf giflib )
( cd %{hgtag}/jdk/src/share/native/java/util/zip && rm -rf zlib-1.2.8 )
( cd %{hgtag} && bash ../applyTuxjdk.sh )

%build
pushd %{hgtag}
bash ./common/autoconf/autogen.sh
popd
mkdir build
pushd build
BOOT_JDK="$JAVA_HOME"
unset JAVA_HOME
bash ../%{hgtag}/configure \
--with-zlib=system \
--with-giflib=system \
--disable-debug-symbols \
--disable-zip-debug-info \
--with-debug-level=release \
--with-milestone='fcs' \
--with-update-version=%{update} \
--with-user-release-suffix=tuxjdk \
--enable-unlimited-crypto \
--with-build-number=%{minor} \
--with-stdc++lib=dynamic \
--with-boot-jdk="$BOOT_JDK"
make \
  JAVAC_FLAGS=-g \
  HOTSPOT_VM_DISTRO=TuxJdk \
  HOTSPOT_BUILD_VERSION=tuxjdk-%{minor} \
  images
popd

%install
install -dm 755 %{buildroot}/opt/%{name}
cd build/images/j2sdk-image
cp -R * %{buildroot}/opt/%{name}/

%files
%defattr(644,root,root,755)
/opt/%{name}
%attr(755,root,root) /opt/%{name}/bin/*
%attr(755,root,root) /opt/%{name}/jre/bin/*

%changelog
* Fri Apr  3 2015 baiduzhyi.devel@gmail.com
- Working spec file based on tuxjdk 8.40.0.
* Thu Apr  2 2015 baiduzhyi.devel@gmail.com
- Initial attempt to build normal openJDK source code.
