import pygame

from personaje import Personaje
import recursos


class Cacique(Personaje):
    def __init__(self, imagenes_quieto_rutas, x, y, dialogo):
        super().__init__(
            nombre="Cacique",
            fuerza=0,
            vida=100,
            x=x,
            y=y,
            imagenes_rutas=imagenes_quieto_rutas,
            imagenes_quieto_rutas=imagenes_quieto_rutas,
            imagenes_atacar_rutas=imagenes_quieto_rutas,
            clase="Cacique")
        self.dialogo = dialogo
        self.moviendo = False
        self.pagina_dialogo = 0
        self.caras = {
            "serio": self._cargar_cara(recursos.CARA_CACIQUE_SERIO),
            "feliz": self._cargar_cara(recursos.CARA_CACIQUE_FELIZ),
            "enojado": self._cargar_cara(recursos.CARA_CACIQUE_ENOJADO),
        }

    def _cargar_cara(self, ruta):
        imagen = pygame.image.load(ruta).convert_alpha()
        return pygame.transform.scale(imagen, (140, 190))

    def colision(self, jugador):
        if self.forma.colliderect(jugador.forma):
            return True

    def iniciar_dialogo(self):
        self.pagina_dialogo = 0

    def avanzar_dialogo(self):
        self.pagina_dialogo += 1

    def dialogo_terminado(self):
        return self.pagina_dialogo >= len(self.dialogo)

    def hablar(self, ventana):
        lineas, expresion = self.dialogo[self.pagina_dialogo]
        fuente = pygame.font.SysFont(None, 28)
        nombre_cacique = pygame.font.SysFont(None, 32)
        cuadro = pygame.Rect(150, 200, 1000, 200)
        pygame.draw.rect(ventana, (40, 30, 20), cuadro)
        pygame.draw.rect(ventana, (200, 180, 100), cuadro, 3)

        cara = self.caras[expresion]
        cara_rect = cara.get_rect(topleft=(cuadro.x + 10, cuadro.y + 5))
        ventana.blit(cara, cara_rect)

        nombre_texto = nombre_cacique.render(self.nombre + ":", True, (255, 215, 0))
        ventana.blit(nombre_texto, (cara_rect.right + 20, cuadro.y + 10))
        y_pos = cuadro.y + 50
        for linea in lineas:
            texto = fuente.render(linea, True, (255, 255, 255))
            ventana.blit(texto, (cara_rect.right + 20, y_pos))
            y_pos += 35
