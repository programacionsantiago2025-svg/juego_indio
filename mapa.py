import pygame

import recursos


class Colision:
    def __init__(self):
        self.arriba = pygame.Rect(610, -40, 50, 50)
        self.izquierda = pygame.Rect(-10, 340, 50, 50)
        self.derecha = pygame.Rect(1240, 370, 50, 50)
        self.abajo = pygame.Rect(600, 650, 50, 50)
        self.camino_vertical = pygame.Rect(575, 0, 150, 704)
        self.camino_horizontal = pygame.Rect(0, 315, 1300, 90)


class Mapa(Colision):
    def __init__(self, cacique, enemigos_nivel2, enemigos_nivel3):
        super().__init__()
        self.cacique_hablando = False
        self.cacique = cacique
        self.enemigos_nivel2 = enemigos_nivel2
        self.enemigos_nivel3 = enemigos_nivel3
        self.nivel = 0
        self.en_choza = False
        self.colision_choza = pygame.Rect(620, 370, 100, 100)
        self.sonido_puerta = pygame.mixer.Sound(recursos.SONIDO_PUERTA)
        self.mision = False
        self.item1 = True
        self.pos_valida_nivel1 = None

    def dibujar_nivel(self, ventana, ancho, largo, jugador):
        keys = pygame.key.get_pressed()
        fuente = pygame.font.SysFont(None, 30)
        if self.nivel == 0:
            if not self.en_choza:
                cielo = pygame.Rect(0, 0, 1200, 370)
                if jugador.forma.colliderect(cielo):
                    jugador.forma.y = 370
                imagen = pygame.image.load(recursos.FONDO_ALDEA).convert()
                imagen = pygame.transform.scale(imagen, (ancho, largo))
                ventana.blit(imagen, (0, 0))
                if jugador.forma.colliderect(self.colision_choza):
                    texto = fuente.render("Presiona E para entrar a la choza", True, (255, 255, 255))
                    ventana.blit(texto, (500, 320))
                    if keys[pygame.K_e]:
                        pygame.time.delay(100)
                        self.sonido_puerta.play()
                        self.en_choza = True
                        jugador.forma.x = 650
                        jugador.forma.y = 500
                if jugador.forma.colliderect(self.abajo) and self.mision == True:
                    self.nivel = 1
                    jugador.forma.x = 590
                    jugador.forma.y = 20
                elif jugador.forma.colliderect(self.abajo) and self.mision == False:
                    texto = fuente.render("Primero debes hablar con el cacique, ve a la choza", False, (255, 255, 255))
                    ventana.blit(texto, (500, 300))
            elif self.en_choza:
                imagen = pygame.image.load(recursos.FONDO_CHOZA).convert()
                imagen = pygame.transform.scale(imagen, (ancho, largo))
                ventana.blit(imagen, (0, 0))
                self.cacique.animar()
                self.cacique.dibujar(ventana)
                if not self.cacique_hablando:
                    if self.cacique.colision(jugador):
                        texto = fuente.render("Presiona F para hablar con el cacique", True, (255, 255, 255))
                        ventana.blit(texto, (500, 250))
                        if keys[pygame.K_f]:
                            self.mision = True
                            self.cacique_hablando = True
                            self.cacique.iniciar_dialogo()
                            pygame.time.delay(150)
                else:
                    self.cacique.hablar(ventana)
                    texto = fuente.render("Presiona F para continuar, G para salir", False, (255, 255, 255))
                    ventana.blit(texto, (500, 400))
                    if keys[pygame.K_g]:
                        self.cacique_hablando = False
                    elif keys[pygame.K_f]:
                        self.cacique.avanzar_dialogo()
                        pygame.time.delay(150)
                        if self.cacique.dialogo_terminado():
                            self.cacique_hablando = False
                fuente = pygame.font.SysFont(None, 30)
                puerta = pygame.Rect(230, 410, 30, 30)
                texto = fuente.render("Presiona E para salir de la choza", True, (255, 255, 255))
                if jugador.forma.colliderect(puerta):
                    ventana.blit(texto, (230, 300))
                    if keys[pygame.K_e] and jugador.forma.colliderect(puerta):
                        pygame.time.delay(100)
                        self.sonido_puerta.play()
                        self.en_choza = False
                        jugador.forma.x = 650
                        jugador.forma.y = 460
        if self.nivel == 1:
            imagen = pygame.image.load(recursos.FONDO_NIVEL1).convert()
            imagen = pygame.transform.scale(imagen, (ancho, largo))
            ventana.blit(imagen, (0, 0))
            pies = pygame.Rect(0, 0, 40, 20)
            pies.midbottom = jugador.forma.midbottom
            en_camino = pies.colliderect(self.camino_vertical) or pies.colliderect(self.camino_horizontal)
            if en_camino or self.pos_valida_nivel1 is None:
                self.pos_valida_nivel1 = (jugador.forma.x, jugador.forma.y)
            else:
                jugador.forma.x, jugador.forma.y = self.pos_valida_nivel1
            if jugador.forma.colliderect(self.arriba):
                self.nivel = 0
            if jugador.forma.colliderect(self.izquierda):
                jugador.forma.x = self.derecha.x - 100
                self.nivel = 2
        if self.nivel == 2:
            imagen = pygame.image.load(recursos.FONDO_NIVEL2).convert()
            imagen = pygame.transform.scale(imagen, (ancho, largo))
            ventana.blit(imagen, (0, 0))

            for enemigo in self.enemigos_nivel2:
                if enemigo.vida > 0:
                    enemigo.seguir(jugador)
                    enemigo.animar()
                    enemigo.dibujar(ventana)
                    enemigo.dibujar_barra_vida(ventana, enemigo.forma.x, enemigo.forma.y - 15)

            if jugador.forma.colliderect(self.derecha):
                self.nivel = 1
            if jugador.forma.colliderect(self.arriba):
                jugador.forma.x = self.abajo.x
                jugador.forma.y = self.abajo.y - 100
                self.nivel = 3
        if self.nivel == 3:
            imagen = pygame.image.load(recursos.FONDO_NIVEL3).convert()
            imagen = pygame.transform.scale(imagen, (ancho, largo))
            ventana.blit(imagen, (0, 0))
            if self.item1:
                imagen_item = pygame.image.load(recursos.ITEM_SOL)
                imagen_item = pygame.transform.scale(imagen_item, (50, 50))
                ventana.blit(imagen_item, (650, 150))
            if jugador.forma.colliderect(imagen_item.get_rect()):
                self.item1 = False
            if jugador.forma.colliderect(self.abajo):
                self.nivel = 2
            for enemigo in self.enemigos_nivel3:
                if enemigo.vida > 0:
                    enemigo.seguir(jugador)
                    enemigo.animar()
                    enemigo.dibujar(ventana)
                    enemigo.dibujar_barra_vida(ventana, enemigo.forma.x, enemigo.forma.y - 15)
