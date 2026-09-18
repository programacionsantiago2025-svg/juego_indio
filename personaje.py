import pygame


class Personaje:
    def __init__(self, nombre, fuerza, vida, x, y, imagenes_rutas, imagenes_quieto_rutas, imagenes_atacar_rutas, clase):
        self.atacando = False
        self.nombre = nombre
        self.clase = clase
        self.fuerza = fuerza
        self.vida_maxima = vida
        self.vida = vida
        self.forma = pygame.Rect(620, 440, 100, 100)
        self.forma.center = (x, y)
        self.imagenes = [pygame.transform.scale(pygame.image.load(ruta), (100, 100)) for ruta in imagenes_rutas]
        if self.clase == "Indio":
            self.imagenes_quieto = [pygame.transform.scale(pygame.image.load(ruta), (100, 100)) for ruta in imagenes_quieto_rutas]
        else:
            self.imagenes_quieto = [pygame.transform.scale(pygame.image.load(ruta), (100, 100)) for ruta in imagenes_quieto_rutas]
        self.imagenes_atacar = [pygame.transform.scale(pygame.image.load(ruta), (100, 100)) for ruta in imagenes_atacar_rutas]
        self.imagenes_ataque = self.imagenes_atacar
        self.frame = 0
        self.frame_quieto = 0
        self.frame_atacar = 0
        self.direccion = "derecha"
        self.moviendo = False

    def dibujar(self, ventana):
        if self.moviendo:
            imagen_actual = self.imagenes[self.frame]
        else:
            imagen_actual = self.imagenes_quieto[self.frame_quieto]
        if self.direccion == "izquierda":
            imagen_actual = pygame.transform.flip(imagen_actual, True, False)
        if self.atacando:
            imagen_actual = self.imagenes_atacar[self.frame_atacar]
        ventana.blit(imagen_actual, self.forma)

    def animar(self):
        if self.moviendo:
            self.frame = (self.frame + 1) % len(self.imagenes)
        elif not self.moviendo:
            self.frame_quieto = (self.frame_quieto + 1) % len(self.imagenes_quieto)
        if self.atacando:
            self.frame_atacar = (self.frame_atacar + 1) % len(self.imagenes_atacar)

    def animar_ataque(self, ventana, mapa, ancho, largo):
        if self.imagenes_ataque:
            self.atacando = True
            for img in self.imagenes_ataque:
                imagen_actual = img
                if self.direccion == "izquierda":
                    imagen_actual = pygame.transform.flip(imagen_actual, True, False)
                mapa.dibujar_nivel(ventana, ancho, largo, self)
                ventana.blit(imagen_actual, self.forma)
                pygame.display.update()
                pygame.time.delay(20)
            self.atacando = False

    def dibujar_barra_vida(self, ventana, x, y):
        ancho_barra = 100
        alto_barra = 10
        pygame.draw.rect(ventana, (255, 0, 0), (x, y, ancho_barra, alto_barra))
        vida_actual = (self.vida / self.vida_maxima) * ancho_barra
        pygame.draw.rect(ventana, (0, 255, 0), (x, y, vida_actual, alto_barra))
        pygame.draw.rect(ventana, (255, 255, 255), (x, y, ancho_barra, alto_barra), 2)

    def recibir_daño(self, daño):
        self.vida -= daño
        if self.vida < 0:
            self.vida = 0
