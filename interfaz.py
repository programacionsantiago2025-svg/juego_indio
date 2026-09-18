import pygame


def dibujar_boton(superficie, rect, texto, fuente, color_bg=(60, 60, 60), color_txt=(255, 255, 255)):
    pygame.draw.rect(superficie, color_bg, rect)
    txt = fuente.render(texto, True, color_txt)
    superficie.blit(txt, txt.get_rect(center=rect.center))
