#!/bin/bash

set -e

# Step 1: Install required system packages
echo "Installing build dependencies..."
sudo apt update
sudo apt install --no-install-recommends -y \
    git python3 bison flex make cmake \
    python3-pip python3-setuptools python3-psutil \
    python3-six python3-wheel rpm binutils

# Step 2: Install Python packages needed for testing
echo "Installing Python packages..."
pip3 install timeout_decorator thrift==0.11.0 osquery pexpect==3.3

# Step 3: Install osquery toolchain
ARCH=$(uname -m)
TOOLCHAIN_URL="https://github.com/osquery/osquery-toolchain/releases/download/1.1.0/osquery-toolchain-1.1.0-${ARCH}.tar.xz"
echo "Downloading osquery toolchain from $TOOLCHAIN_URL ..."
wget -q --show-progress "$TOOLCHAIN_URL"
sudo tar -xf "osquery-toolchain-1.1.0-${ARCH}.tar.xz" -C /usr/local

# Step 4: Install newer CMake
echo "Installing CMake 3.21.4..."
CMAKE_URL="https://cmake.org/files/v3.21/cmake-3.21.4-linux-${ARCH}.tar.gz"
wget -q --show-progress "$CMAKE_URL"
sudo tar -xf "cmake-3.21.4-linux-${ARCH}.tar.gz" -C /usr/local --strip-components=1

# Step 5: Clone and build osquery
echo "Cloning and building osquery..."
if [ ! -d "osquery" ]; then
    git clone https://github.com/osquery/osquery
fi
cd osquery
mkdir -p build && cd build
cmake -DOSQUERY_TOOLCHAIN_SYSROOT=/usr/local/osquery-toolchain ..
cmake --build . -j$(nproc)

echo "Build complete! Binaries located in: $(pwd)/osquery"
