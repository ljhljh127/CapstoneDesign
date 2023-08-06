OPENSSL_VER=1.1.0g
mkdir openssl
cd openssl
wget https://www.openssl.org/source/openssl-${OPENSSL_VER}.tar.gz
tar xf openssl-${OPENSSL_VER}.tar.gz
cd openssl-${OPENSSL_VER}
./config zlib shared no-ssl3
make -j4
sudo make install
