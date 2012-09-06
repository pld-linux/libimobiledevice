#
# Conditional build:
%bcond_without	static_libs	# don't build static libraries
%bcond_without	cython		# build with Cython based Python bindings
%bcond_without	openssl		# build with openssl for SSL support
%bcond_with	gnutls		# build with GnuTLS for SSL support

%if %{with gnutls}
%undefine	with_openssl
%endif

Summary:	Library for connecting to mobile devices
Summary(pl.UTF-8):	Biblioteka do łączenia się z urządzeniami mobilnymi
Name:		libimobiledevice
Version:	1.1.4
Release:	1
License:	LGPL v2+
Group:		Libraries
#Source0Download: http://www.libimobiledevice.org/
Source0:	http://www.libimobiledevice.org/downloads/%{name}-%{version}.tar.bz2
# Source0-md5:	3f28cbc6a2e30d34685049c0abde5183
Patch0:		%{name}-cython.patch
URL:		http://www.libimobiledevice.org/
BuildRequires:	autoconf >= 2.61
BuildRequires:	automake
%{?with_gnutls:BuildRequires:	gnutls-devel >= 2.2.0}
BuildRequires:	libgcrypt-devel
BuildRequires:	libplist-devel >= 1.8
BuildRequires:	libstdc++-devel
%{?with_gnutls:BuildRequires:	libtasn1-devel >= 1.1}
BuildRequires:	libtool
%{?with_openssl:BuildRequires:	openssl-devel >= 0.9.8}
BuildRequires:	pkgconfig
%{?with_cython:BuildRequires:	python-Cython >= 0.13.0}
BuildRequires:	python-devel
BuildRequires:	python-modules
BuildRequires:	rpm-pythonprov
BuildRequires:	usbmuxd-devel >= 1.0.8
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
Requires:	libplist-devel >= 1.8
%{?with_gnutls:Requires:	libtasn1-devel >= 1.1}
%{?with_openssl:Requires:	openssl-devel >= 0.9.8}
Requires:	usbmuxd-devel >= 1.0.8

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

%package -n python-imobiledevice
Summary:	libimobiledevice Python bindings
Summary(pl.UTF-8):	Wiązania libimobiledevice dla Pythona
Group:		Development/Languages/Python
Requires:	%{name} = %{version}-%{release}

%description -n python-imobiledevice
libimobiledevice Python bindings.

%description -n python-imobiledevice -l pl.UTF-8
Wiązania libimobiledevice dla Pythona.

%prep
%setup -q
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{!?with_static_libs:--disable-static} \
	%{!?with_cython:--without-cython} \
	%{!?with_openssl:--disable-openssl} \
	--disable-silent-rules
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{py_sitedir}/*.{a,la}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

%py_comp $RPM_BUILD_ROOT%{py_sitedir}
%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS NEWS README
%attr(755,root,root) %{_bindir}/idevicebackup
%attr(755,root,root) %{_bindir}/idevicebackup2
%attr(755,root,root) %{_bindir}/idevicedate
%attr(755,root,root) %{_bindir}/ideviceenterrecovery
%attr(755,root,root) %{_bindir}/idevice_id
%attr(755,root,root) %{_bindir}/ideviceimagemounter
%attr(755,root,root) %{_bindir}/ideviceinfo
%attr(755,root,root) %{_bindir}/idevicepair
%attr(755,root,root) %{_bindir}/idevicescreenshot
%attr(755,root,root) %{_bindir}/idevicesyslog
%attr(755,root,root) %{_libdir}/libimobiledevice.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libimobiledevice.so.3
%{_mandir}/man1/idevicebackup.1*
%{_mandir}/man1/idevicebackup2.1*
%{_mandir}/man1/idevicedate.1*
%{_mandir}/man1/ideviceenterrecovery.1*
%{_mandir}/man1/idevice_id.1*
%{_mandir}/man1/ideviceimagemounter.1*
%{_mandir}/man1/ideviceinfo.1*
%{_mandir}/man1/idevicepair.1*
%{_mandir}/man1/idevicescreenshot.1*
%{_mandir}/man1/idevicesyslog.1*

%files devel
%defattr(644,root,root,755)
%doc docs/html/
%attr(755,root,root) %{_libdir}/libimobiledevice.so
%{_includedir}/libimobiledevice
%{_pkgconfigdir}/libimobiledevice-1.0.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libimobiledevice.a
%endif

%if %{with cython}
%files -n python-imobiledevice
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/imobiledevice.so
%endif
