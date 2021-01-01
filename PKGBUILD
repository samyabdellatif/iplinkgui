# Maintainer: Samy Abdellatif samiahmed086@gmail.com
pkgname=netui-gtk
pkgver=0.0.1
pkgrel=1
pkgdesc="A GUI tool for managing physical network interfaces"
arch=('i686' 'x86_64')
url="git+https://github.com/samyabdellatif/netui-gtk/dist"
license=('MIT')
groups=('base-devel')
depends=('python-setuptools' 'python3' 'gtk3' 'dhcpcd')
install='netui-gtk.install'
source=("$pkgname-$pkgver.tar.gz")
md5sums=('f07705c3dccc5a21cb620dcddf193d63') #autofill using updpkgsums
#validpgpkeys=()

build() {
  cd "$pkgname-$pkgver"
  python setup.py build
}

package() {
  chmod a+x "$pkgname-$pkgver"
  cd "$pkgname-$pkgver"
  python setup.py install --root="$pkgdir/" --optimize=1 --skip-build
}