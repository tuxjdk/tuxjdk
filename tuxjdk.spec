%global hgtag   jdk8u40-b25
%global update  40

Name:           tuxjdk
Version:        8.%{update}
Release:        1
Summary:        Enhanced Open Java Development Kit for Linux developers
License:        GNU General Public License, version 2, with the Classpath Exception
Group:          Development/Languages
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gawk
BuildRequires:  grep
BuildRequires:  findutils
BuildRequires:  which
BuildRequires:  procps
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
BuildRequires:  mercurial

%description
Enhanced Open Java Development Kit for Linux developers. Contains series of
patched to OpenJDK to enhance user experience with Java-based and Swing-based
tools (NetBeans, Idea, Android Studio, etc).

%prep
hg clone http://hg.openjdk.java.net/jdk8u/jdk8u/
cd jdk8u
bash get_source.sh
bash ./common/bin/hgforest.sh checkout %{hgtag}

%build
( cd common/autoconf && bash ./autogen.sh )
bash configure \
--with-zlib=system \
--with-giflib=system \
--disable-debug-symbols \
--disable-zip-debug-info \
--with-debug-level=release \
--with-milestone='fcs' \
--with-update-version=%{update} \
--with-user-release-suffix=tuxjdk \
--enable-unlimited-crypto \
--with-build-number=%{release} \
--prefix=/opt/%{name}

make JAVAC_FLAGS=-g images

%install
make install

%files
%defattr(-,root,root)
/opt/%{name}

%changelog
* Wed Mar 26 2015 baiduzhyi.devel@gmail.com
- Initial attempt to build normal openJDK source code.
