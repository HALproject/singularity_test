# Singularity Setup Instructions
## 1. Install Dependencies
```bash
sudo apt-get update
sudo apt-get install -y \
  autoconf \
  automake \
  cryptsetup\
  fuse2fs \
  git \
  fuse3 \
  libfuse3-dev \
  libseccomp-dev \
  libtool \
  pkg-config\
  runc \
  squashfs-tools \
  uidmap\
  wget \
  zlib1g-dev
```

## 2. Install Go
```bash
wget -O /tmp/go.tar.gz https://dl.google.com/go/go1.26.1.linux-amd64.tar.gz
sudo tar -C /usr/local -xzf/tmp/go.tar.gz
echo 'export GOROOT=/usr/local/go' >> ~/.bashrc
echo 'export GOPATH=$HOME/go' >> ~/.bashrc
echo 'export PATH=$GOROOT/bin:$GOPATH/bin:$PATH' >> ~/.bashrc
source ~/.bashrc
```

## 3. Build and Install Singularity
```bash
wget https://github.com/sylabs/singularity/releases/download/v4.4.1/singularity-ce-4.4.1.tar.gz
tar -xzf singularity-ce-4.4.1.tar.gz
cd singularity-ce-4.4.1
./mconfig
make -C builddir -j$(nproc)
sudo make -C builddir install
```

## 4. Verify Installation
```bash
singularity --version
```
You should see the installed version of Singularity, confirming that the installation was successful.

## 5. Create a Singularity Image from a Definition File
```bash
sudo singularity build python_env.sif Singularity
# or
sudo singularity build python_env.sif python_env.def
```
This command will create a Singularity image named python_env.sif based on the definition file `Singularity or python_env.def. Make sure to have the respective definition file in the current directory before running this command.

## 6. Run a Singularity Container
```bash
singularity run python_env.sif
```
