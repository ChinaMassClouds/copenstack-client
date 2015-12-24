# This if a sample spec file for mcos-openstack

Summary:  mcos-node-setscrpit
Name:     mcos-node-setscrpit
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
install -d %{buildroot}/usr/local/bin
cp setup-mysql  %{buildroot}/usr/local/bin
cp setup-rabbitmq  %{buildroot}/usr/local/bin

cp setup-controller-ceilometer %{buildroot}/usr/local/bin
cp setup-mongodb %{buildroot}/usr/local/bin
cp setup-controller-heat %{buildroot}/usr/local/bin
cp setup-controller-node %{buildroot}/usr/local/bin
cp setup-controller-cinder %{buildroot}/usr/local/bin
cp setup-controller-glance %{buildroot}/usr/local/bin
cp setup-controller-horizon %{buildroot}/usr/local/bin
cp setup-controller-keystone %{buildroot}/usr/local/bin
cp setup-controller-neutron %{buildroot}/usr/local/bin
cp setup-controller-nova %{buildroot}/usr/local/bin
cp setup-controller-node %{buildroot}/usr/local/bin


cp views.py %{buildroot}/usr/local/bin
cp forms.py %{buildroot}/usr/local/bin
cp backend.py %{buildroot}/usr/local/bin
cp django.mo %{buildroot}/usr/local/bin
cp openstack_auth.pot %{buildroot}/usr/local/bin

cp setup-network-gre-node %{buildroot}/usr/local/bin
cp setup-network-vlan-node %{buildroot}/usr/local/bin
cp setup-network-vxlan-node %{buildroot}/usr/local/bin

cp setup-store-cinder %{buildroot}/usr/local/bin
cp expand-cinder-store %{buildroot}/usr/local/bin
cp reduce-cinder-store %{buildroot}/usr/local/bin

cp setup-store-nfs %{buildroot}/usr/local/bin
cp expand-nfs-store %{buildroot}/usr/local/bin

cp setup-compute-vlan-node %{buildroot}/usr/local/bin
cp setup-compute-vxlan-node %{buildroot}/usr/local/bin
cp setup-compute-gre-node %{buildroot}/usr/local/bin

cp setup-deploy-zabbix %{buildroot}/usr/local/bin
cp setup-zabbix-agent %{buildroot}/usr/local/bin
cp clear-zabbix %{buildroot}/usr/local/bin
cp setup-ceilometer-snmp %{buildroot}/usr/local/bin

cp -rf compute-node-clear %{buildroot}/usr/local/bin
cp -rf controller-node-clear %{buildroot}/usr/local/bin
cp -rf network-node-clear %{buildroot}/usr/local/bin
cp -rf store-node-clear %{buildroot}/usr/local/bin

cp -rf setup-ceph %{buildroot}/usr/local/bin

cp -rf send-service-report %{buildroot}/usr/local/bin

cp mongodb_clear %{buildroot}/usr/local/bin

install -d %{buildroot}/usr/local/share/mongodb
cp mongodb_clear.py %{buildroot}/usr/local/share/mongodb

install -d %{buildroot}/usr/local/include
cp massclouds_console.py %{buildroot}/usr/local/include
cp tsTclnt.py %{buildroot}/usr/local/include

install -d %{buildroot}/etc/
#cp openstack.cfg %{buildroot}/etc/

cp manualDeploy_file/manualDeployment.py %{buildroot}/usr/local/bin
cp manualDeploy_file/openstack.cfg %{buildroot}/etc/
cp manualDeploy_file/openstack_deploy.conf %{buildroot}/etc/
cp manualDeploy_file/manualDeploy-readme.txt %{buildroot}/etc/

%files
/usr/local/*
#/usr/local/include/*
/etc/*

