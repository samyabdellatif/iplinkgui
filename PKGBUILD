# Maintainer: Samy Abdellatif samiahmed086@gmail.com
pkgname=netui-gtk
pkgver=0.0.1
pkgrel=1
pkgdesc="A GUI tool for managing physical network interfaces"
arch=('i686' 'x86_64')
url="git+https://github.com/samyabdellatif/netui-gtk/dist"
license=('MIT')
groups=('base-devel')
depends=('python3' 'gtk3' 'dhcpcd')
makedepends=('python-setuptools')
install='netui-gtk.install'
source=("$pkgname-$pkgver.tar.gz")
md5sums=('7baeb06b4ad25687543c6e48ea6e2ad4') #autofill using updpkgsums
#validpgpkeys=()

# build() {
#   cd "$pkgname-$pkgver"

#   ./configure
#   make
# }

package() {
  cd "$pkgname-$pkgver"

  make DESTDIR="$pkgdir/" install
}