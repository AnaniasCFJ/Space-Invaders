from pplay.gameimage import *
from pplay.window import *
from pplay.sprite import *
from pplay.mouse import *
from pplay.animation import *
from pplay.gameobject import *
from pplay.keyboard import *
from pplay.collision import *
import random
import pygame
import os
import sys
import subprocess

diretorio_do_jogo = os.path.dirname(os.path.abspath(sys.argv[0]))

os.chdir(diretorio_do_jogo)

janela = Window(1360, 768)
janela.set_title("Space Invaders")

play = Sprite("play.jpg")
level = Sprite("level.jpg")
ranking = Sprite("ranking.jpg")
sair = Sprite("exit.jpg")
easy = Sprite("easy2.jpg")
medium = Sprite("medium.jpg")
hard = Sprite("hard.jpg")
                 
play_destacado = Sprite("play_destacado.jpg")
level_destacado = Sprite("level_destacado.jpg")
ranking_destacado = Sprite("ranking_destacado.jpg")
sair_destacado = Sprite("exit_destacado.jpg")
easy_destacado = Sprite("easy2_destacado.jpg")
medium_destacado = Sprite("medium_destacado.jpg")
hard_destacado = Sprite("hard_destacado.jpg")
                           
play.set_position(janela.width/2 - play.width/2, 150)
level.set_position(janela.width/2 - level.width/2, 250)
ranking.set_position(janela.width/2 - ranking.width/2, 350)
sair.set_position(janela.width/2 - sair.width/2, 450)
easy.set_position(janela.width/2 - easy.width/2, 250)
medium.set_position(janela.width/2 - medium.width/2, 350)
hard.set_position(janela.width/2 - hard.width/2, 450)

play_destacado.set_position(janela.width/2 - play.width/2, 150)
level_destacado.set_position(janela.width/2 - level.width/2, 250)
ranking_destacado.set_position(janela.width/2 - ranking.width/2, 350)
sair_destacado.set_position(janela.width/2 - sair.width/2, 450)
easy_destacado.set_position(janela.width/2 - easy.width/2, 250)
medium_destacado.set_position(janela.width/2 - medium.width/2, 350)
hard_destacado.set_position(janela.width/2 - hard.width/2, 450)

mouse = Window.get_mouse()
keyboard = Window.get_keyboard()

difficulty = "easy"
dif_rate = 1

primeiro_x = 0
ultimo_x = 0
primeiro_y = 0
primeiro_x = 0

nave = Sprite("nave5.png")
tiro = Sprite("tiro.jpg")
monstro = Sprite("monstro.png")

nave.set_position(janela.width/2 - nave.width/2, janela.height - nave.height)
tiro.set_position(janela.width/2 - tiro.width/2, nave.height + 300)
    
vel_player = 200
vel_tiro = 100
vel_ini = 2

nave.direction = -1
enemy_direction = 1
distancia_abaixo = 0
descer = False
c = 1

derrota = False
pontos = 0

matrix_x = 13
matrix_y = 4

bullets = []
inimigos = [[0 for x in range(20)] for x in range(20)]

nave.shoot_delay = 0.5
nave.shoot_tick = nave.shoot_delay
contador = 0
paralisante = False

tempo_entre_tiros = 15
tempo_passado_desde_ultimo_tiro = 0
tempo_passado_desde_ultimo_tiro_monstros = 0
tempo_desde_ultimo_tiro_levado = 0
cooldown_tiro = 25
vidas = 5
temp = 0
g = 0
fase = 1

piscando = False

def ajustar_bala(autor, bullet):
    x_fire = autor.x + (autor.width/2) - (bullet[0].width/2)

    if autor.direction == -1:
        y_fire = autor.y
    elif autor.direction == 1:
        y_fire = autor.y + autor.height - bullet[0].height
    
    bullet[0].x = x_fire
    bullet[0].y = y_fire

    bullet[0].direction = autor.direction

def atirar(autor):
    global tiro_em_andamento, contador, paralisante
    
    if autor == nave:
        tiro_em_andamento = True
    
    if contador != 3 or autor == nave:
        s = Sprite("tiro.jpg")
    elif contador >= 3 and autor != nave:
        s = Sprite("tiro_paralisante.jpg")
    
    if contador >= 3 and autor != nave:
        d = [s, 1]
        contador = 0
    else:
        d = [s, 0]
        
    ajustar_bala(autor, d)
    
    if autor != nave:
        contador += 1

    bullets.append(d)
    
def nascer_inimigos(i, j, matrix):
    global inimigos
    nave.shoot_delay = 0.5 * dif_rate
    nave.shoot_tick = nave.shoot_delay
    inimigos = [[0 for x in range(20)] for x in range(20)]
    
    for x in range(i):
        for y in range(j):
            ini = Sprite("monstro.png")
            ini.set_position(x*ini.width, y*ini.height)
            ini.direction = 1
            inimigos[x][y] = ini

def movimento_bala():
    for b in bullets:
        b[0].move_y(10*b[0].direction*janela.delta_time())

def movimento_inimigo():
    global enemy_direction
    global vel_ini
    global distancia_abaixo
    global descer
    global c
    
    invert = False

    nova_pos = vel_ini * enemy_direction * janela.delta_time()
    
    for i in range(matrix_x):
        for j in range(matrix_y):
            if inimigos[i][j] != 0:
                inimigos[i][j].move_x(nova_pos)
                if descer == True and distancia_abaixo > inimigos[i][j].y:
                    inimigos[i][j].move_y(nova_pos*c)
                else:
                    descer = False
                if not invert:
                    if inimigos[i][j] != 0:
                        if inimigos[i][j].x <= 0 or inimigos[i][j].x >= janela.width - inimigos[i][j].width:
                            enemy_direction *= -1
                            distancia_abaixo = inimigos[i][j].y + 250 - (inimigos[i][j].height * j)
                            descer = True
                            invert = True
                            if inimigos[i][j].x <= 0:
                                c = 1
                            elif inimigos[i][j].x >= janela.width - inimigos[i][j].width:
                                c = -1

def atualizar_tiros():
    global tempo_passado_desde_ultimo_tiro, tempo_passado_desde_ultimo_tiro_monstros

    tempo_passado_desde_ultimo_tiro += janela.delta_time()
    tempo_passado_desde_ultimo_tiro_monstros += janela.delta_time()

def verificar_tiro():
    global tiro_em_andamento, tempo_passado_desde_ultimo_tiro, tempo_passado_desde_ultimo_tiro_monstros, tempo_entre_tiros_monstros, cooldown_tiro
    
    if keyboard.key_pressed("space") and not tiro_em_andamento and tempo_passado_desde_ultimo_tiro >= tempo_entre_tiros:
        atirar(nave)
        tiro_em_andamento = True
        tempo_passado_desde_ultimo_tiro = 0
    if tempo_passado_desde_ultimo_tiro_monstros >= cooldown_tiro:
        atirar_monstros()
        tempo_passado_desde_ultimo_tiro_monstros = 0

def verificar_derrota():
    global derrota, dif_rate
    
    for i in range(matrix_x):
        for j in range(matrix_y):
            if inimigos[i][j] != 0:
                if inimigos[i][j].collided(nave) or vidas <= 0:
                    derrota = True

def verificar_colisao_inimigo():
    global pontos, primeiro_y, ultimo_y, x_primeira, x_ultima, inimigos, dif_rate
    coords_pontas()
    for b in bullets:
        if b[0].direction == -1 and b[0].x + b[0].width >= x_primeira and b[0].y + b[0].height >= primeiro_y:
            for i in range(matrix_x):
                for j in range(matrix_y):
                    if inimigos[i][j] != 0:
                        if b[0].collided(inimigos[i][j]):
                            bullets.remove(b)
                            inimigos[i][j] = 0
                            pontos += j + (10*dif_rate)
                            return
                        
def coords_pontas():
    global primeiro_y, ultimo_y, x_primeira, x_ultima, inimigos
    
    fim = False
    
    for i in range(matrix_x):
        if fim:
            break
        for j in range(matrix_y):
            if inimigos[i][j] != 0:
                x_primeira = inimigos[i][j].x
                fim = True
                
    fim = False
    
    for i in range(matrix_x-1, 0, -1):
        if fim:
            break
        for j in range(matrix_y-1, 0, -1):
            if inimigos[i][j] != 0:
                x_ultima = inimigos[i][j].x
                fim = True
                break

    fim = False

    for i in range(matrix_y):
        if fim:
            break
        for j in range(matrix_x):
            if inimigos[i][j] != 0:
                primeiro_y = inimigos[i][j].y
                fim = True
                break

    fim = False

    for i in range(matrix_y-1, 0, -1):
        if fim:
            break
        for j in range(matrix_x-1, 0, -1):
            if inimigos[i][j] != 0:
                ultimo_y = inimigos[i][j].y
                fim = True
                break

def resetar_configs():
    global derrota, distancia_abaixo, c, enemy_direction, pontos, bullets, dif_rate, difficulty, nave, paralisante, contador
    
    nave.unhide()
    derrota = False
    distancia_abaixo = 0
    c = 1
    enemy_direction = 1
    nascer_inimigos(matrix_x, matrix_y, inimigos)
    pontos = 0
    bullets = []
    contador = 0
    paralisante = False
    
def atirar_monstros():
    
    for i in range(matrix_x):
        for j in range(matrix_y):
            if inimigos[i][j] != 0:
                chance = random.randint(1,20)
                if chance == 1:
                    atirar(inimigos[i][j])
                    return()
                
def verificar_colisao_nave(nave):
    global vidas, piscando, paralisante, bullets
    
    for b in bullets:
        if b[0].direction == 1 and b[0].collided(nave):
            if b[1] == 0:
                nave.set_position(janela.width/2 - nave.width/2, janela.height - nave.height)
                vidas -= 1
                piscando = True
                bullets.remove(b)
            else:
                paralisante = True
                bullets.remove(b)

def verificar_vitoria():
    global inimigos, matrix_x, matrix_y, dif_rate, fase, distancia_abaixo, c, enemy_direction
    
    vitoria = False
    d = 0
    
    for i in range(matrix_x):
        for j in range(matrix_y):
            if inimigos[i][j] != 0:
                d += 1
                break
    if d == 0:
        vitoria = True
    if vitoria:
        dif_rate += 0.7
        fase += 1
        if fase % 3 == 0:
            matrix_x += 1
            matrix_y += 1
        distancia_abaixo = 0
        c = 1
        enemy_direction = 1
        nascer_inimigos(matrix_x, matrix_y, inimigos)

def inserir_nome():
    
    nome = input("Digite seu nome: ")
    arquivo = open("ranking.txt", "a")
    arquivo.write("{}: {}\n".format(nome, pontos))
    arquivo.close()
    ordenar_ranking()
    i = 0
    with open("ranking.txt", "r") as arquivo:
        linhas2 = []
        for linha in arquivo:
            i += 1
            linhas2.append(linha.strip().split(": "))
    if i == 6:
        i = 0
        linhas2[5].pop()
        with open("ranking.txt", "w") as arquivo:
            for linha in linhas2:
                i += 1
                arquivo.write("{}: {}\n".format(linha[0], linha[1]))
                if i == 5:
                    break
                
def ordenar_ranking():
    
    with open("ranking.txt", "r") as arquivo:
        linhas = [linha.strip().split(": ") for linha in arquivo]

    linhas.sort(key=lambda x: float(x[1]), reverse=True)  

    with open("ranking.txt", "w") as arquivo:
        for linha in linhas:
            arquivo.write("{}: {}\n".format(linha[0], linha[1]))

def verificar_dificuldade():
    global dif_rate, difficulty
    
    if difficulty == "easy":
        dif_rate = 1.0
    elif difficulty == "medium":
        dif_rate = 1.5
    elif difficulty == "hard":
        dif_rate = 2.0

                               
def rodando_jogo():
    janela = Window(1360, 768)
    screen = pygame.display.set_mode((1360, 768))
    
    janela.set_title("Space Invaders")
    
    nave.set_position(janela.width/2 - nave.width/2, janela.height - nave.height)
    
    keyboard = Window.get_keyboard()
    
    global paralisante, enemy_direction, tiro_em_andamento, tempo_passado_desde_ultimo_tiro, c, distancia_abaixo, derrota, pontos, tempo_entre_tiros_monstros, cooldown_tiro, tempo_desde_ultimo_tiro_levado, vidas, dif_rate, vel_ini, piscando
    
    frames = 0
    fps = 0
    tempo = 0
    
    tempo_entre_tiros_monstros = cooldown_tiro
    tempo_passado_desde_ultimo_tiro_monstros = 0
    tempo_desde_ultimo_tiro_levado = 0
    tempo_piscando = 0
    piscar_duracao = 2
    
    paralisante = False
    cont = 0
    
    derrota = False
    distancia_abaixo = 0
    c = 1
    enemy_direction = 1
    nascer_inimigos(matrix_x, matrix_y, inimigos)
    vidas = 5
    temp = 0
    g = 0
    fase = 1
    
    piscando = False

    font = pygame.font.Font(None, 20)
    
    while True:
        janela.set_background_color([0,0,0])
        
        text = font.render('FPS: {}'.format(fps), True, (255, 255, 255))
        text2 = font.render('Pontos: {}'.format(pontos), True, (255, 255, 255))
        text3 = font.render('Vidas: {}'.format(vidas), True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect2 = text.get_rect()
        text_rect3 = text.get_rect()
        text_rect2.center = (1300, 15)
        text_rect.center = (28,15)
        text_rect3.center = (1300, 760)
        screen.blit(text, text_rect)
        screen.blit(text2, text_rect2)
        screen.blit(text3, text_rect3)

        vel_ini = 2 * dif_rate
        
        if not paralisante:
            if keyboard.key_pressed("RIGHT") and nave.x < janela.width - nave.width:
                nave.x += vel_player * janela.delta_time()
            if keyboard.key_pressed("LEFT") and nave.x > 0:
                nave.x -= vel_player * janela.delta_time()
        if not keyboard.key_pressed("space"):
            tiro_em_andamento = False
        else:
            tempo_passado_desde_ultimo_tiro += janela.delta_time()
        
        atualizar_tiros()
        if not paralisante:
            verificar_tiro()
        movimento_bala()
        movimento_inimigo()
        verificar_colisao_inimigo()
        if not piscando:
            verificar_colisao_nave(nave)
        verificar_dificuldade()
        verificar_derrota()
        verificar_vitoria()

        if piscando:
            tempo_piscando += janela.delta_time()
            if tempo_piscando >= piscar_duracao:
                piscando = False
                tempo_piscando = 0
            elif int(tempo_piscando*10) % 2 == 0:
                nave.hide()
            else:
                nave.unhide()
    
            
        for b in bullets:
            b[0].draw()
        for i in range(matrix_x):
            for j in range(matrix_y):
                if inimigos[i][j] != 0:
                    inimigos[i][j].draw()
        frames += 1
        tempo += janela.delta_time()
        
        if paralisante:
            cont += janela.delta_time()
        if cont >= 2:
            paralisante = False
            cont = 0

        if tempo >= 1:
            fps = frames
            frames = 0
            tempo -= 1
            
        if derrota == True or keyboard.key_pressed("ESC"):
            if derrota:
                inserir_nome()
            resetar_configs()
            break
        
        nave.draw()
        janela.update()
        
def dificuldade():
    
    janela = Window(1360, 768)
    janela.set_title("Space Invaders")
    
    mouse = Window.get_mouse()
    keyboard = Window.get_keyboard()
    
    easy = Sprite("easy2.jpg")
    medium = Sprite("medium.jpg")
    hard = Sprite("hard.jpg")
    easy_destacado = Sprite("easy2_destacado.jpg")
    medium_destacado = Sprite("medium_destacado.jpg")
    hard_destacado = Sprite("hard_destacado.jpg")
    
    easy.set_position(janela.width/2 - easy.width/2, 250)
    medium.set_position(janela.width/2 - medium.width/2, 350)
    hard.set_position(janela.width/2 - hard.width/2, 450)
    easy_destacado.set_position(janela.width/2 - easy.width/2, 250)
    medium_destacado.set_position(janela.width/2 - medium.width/2, 350)
    hard_destacado.set_position(janela.width/2 - hard.width/2, 450)
    
    global difficulty
    
    easy_highlighted = False
    medium_highlighted = False
    hard_highlighted = False
    
    while True:
        janela.update()
        janela.delay(100)
        
        if mouse.is_over_object(easy):
            easy_destacado.draw()
            easy_highlighted = True
        else:
            easy.draw()
            easy_highlighted = False
        
        if mouse.is_over_object(medium):
            medium_destacado.draw()
            medium_highlighted = True
        else:
            medium.draw()
            medium_highlighted = False
        
        if mouse.is_over_object(hard):
            hard_destacado.draw()
            hard_highlighted = True
        else:
            hard.draw()
            hard_highlighted = False

        if easy_highlighted and mouse.is_button_pressed(1):
            difficulty = "easy"
            break
        elif medium_highlighted and mouse.is_button_pressed(1):
            difficulty = "medium"
            break
        elif hard_highlighted and mouse.is_button_pressed(1):
            difficulty = "hard"
            break

        if keyboard.key_pressed("esc"):
            break

while True:
    
    janela.set_background_color([0, 0, 0])
    
    play_highlighted = mouse.is_over_object(play)
    level_highlighted = mouse.is_over_object(level)
    ranking_highlighted = mouse.is_over_object(ranking)
    sair_highlighted = mouse.is_over_object(sair)
    
    if play_highlighted:
        play_destacado.draw()
        if mouse.is_button_pressed(1):
            rodando_jogo()
    else:
        play.draw()
    if level_highlighted:
        level_destacado.draw()
        if mouse.is_button_pressed(1):
            dificuldade()
    else:
        level.draw()
    if ranking_highlighted:
        ranking_destacado.draw()
        if mouse.is_button_pressed(1):
            arquivo = os.path.join(os.path.dirname(__file__), "ranking.txt")

            subprocess.run(["notepad", arquivo])
    else:
        ranking.draw()
    if sair_highlighted:
        sair_destacado.draw()
        if mouse.is_button_pressed(1):
            janela.close()
    else:
        sair.draw()
    
    janela.delay(100)
    janela.update()


