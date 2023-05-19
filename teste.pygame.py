import pygame
from pygame.locals import *
from sys import exit

pygame.init()

largura = 640
altura = 480
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Breakout")
relogio = pygame.time.Clock()

margem = 5

# posição bola
x_bola = 335
y_bola = 460
# posição prancha
x_prancha = 300
y_prancha = 467

# Velocidade da bola
velocidade_bola_x = 0
velocidade_bola_y = 0

bloco_largura = 55
bloco_altura = 18
padding_left = 2
padding_top = 2
linhas = 4
colunas = 11
bloco_lista = []


def criar_blocos():
    for linha in range(linhas):
        for coluna in range(colunas):
            x = ((padding_left * coluna) + 5 + padding_left) + \
                (coluna * bloco_largura)
            y = ((padding_top * linha) + 35 + padding_top) + (linha * bloco_altura)
            bloco = pygame.Rect(x, y, bloco_largura, bloco_altura)
            bloco_lista.append(bloco)


criar_blocos()

pontuacao = 0
vidas = 3
# Boleano de lançamento da bola
lancar_bola = False
bola_lancada = False
# Tela de início
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

    # Desenhe a tela de início
    tela.fill((0, 0, 0))
    pygame.draw.rect(tela, (255, 255, 255), (100, 100, 440, 200), 2)
    pygame.draw.rect(tela, (255, 255, 255), (120, 250, 200, 50))
    pygame.draw.rect(tela, (255, 255, 255), (320, 250, 200, 50))
    fonte_titulo = pygame.font.SysFont(None, 64)
    texto_titulo = fonte_titulo.render("Breakout", True, (255, 0, 0))
    tela.blit(texto_titulo, (180, 130))
    fonte_opcoes = pygame.font.SysFont(None, 36)
    texto_jogar = fonte_opcoes.render("Jogar", True, (255, 0, 0))
    tela.blit(texto_jogar, (185, 260))
    texto_sair = fonte_opcoes.render("Sair", True, (255, 0, 0))
    tela.blit(texto_sair, (385, 260))
    pygame.display.update()

    # Verifique se o jogador selecionou uma opção
    if pygame.mouse.get_pressed()[0]:
        posicao_mouse = pygame.mouse.get_pos()
        if posicao_mouse[0] >= 120 and posicao_mouse[0] <= 320 \
                and posicao_mouse[1] >= 250 and posicao_mouse[1] <= 300:
            # Inicie o jogo
            break
        elif posicao_mouse[0] >= 320 and posicao_mouse[0] <= 520 \
                and posicao_mouse[1] >= 250 and posicao_mouse[1] <= 300:
            # Saia do jogo
            pygame.quit()
            exit()

while True:
    relogio.tick(60)
    tela.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        
        if not lancar_bola and pygame.key.get_pressed()[K_SPACE]:
            lancar_bola = True
            bola_lancada = True
            velocidade_bola_x = 5
            velocidade_bola_y = -5
            x_bola = 335
            y_bola = 460
            x_prancha = 300
            y_prancha = 467
            
    if bola_lancada:                
        if pygame.key.get_pressed()[K_a]:
            x_prancha = x_prancha - 10
        if pygame.key.get_pressed()[K_d]:
            x_prancha = x_prancha + 10

    # Atualiza a posição da bola
    x_bola += velocidade_bola_x
    y_bola += velocidade_bola_y

    # Verifica se a bola atingiu a parede esquerda ou direita
    if x_bola < 10 or x_bola > largura - 10:
        velocidade_bola_x = -velocidade_bola_x

    # Verifica se a bola atingiu o teto
    if y_bola < 40:
        velocidade_bola_y = -velocidade_bola_y
        y_bola = 40

    # Verifica se a bola atingiu o chão
    if y_bola >= 470:
        velocidade_bola_y = 0
        velocidade_bola_x = 0
        x_bola = 335
        y_bola = 460
        x_prancha = 300
        y_prancha = 467
        vidas -= 1
        lancar_bola = False
        bola_lancada = False

    for bloco in bloco_lista:
        if bloco.colliderect(pygame.Rect(x_bola, y_bola, 5, 5)):
            bloco_lista.remove(bloco)
            velocidade_bola_y = -velocidade_bola_y
            pontuacao += 10

    # Verifica se a bola atingiu a prancha
    if y_bola + 5 >= y_prancha and y_bola + 5 <= y_prancha + 10 and \
            x_bola >= x_prancha and x_bola <= x_prancha + 70:
        velocidade_bola_y = -velocidade_bola_y

    # Atualiza a posição da prancha
    prancha = pygame.Rect(x_prancha, y_prancha, 70, 10)
    if x_prancha < 0:
        x_prancha = 0
    elif x_prancha > largura - 70:
        x_prancha = largura - 70

    # Desenha todos os blocos na tela
    for bloco in bloco_lista:
        pygame.draw.rect(tela, (255, 255, 255,), bloco)

    # Desenha a prancha e a bola na tela
    bola = pygame.draw.circle(tela, (255, 255, 255), (x_bola, y_bola), 10)
    pygame.draw.rect(tela, (255, 255, 255), prancha)
    # Desenhe a parede esquerda
    pygame.draw.rect(tela, (255, 255, 255), (0, 0, margem, altura))

    # Desenhe a parede direita
    pygame.draw.rect(tela, (255, 255, 255), (largura - margem, 0, margem, altura))

    # Desenhe o teto
    pygame.draw.rect(tela, (255, 255, 255), (0, 30, largura, margem))
    # Desenha a pontuação na tela
    pontuacao_fonte = pygame.font.Font(None, 30)
    pontuacao_texto = pontuacao_fonte.render(f"Pontuação: {pontuacao}", True, (255, 0, 0))
    vidas_fonte = pygame.font.Font(None, 30)
    vidas_texto = vidas_fonte.render(f"Vidas: {vidas}", True, (255, 0, 0))
    tela.blit(pontuacao_texto, (15, 5))
    tela.blit(vidas_texto, (550, 5))


    # Acrescentando gameover e menu pós game over
    def menu_gameover():
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()

            tela.fill((0, 0, 0))
            fonte_game_over = pygame.font.SysFont(None, 64)
            texto_game_over = fonte_game_over.render("Game Over", True, (255, 0, 0))
            tela.blit(texto_game_over, (220, 130))
            fonte_pontuacao_final = pygame.font.SysFont(None, 36)
            texto_pontuacao_final = fonte_pontuacao_final.render(f"Pontuação final: {pontuacao}", True, (255, 0, 0))
            tela.blit(texto_pontuacao_final, (220, 200))
            fonte_opcoes = pygame.font.SysFont(None, 36)
            texto_reiniciar = fonte_opcoes.render("Reiniciar", True, (255, 255, 255))
            tela.blit(texto_reiniciar, (250, 260))
            texto_sair = fonte_opcoes.render("Sair", True, (255, 255, 255))
            tela.blit(texto_sair, (370, 260))
            pygame.display.update()

            if pygame.mouse.get_pressed()[0]:
                posicao_mouse = pygame.mouse.get_pos()
                if posicao_mouse[0] >= 250 and posicao_mouse[0] <= 370 \
                        and posicao_mouse[1] >= 260 and posicao_mouse[1] <= 310:
                    # Reiniciar jogo
                    return
                elif posicao_mouse[0] >= 360 and posicao_mouse[0] <= 420 \
                        and posicao_mouse[1] >= 260 and posicao_mouse[1] <= 310:
                    # Sair do jogo
                    pygame.quit()
                    exit()

    if vidas == 0:
        menu_gameover()
        pontuacao = 0
        vidas = 3
        criar_blocos()
     # Acrescentando Vitoria e menu pós vitoria
    def menu_vitoria():
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()

            tela.fill((0, 0, 0))
            fonte_nivel_clean = pygame.font.SysFont(None, 64)
            texto_nivel_clean = fonte_nivel_clean.render(F"Congratulations", True, (255, 255, 255))
            tela.blit(texto_nivel_clean, (160, 130))
            fonte_pontuacao_final = pygame.font.SysFont(None, 36)
            texto_pontuacao_final = fonte_pontuacao_final.render(f"Pontuação final: {pontuacao}", True, (255, 0, 0))
            tela.blit(texto_pontuacao_final, (220, 200))
            fonte_opcoes = pygame.font.SysFont(None, 36)
            texto_reiniciar = fonte_opcoes.render("Reiniciar", True, (255, 255, 255))
            tela.blit(texto_reiniciar, (250, 260))
            texto_sair = fonte_opcoes.render("Sair", True, (255, 255, 255))
            tela.blit(texto_sair, (370, 260))
            pygame.display.update()

            if pygame.mouse.get_pressed()[0]:
                posicao_mouse = pygame.mouse.get_pos()
                if posicao_mouse[0] >= 250 and posicao_mouse[0] <= 370 \
                        and posicao_mouse[1] >= 260 and posicao_mouse[1] <= 310:
                    # Reiniciar jogo
                    return
                elif posicao_mouse[0] >= 360 and posicao_mouse[0] <= 420 \
                        and posicao_mouse[1] >= 260 and posicao_mouse[1] <= 310:
                    # Sair do jogo
                    pygame.quit()
                    exit()
    if len(bloco_lista) == 0:
        menu_vitoria()
    
    pygame.display.update()
