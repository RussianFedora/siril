Summary:	Astronomical image processing software for Linux
Name:		siril
Version:	0.9.4
Release:	2%{?dist}

License:	GPLv3+
URL:		http://free-astro.org/index.php/Siril
Source0:	https://free-astro.org/download/%{name}-%{version}.tar.bz2
Source2:	%{name}.appdata.xml

BuildRequires:	autoconf, automake, intltool
BuildRequires:	desktop-file-utils

# giflib in Fedora is too old
#BuildRequires:	giflib-devel >= 5

BuildRequires:	libappstream-glib
BuildRequires:	pkgconfig(cfitsio)
BuildRequires:	pkgconfig(ffms2)
BuildRequires:	pkgconfig(fftw3)
BuildRequires:	pkgconfig(gsl)
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(libconfig)
%if 0%{?fedora} >= 24
BuildRequires:	pkgconfig(libjpeg)
%endif
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(libraw)
BuildRequires:	pkgconfig(libtiff-4)
BuildRequires:	pkgconfig(opencv)

%description
Siril is an image processing tool specially tailored for noise reduction and
improving the signal/noise ratio of an image from multiple captures, as
required in astronomy. Siril can align automatically or manually, stack and
enhance pictures from various file formats, even images sequences (movies and
SER files).


%prep
%autosetup


%build
intltoolize -f -c
autoreconf -fi -Wno-portability
%configure
%make_build


%install
%make_install

install -Dm 644 platform-specific/linux/%{name}.xml %{buildroot}%{_datadir}/mime/packages/%{name}.xml
install -Dm 644 %{SOURCE2} %{buildroot}%{_datadir}/metainfo/%{name}.appdata.xml

install -d %{buildroot}%{_datadir}/icons/
cp -r pixmaps/icons/* %{buildroot}%{_datadir}/icons/

desktop-file-install						\
	--dir=%{buildroot}%{_datadir}/applications		\
	platform-specific/linux/%{name}.desktop

%find_lang %{name}


%check
appstream-util validate-relax --nonet %{buildroot}%{_datadir}/metainfo/%{name}.appdata.xml


%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :


%postun
update-desktop-database &> /dev/null || :
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi


%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files -f %{name}.lang
%license LICENSE
%doc COPYING AUTHORS NEWS README LICENSE
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/mime/packages/%{name}.xml
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%{_datadir}/metainfo/%{name}.appdata.xml
%{_datadir}/%{name}/
%{_mandir}/man1/%{name}.1*


%changelog
* Wed Sep 14 2016 Cyril Richard <lock042@gmail.com> - 0.9.4-2
- update description

* Tue Sep 13 2016 Arkady L. Shane <ashejn@russianfedora.pro> - 0.9.4-1
- initial build
