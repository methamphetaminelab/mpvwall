pkgname=mpvwall-git
pkgver=0.1.2.r0.g$(git rev-parse --short HEAD)
pkgrel=1
pkgdesc="Terminal UI manager for mpvpaper video wallpapers"
arch=('any')
url="https://github.com/methamphetaminelab/mpvwall"
license=('MIT')
depends=('python' 'mpv' 'mpvpaper' 'hyprland')
makedepends=('git')
provides=('mpvwall')
conflicts=('mpvwall')

source=("git+$url.git")
sha256sums=('SKIP')

pkgver() {
  cd mpvwall
  git describe --long --tags | sed 's/^v//;s/-/.r/;s/-/./'
}

build() {
  cd mpvwall
  python -m build --wheel --no-isolation
}

package() {
  cd mpvwall
  python -m installer --destdir="$pkgdir" dist/*.whl
}
