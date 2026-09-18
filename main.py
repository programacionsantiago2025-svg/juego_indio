import pygame

import recursos
from config import ANCHO, LARGO, FPS
from personaje import Personaje
from cacique import Cacique
from enemigo import Enemigo
from mapa import Mapa
from interfaz import dibujar_boton
from play_videos import VideoFondo
pygame.init()
icono = pygame.image.load(recursos.ICONO)
pygame.display.set_caption("El ultimo heroe")
pygame.display.set_icon(icono)
ventana = pygame.display.set_mode((ANCHO, LARGO), pygame.FULLSCREEN | pygame.SCALED)

jugador = Personaje("Mago", 8, 100, 670, 510, recursos.IMAGENES_MOVER_INDIO, recursos.IMAGENES_QUIETO_INDIO, recursos.IMAGENES_ATACAR_INDIO, "Indio")
enemigos_nivel2 = [
    Enemigo(recursos.IMAGENES_MOVER_ESPAÑOL, 300, 400, recursos.IMAGENES_ATACAR_ESPAÑOL),
    Enemigo(recursos.IMAGENES_MOVER_ESPAÑOL, 700, 300, recursos.IMAGENES_ATACAR_ESPAÑOL),
    Enemigo(recursos.IMAGENES_MOVER_ESPAÑOL, 900, 500, recursos.IMAGENES_ATACAR_ESPAÑOL)
]
enemigos_nivel3 = [
    Enemigo(recursos.IMAGENES_MOVER_ESPAÑOL, 300, 400, recursos.IMAGENES_ATACAR_ESPAÑOL),
    Enemigo(recursos.IMAGENES_MOVER_ESPAÑOL, 700, 300, recursos.IMAGENES_ATACAR_ESPAÑOL),
    Enemigo(recursos.IMAGENES_MOVER_ESPAÑOL, 900, 500, recursos.IMAGENES_ATACAR_ESPAÑOL)
]
cacique = Cacique(recursos.IMAGENES_CACIQUE_QUIETO, 650, 500, recursos.DIALOGO_CACIQUE)
mapa = Mapa(cacique, enemigos_nivel2, enemigos_nivel3)
clock = pygame.time.Clock()
run = True
pygame.mixer.init()
sonido_paso = pygame.mixer.Sound(recursos.SONIDO_PASO)
sonido_caminando = False
sonido_boton_hover = pygame.mixer.Sound(recursos.SONIDO_BOTON_HOVER)
sonido_boton_jugar = pygame.mixer.Sound(recursos.SONIDO_BOTON_JUGAR)
hover_boton_jugar = False

pygame.mixer.music.load(recursos.MUSICA_AMBIENTE)
pygame.mixer.music.play(-1)

fuente_boton = pygame.font.SysFont(None, 32)

fondo_menu = pygame.image.load(recursos.FONDO_MENU).convert()
fondo_menu = pygame.transform.scale(fondo_menu, (ANCHO, LARGO))
video_menu = VideoFondo(recursos.FONDO_VIDEO_MENU, ANCHO, LARGO)
titulo_img = pygame.image.load(recursos.TEXTO_TITULO).convert_alpha()
recorte = titulo_img.get_bounding_rect()
titulo_img = titulo_img.subsurface(recorte).copy()
ancho_titulo = 460
alto_titulo = round(ancho_titulo * recorte.height / recorte.width)
titulo_img = pygame.transform.scale(titulo_img, (ancho_titulo, alto_titulo))
rect_titulo = titulo_img.get_rect(center=(ANCHO // 2, 90))
ancho_boton_jugar = 190
alto_boton_jugar = round(ancho_boton_jugar * 1194 / 880) 
bot_jugar_hover = pygame.image.load(recursos.FONDO_BOTON_JUGAR_HOVER).convert_alpha()
bot_jugar_hover = pygame.transform.scale(bot_jugar_hover, (ancho_boton_jugar, alto_boton_jugar))

fondo_controles = pygame.image.load(recursos.FONDO_CONTROLES).convert()
fondo_controles = pygame.transform.scale(fondo_controles, (ANCHO, LARGO))

bot_jugar = pygame.image.load(recursos.FONDO_BOTON_JUGAR).convert_alpha()
bot_jugar = pygame.transform.scale(bot_jugar, (ancho_boton_jugar, alto_boton_jugar))
rect_boton = bot_jugar.get_rect(center=(ANCHO // 2, round(LARGO * 0.616)))
ancho_boton = 170
alto_boton = 50
bot_opciones = pygame.Rect(20, LARGO - alto_boton - 20, ancho_boton, alto_boton)
bot_salir = pygame.Rect(ANCHO - ancho_boton - 20, LARGO - alto_boton - 20, ancho_boton, alto_boton)
ahora = "menu"

while run:
    movio = False
    for event in pygame.event.get():
        jugador.forma.clamp_ip(ventana.get_rect())
        if event.type == pygame.QUIT:
            run = False
        if ahora == 'menu':
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                if rect_boton.collidepoint(mx, my):
                    sonido_boton_jugar.play()
                    ahora = 'controles'
                elif bot_opciones.collidepoint(mx, my):
                    ahora = 'opciones'
                elif bot_salir.collidepoint(mx, my):
                    run = False
        elif ahora == 'controles':
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                ahora = 'jugando'
                pygame.mixer.music.load(recursos.MUSICA_JUEGO)
                pygame.mixer.music.play(-1)
        elif ahora == 'jugando':
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                sonido = pygame.mixer.Sound(recursos.SONIDO_ATAQUE)
                sonido.play()
                jugador.animar_ataque(ventana, mapa, ANCHO, LARGO)
                if mapa.nivel == 2:
                    for enemigo in enemigos_nivel2:
                        if enemigo.vida > 0 and jugador.forma.colliderect(enemigo.forma):
                            enemigo.recibir_daño(jugador.fuerza)
                elif mapa.nivel == 3:
                    for enemigo in enemigos_nivel3:
                        if enemigo.vida > 0 and jugador.forma.colliderect(enemigo.forma):
                            enemigo.recibir_daño(jugador.fuerza)
    if ahora == 'menu':
        video_menu.dibujar(ventana)
        ventana.blit(titulo_img, rect_titulo)
        if rect_boton.collidepoint(pygame.mouse.get_pos()):
            if not hover_boton_jugar:
                sonido_boton_hover.play()
                hover_boton_jugar = True
            ventana.blit(bot_jugar_hover, rect_boton)
        else:
            hover_boton_jugar = False
            ventana.blit(bot_jugar, rect_boton)
        dibujar_boton(ventana, bot_opciones, "Opciones", fuente_boton)
        dibujar_boton(ventana, bot_salir, "Salir", fuente_boton)
    elif ahora == 'controles':
        ventana.blit(fondo_controles, (0, 0))
    elif ahora == 'jugando':
        mapa.dibujar_nivel(ventana, ANCHO, LARGO, jugador)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            jugador.forma.x -= 10
            jugador.direccion = 'izquierda'
            movio = True
        if keys[pygame.K_d]:
            jugador.forma.x += 10
            jugador.direccion = 'derecha'
            movio = True
        if keys[pygame.K_w]:
            jugador.forma.y -= 10
            movio = True
        if keys[pygame.K_s]:
            jugador.forma.y += 10
            movio = True
        jugador.moviendo = movio
        jugador.animar()
        if movio and not sonido_caminando:
            sonido_caminando = True
            sonido_paso.play(-1)
        elif not movio and sonido_caminando:
            sonido_caminando = False
            sonido_paso.stop()
        jugador.dibujar(ventana)
        jugador.dibujar_barra_vida(ventana, 20, 20)
        fuente_vida = pygame.font.SysFont(None, 24)
        texto_vida = fuente_vida.render(f"Vida: {int(jugador.vida)}/{int(jugador.vida_maxima)}", True, (255, 255, 255))
        ventana.blit(texto_vida, (20, 35))
        if jugador.vida <= 0:
            fuente_game_over = pygame.font.SysFont(None, 80)
            texto_game_over = fuente_game_over.render("GAME OVER", True, (255, 0, 0))
            ventana.blit(texto_game_over, (ANCHO // 2 - 200, LARGO // 2 - 40))
            pygame.display.update()
            pygame.time.delay(3000)
            exit()

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
