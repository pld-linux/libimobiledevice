#
# Conditional build:
%bcond_without	static_libs	# static library
%bcond_without	cython		# Cython based Python bindings
%bcond_without	python3		# Python 3 module
%bcond_without	openssl		# OpenSSL for SSL support
%bcond_with	gnutls		# GnuTLS for SSL support

%if %{without cython}
%undefine	with_python3
%endif
%if %{with gnutls}
%undefine	with_openssl
%endif
Summary:	Library for connecting to mobile devices
Summary(pl.UTF-8):	Biblioteka do łączenia się z urządzeniami mobilnymi
Name:		libimobiledevice
Version:	1.3.0
Release:	7
License:	LGPL v2+
Group:		Libraries
#Source0Download: https://www.libimobiledevice.org/
Source0:	https://github.com/libimobiledevice/libimobiledevice/releases/download/%{version}/%{name}-%{version}.tar.bz2
# Source0-md5:	c50a3a32acf33dc8c9ec88137ad12ec4
Patch0:		%{name}-cython.patch
Patch1:		%{name}-libplist.patch
URL:		https://libimobiledevice.org/
BuildRequires:	autoconf >= 2.64
BuildRequires:	automake
%{?with_gnutls:BuildRequires:	gnutls-devel >= 2.2.0}
BuildRequires:	libgcrypt-devel
BuildRequires:	libplist-devel >= 2.3.0
BuildRequires:	libplist-c++-devel >= 2.3.0
BuildRequires:	libstdc++-devel
%{?with_gnutls:BuildRequires:	libtasn1-devel >= 1.1}
BuildRequires:	libtool
BuildRequires:	libusbmuxd-devel >= 2.0.2
%{?with_openssl:BuildRequires:	openssl-devel >= 0.9.8}
BuildRequires:	pkgconfig
%if %{with cython}
BuildRequires:	python-Cython >= 0.17.0
BuildRequires:	python-devel >= 1:2.3
BuildRequires:	python-modules >= 1:2.3
BuildRequires:	python-plist-devel >= 2.2.0
%endif
%if %{with python3}
BuildRequires:	python3-Cython >= 0.17.0
BuildRequires:	python3-devel >= 1:3.2
BuildRequires:	python3-modules >= 1:3.2
%endif
BuildRequires:	rpm-pythonprov
Requires:	libplist >= 2.3.0
Requires:	libplist-c++ >= 2.3.0
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
Requires:	libplist-devel >= 2.3.0
Requires:	libplist-c++-devel >= 2.3.0
%{?with_gnutls:Requires:	libtasn1-devel >= 1.1}
Requires:	libusbmuxd-devel >= 2.0.2
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

%package -n python-imobiledevice
Summary:	libimobiledevice Python 2 bindings
Summary(pl.UTF-8):	Wiązania libimobiledevice dla Pythona 2
Group:		Development/Languages/Python
Requires:	%{name} = %{version}-%{release}
Requires:	python-plist >= 2.2.0

%description -n python-imobiledevice
libimobiledevice Python 2 bindings.

%description -n python-imobiledevice -l pl.UTF-8
Wiązania libimobiledevice dla Pythona 2.

%package -n python3-imobiledevice
Summary:	libimobiledevice Python 3 bindings
Summary(pl.UTF-8):	Wiązania libimobiledevice dla Pythona 3
Group:		Development/Languages/Python
Requires:	%{name} = %{version}-%{release}
Requires:	python3-plist >= 2.2.0

%description -n python3-imobiledevice
libimobiledevice Python 3 bindings.

%description -n python3-imobiledevice -l pl.UTF-8
Wiązania libimobiledevice dla Pythona 3.

%prep
%setup -q
%patch -P 0 -p1
%patch -P 1 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
install -d build
cd build
../%configure \
	%{!?with_openssl:--disable-openssl} \
	--disable-silent-rules \
	%{!?with_static_libs:--disable-static} \
	%{!?with_cython:--without-cython}

%{__make}
cd ..

%if %{with python3}
topdir=$(pwd)
install -d build-py3
cd build-py3
../%configure \
	PYTHON=%{__python3} \
	--disable-silent-rules \
	%{!?with_static_libs:--disable-static}

%{__make} -C cython \
	top_builddir="${topdir}/build"
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libimobiledevice-1.0.la

%if %{with cython}
%{__rm} $RPM_BUILD_ROOT%{py_sitedir}/*.la \
	%{?with_static_libs:$RPM_BUILD_ROOT%{py_sitedir}/*.a}
%endif

%if %{with python3}
%{__make} -C build-py3/cython install \
	DESTDIR=$RPM_BUILD_ROOT \
	top_builddir="$(pwd)/build"

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
%attr(755,root,root) %{_bindir}/idevice_id
%attr(755,root,root) %{_bindir}/idevicebackup
%attr(755,root,root) %{_bindir}/idevicebackup2
%attr(755,root,root) %{_bindir}/idevicecrashreport
%attr(755,root,root) %{_bindir}/idevicedate
%attr(755,root,root) %{_bindir}/idevicedebug
%attr(755,root,root) %{_bindir}/idevicedebugserverproxy
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
%attr(755,root,root) %{_libdir}/libimobiledevice-1.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libimobiledevice-1.0.so.6
%{_mandir}/man1/idevice_id.1*
%{_mandir}/man1/idevicebackup.1*
%{_mandir}/man1/idevicebackup2.1*
%{_mandir}/man1/idevicecrashreport.1*
%{_mandir}/man1/idevicedate.1*
%{_mandir}/man1/idevicedebug.1*
%{_mandir}/man1/idevicedebugserverproxy.1*
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
%attr(755,root,root) %{_libdir}/libimobiledevice-1.0.so
%{_includedir}/libimobiledevice
%{_pkgconfigdir}/libimobiledevice-1.0.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libimobiledevice-1.0.a
%endif

%files apidocs
%defattr(644,root,root,755)
%doc docs/html/*

%if %{with cython}
%files -n python-imobiledevice
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/imobiledevice.so
%endif

%if %{with python3}
%files -n python3-imobiledevice
%defattr(644,root,root,755)
%attr(755,root,root) %{py3_sitedir}/imobiledevice.so
%endif
