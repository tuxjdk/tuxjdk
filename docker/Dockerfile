## following commands can be used to create and run image:
## docker build --force-rm -t tuxjdk-static-leap .
## docker run --rm -v /home/user/dev/tuxjdk/8.66.03/docker:/tuxjdk tuxjdk-static-leap

FROM opensuse:42.1

# maybe reuse caches?
VOLUME /var/tmp
VOLUME /var/cache
VOLUME /tmp

# tuxjdk dependencies:
RUN zypper --non-interactive --gpg-auto-import-keys update --no-recommends && \
    zypper --non-interactive --gpg-auto-import-keys install --no-recommends \
    bash which sed xz make gcc gcc-c++ autoconf automake time tar zip unzip \
    freetype2-devel fontconfig-devel alsa-devel cups-devel gtk2-devel libX11-devel \
    libXi-devel libXinerama-devel libXt-devel libXtst-devel site-config \
    ca-certificates ca-certificates-mozilla ca-certificates-cacert quilt fdupes \
    dejavu-fonts

## Optionally, uncomment this line to build with the java-devel provided by openSUSE:
# RUN zypper --non-interactive --gpg-auto-import-keys install --no-recommends java-devel

## Setup user environment. Replace 1000 with your user / group id.
RUN \
  export uid=1000 gid=1000 && \
  groupadd --gid ${gid} builder && \
  useradd --uid ${uid} --gid ${gid} --create-home builder && \
  mkdir /tuxjdk && \
  chown builder:builder /tuxjdk

COPY ./docker-build-static-tuxjdk.sh /home/builder/
## choose one of two options, either TuxJdk or Oracle JDK:
ADD ./tuxjdk-static-8.66.03.tar.xz /opt/
RUN ln -s /opt/tuxjdk-static-8.66.03 /opt/jdk
# ADD ./jdk-8u66-linux-x64.tar.gz /opt/
# RUN ln -s /opt/jdk1.8.0_66 /opt/jdk

USER builder
WORKDIR /tuxjdk
VOLUME /tuxjdk
ENTRYPOINT ["/bin/bash"]
CMD ["/home/builder/docker-build-static-tuxjdk.sh"]
