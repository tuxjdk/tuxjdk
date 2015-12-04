FROM opensuse:42.1

# maybe reuse caches?
VOLUME /var/tmp
VOLUME /var/cache
VOLUME /tmp

# tuxjdk dependencies:
RUN zypper --non-interactive --gpg-auto-import-keys install --no-recommends bash which sed make gcc5 gcc5-c++ autoconf automake time tar zip unzip freetype2-devel fontconfig-devel alsa-devel cups-devel gtk2-devel libX11-devel libXi-devel libXinerama-devel libXt-devel libXtst-devel java-devel ca-certificates ca-certificates-mozilla ca-certificates-cacert quilt fdupes

# Setup user environment. Replace 1000 with your user / group id.
RUN \
  export uid=1024 gid=1024 && \
  groupadd --gid ${gid} builder && \
  useradd --uid ${uid} --gid ${gid} --create-home builder && \
  mkdir /tuxjdk && \
  chown builder:builder /tuxjdk

COPY ./docker-build-static-tuxjdk.sh /home/builder/

USER builder
WORKDIR /tuxjdk
VOLUME /tuxjdk
ENTRYPOINT ["/bin/bash"]
CMD ["/home/builder/docker-build-static-tuxjdk.sh"]
