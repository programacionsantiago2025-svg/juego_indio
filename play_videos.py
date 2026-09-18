import pygame
import cv2


class VideoFondo:
    def __init__(self, ruta, ancho, largo):
        self.video = cv2.VideoCapture(ruta)
        if not self.video.isOpened():
            raise FileNotFoundError(f"No se pudo abrir el video: {ruta}")
        self.ancho = ancho
        self.largo = largo
        self.fps = self.video.get(cv2.CAP_PROP_FPS) or 24
        self.ms_por_frame = 1000 / self.fps
        self.ultimo_tiempo = pygame.time.get_ticks()
        self.superficie = None
        self._leer_frame()
    def _leer_frame(self):
        ret, frame = self.video.read()
        if not ret:
            self.video.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = self.video.read()
            if not ret:
                return
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (self.ancho, self.largo))
        self.superficie = pygame.surfarray.make_surface(frame.swapaxes(0, 1))

    def actualizar(self):
        ahora = pygame.time.get_ticks()
        if ahora - self.ultimo_tiempo >= self.ms_por_frame:
            self.ultimo_tiempo = ahora
            self._leer_frame()

    def dibujar(self, ventana):
        self.actualizar()
        if self.superficie:
            ventana.blit(self.superficie, (0, 0))
    def cerrar(self):
        self.video.release()