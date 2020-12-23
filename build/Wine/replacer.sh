#!/bin/bash

export "WINEPREFIX=$HOME/wine/python38_vista"

product="ReplaceR"
productlow='replacer'
python="$WINEPREFIX/drive_c/Python"
pyinstaller="$python/Scripts/pyinstaller.exe"
binariesdir="$HOME/binaries"
srcdir="$HOME/bin/$product/src"
resdir="$HOME/bin/$product/resources"
cmd="$HOME/bin/$product/build/Wine/$productlow.cmd"
tmpdir="$WINEPREFIX/drive_c/$product" # Will be deleted!
builddir="$tmpdir/$product" # Will be deleted!
srcshared="$HOME/bin/skl_shared"
resshared="$WINEPREFIX/drive_c/skl_shared" # Will be overwritten!

if [ ! -e "$pyinstaller" ]; then
    echo "pyinstaller is not installed!"; exit
fi

if [ ! -e "$cmd" ]; then
    echo "File $cmd does not exist!"; exit
fi

if [ ! -d "$binariesdir/$product" ]; then
    echo "Folder $binariesdir/$product does not exist!"; exit
fi

if [ ! -d "$srcdir" ]; then
    echo "Folder $srcdir does not exist!"; exit
fi

if [ ! -d "$resdir" ]; then
    echo "Folder $resdir does not exist!"; exit
fi

if [ ! -d "$srcshared" ]; then
    echo "Folder $srcshared does not exist!"; exit
fi

# Update shared
rm -rf "$resshared"
mkdir -p "$resshared"
cp -r "$srcshared/src" "$resshared/src"
cp -r "$srcshared/resources" "$resshared/resources"

# Build with pyinstaller
rm -rf "$tmpdir"
mkdir -p "$builddir/app" "$tmpdir/app/usr/bin" "$tmpdir/app/resources"
cp -r "$srcdir"/* "$tmpdir"
cp -r "$resdir" "$builddir"
cp "$cmd" "$builddir"
cd "$tmpdir"
# Icon path should be windows-compliant
wine "$pyinstaller" -w -i ./$product/resources/$productlow.ico "$productlow.py"
mv "$tmpdir/dist/$productlow"/* "$builddir/app"
# Tesh launch
cd "$builddir/app"
wine ./$productlow.exe&
# Update the archive
read -p "Update the archive? (y/n) " choice
if [ "$choice" = "n" ] || [ "$choice" = "N" ]; then
    exit;
fi
rm -f "$binariesdir/$product/$productlow-win32.7z"
7z a "$binariesdir/$product/$productlow-win32.7z" "$builddir"
rm -rf "$tmpdir"
