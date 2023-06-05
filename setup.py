import cx_Freeze

executables = [cx_Freeze.Executable('Breakout.py')]

cx_Freeze.setup(
    name="Breakout GAME",
    options={'build_exe': {'packages':['pygame'],
                           'include_files':['Som']}},

    executables = executables
    
)