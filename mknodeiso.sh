#!/bin/bash
#
# 1. Install Mini CentOS with english.
# 2. Create packages list.
#       cat /root/install.log | grep Installing | sed 's/Installing //g' > ./PackageList.
# 3. Install tools for create iso.
#       yum -y install anaconda repodata createrepo mkisofs rsync 
# 4. Run mcos.sh.
# 5. Root password is rootroot.

# Init EVN.
VERSION=`cat ./iso/version`
STORAGE=http://192.168.1.40/plibs/storage/cDesktop/
CUR_PATH=`pwd`
DATETIME=`date -d today +"%Y%m%d%H%M"`
DIST=`rpm -E %{dist}`
ISO_NAME=MCOS-Openstack-node-V${VERSION}-${DATETIME}.iso
ISO_NAME_VERSION=MCOS-Openstack-node-V${VERSION}.iso
SRC_PATH=/CentOS
#CENTOS_ISO=$CUR_PATH/iso/CentOS-7-x86_64-Minimal-1503-01.iso
CENTOS_ISO=../copenstack-server/isos/CentOS-7-x86_64-DVD-1503-01.iso
#HTTP_ISO=$STORAGE/oiso/CentOS/CentOS-6.5-x86_64-bin-DVD1.iso
#HTTP_ISO=http://192.168.1.25/cilib/mcos-openstack/iso/CentOS-7-x86_64-DVD-1503-01.iso
TMP_PATH=$CUR_PATH/iso_cache
PKG_LIST=$CUR_PATH/iso/PackageList
PKG_LIST_NUM=`cat $PKG_LIST | wc -l`
#PICTURE_RES=${CUR_PATH}/iso/oem/res
ISO_NRPM_PATH=$CUR_PATH/iso/extras/Mcos-extras
NRPM_CACHE_PATH=$CUR_PATH/node_cache
NRPM_RPMS=$NRPM_CACHE_PATH/RPMS/
#GIT_URL="git@192.168.1.202:cOpenstack/openstack-client.git"


#创建打iso临时目录
if [ -d ${TMP_PATH} ]; then
    rm -rf ${TMP_PATH}
fi
mkdir ${TMP_PATH}

if [ -d $SRC_PATH ]; then umount $SRC_PATH; rm -rf $SRC_PATH; fi
if [ -d $TMP_PATH ]; then rm -rf $TMP_PATH; fi

mkdir -p $SRC_PATH
mkdir -p $TMP_PATH

# Mount iso to $SRC_PATH.
echo "Mount iso to $SRC_PATH ......"
if [ -f $CENTOS_ISO ]; then
    echo "$CENTOS_ISO exist."
else
    cd $CUR_PATH/iso
    wget $HTTP_ISO
fi
cd $CUR_PATH
mount -o loop $CENTOS_ISO $SRC_PATH

# Sync cd.
echo "Sync from $SRC_PATH to $TMP_PATH ......"
cd $SRC_PATH
rsync -av --exclude=Packages . $TMP_PATH
mkdir -p $TMP_PATH/Packages

cd $CUR_PATH
#./changepic.sh

# Copy rpm to tmp path.
echo "Copy Packages to $TMP_PATH/Packages ......"
i=1
while [ $i -le $PKG_LIST_NUM ] ; do
    line=`head -n $i $PKG_LIST | tail -n -1`
    name=`echo $line | awk '{print $1}'`
    # version=`echo $line | awk '{print $3}' | cut -f 2 -d :`
    UPDATENAME=`find $SRC_PATH/Packages/* -maxdepth 1 -name "$name*" -type f -print`
    # in case the copy failed
    if [ -z "$UPDATENAME" ] ; then
        echo "Not found $SRC_PATH/Packages/$name*."
    else
        echo "cp $SRC_PATH/Packages/$name*."
        cp $SRC_PATH/Packages/$name* $TMP_PATH/Packages/
    fi
    i=`expr $i + 1`
done

# copy extras rpm-packages to $TMP_PATH/Packages
#echo "Copy extras rpm-packages to $TMP_PATH/Packages/ ..."
cpextersrpm() {
for pkg in `find $CUR_PATH/iso/extras/ -name "*.rpm"`; do cp ${pkg} $TMP_PATH/Packages/; done
}

# Copy script file to tmp path.
echo "Copy script to $TMP_PATH/isolinux ......"
rm -rf $TMP_PATH/isolinux/isolinux.cfg
cp $CUR_PATH/iso/script/*.cfg $TMP_PATH/isolinux/
cp $CUR_PATH/iso/script/*.ks $TMP_PATH/isolinux/
sed -i "s/PRODUCT_NAME/MCOS-Openstack-manager ${VERSION}/" $TMP_PATH/isolinux/isolinux.cfg

# make node rpm packages
mkrpm() {
    cd $CUR_PATH
    chmod +x mknoderpm.sh
    ./mknoderpm.sh
    [ $? -ne 0 ] && exit 1
    rm -f ${ISO_NRPM_PATH}/*
    cp ${NRPM_RPMS}/x86_64/*.rpm ${ISO_NRPM_PATH}/
}

# Change picture.
change_pic() {
    echo "Change picture ......"
    cp -fv $CUR_PATH/res/splash.jpg $TMP_PATH/isolinux/
    mkdir $MED_PATH/install
    mount -o loop $SRC_PATH/images/install.img $MED_PATH/install
    if [ -d /tmp/install ]; then rm -rf /tmp/install; fi
    if [ -f /tmp/install.img ]; then rm -rf /tmp/install.img; fi
    rsync -av $MED_PATH/install /tmp/
    umount $MED_PATH/install
    cp -fv $CUR_PATH/res/progress_first.png /tmp/install/usr/share/anaconda/pixmaps/
    cp -fv $CUR_PATH/res/progress_first-lowres.png /tmp/install/usr/share/anaconda/pixmaps/
    cp -fv $CUR_PATH/res/splash.png /tmp/install/usr/share/anaconda/pixmaps/
    cp -fv $CUR_PATH/res/syslinux-splash.png /tmp/install/usr/share/anaconda/pixmaps/
    sed -i 's/Minimal/MCOS/g' /tmp/install/usr/lib/anaconda/installclasses/rhel.py
    #cd /tmp/install/usr/share/locale
    #rm -rf ls | egrep -v '(en_us|local.alias|zh_CN)'
    cd /tmp
    mksquashfs install install.img
    cp -fv install.img $TMP_PATH/images/
}

create_yum() {
    cd $TMP_PATH/
    rm -rf $TMP_PATH/repodata/*
    cp $CUR_PATH/iso/script/c7-x86_64-comps.xml $TMP_PATH/repodata/c7-x86_64-comps.xml
    #declare -x discinfo=`head -1 .discinfo`
    createrepo -g $TMP_PATH/repodata/c7-x86_64-comps.xml ./
    #createrepo  -g repodata/c7-x86_64-comps.xml ./
}

# Create iso.
build_iso() {
    echo "Create iso ......"
    cd $TMP_PATH
    rm -f *.iso
    mkisofs -o $ISO_NAME -b isolinux/isolinux.bin -c isolinux/boot.cat -no-emul-boot -boot-load-size 4 -boot-info-table -R -J -v -T $TMP_PATH/
    #implantisomd5 $ISO_PATH/$ISO_NAME
    cp $ISO_NAME $ISO_NAME_VERSION
    [ $? -ne 0 ] && exit 1
}

mkiso() {
    mkrpm
    cpextersrpm
    create_yum
#   change_pic
    build_iso
}

mkiso

mv MCOS-Openstack-node-V1.1.0.iso Openstack-node-x86_64.iso
#将node iso打成tar.gz包以便打到部署iso中
tar zcvf Openstack-node-x86_64.tar.gz Openstack-node-x86_64.iso
#mv Openstack-node-x86_64.tar.gz /home/byq/openstack-server/extsrc/mcos-deploy-node-iso-1.1/

umount $SRC_PATH; rm -rf $SRC_PATH
cd $CUR_PATH
cp ./iso_cache/Openstack-node-x86_64.tar.gz ../copenstack-server/deploy/src/mcos-deploy-node-iso-1.1/ -rf
