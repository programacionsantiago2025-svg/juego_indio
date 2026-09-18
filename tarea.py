import random
import time
class Personaje:
    def __init__(self, clase, nombre, fuerza, inteligencia, vida, defensa, critico, velocidad):
        self.clase = clase
        self.nombre = nombre
        self.fuerza = fuerza
        self.inteligencia = inteligencia
        self.defensa = defensa
        self.vida = vida
        self.prob_critico = critico
        self.velocidad = velocidad
        if self.clase == "Mago":
            self.prob_critico += self.prob_critico * 0.08
            self.velocidad += self.velocidad * 0.08
        elif self.clase == "Guerrero":
            self.fuerza += self.fuerza * 0.1
            self.defensa += self.defensa * 0.1
        elif self.clase == "Tanque":
            self.defensa += self.defensa * 0.15
            self.vida += self.vida * 0.15

    def ver_datos(self):
        print(f"---Nombre-------: {self.nombre}")
        print(f"---Clase--------: {self.clase}")
        print(f"---Fuerza-------: {self.fuerza:.2f}")
        print(f"---Inteligencia-: {self.inteligencia:.2f}")
        print(f"---Defensa------: {self.defensa:.2f}")
        print(f"---Vida---------: {self.vida:.2f}")
        print(f"---Velocidad----: {self.velocidad:.2f}")
        print(f"---Prob Critico: {self.prob_critico * 100:.1f}%")
        print(f"---Esta Vivo----: {self.esta_vivo()}")
        print("-" * 40)
    def esta_vivo(self):
        if self.vida >0:
            vivo = "Si"
            return vivo
        else:
            vivo ="No"
            return vivo
    def calcular_daño(self, enemigo):
        #Daño base
        #En el daño influye un 70% la fuerza y un 30% la inteligencia
        daño_base = (self.fuerza * 0.7) + (self.inteligencia * 0.3)
        #Calculamos el daño 
        valor_critico = random.random()
        #Calculamos si es critico
        if valor_critico <= self.prob_critico: 
            critico =True
            daño_base *= 2 #El doble de daño
        else:
            critico =False
        #la logica funciona de la siguiente manera
        #La variable valor_critico toma valores de 0 a 1
        #Entonces si es menor que la probailidad de critico da critico
        #Entre mas grande sea el valor de probailidad critico, mas probable va a hacer que sea mayor que el valor critico
        fallo = random.choice(["Si", "No"])
        if fallo =="Si":
            daño_base =0
        #Defensa del enemigo reduce parte del daño
        daño_final = daño_base - (enemigo.defensa * random.uniform(0.5, 1.0))
        if daño_final < 0:
            daño_final = 0
        return round(daño_final, 2), critico, fallo
    def atacar(self, enemigo):
        daño, critico, fallo = self.calcular_daño(enemigo)
        enemigo.vida -= daño
        if enemigo.vida < 0:
            enemigo.vida = 0
        print(f"{self.nombre} ataca a {enemigo.nombre}")
        if fallo =="Si":
            print(f"{self.nombre} fallo el ataque")
        elif critico:
            print(f"CRITICO :0 {self.nombre} causa {daño} puntos de daño")
        else:
            print(f"{self.nombre} causa {daño} puntos de daño a {enemigo.nombre}.")
        print(f"Vida de {enemigo.nombre}: {enemigo.vida:.2f}")
        print(f"{enemigo.nombre} sigue vivo?: {enemigo.esta_vivo()}")
        print("-" * 40)
#COMBATE
personaje1 = Personaje("Guerrero", "Caballero", 8, 4, 20, 6, 0.3, 5)
personaje2 = Personaje("Mago", "Hechicero", 5, 8, 18, 5, 0.4, 7)
personaje1.ver_datos()
personaje2.ver_datos()
#Aca simulo las rondas, en total 5 rondas
for ronda in range(1, 6):
    print(f" RONDA {ronda}")
    personaje1.atacar(personaje2)
    if personaje2.vida <= 0:
        print(f"{personaje2.nombre} ha sido derrotado")
        break
    time.sleep(5)
    personaje2.atacar(personaje1)
    if personaje1.vida <= 0:
        print(f"{personaje1.nombre} ha sido derrotado")
        break