# This if a sample spec file for mcos-openstack

Summary:  mcos-openstack-base
Name:     mcos-openstack-base
Version:  1.1
Release:  1
Vendor:   byq
License:  GPL
Source0:  %{name}-%{version}.tar.gz
Group:    Applications/Text

%description
The mcos-openstack uses to config openstack environment.

%prep
%setup -q

%build
%install
#echo `pwd`
install -d %{buildroot}/usr/local/bin
cp change-dashboard-style %{buildroot}/usr/local/bin
cp setup-static-address   %{buildroot}/usr/local/bin

install -d %{buildroot}/usr/local/include
cp dashboard.css %{buildroot}/usr/local/include

install -d %{buildroot}/var/lib/iso/
cp cirros-0.3.3-x86_64-disk.img %{buildroot}/var/lib/iso/
cp cirros-0.3.3-x86_64-disk.vmdk %{buildroot}/var/lib/iso/
%files
/usr/*
/var/*



