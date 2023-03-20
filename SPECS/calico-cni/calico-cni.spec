Summary:        Calico networking for CNI
Name:           calico-cni
Version:        3.25.0
Release:        1%{?dist}
License:        ASL 2.0
URL:            https://github.com/projectcalico/calico
Source0:        https://github.com/projectcalico/calico/archive/refs/tags/calico-%{version}.tar.gz
%define sha512  calico=8899b65be0b3b93f371942113f6bb0c958b31ff0db106d181152c3c5bf6f2f3e842719bc3ac21c573ae5fd681176ee46222798b43ebf029140a5c32ab27d9fbf
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  git
BuildRequires:  go
Requires:       cni
%define debug_package %{nil}

%description
Project Calico network plugin for CNI. This allows kubernetes to use Calico networking. This repository includes a top-level CNI networking plugin, as well as a CNI IPAM plugin which makes use of Calico IPAM.

%prep
%autosetup -p1 -n calico-%{version}

%build
cd cni-plugin
mkdir -p dist
CGO_ENABLED=0 go build -v -o dist/calico -ldflags "-X main.VERSION= -s -w" ./cmd/calico
CGO_ENABLED=0 go build -v -o dist/calico-ipam -ldflags "-X main.VERSION= -s -w" ./cmd/calico
CGO_ENABLED=0 go build -v -o dist/install -ldflags "-X main.VERSION= -s -w" ./cmd/calico

%install
install -vdm 755 %{buildroot}/opt/cni/bin
install -vpm 0755 -t %{buildroot}/opt/cni/bin/ cni-plugin/dist/calico
install -vpm 0755 -t %{buildroot}/opt/cni/bin/ cni-plugin/dist/calico-ipam
install -vpm 0755 -t %{buildroot}/opt/cni/bin/ cni-plugin/dist/install

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
/opt/cni/bin/calico
/opt/cni/bin/calico-ipam
/opt/cni/bin/install

%changelog
* Thu Mar 09 2023 Prashant S Chauhan <psinghchauha@vmware.com> 3.25.0-1
- Update to 3.25.0
* Thu Mar 09 2023 Piyush Gupta <gpiyush@vmware.com> 3.15.2-8
- Bump up version to compile with new go
* Mon Nov 21 2022 Piyush Gupta <gpiyush@vmware.com> 3.15.2-7
- Bump up version to compile with new go
* Wed Oct 26 2022 Piyush Gupta <gpiyush@vmware.com> 3.15.2-6
- Bump up version to compile with new go
*   Fri Jun 17 2022 Piyush Gupta <gpiyush@vmware.com> 3.15.2-5
-   Bump up version to compile with new go
*   Fri Jun 11 2021 Piyush Gupta<gpiyush@vmware.com> 3.15.2-4
-   Bump up version to compile with new go
*   Fri Feb 05 2021 Harinadh D <hdommaraju@vmware.com> 3.15.2-3
-   Bump up version to compile with new go
*   Fri Jan 15 2021 Piyush Gupta<gpiyush@vmware.com> 3.15.2-2
-   Bump up version to compile with new go
*   Sat Aug 29 2020 Ashwin H <ashwinh@vmware.com> 3.15.2-1
-   Update to 3.15.2
*   Wed May 08 2019 Ashwin H <ashwinh@vmware.com> 3.6.1-1
-   Update to 3.6.1
*   Mon Jan 21 2019 Bo Gan <ganb@vmware.com> 1.11.2-3
-   Build using go 1.9.7
*   Mon Sep 24 2018 Tapas Kundu <tkundu@vmware.com> 1.11.2-2
-   Build using go version 1.9
*   Fri May 18 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 1.11.2-1
-   calico-cni v1.11.2
*   Thu Dec 07 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.11.0-2
-   Cache build dependencies in our repo.
*   Fri Nov 03 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.11.0-1
-   calico-cni v1.11.0.
*   Mon Aug 14 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.10.0-1
-   calico-cni for PhotonOS.
