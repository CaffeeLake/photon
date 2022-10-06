%global major 78

Summary:       Mozilla's JavaScript engine.
Name:          mozjs
Version:       78.15.0
Release:       4%{?dist}
Group:         Applications/System
Vendor:        VMware, Inc.
License:       GPLv2+ or LGPLv2+ or MPL-2.0
URL:           https://developer.mozilla.org/en-US/docs/Mozilla/Projects/SpiderMonkey
Distribution:  Photon

Source0: https://ftp.mozilla.org/pub/firefox/releases/%{version}esr/source/firefox-%{version}esr.source.tar.xz
%define sha512 firefox-%{version}=ac3de735b246ce4f0e1619cd2664321ffa374240ce6843e785d79a350dc30c967996bbcc5e3b301cb3d822ca981cbea116758fc4122f1738d75ddfd1165b6378

Patch0:        emitter.patch
Patch1:        emitter_test.patch
# Build fixes
Patch2:        init_patch.patch
Patch3:        spidermonkey_checks_disable.patch

BuildRequires: which
BuildRequires: python3-xml
BuildRequires: python3-libs
BuildRequires: python3-devel
BuildRequires: zlib-devel
BuildRequires: clang-devel
BuildRequires: icu-devel >= 70.1
BuildRequires: rust
BuildRequires: autoconf = 2.13

Requires:      icu >= 70.1
Requires:      python3
Requires:      python3-libs

Obsoletes:     mozjs60
Obsoletes:     js

%description
Mozilla's JavaScript engine includes a just-in-time compiler (JIT) that compiles
JavaScript to machine code, for a significant speed increase.

%package       devel
Summary:       mozjs devel
Group:         Development/Tools
Requires:      %{name} = %{version}-%{release}

%description   devel
This contains development tools and libraries for SpiderMonkey.

%prep
%autosetup -p1 -n firefox-%{version}
rm -rf modules/zlib

%build
cd js/src
%configure \
    --with-system-icu \
    --enable-readline \
    --disable-jemalloc \
    --disable-tests \
    --with-system-zlib

%make_build

%install
cd js/src
%make_install %{?_smp_mflags}
chmod -x %{buildroot}%{_libdir}/pkgconfig/*.pc
# remove non required files
rm %{buildroot}%{_libdir}/libjs_static.ajs
find %{buildroot} -name '*.la' -delete

%ldconfig_scriptlets

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_bindir}/js%{major}
%{_bindir}/js%{major}-config
%{_libdir}/libmozjs-%{major}.so

%files devel
%defattr(-,root,root)
%{_includedir}/mozjs-%{major}
%{_libdir}/pkgconfig/mozjs-%{major}.pc

%changelog
* Tue Oct 04 2022 Shreenidhi Shedi <sshedi@vmware.com> 78.15.0-4
- Bump version as a part of icu upgrade
* Wed Sep 28 2022 Shreenidhi Shedi <sshedi@vmware.com> 78.15.0-3
- Bump version as a part of clang upgrade
* Tue Dec 07 2021 Alexey Makhalov <amakhalov@vmware.com> 78.15.0-2
- Require specific version of icu
* Tue Oct 19 2021 Shreenidhi Shedi <sshedi@vmware.com> 78.15.0-1
- Version upgrade
* Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 78.10.0-1
- Automatic Version Bump
* Fri Feb 19 2021 Alexey Makhalov <amakhalov@vmware.com> 78.3.1-2
- Remove python2 requirements
* Mon Oct 05 2020 Ankit Jain <ankitja@vmware.com> 78.3.1-1
- Updated to 78.3.1
* Tue Aug 25 2020 Ankit Jain <ankitja@vmware.com> 68.11.0-2
- Removed autoconf213 dependency and obsoletes js
* Sat Oct 26 2019 Ankit Jain <ankitja@vmware.com> 68.11.0-1
- initial version
