#!/usr/bin/env bash

set -eux

echo "Getting the correct source source & version"

case "${QPDF_VERSION}" in
	"10.6.3")
		src_src="bookworm"
		deb_version="${QPDF_VERSION}-1"
		;;
	"11.0.0")
		src_src="sid"
		deb_version="${QPDF_VERSION}-3"
		;;
	"11.1.0")
		src_src="sid"
		deb_version="${QPDF_VERSION}-1"
		;;
	*)
		echo "No match for ${QPDF_VERSION}"
		exit 1
		;;
esac

echo "Choosing source from $src_src version $deb_version"

echo "deb-src http://deb.debian.org/debian/ $src_src main" > "/etc/apt/sources.list.d/$src_src-src.list"

apt-get update

mkdir qpdf
cd qpdf

apt-get source --yes --quiet qpdf="$deb_version/$src_src"
