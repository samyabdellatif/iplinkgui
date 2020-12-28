# Maintainer: Samy Abdellatif samiahmed086@gmail.com
pkgname=netui-gtk
pkgver=1.0.0
pkgrel=1
pkgdesc="A GUI tool for managing physical network interfaces"
arch=('i686' 'x86_64')
url="git+https://github.com/samyabdellatif/netui-gtk"
license=('MIT')
groups=('base-devel')
depends=('python3' 'gtk3' 'dhcpcd')
makedepends=('python-setuptools')
install='netui-gtk.install'
source=("git+https://github.com/samyabdellatif/netui-gtk/dist/$pkgname-$pkgver.tar.gz")
md5sums=() #autofill using updpkgsums
validpgpkeys=()

build() {
  cd "$pkgname-$pkgver"

  ./configure --prefix=/usr
  make
}
check() {
	cd "$pkgname-$pkgver"
	make -k check
}

package() {
  cd "$pkgname-$pkgver"

  make DESTDIR="$pkgdir/" install
}