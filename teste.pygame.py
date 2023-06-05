import pygame
import time
import random
from pygame.locals import *
from sys import exit
import os
##### INICIA O PYGAME ######################################################
pygame.init()
##### CRIAÇÃO DE DIRETORIO #################################################
diretorio_principal = os.path.dirname(__file__)
diretorio_sons = os.path.join(diretorio_principal, 'Som')
##### CONDIÇÕES DE SOM #####################################################
game_start = pygame.mixer.music.load(os.path.join(diretorio_sons,'game-start.mp3'))
pygame.mixer.music.play(1)
musica_fundo = pygame.mixer.Sound(os.path.join(diretorio_sons,'fundo1.mp3'))
musica_fundo.set_volume(0.2)
musica_kick = pygame.mixer.Sound(os.path.join(diretorio_sons,'smw_kick.mp3'))
musica_kick.set_volume(0.25)
musica_pancada = pygame.mixer.Sound(os.path.join(diretorio_sons,'pancada.mp3'))
musica_pancada.set_volume(0.3)
musica_fail = pygame.mixer.Sound(os.path.join(diretorio_sons,'fail.mp3'))
musica_fail.set_volume(0.5)
musica_game_over = pygame.mixer.Sound(os.path.join(diretorio_sons,'game-over.mp3'))
musica_game_over.set_volume(1)
musica_win = pygame.mixer.Sound(os.path.join(diretorio_sons,'win.mp3'))
musica_win.set_volume(1)
musica_click = pygame.mixer.Sound(os.path.join(diretorio_sons,'click-button.mp3'))
musica_click.set_volume(0.5)
musica_lvl = pygame.mixer.Sound(os.path.join(diretorio_sons,'level-passed.mp3'))
musica_lvl.set_volume(1)
musica_clap = pygame.mixer.Sound(os.path.join(diretorio_sons,'claps.mp3'))
musica_clap.set_volume(0.5)
musica_exit = pygame.mixer.Sound(os.path.join(diretorio_sons,'door-closing.mp3'))
musica_exit.set_volume(1)
##### VARIÁVEIS DO JOGO ###################################################
largura = 640
altura = 480
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Breakout")
relogio = pygame.time.Clock()
start_time = 0
tempo = 0
contando = False
margem = 5
lvl = 1
stage = 1
pontuacao = 0
vidas = 3
pontos = 10
raio_bola = 10 // 2
##### DEFINIÇÃO DAS CORES #################################################
cores = [(227, 38, 54), (255, 117, 24), (255, 255, 0), (50, 205, 50), (0, 0, 255), (138, 43, 226)] 
cor_blocos = []
##### POSIÇÃO INICIAL DA BOLA E DA PRANCHA ################################
x_bola = 335
y_bola = 455
x_prancha = 300
y_prancha = 467
##### BOLEANO PARA LANÇAMENTO DA BOLA #####################################
lancar_bola = False
bola_lancada = False
##### VARIÁVEL DE MOVIMENTO DA BOLA #######################################
velocidade_bola_x = 0
velocidade_bola_y = 0
mov_bola_xD = 5
mov_bola_xE = -5
mov_bola_y = -5
##### VARIÁVEIS DOS BLOCOS ################################################
bloco_largura = 50
bloco_altura = 18
padding_left = 2
padding_top = 2
linhas = 4
colunas = 12
bloco_lista = []
##### FUNÇÃO DE CRIAÇÃO DE BLOCOS #########################################
def criar_blocos():
    for linha in range(linhas):
        for coluna in range(colunas):
            x = ((padding_left * coluna) + 7 + padding_left) + \
                (coluna * bloco_largura)
            y = ((padding_top * linha) + 35 + padding_top) + (linha * bloco_altura)
            bloco = pygame.Rect(x, y, bloco_largura, bloco_altura)
            bloco_lista.append(bloco) # Adociona os blocos a lista
            cor = cores[linha % len(cores)]  # Obtém a cor com base na ordem das cores
            cor_blocos.append(cor)  # Adiciona a cor à lista cor_blocos
##### CHAMADA DA CRIAÇÃO DE BLOCOS ########################################
criar_blocos()
##### FUNÇÃO DE REINICIO DE TIMER #########################################
def restart_timer(): # Define como calcular o tempo usando o time.time
    global start_time
    start_time = time.time()
##### FUNÇÃO DE FORMATAÇÃO DO TIMER #######################################
def format_time(time): # Formata o tempo para XX : XX
    minutos, segundos = divmod(time, 60)
    tempo_formatado = f"{minutos:02d}:{segundos:02d}"
    return tempo_formatado
def lancamento():
    global lancar_bola, bola_lancada, velocidade_bola_x, velocidade_bola_y
    velocidade_bola_x = random.choice([mov_bola_xD, mov_bola_xE])
    velocidade_bola_y = mov_bola_y
    lancar_bola = True
    bola_lancada = True
##### FUNÇÃO DE CRIAÇÃO DE NOVO NÍVEL #####################################
def new_lvl(): # Adiciona novos valores as variaveis para criar um proximo nivel
    global vidas, linhas, velocidade_bola_x, velocidade_bola_y, x_bola, y_bola, x_prancha, y_prancha, lancar_bola, bola_lancada, lvl, pontos, mov_bola_xD, mov_bola_xE, mov_bola_y
    vidas += 1
    linhas += 1    
    velocidade_bola_y = 0
    velocidade_bola_x = 0
    x_bola = 335
    y_bola = 455
    x_prancha = 300
    y_prancha = 467
    lancar_bola = False
    bola_lancada = False
    lvl += 1
    pontos += 5
    mov_bola_xD = mov_bola_xD * 1.1
    mov_bola_xE = mov_bola_xE * 1.1
    mov_bola_y = mov_bola_y * 1.1
##### FUNÇÃO PARA RESETAR PARAMETROS ######################################
def valores_inicio(): # Reseta todos os valores iniciais em caso de fim de jogo por nivel maximo ou perda de todas as vidas
    global vidas, linhas, velocidade_bola_x, velocidade_bola_y, x_bola, y_bola, x_prancha, y_prancha, lancar_bola, bola_lancada, lvl, pontos, pontuacao, mov_bola_xD, mov_bola_xE, mov_bola_y
    vidas = 3
    linhas = 4    
    velocidade_bola_y = 0
    velocidade_bola_x = 0
    x_bola = 335
    y_bola = 455
    x_prancha = 300
    y_prancha = 467
    lancar_bola = False
    bola_lancada = False
    lvl = 1
    pontos = 10
    pontuacao = 0
    mov_bola_xD = 5
    mov_bola_xE = -5
    mov_bola_y = -5
##### FUNÇÃO DE MENU GAME OVER ############################################
def menu_gameover():
    musica_game_over.play()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT: # Opção de fechar o jogo atráves da janela 
                pygame.quit()
                exit()
##### DESENHO DO MENU GAME OVER ###########################################
            tela.fill((0, 0, 0))
            pygame.draw.rect(tela, (200, 0, 0), (100, 100, 440, 200), 5)
            pygame.draw.rect(tela, (200, 0, 0), (100, 250, 220, 50), 3)
            pygame.draw.rect(tela, (200, 0, 0), (320, 250, 220, 50), 3)

            fonte_game_over = pygame.font.SysFont('Arial', 68, bold=True)
            texto_game_over = fonte_game_over.render("GAME OVER", True, (255, 0, 0)) # Game over
            tela.blit(texto_game_over, (150, 105))

            fonte_pontuacao_final = pygame.font.SysFont('Arial', 30, bold=True)
            texto_pontuacao_final = fonte_pontuacao_final.render(f"Pontuação final: {pontuacao}", True, (255, 255, 255)) # Pontuação
            tela.blit(texto_pontuacao_final, (200, 175))

            fonte_tempo_final = pygame.font.SysFont('Arial', 30, bold=True)
            texto_tempo_final = fonte_tempo_final.render(f"Tempo de jogo: {tempo_formatado}", True, (255, 255, 255)) # Tempo jogado
            tela.blit(texto_tempo_final, (200, 205))

            fonte_opcoes = pygame.font.SysFont('Arial', 36, bold=True)
            texto_reiniciar = fonte_opcoes.render("Restart", True, (255, 255, 255)) # Restart
            tela.blit(texto_reiniciar, (155, 252))

            texto_sair = fonte_opcoes.render("Exit", True, (255, 255, 255)) # Exit
            tela.blit(texto_sair, (400, 252)) 
            pygame.display.update()
##### VERIFICAÇÃO DE ESCOLHA ##############################################
            if pygame.mouse.get_pressed()[0]:
                posicao_mouse = pygame.mouse.get_pos()
                # REINICIA O JOGO #
                if posicao_mouse[0] >= 100 and posicao_mouse[0] <= 320 \
                        and posicao_mouse[1] >= 250 and posicao_mouse[1] <= 300: # Determina a posição do mouse sobre a tela/botão
                    musica_click.play()
                    pygame.time.wait(250)
                    musica_fundo.play(-1)                       
                    restart_timer()
                    return
                # SAI DO JOGO #
                elif posicao_mouse[0] >= 320 and posicao_mouse[0] <= 540 \
                        and posicao_mouse[1] >= 250 and posicao_mouse[1] <= 300: # Determina a posição do mouse sobre a tela/botão          
                    musica_exit.play()
                    pygame.time.wait(800)
                    pygame.quit()
                    exit()
##### FUNÇÃO DE MENU VITORIA ##############################################
def menu_vitoria():
    musica_win.play()
    musica_clap.play()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT: # Opção de fechar o jogo atráves da janela 
                pygame.quit()
                exit()
##### DESENHO DO MENU VITORIA #############################################        
            tela.fill((0, 0, 0))
            pygame.draw.rect(tela, (200, 0, 0), (100, 100, 440, 200), 5)
            pygame.draw.rect(tela, (200, 0, 0), (100, 250, 220, 50), 3)
            pygame.draw.rect(tela, (200, 0, 0), (320, 250, 220, 50), 3)

            fonte_nivel_clean = pygame.font.SysFont('Arial', 68, bold=True)
            texto_nivel_clean = fonte_nivel_clean.render(F"YOU WON!", True, (255, 255, 255)) # You won!
            tela.blit(texto_nivel_clean, (170, 105))

            fonte_pontuacao_final = pygame.font.SysFont('Arial', 30, bold=True)
            texto_pontuacao_final = fonte_pontuacao_final.render(f"Pontuação: {pontuacao}", True, (255, 255, 255)) # Pontuação
            tela.blit(texto_pontuacao_final, (200, 175))

            fonte_tempo_final = pygame.font.SysFont('Arial', 30, bold=True)
            texto_tempo_final = fonte_tempo_final.render(f"Tempo de jogo: {tempo_formatado}", True, (255, 255, 255)) # Tempo jogado
            tela.blit(texto_tempo_final, (200, 205))

            fonte_opcoes = pygame.font.SysFont('Arial', 36, bold=True)
            texto_reiniciar = fonte_opcoes.render("Restart", True, (255, 255, 255)) # Restart
            tela.blit(texto_reiniciar, (155, 252))

            texto_sair = fonte_opcoes.render("Exit", True, (255, 255, 255)) # Exit
            tela.blit(texto_sair, (400, 252))
            pygame.display.update()
##### VERIFICAÇÃO DE ESCOLHA ##############################################
            if pygame.mouse.get_pressed()[0]:
                posicao_mouse = pygame.mouse.get_pos()
                # REINICIA O JOGO #
                if posicao_mouse[0] >= 100 and posicao_mouse[0] <= 320 \
                        and posicao_mouse[1] >= 250 and posicao_mouse[1] <= 300: # Determina a posição do mouse sobre a tela/botão
                    musica_click.play()
                    pygame.time.wait(250)
                    musica_fundo.play(-1)
                    restart_timer()
                    return
                # SAI DO JOGO #
                elif posicao_mouse[0] >= 320 and posicao_mouse[0] <= 540 \
                        and posicao_mouse[1] >= 250 and posicao_mouse[1] <= 300: # Determina a posição do mouse sobre a tela/botão          
                    musica_exit.play()
                    pygame.time.wait(800)
                    pygame.quit()
                    exit()
##### FUNÇÃO DE MENU NXT LEVEL ############################################
def menu_nxt_lvl():
    musica_lvl.play()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT: # Opção de fechar o jogo atráves da janela 
                pygame.quit()
                exit()
##### DESENHO DO MENU NXT LEVEL ########################################### 
            tela.fill((0, 0, 0))
            pygame.draw.rect(tela, (200, 0, 0), (100, 100, 440, 200), 5)
            pygame.draw.rect(tela, (200, 0, 0), (100, 250, 220, 50), 3)
            pygame.draw.rect(tela, (200, 0, 0), (320, 250, 220, 50), 3)

            fonte_nivel_clean = pygame.font.SysFont('Arial', 60, bold=True)
            texto_nivel_clean = fonte_nivel_clean.render(F"COMPLETED", True, (255, 255, 255)) #Completed level
            tela.blit(texto_nivel_clean, (170, 110))

            texto_nivel_clean = fonte_nivel_clean.render(F"LEVEL", True, (255, 255, 255)) #Completed level
            tela.blit(texto_nivel_clean, (240, 170))

            fonte_opcoes = pygame.font.SysFont('Arial', 36, bold=True)
            texto_reiniciar = fonte_opcoes.render("Next level", True, (255, 255, 255)) # Next level
            tela.blit(texto_reiniciar, (150, 252))

            texto_sair = fonte_opcoes.render("Exit", True, (255, 255, 255)) # Exit
            tela.blit(texto_sair, (400, 252))
            pygame.display.update()
##### VERIFICAÇÃO DE ESCOLHA ##############################################
            if pygame.mouse.get_pressed()[0]:
                posicao_mouse = pygame.mouse.get_pos()
                # NEXT LEVEL #
                if posicao_mouse[0] >= 100 and posicao_mouse[0] <= 320 \
                        and posicao_mouse[1] >= 250 and posicao_mouse[1] <= 300: # Determina a posição do mouse sobre a tela/botão 
                    musica_click.play()
                    pygame.time.wait(250)
                    musica_fundo.play(-1)
                    new_lvl()
                    criar_blocos()
                    return
                # SAI DO JOGO #
                elif posicao_mouse[0] >= 320 and posicao_mouse[0] <= 540 \
                        and posicao_mouse[1] >= 250 and posicao_mouse[1] <= 300: # Determina a posição do mouse sobre a tela/botão          
                    musica_exit.play()
                    pygame.time.wait(800)
                    pygame.quit()
                    exit()
##### TELA DE INICIO DE JOGO ##############################################
while True:
    for event in pygame.event.get(): 
        if event.type == QUIT: # Opção de fechar o jogo atráves da janela
            pygame.quit()
            exit()
##### DESENHO DA TELA INICIAL #############################################
    tela.fill((0, 0, 0))
    pygame.draw.rect(tela, (200, 0, 0), (100, 100, 440, 200), 5)
    pygame.draw.rect(tela, (200, 0, 0), (100, 250, 220, 50), 3)
    pygame.draw.rect(tela, (200, 0, 0), (320, 250, 220, 50), 3)

    fonte_titulo = pygame.font.SysFont('Arial', 64, bold=True)
    texto_titulo = fonte_titulo.render("BREAKOUT", True, (255, 255, 255)) # Breakout
    tela.blit(texto_titulo, (170, 130))
    
    fonte_opcoes = pygame.font.SysFont('Arial', 36, bold=True) # Start
    texto_jogar = fonte_opcoes.render("Start", True, (255, 255, 255))
    tela.blit(texto_jogar, (185, 250))

    texto_sair = fonte_opcoes.render("Exit", True, (255, 255, 255)) # Exit
    tela.blit(texto_sair, (385, 250))
    pygame.display.update()
##### VERIFICAÇÃO DE ESCOLHA ##############################################
    if pygame.mouse.get_pressed()[0]:
        posicao_mouse = pygame.mouse.get_pos() # Obtem a posição do mouse dentro do jogo
        # INICIA DE JOGO #
        if posicao_mouse[0] >= 100 and posicao_mouse[0] <= 320 \
                and posicao_mouse[1] >= 250 and posicao_mouse[1] <= 300: # Determina a posição do mouse sobre a tela/botão
            contando = True
            start_time = time.time()
            musica_click.play()
            pygame.time.wait(250)
            musica_fundo.play(-1)
            break
        # SAI DO JOGO #
        elif posicao_mouse[0] >= 320 and posicao_mouse[0] <= 540 \
                and posicao_mouse[1] >= 250 and posicao_mouse[1] <= 300: # Determina a posição do mouse sobre a tela/botão   
            musica_exit.play()
            pygame.time.wait(800)
            pygame.quit()
            exit()
##### INICIO DO LOOP DO JOGO ##############################################
while True:
    relogio.tick(60) # FPS do jogo
    tela.fill((0, 0, 0)) # Atualiza os desenhos da tela
##### OPÇÃO DE FECHAR A JANELA DO JOGO ####################################    
    for event in pygame.event.get():
        if event.type == QUIT: # Opção de fechar o jogo atráves da janela
            pygame.quit()
            exit()
##### DEFINIÇÃO DE LANÇAMENTO E MOVIMENTO DA BOLA #########################
        if not lancar_bola and pygame.key.get_pressed()[K_SPACE]:
            lancamento()
            x_bola = 335 # Determina posição inicial da bola
            y_bola = 455
            x_prancha = 300 # Determina posição inicial da prancha
            y_prancha = 467
##### DEFINIÇÃO DE CONTROLE DA PRANCHA ####################################
    if bola_lancada:
        if pygame.key.get_pressed()[K_a]: # Controla a prancha pra esquerda
            x_prancha = x_prancha - 10
        if pygame.key.get_pressed()[K_d]: # Controla a prancha pra direita
            x_prancha = x_prancha + 10
##### ATUALIZAÇÃO E MOVIMENTO DA BOLA #####################################
    x_bola += velocidade_bola_x
    y_bola += velocidade_bola_y
##### VERIFICAÇÃO DE COLISÃO COM PAREDES DIREITA E ESQUERDA ###############
    if x_bola < 15 or x_bola > largura - 15:
        velocidade_bola_x = -velocidade_bola_x # Muda o movimento da bola após contato com a parede
        musica_kick.play()
##### VERIFICAÇÃO DE COLISÃO COM O TETO ###################################
    if y_bola < 45: 
        velocidade_bola_y = -velocidade_bola_y
        y_bola = 45 # Determina a posição maxima da bola caso toque o teto
        musica_kick.play()
##### VERIFICAÇÃO DE COLISÃO COM O CHÃO ###################################
    if y_bola >= 475:
        velocidade_bola_y = 0 # Zera o movimento da bola
        velocidade_bola_x = 0
        x_bola = 335 # Retorna a bola pra posição inicial
        y_bola = 455
        x_prancha = 300 # Retorna a prancha pra posição inicial
        y_prancha = 467
        vidas -= 1 # Desconta uma vida
        lancar_bola = False # Muda o boleano pra não mover a prancha até a bola ser lançada
        bola_lancada = False
        musica_fundo.stop()       
        musica_fail.play()
        pygame.time.wait(1000)
        musica_fundo.play(-1)
##### VERIFICAÇÃO DE COLISÃO COM OS BLOCOS E REMOÇÃO DOS ATINGIDOS ########            
    for i, bloco in enumerate(bloco_lista):
        if bloco.collidepoint(x_bola + raio_bola, y_bola + raio_bola):
            bloco_lista.pop(i)
            cor_blocos.pop(i)
            velocidade_bola_y = -mov_bola_y
            pontuacao += pontos
            musica_pancada.play()
            break # Evita que bugs onde a bola elimina varios blocos de um vez
        elif bloco.collidepoint(x_bola - raio_bola, y_bola + raio_bola):
            bloco_lista.pop(i)
            cor_blocos.pop(i)
            velocidade_bola_y = -mov_bola_y
            velocidade_bola_x = -velocidade_bola_x
            pontuacao += pontos
            musica_pancada.play()
            break # Evita que bugs onde a bola elimina varios blocos de um vez
        elif bloco.collidepoint(x_bola + raio_bola, y_bola - raio_bola):
            bloco_lista.pop(i)
            cor_blocos.pop(i)
            velocidade_bola_y = -mov_bola_y
            velocidade_bola_x = -velocidade_bola_x
            pontuacao += pontos
            musica_pancada.play()
            break # Evita que bugs onde a bola elimina varios blocos de um vez
        elif bloco.collidepoint(x_bola - raio_bola, y_bola - raio_bola):
            bloco_lista.pop(i)
            cor_blocos.pop(i)
            velocidade_bola_y = -mov_bola_y
            pontuacao += pontos
            musica_pancada.play()
            break # Evita que bugs onde a bola elimina varios blocos de um vez
##### VERICFICAÇÃO DE COLISÃO COM A PRANCHA ###############################
    if y_bola + 10 >= y_prancha and y_bola + 10 <= y_prancha + 10 and \
            x_bola >= x_prancha and x_bola <= x_prancha + 70:
        if x_bola < x_prancha + 20:  # Colisão com a ponta esquerda da prancha
            velocidade_bola_x = mov_bola_xE # Move a bola para a esquerda
            velocidade_bola_y = -velocidade_bola_y
        elif x_bola > x_prancha + 50:  # Colisão com a ponta direita da prancha
            velocidade_bola_x = mov_bola_xD  # Move a bola para a direita
            velocidade_bola_y = -velocidade_bola_y
        else:  # Colisão com as partes do meio da prancha
            velocidade_bola_y = -velocidade_bola_y
        musica_kick.play()
##### ATUALIZAÇÃO E MOVIMENTO DA PRANCHA ##################################
    prancha = pygame.Rect(x_prancha, y_prancha, 70, 10)
    if x_prancha < 5: #Limitação do movimento da prancha
        x_prancha = 5
    elif x_prancha > largura - 75: #Limitação do movimento da prancha
        x_prancha = largura - 75
##### DESENHO DOS BLOCOS NA TELA ########################################## 
    for i, bloco in enumerate(bloco_lista):
        cor = cor_blocos[i]  # Obtém a cor correspondente ao bloco
        pygame.draw.rect(tela, cor, bloco)
##### DESENHO DE BOLA E PRANCHA NA TELA ###################################
    bola = pygame.draw.circle(tela, (255, 255, 255), (x_bola, y_bola), 10)
    pygame.draw.rect(tela, (105, 105, 105), prancha)
##### DESENHO DAS PAREDES #################################################     
    pygame.draw.rect(tela, (255, 255, 255), (0, 0, margem, altura)) # Desenho da parede esquerda   
    pygame.draw.rect(tela, (255, 255, 255), (largura - margem, 0, margem, altura)) # Desenho da parede direita   
    pygame.draw.rect(tela, (255, 255, 255), (0, 30, largura, margem)) # Desenho do teto
##### FUNCIONAMENTO DO TIMER ##############################################
    if contando == True:
        tempo = int(time.time() - start_time)
        tempo_formatado = format_time(tempo)
##### DESENHA O HUD DA TELA ###############################################         
    tempo_fonte = pygame.font.Font(None, 30) # Timer
    contador_tempo = tempo_fonte.render(f"Timer: {tempo_formatado}", True, (255, 255, 255))
    tela.blit(contador_tempo, (350, 5))
    
    pontuacao_fonte = pygame.font.Font(None, 30) # Pontuação  
    pontuacao_texto = pontuacao_fonte.render(f"Pontuação: {pontuacao}", True, (255, 255, 255))
    tela.blit(pontuacao_texto, (15, 5))
  
    vidas_fonte = pygame.font.Font(None, 30) # Vidas
    vidas_texto = vidas_fonte.render(f"Vidas: {vidas}", True, (255, 255, 255))   
    tela.blit(vidas_texto, (550, 5)) 
   
    lvl_fonte = pygame.font.Font(None, 30) # LVL
    lvl_texto = lvl_fonte.render(f"Nível - {lvl}", True, (255, 255, 255))   
    tela.blit(lvl_texto, (210, 5))
##### CONDIÇÃO DE DERROTA #################################################
    if vidas == 0:        
        musica_fundo.stop()
        pygame.time.wait(1000)
        menu_gameover()
        valores_inicio()
        criar_blocos()
##### CONDIÇÃO DE VITORIA #################################################
    if len(bloco_lista) == 0:
        # CONDIÇÃO DE VITORIA NXT LEVEL #
        if lvl < 3: # Prox level
            musica_fundo.stop()
            pygame.time.wait(1000)
            menu_nxt_lvl() 
        # CONDIÇÃO DE VITORIA JOGO #    
        elif lvl == 3: # Level max          
            musica_fundo.stop()
            pygame.time.wait(1000)
            menu_vitoria()
            valores_inicio()
            criar_blocos()
##### ATUALIZA O JOGO #####################################################      
    pygame.display.update()
