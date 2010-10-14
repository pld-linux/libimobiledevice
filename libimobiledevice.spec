#
# Conditional build:
%bcond_without	static_libs	# don't build static libraries

Summary:	Library for connecting to mobile devices
Summary(pl.UTF-8):	Biblioteka do łączenia się z urządzeniami mobilnymi
Name:		libimobiledevice
Version:	1.0.3
Release:	1
License:	LGPL v2+
Group:		Libraries
Source0:	http://www.libimobiledevice.org/downloads/%{name}-%{version}.tar.bz2
# Source0-md5:	68e68b5c2bea3ad99917add839d32cb2
URL:		http://www.libimobiledevice.org/
BuildRequires:	autoconf >= 2.61
BuildRequires:	automake
BuildRequires:	glib2-devel >= 1:2.14.1
BuildRequires:	gnutls-devel >= 1.6.3
BuildRequires:	libgcrypt-devel
BuildRequires:	libplist-devel >= 0.15
BuildRequires:	libtasn1-devel >= 1.1
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	swig-python >= 1.3.21
BuildRequires:	usbmuxd-devel >= 0.1.4
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
Requires:	glib2-devel >= 1:2.14.1
Requires:	gnutls-devel >= 1.6.3
Requires:	libplist-devel >= 0.15
Requires:	libtasn1-devel >= 1.1
Requires:	usbmuxd-devel >= 0.1.4

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

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{!?with_static_libs:--disable-static} \
	--disable-silent-rules
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{py_sitedir}/imobiledevice/*.{a,la}

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
%attr(755,root,root) %{_bindir}/idevice_id
%attr(755,root,root) %{_bindir}/ideviceimagemounter
%attr(755,root,root) %{_bindir}/ideviceinfo
%attr(755,root,root) %{_bindir}/idevicepair
%attr(755,root,root) %{_bindir}/idevicescreenshot
%attr(755,root,root) %{_bindir}/idevicesyslog
%attr(755,root,root) %{_libdir}/libimobiledevice.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libimobiledevice.so.1
%{_mandir}/man1/idevice_id.1*
%{_mandir}/man1/idevicebackup.1*
%{_mandir}/man1/ideviceimagemounter.1*
%{_mandir}/man1/ideviceinfo.1*
%{_mandir}/man1/idevicescreenshot.1*
%{_mandir}/man1/idevicesyslog.1*

%files devel
%defattr(644,root,root,755)
%doc docs/html/
%attr(755,root,root) %{_libdir}/libimobiledevice.so
%{_libdir}/libimobiledevice.la
%{_includedir}/libimobiledevice
%{_pkgconfigdir}/libimobiledevice-1.0.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libimobiledevice.a
%endif

%files -n python-imobiledevice
%defattr(644,root,root,755)
%dir %{py_sitedir}/imobiledevice
%attr(755,root,root) %{py_sitedir}/imobiledevice/_imobiledevice.so
%{py_sitedir}/imobiledevice/*.py[co]
