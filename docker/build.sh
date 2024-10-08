#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
BUILDROOT=$DIR/..
 
#cd $BUILDROOT
#echo $BUILDROOT
echo $DIR

CONTAINER="supply_chain_optimization"   #Replace it with the name of your container
#VERSION=`git describe --abbrev=0 --tags`
 
IMAGE_NAME="${CONTAINER}"
cmd="docker build -t $IMAGE_NAME ."
echo 1
echo $cmd
eval $cmd
$SHELL
#docker push $IMAGE_NAME