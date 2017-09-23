INSTRUCTIONS ON HOW TO BUILD THIS PROGRAM

Windows
I did this in Wine:

Install Python:
wine msiexec /i setup/python-3.4.4rc1.msi

Install dependencies:
wine python -m pip install pypiwin32
wine python Scripts/pywin32_postinstall.py -install

Build:
wine $HOME/.wine/drive_c/Python34/python.exe setup_win.py build

Avoid gencache.py problem:
cd build/exe.win32-3.4
cp -r ~/.wine/drive_c/Python34/Lib/importlib/ ~/.wine/drive_c/Python34/Lib/site-packages/win32com* .
mv win32comext/shell win32com
rm -r win32comext

Add the following Tkinter's folders/files from mclient's build:
tk, tcl, tcl86t.dll, tk86t.dll

Add 'dic.txt', 'in.txt', 'resources', 'locale'

Check it:
wine replacer.exe
