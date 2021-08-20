#! /bin/bash
#$1 -- Project name -- String -- Required
#$2 -- Sampling size -- float -- Required
#$3 -- ubset size -- int -- Required

if [ ! -n "$1" ]; then
    echo "you have not input a project name!"
else
    echo "The project name will be set to $1"
fi
if [ ! -n "$2" ]; then
    echo "you have not specified subset % for preparing data, setting to default -> 20%"
    $2=0.2
else
    e=$(echo "scale=4; $2*100" | bc)
    echo "The subset size will be set to $e%"
fi
if [ ! -n "$3" ]; then
    echo "you have not specified subset for Back-Translation, setting to default -> 2048"
    $3=2048
else
    echo "The subset size will be set to $3"
fi
 echo "Preparing data for BackTranslation."
    wget https://ndownloader.figshare.com/articles/6118505/versions/2
    mkdir ./$1
    unzip 2 -d ./$1/data
    python3 augment_data.py $1/data $2 $3
    