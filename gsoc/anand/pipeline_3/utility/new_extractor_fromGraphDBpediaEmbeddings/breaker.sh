echo "Creating data_fragments folder"
mkdir data_fragments
cd data_fragments
echo "Usage:    ./breaker.sh <size> <name of file to be split>" 
echo "Example:  ./breaker.sh 1000MB pageRank.txt"
echo "It will take some time, please remain calm." 
split -b $1  ../$2