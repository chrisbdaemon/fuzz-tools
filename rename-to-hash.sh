SRCDIR=$1
DSTDIR=$2

if [ $# -ne 2 ]; then
    echo "Usage: ./$0 <src dir> <dst dir>"
    exit -1
fi

for F in $SRCDIR/*; do
    mv -v "$F" "$DSTDIR/$(sha256sum "$F" | cut -d' ' -f1)";
done
