# This if a sample spec file for mcos-openstack

Summary:  mcos-node-info-udp
Name:     mcos-node-info-udp
Version:  1.1
Release:  1
Vendor:   byq
License:  GPL
Source0:  %{name}-%{version}.tar.gz
Group:    Applications/Text

%description
The mcos-openstack uses to send node info to deploy machine.

%prep
%setup -q

%build
%install
#echo `pwd`
install -d %{buildroot}/usr/share/client_node_info/
cp nodeInfoUdp.py    %{buildroot}/usr/share/client_node_info

install -d %{buildroot}/lib/systemd/system/
cp nodeInfoUdp.service %{buildroot}/lib/systemd/system

install -d %{buildroot}/usr/local/bin/
cp nodeinfoudp        %{buildroot}/usr/local/bin

install -d %{buildroot}/etc/yum.repos.d/
cp openstack-deploy.repo %{buildroot}/etc/yum.repos.d/

%files
/usr/share/client_node_info/*
/lib/systemd/system/*
/usr/local/bin/*
/etc/yum.repos.d/*


