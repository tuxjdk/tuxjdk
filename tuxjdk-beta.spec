%global hgtag   jdk8u45-b14
%global update  45
%global minor   beta

# openjdk build system is different,
# we are building release so there is no useful debuginfo,
# so disabling debuginfo package creation:
%global debug_package %{nil}

Name:           tuxjdk-beta
Version:        8.%{update}.%{minor}
Release:        0
URL:            https://github.com/TheIndifferent/tuxjdk
Summary:        Beta or early development version of TuxJdk
Conflicts:      tuxjdk
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
Source0:        %{name}.tar.xz
Source1:        %{hgtag}.tar.xz
Source13:       %{name}-rpmlintrc

%description
Beta/TP/early development version of TuxJdk.
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
install -dm 755 %{buildroot}/opt/%{name}
# processing the image:
pushd %{hgtag}/build/images/j2sdk-image
# deleting useless files:
rm -rf 'demo' 'sample'
# copy everything to /opt:
cp -R * %{buildroot}/opt/%{name}/
popd
# hardlinks instead of duplicates:
%fdupes %{buildroot}/opt/%{name}/
# copy launchers to /usr/local/bin:
install -Dm 755 launcher.sh %{buildroot}/usr/local/bin/java
install -Dm 755 launcher.sh %{buildroot}/usr/local/bin/javac
install -Dm 755 launcher.sh %{buildroot}/usr/local/bin/javap
install -Dm 755 launcher.sh %{buildroot}/usr/local/bin/javah
# hadlink launchers as well:
%fdupes %{buildroot}/usr/local/bin/

%files
%defattr(644,root,root,755)
/opt/%{name}
%attr(755,root,root) /opt/%{name}/bin/*
%attr(755,root,root) /opt/%{name}/jre/bin/*

%files launchers
%defattr(755,root,root,755)
/usr/local/bin/*

%changelog
* Sat May 30 2015 baiduzhyi.devel@gmail.com
- Branching into tuxjdk-beta project.
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
