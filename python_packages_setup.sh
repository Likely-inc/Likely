# update repos
echo "updating apt repos"
apt-get update

# install python packages
echo "installing python packages"
conda update conda
conda install scikit-learn
conda install tornado
conda install beatiful-soup
