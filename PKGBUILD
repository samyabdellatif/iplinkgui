# Maintainer: Samy Abdellatif samiahmed086@gmail.com
pkgname=netui-gtk3
pkgver=0.0.1
pkgrel=1
pkgdesc="A GUI tool for managing physical network interfaces"
arch=('x86_64')
url=""
license=('GPL')
groups=()
depends=('dhcpcd')
makedepends=()
backup=()
options=()
install=
changelog=
source=($pkgname-$pkgver.tar.gz)
noextract=()
md5sums=() #autofill using updpkgsums

build() {
  cd "$pkgname-$pkgver"

  ./configure --prefix=/usr
  make
}

package() {
  cd "$pkgname-$pkgver"

  make DESTDIR="$pkgdir/" install
}