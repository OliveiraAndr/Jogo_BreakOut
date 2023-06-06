import cx_Freeze

executables = [cx_Freeze.Executable('teste.pygame.py')]

cx_Freeze.setup(
    name="Breakout GAME",
    options={'build_exe': {'packages':['pygame'],
                           'include_files':['Som']}},

    executables = executables
    
)

# No cmd instalar o cx-Freeze 
# 'cx-Freeze'
# Abrir diretorio da pasta no cmd
# 'cd + diretorio da pasta'
# Executar para criar o executável do jogo
# 'python setup.py build'
