from personaje import Personaje


class Enemigo(Personaje):
    def __init__(self, imagenes_mover_rutas, x, y, imagenes_atacar_rutas):
        super().__init__(nombre="Español", fuerza=5, vida=20, x=x, y=y, imagenes_rutas=imagenes_mover_rutas, imagenes_quieto_rutas=imagenes_mover_rutas, imagenes_atacar_rutas=imagenes_atacar_rutas, clase="Enemigo")
        self.puede_atacar = True

    def seguir(self, jugador):
        if self.vida <= 0:
            return
        x, y = jugador.forma.x, jugador.forma.y
        if self.forma.colliderect(jugador.forma):
            if self.puede_atacar:
                self.atacando = True
                jugador.recibir_daño(self.fuerza)
                self.puede_atacar = False
            self.moviendo = False
        else:
            self.atacando = False
            self.puede_atacar = True
            self.moviendo = True
            if x < self.forma.x:
                self.direccion = 'izquierda'
                self.forma.x -= 5
            if x > self.forma.x:
                self.direccion = 'derecha'
                self.forma.x += 5
            if y < self.forma.y:
                self.forma.y -= 5
            if y > self.forma.y:
                self.forma.y += 5
