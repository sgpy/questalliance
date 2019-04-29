# -------------- #
# Configurations #
# -------------- #

USER_HOME="/home/vagrant"
TOX_INI="/vagrant/config/tox.ini"
WORKSPACE_HOME="${USER_HOME}/sandbox"
PROJECT_HOME="${WORKSPACE_HOME}/projects"

# ------------ #
# Env settings #
# ------------ #

sudo echo "LANG=en_US.utf-8" >> /etc/environment
sudo echo "LC_ALL=en_US.utf-8" >> /etc/environment

# -------------------- #
# Install dependencies #
# -------------------- #

sudo yum install nmap wget gcc openssl-devel bzip2-devel libffi-devel unzip -y

# ---------- #
# Get Python #
# ---------- #

cd /usr/src
sudo wget https://www.python.org/ftp/python/3.7.3/Python-3.7.3.tgz
sudo tar xzf Python-3.7.3.tgz
cd Python-3.7.3


# -------------- #
# Install Python #
# -------------- #

sudo ./configure --enable-optimizations
sudo make altinstall
sudo ln -s /usr/local/bin/python3.7 /usr/bin/python3

# ------------- #
# Configure Tox #
# ------------- #

cd ${USER_HOME}
mkdir -p ${WORKSPACE_HOME} && cd ${WORKSPACE_HOME}
python3 -m venv ${WORKSPACE_HOME}/.toxbox
mkdir -p .bin

${WORKSPACE_HOME}/.toxbox/bin/pip install --upgrade pip
${WORKSPACE_HOME}/.toxbox/bin/pip install tox

ln -s ${WORKSPACE_HOME}/.toxbox/bin/tox ${WORKSPACE_HOME}/.bin/tox
ln -s ${WORKSPACE_HOME}/.toxbox/bin/tox-quickstart ${WORKSPACE_HOME}/.bin/tox-quickstart

mkdir -p ${PROJECT_HOME} && cd ${PROJECT_HOME}
cp ${TOX_INI} .
${WORKSPACE_HOME}/.bin/tox

# ------------------ #
# Setup user profile #
# ------------------ #
echo "export USER_HOME=${USER_HOME}" >> ${USER_HOME}/.bashrc
echo 'export WORKSPACE_HOME=${USER_HOME}/sandbox'  >> ${USER_HOME}/.bashrc
echo 'export PROJECT_HOME=${WORKSPACE_HOME}/projects' >> ${USER_HOME}/.bashrc
echo 'PATH="${WORKSPACE_HOME}/.bin:${PATH}"' >> ${USER_HOME}/.bashrc
echo 'export PATH' >> ${USER_HOME}/.bashrc
echo 'source ${PROJECT_HOME}/.tox/py3/bin/activate' >> ${USER_HOME}/.bashrc
echo 'cd ${PROJECT_HOME}' >> ${USER_HOME}/.bashrc

# Reset ownership
sudo chown -R vagrant:vagrant ${WORKSPACE_HOME}

