#!/usr/bin/env bash

set -eux

echo "Getting the correct source source"

src_src="bookworm"
deb_version="${QPDF_VERSION}-1"

if [ "${QPDF_VERSION}" = "11.0.0" ] ; then
	echo "Choosing deb-src from sid"
	src_src="sid"
	deb_version="${QPDF_VERSION}-3"
fi;

echo "deb-src http://deb.debian.org/debian/ $src_src main" > /etc/apt/sources.list.d/$src_src-src.list

apt-get update

mkdir qpdf
cd qpdf

apt-get source --yes --quiet qpdf=$deb_version/$src_src

ls -ahl .

cd qpdf-$QPDF_VERSION

# Remove the tests so they are not built or run
rm -rf libtests

if [ "${QPDF_VERSION}" = "11.0.0" ] ; then

	# cmake prefers an out of source build
	mkdir build
	cd build

	cmake -DMAINTAINER_MODE=1 -DBUILD_STATIC_LIBS=0 -DCMAKE_BUILD_TYPE=RelWithDebInfo ..

else

	DEBEMAIL=hello@paperless-ngx.com debchange --bpo
	export DEB_BUILD_OPTIONS="terse nocheck nodoc parallel=2"
	dpkg-buildpackage --build=binary --unsigned-source --unsigned-changes --post-clean
	ls -ahl ../*.deb

fi;


