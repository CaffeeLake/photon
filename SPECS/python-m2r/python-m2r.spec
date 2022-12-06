Summary:        Markdown to reStructuredText converter.
Name:           python3-m2r
Version:        0.2.1
Release:        3%{?dist}
License:        MIT
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.python.org/pypi/m2r
Source0:        https://github.com/miyakogi/m2r/archive/v%{version}/m2r-%{version}.tar.gz
%define sha512  m2r=4e68e8d5a2d4645d2f7c68c0412b24e1f69845af344a96b8a7120106117e9f08ebeba1ddf0351e33dc6eeb475f89836caf1eefe6168ad003750bfa9081534bbe

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
BuildRequires:  python3-mistune
BuildRequires:  python3-docutils
%if %{with_check}
BuildRequires:  python3-Pygments
BuildRequires:  curl-devel
BuildRequires:  openssl-devel
BuildRequires:  python3-pip
%endif

Requires:       python3
Requires:       python3-libs
Requires:       python3-mistune
Requires:       python3-docutils

BuildArch:      noarch

%description
M2R converts a markdown file including reST markups to a valid reST format.

Why another converter?

I wanted to write sphinx document in markdown, since it’s widely used now and easy to write code blocks and lists. However, converters using pandoc or recommonmark do not support many reST markups and sphinx extensions. For example, reST’s reference link like see `ref`_ (this is very convenient in long document in which same link appears multiple times) will be converted to a code block in HTML like see <code>ref</code>_, which is not expected.

%prep
%autosetup -n m2r-%{version}

%build
%py3_build

%install
%py3_install
mv %{buildroot}/%{_bindir}/m2r %{buildroot}/%{_bindir}/m2r3

%check
pip3 install mock
python3 setup.py test -s tests

%files
%defattr(-,root,root)
%{python3_sitelib}/*
%{_bindir}/m2r3

%changelog
* Mon Nov 28 2022 Prashant S Chauhan <psinghchauha@vmware.com> 0.2.1-3
- Update release to compile with python 3.11
* Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 0.2.1-2
- openssl 1.1.1
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 0.2.1-1
- Automatic Version Bump
* Sat Jun 20 2020 Tapas Kundu <tkundu@vmware.com> 0.2.0-4
- Mass removal python2
* Thu Feb 27 2020 Tapas Kundu <tkundu@vmware.com> 0.2.0-3
- Fix makecheck
* Mon Nov 26 2018 Tapas Kundu <tkundu@vmware.com> 0.2.0-2
- Fix makecheck
- Removed buildrequires from subpackage
* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 0.2.0-1
- Update to version 0.2.0
* Fri Jul 21 2017 Divya Thaluru <dthaluru@vmware.com> 0.1.7-1
- Updated version to 0.1.7
- Fixed make check errors
* Mon Jun 19 2017 Xiaolin Li <xiaolinl@vmware.com> 0.1.5-3
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
* Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 0.1.5-2
- Separate the python2 and python3 scripts in the bin directory
* Mon Mar 20 2017 Xiaolin Li <xiaolinl@vmware.com> 0.1.5-1
- Initial packaging for Photon
