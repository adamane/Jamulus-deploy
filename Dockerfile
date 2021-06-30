# Thank you to @grundic on github for this Dockerfile for me to modify
# check it out at github.com/grundic/jamulus-docker
FROM alpine:3.11 as builder

ENV JAMULUS_VERSION 3_7_0

RUN \
 echo "**** updating system packages ****" && \
 apk update

RUN \
 echo "**** install build packages ****" && \
   apk add --no-cache --virtual .build-dependencies \
        build-base \
        wget \
        qt5-qtbase-dev \
        qt5-qttools-dev \
        qtchooser

WORKDIR /tmp
RUN \
 echo "**** getting source code ****" && \
   wget "https://github.com/jamulussoftware/jamulus/archive/r${JAMULUS_VERSION}.tar.gz" && \
   tar xzf r${JAMULUS_VERSION}.tar.gz

# Github directory format for tar.gz export
WORKDIR /tmp/jamulus-r${JAMULUS_VERSION}
RUN \
 echo "**** compiling source code ****" && \
   qmake "CONFIG+=nosound headless" Jamulus.pro && \
   make clean && \
   make && \
   cp Jamulus /usr/local/bin/ && \
   rm -rf /tmp/* && \
   apk del .build-dependencies

FROM alpine:3.11

RUN apk add --update --no-cache \
    qt5-qtbase-x11 icu-libs tzdata

COPY --from=builder /usr/local/bin/Jamulus /usr/local/bin/Jamulus
LABEL org.opencontainers.image.source https://github.com/adamane/Jamulus-deploy
EXPOSE 22124/udp
ENTRYPOINT ["Jamulus"]

# MIT License
#
#Copyright (c) 2020 Grigory Chernyshev
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.
#
