from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict (packages = []
                    ,includes = ['re']
                    ,excludes = []
                    )

executables = [Executable ('replacer.py'
                          ,base = 'Win32GUI'
                          ,targetName = 'replacer.exe'
                          )
              ]

setup (name = 'ReplaceR'
      ,version = '1'
      ,description = 'Simple batch replace in text files/clipboard'
      ,options = dict(build_exe=buildOptions)
      ,executables = executables
      )
