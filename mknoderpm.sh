#!/bin/bash

CUR_PATH=`pwd`
NSRC_PATH=$CUR_PATH/node/src
NSPEC_PATH=$CUR_PATH/node/spec
NRPM_CACHE_PATH=$CUR_PATH/node_cache
NRPM_SOURCES=$NRPM_CACHE_PATH/SOURCES
NRPM_SPECS=$NRPM_CACHE_PATH/SPECS
NRPM_RPMS=$NRPM_CACHE_PATH/RPMS
ISO_NRPM_PATH=$CUR_PATH/iso/extras/Mcos-extras

#make build cache dir
echo "clean $NRPM_CACHE_PATH"
if [ -d $NRPM_CACHE_PATH ]; then rm -rf $NRPM_CACHE_PATH; fi
mkdir -p {$NRPM_SOURCES,$NRPM_SPECS,$NRPM_RPMS}

#make ext source to tar file
cd $NSRC_PATH
for subdir in `ls`; do
    if [ -d "$subdir" ]; then
        echo "Compress directory $subdir"
        tar zcvf $subdir.tar.gz $subdir;
        echo ""
    fi
done

#move the tar file to  SOURCES
echo "Move compressed file to $NRPM_SOURCES"
mv ./*.tar.gz $NRPM_SOURCES

#copy the spec file to SPECS
fcho "Move spec file to $NRPM_SPECS"
cp -rf $NSPEC_PATH/*.spec $NRPM_SPECS/

#create the rpm 
cd $NRPM_SPECS
for specs in `ls`; do
    if [ -f "$specs" ]; then
        echo "build $specs to rpm";
        rpmbuild -bb --define="%_topdir $NRPM_CACHE_PATH" $specs;  
	[ $? -ne 0 ] && exit 1
    fi
done

cd $NRPM_RPMS
rm *debuginfo* -rf

#copy the rpm to iso extras dir"
#cp ${NRPM_RPMS}/x86_64/* ${ISO_NRPM_PATH}/  


 




