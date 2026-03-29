#
# Conditional build:
%bcond_without	apidocs		# Doxygen documentation
%bcond_without	static_libs	# static library
%bcond_without	cython		# Cython based Python bindings
%bcond_without	openssl		# OpenSSL for SSL support
%bcond_with	gnutls		# GnuTLS for SSL support
%bcond_with	mbedtls		# mbedTLS for SSL support

%if %{with gnutls} || %{with mbedtls}
%undefine	with_openssl
%endif
Summary:	Library for connecting to mobile devices
Summary(pl.UTF-8):	Biblioteka do łączenia się z urządzeniami mobilnymi
Name:		libimobiledevice
Version:	1.4.0
Release:	1
License:	LGPL v2+
Group:		Libraries
#Source0Download: https://www.libimobiledevice.org/
Source0:	https://github.com/libimobiledevice/libimobiledevice/releases/download/%{version}/%{name}-%{version}.tar.bz2
# Source0-md5:	487f89a041a1ffd068768ea099cbb358
Patch0:		%{name}-sh.patch
URL:		https://libimobiledevice.org/
BuildRequires:	autoconf >= 2.68
BuildRequires:	automake
%{?with_apidocs:BuildRequires:	doxygen}
%{?with_gnutls:BuildRequires:	gnutls-devel >= 2.2.0}
BuildRequires:	libgcrypt-devel
BuildRequires:	libimobiledevice-glue-devel >= 1.3.0
BuildRequires:	libplist-devel >= 2.3.0
BuildRequires:	libplist-c++-devel >= 2.3.0
BuildRequires:	libstdc++-devel
%{?with_gnutls:BuildRequires:	libtasn1-devel >= 1.1}
BuildRequires:	libtatsu-devel >= 1.0.3
BuildRequires:	libtool
BuildRequires:	libusbmuxd-devel >= 2.0.2
%{?with_mbedtls:BuildRequires:	mbedtls-devel}
%{?with_openssl:BuildRequires:	openssl-devel >= 0.9.8}
BuildRequires:	pkgconfig >= 1:0.9.0
%if %{with cython}
BuildRequires:	python-plist-devel >= 2.3.0
BuildRequires:	python3-Cython >= 3.0.0
BuildRequires:	python3-devel >= 1:3.2
BuildRequires:	python3-modules >= 1:3.2
%endif
BuildRequires:	readline-devel >= 1.0
BuildRequires:	rpmbuild(macros) >= 2.043
BuildRequires:	rpm-pythonprov
Requires:	libimobiledevice-glue >= 1.3.0
Requires:	libplist >= 2.3.0
Requires:	libplist-c++ >= 2.3.0
# required by ideviceimagemounter
Requires:	libtatsu >= 1.0.3
Requires:	libusbmuxd >= 2.0.2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libimobiledevice is a library for connecting to mobile devices.

%description -l pl.UTF-8
libimobiledevice jest biblioteką do łączenia się z urządzeniami
mobilnymi.

%package devel
Summary:	Header files for libimobiledevice library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libimobiledevice
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
%{?with_gnutls:Requires:	gnutls-devel >= 2.2.0}
Requires:	libimobiledevice-glue-devel >= 1.3.0
Requires:	libplist-devel >= 2.3.0
Requires:	libplist-c++-devel >= 2.3.0
%{?with_gnutls:Requires:	libtasn1-devel >= 1.1}
Requires:	libusbmuxd-devel >= 2.0.2
%{?with_mbedtls:Requires:	mbedtls-devel}
%{?with_openssl:Requires:	openssl-devel >= 0.9.8}

%description devel
Header files for libimobiledevice library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libimobiledevice.

%package static
Summary:	Static libimobiledevice library
Summary(pl.UTF-8):	Statyczna biblioteka libimobiledevice
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libimobiledevice library.

%description static -l pl.UTF-8
Statyczna biblioteka libimobiledevice.

%package apidocs
Summary:	API documentation for libimobiledevice library
Summary(pl.UTF-8):	Dokumentacja API biblioteki libimobiledevice
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for libimobiledevice library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki libimobiledevice.

%package -n python3-imobiledevice
Summary:	libimobiledevice Python 3 bindings
Summary(pl.UTF-8):	Wiązania libimobiledevice dla Pythona 3
Group:		Development/Languages/Python
Requires:	%{name} = %{version}-%{release}
Requires:	python3-plist >= 2.3.0

%description -n python3-imobiledevice
libimobiledevice Python 3 bindings.

%description -n python3-imobiledevice -l pl.UTF-8
Wiązania libimobiledevice dla Pythona 3.

%prep
%setup -q
%patch -P0 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	CYTHON=/usr/bin/cython3 \
	PYTHON=%{__python3} \
	--disable-silent-rules \
	%{!?with_static_libs:--disable-static} \
	%{!?with_cython:--without-cython} \
	%{?with_gnutls:--with-gnutls} \
	%{?with_mbedtls:--with-mbedtls} \
	%{!?with_openssl:--without-openssl}

%if %{with apidocs}
%{__make} docs
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libimobiledevice-1.0.la

%if %{with cython}
%{__rm} $RPM_BUILD_ROOT%{py3_sitedir}/*.la \
	%{?with_static_libs:$RPM_BUILD_ROOT%{py3_sitedir}/*.a}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS NEWS README.md
%attr(755,root,root) %{_bindir}/afcclient
%attr(755,root,root) %{_bindir}/idevice_id
%attr(755,root,root) %{_bindir}/idevicebackup
%attr(755,root,root) %{_bindir}/idevicebackup2
%attr(755,root,root) %{_bindir}/idevicebtlogger
%attr(755,root,root) %{_bindir}/idevicecrashreport
%attr(755,root,root) %{_bindir}/idevicedate
%attr(755,root,root) %{_bindir}/idevicedebug
%attr(755,root,root) %{_bindir}/idevicedebugserverproxy
%attr(755,root,root) %{_bindir}/idevicedevmodectl
%attr(755,root,root) %{_bindir}/idevicediagnostics
%attr(755,root,root) %{_bindir}/ideviceenterrecovery
%attr(755,root,root) %{_bindir}/ideviceimagemounter
%attr(755,root,root) %{_bindir}/ideviceinfo
%attr(755,root,root) %{_bindir}/idevicename
%attr(755,root,root) %{_bindir}/idevicenotificationproxy
%attr(755,root,root) %{_bindir}/idevicepair
%attr(755,root,root) %{_bindir}/ideviceprovision
%attr(755,root,root) %{_bindir}/idevicescreenshot
%attr(755,root,root) %{_bindir}/idevicesetlocation
%attr(755,root,root) %{_bindir}/idevicesyslog
%{_libdir}/libimobiledevice-1.0.so.*.*.*
%ghost %{_libdir}/libimobiledevice-1.0.so.6
%{_mandir}/man1/afcclient.1*
%{_mandir}/man1/idevice_id.1*
%{_mandir}/man1/idevicebackup.1*
%{_mandir}/man1/idevicebackup2.1*
%{_mandir}/man1/idevicebtlogger.1*
%{_mandir}/man1/idevicecrashreport.1*
%{_mandir}/man1/idevicedate.1*
%{_mandir}/man1/idevicedebug.1*
%{_mandir}/man1/idevicedebugserverproxy.1*
%{_mandir}/man1/idevicedevmodectl.1*
%{_mandir}/man1/idevicediagnostics.1*
%{_mandir}/man1/ideviceenterrecovery.1*
%{_mandir}/man1/ideviceimagemounter.1*
%{_mandir}/man1/ideviceinfo.1*
%{_mandir}/man1/idevicename.1*
%{_mandir}/man1/idevicenotificationproxy.1*
%{_mandir}/man1/idevicepair.1*
%{_mandir}/man1/ideviceprovision.1*
%{_mandir}/man1/idevicescreenshot.1*
%{_mandir}/man1/idevicesetlocation.1*
%{_mandir}/man1/idevicesyslog.1*

%files devel
%defattr(644,root,root,755)
%{_libdir}/libimobiledevice-1.0.so
%{_includedir}/libimobiledevice
%{_pkgconfigdir}/libimobiledevice-1.0.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libimobiledevice-1.0.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc docs/html/*.{css,html,ico,js,png}
%endif

%if %{with cython}
%files -n python3-imobiledevice
%defattr(644,root,root,755)
%{py3_sitedir}/imobiledevice.so
%endif
