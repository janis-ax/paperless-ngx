#!/usr/bin/env bash

set -eux

echo "Getting the correct source source"

src_src="sid"
deb_version="${QPDF_VERSION}-3"

if [ "${QPDF_VERSION}" = "10.6.3" ] ; then
	src_src="bookworm"
	deb_version="${QPDF_VERSION}-1"
fi;

echo "Choosing source from $src_src version $deb_version"

echo "deb-src http://deb.debian.org/debian/ $src_src main" > /etc/apt/sources.list.d/$src_src-src.list

apt-get update

mkdir qpdf
cd qpdf

apt-get source --yes --quiet qpdf="$deb_version/$src_src"
