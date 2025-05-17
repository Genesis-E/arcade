import random
import time
from abc import ABC, abstractmethod

# Clase base para ataques
class Ataque(ABC):
    def __init__(self, nombre, poder, tipo, precision=100, pp=10):
        self.nombre = nombre
        self.poder = poder
        self.tipo = tipo
        self.precision = precision
        self.pp = pp
        self.pp_max = pp
    
    @abstractmethod
    def efecto(self, atacante, defensor):
        pass

class AtaqueNormal(Ataque):
    def efecto(self, atacante, defensor):
        if random.randint(1, 100) > self.precision:
            return f"{atacante.nombre} falló el ataque!"
        
        self.pp -= 1
        daño = self.calcular_daño(atacante, defensor)
        defensor.hp_actual -= daño
        
        return f"{atacante.nombre} usó {self.nombre}. ¡Hizo {daño} de daño!"

    def calcular_daño(self, atacante, defensor):
        # Fórmula simplificada de daño
        nivel = atacante.nivel
        ataque = atacante.ataque
        defensa = defensor.defensa
        
        # Ventaja/desventaja de tipo
        efectividad = self.calcular_efectividad(defensor.tipo)
        
        daño = (((2 * nivel / 5 + 2) * self.poder * ataque / defensa) / 50 + 2) 
                * efectividad * random.uniform(0.85, 1.0))
        
        return int(daño)
    
    def calcular_efectividad(self, tipo_defensor):
        tabla_efectividad = {
            'fuego': {'planta': 2.0, 'agua': 0.5, 'fuego': 0.5},
            'agua': {'fuego': 2.0, 'planta': 0.5, 'agua': 0.5},
            'planta': {'agua': 2.0, 'fuego': 0.5, 'planta': 0.5},
            'electrico': {'agua': 2.0, 'planta': 1.0, 'electrico': 0.5}
        }
        
        return tabla_efectividad.get(self.tipo, {}).get(tipo_defensor, 1.0)

# Clase base para Pokémon
class Pokemon:
    def __init__(self, nombre, tipo, nivel, hp, ataque, defensa, ataques):
        self.nombre = nombre
        self.tipo = tipo
        self.nivel = nivel
        self.hp_max = hp
        self.hp_actual = hp
        self.ataque = ataque
        self.defensa = defensa
        self.ataques = ataques
        self.experiencia = 0
        self.estado = "normal"
    
    def usar_ataque(self, indice_ataque, defensor):
        if indice_ataque < 0 or indice_ataque >= len(self.ataques):
            return "¡Ataque inválido!"
        
        ataque = self.ataques[indice_ataque]
        if ataque.pp <= 0:
            return f"¡{self.nombre} no tiene PP para {ataque.nombre}!"
        
        return ataque.efecto(self, defensor)
    
    def recibir_daño(self, cantidad):
        self.hp_actual -= cantidad
        if self.hp_actual <= 0:
            self.hp_actual = 0
            self.estado = "debilitado"
            return f"¡{self.nombre} se ha debilitado!"
        return f"¡{self.nombre} tiene {self.hp_actual}/{self.hp_max} HP!"
    
    def usar_pocion(self):
        if self.estado == "debilitado":
            return "¡No se puede usar poción en un Pokémon debilitado!"
        
        curacion = self.hp_max * 0.3
        self.hp_actual = min(self.hp_max, self.hp_actual + curacion)
        return f"¡{self.nombre} recuperó {curacion} HP!"
    
    def ganar_experiencia(self, cantidad):
        self.experiencia += cantidad
        if self.experiencia >= self.nivel * 100:
            self.subir_nivel()
            return f"¡{self.nombre} subió al nivel {self.nivel}!"
        return f"{self.nombre} ganó {cantidad} puntos de experiencia."
    
    def subir_nivel(self):
        self.nivel += 1
        self.hp_max += random.randint(5, 10)
        self.ataque += random.randint(2, 5)
        self.defensa += random.randint(2, 5)
        self.hp_actual = self.hp_max
        self.experiencia = 0

# Clases específicas de Pokémon
class PokemonFuego(Pokemon):
    def __init__(self, nombre, nivel, ataques):
        hp = 39 + nivel * 10
        ataque = 52 + nivel * 3
        defensa = 43 + nivel * 2
        super().__init__(nombre, 'fuego', nivel, hp, ataque, defensa, ataques)

class PokemonAgua(Pokemon):
    def __init__(self, nombre, nivel, ataques):
        hp = 44 + nivel * 10
        ataque = 48 + nivel * 3
        defensa = 65 + nivel * 2
        super().__init__(nombre, 'agua', nivel, hp, ataque, defensa, ataques)

class PokemonPlanta(Pokemon):
    def __init__(self, nombre, nivel, ataques):
        hp = 45 + nivel * 10
        ataque = 49 + nivel * 3
        defensa = 49 + nivel * 2
        super().__init__(nombre, 'planta', nivel, hp, ataque, defensa, ataques)

class PokemonElectrico(Pokemon):
    def __init__(self, nombre, nivel, ataques):
        hp = 35 + nivel * 10
        ataque = 55 + nivel * 3
        defensa = 40 + nivel * 2
        super().__init__(nombre, 'electrico', nivel, hp, ataque, defensa, ataques)

# Implementaciones concretas de Pokémon
class Charmander(PokemonFuego):
    def __init__(self, nivel):
        ataques = [
            AtaqueNormal("Lanzallamas", 90, 'fuego', 85, 15),
            AtaqueNormal("Arañazo", 40, 'normal', 100, 35),
            AtaqueNormal("Giro Fuego", 35, 'fuego', 85, 15),
            AtaqueNormal("Ascuas", 40, 'fuego', 100, 25)
        ]
        super().__init__("Charmander", nivel, ataques)

class Squirtle(PokemonAgua):
    def __init__(self, nivel):
        ataques = [
            AtaqueNormal("Pistola Agua", 40, 'agua', 100, 25),
            AtaqueNormal("Mordisco", 60, 'normal', 100, 25),
            AtaqueNormal("Hidrobomba", 110, 'agua', 80, 5),
            AtaqueNormal("Cabezazo", 70, 'normal', 100, 15)
        ]
        super().__init__("Squirtle", nivel, ataques)

class Bulbasaur(PokemonPlanta):
    def __init__(self, nivel):
        ataques = [
            AtaqueNormal("Latigazo", 45, 'planta', 100, 25),
            AtaqueNormal("Drenadoras", 20, 'planta', 100, 10),
            AtaqueNormal("Hoja Afilada", 55, 'planta', 95, 25),
            AtaqueNormal("Somnífero", 0, 'planta', 75, 15)
        ]
        super().__init__("Bulbasaur", nivel, ataques)

class Pikachu(PokemonElectrico):
    def __init__(self, nivel):
        ataques = [
            AtaqueNormal("Impactrueno", 40, 'electrico', 100, 30),
            AtaqueNormal("Rayo", 90, 'electrico', 100, 15),
            AtaqueNormal("Ataque Rápido", 40, 'normal', 100, 30),
            AtaqueNormal("Onda Trueno", 0, 'electrico', 90, 20)
        ]
        super().__init__("Pikachu", nivel, ataques)

# Clase para manejar la batalla
class Batalla:
    def __init__(self, jugador, enemigo):
        self.jugador = jugador
        self.enemigo = enemigo
        self.turno = 1
        self.clima = None
    
    def iniciar_batalla(self):
        print(f"¡Comienza la batalla entre {self.jugador.nombre} y {self.enemigo.nombre}!")
        
        while not self.batalla_terminada():
            print(f"\n--- Turno {self.turno} ---")
            self.mostrar_estados()
            
            # Turno del jugador
            accion = self.menu_acciones()
            
            if accion == "1":  # Atacar
                self.turno_jugador_atacar()
            elif accion == "2":  # Usar poción
                print(self.jugador.usar_pocion())
            elif accion == "3":  # Huir
                print("¡Has huido de la batalla!")
                return False
            
            # Verificar si el enemigo fue derrotado
            if self.enemigo.estado == "debilitado":
                print(f"¡{self.enemigo.nombre} se ha debilitado!")
                print(self.jugador.ganar_experiencia(self.enemigo.nivel * 20))
                return True
            
            # Turno del enemigo (IA simple)
            self.turno_enemigo()
            
            # Verificar si el jugador fue derrotado
            if self.jugador.estado == "debilitado":
                print(f"¡{self.jugador.nombre} se ha debilitado!")
                return False
            
            self.turno += 1
    
    def menu_acciones(self):
        while True:
            print("\n¿Qué deseas hacer?")
            print("1. Atacar")
            print("2. Usar poción")
            print("3. Huir")
            
            opcion = input("Selecciona una opción: ")
            if opcion in ["1", "2", "3"]:
                return opcion
            print("¡Opción inválida! Intenta de nuevo.")
    
    def turno_jugador_atacar(self):
        print("\nSelecciona un ataque:")
        for i, ataque in enumerate(self.jugador.ataques):
            print(f"{i+1}. {ataque.nombre} (PP: {ataque.pp}/{ataque.pp_max})")
        
        while True:
            try:
                seleccion = int(input("Elige un ataque: ")) - 1
                if 0 <= seleccion < len(self.jugador.ataques):
                    print(self.jugador.usar_ataque(seleccion, self.enemigo))
                    break
                print("¡Número de ataque inválido!")
            except ValueError:
                print("¡Ingresa un número válido!")
    
    def turno_enemigo(self):
        # IA simple: elige un ataque al azar que tenga PP
        ataques_disponibles = [i for i, ataque in enumerate(self.enemigo.ataques) if ataque.pp > 0]
        
        if not ataques_disponibles:
            print(f"{self.enemigo.nombre} no puede atacar!")
            return
        
        ataque_elegido = random.choice(ataques_disponibles)
        print(self.enemigo.usar_ataque(ataque_elegido, self.jugador))
    
    def mostrar_estados(self):
        print(f"\n{self.jugador.nombre}: HP {self.jugador.hp_actual}/{self.jugador.hp_max}")
        print(f"{self.enemigo.nombre}: HP {self.enemigo.hp_actual}/{self.enemigo.hp_max}")
    
    def batalla_terminada(self):
        return (self.jugador.estado == "debilitado" or 
                self.enemigo.estado == "debilitado")

# Menú principal del juego
class JuegoPokemon:
    def __init__(self):
        self.pokemones_disponibles = {
            "1": ("Charmander", lambda nivel: Charmander(nivel)),
            "2": ("Squirtle", lambda nivel: Squirtle(nivel)),
            "3": ("Bulbasaur", lambda nivel: Bulbasaur(nivel)),
            "4": ("Pikachu", lambda nivel: Pikachu(nivel))
        }
        self.jugador = None
    
    def menu_principal(self):
        print("¡Bienvenido al Mundo Pokémon!")
        
        while True:
            print("\nMenú Principal:")
            print("1. Iniciar nueva partida")
            print("2. Salir")
            
            opcion = input("Selecciona una opción: ")
            
            if opcion == "1":
                self.nueva_partida()
            elif opcion == "2":
                print("¡Hasta luego!")
                break
            else:
                print("¡Opción inválida! Intenta de nuevo.")
    
    def nueva_partida(self):
        print("\nSelecciona tu Pokémon inicial:")
        for num, (nombre, _) in self.pokemones_disponibles.items():
            print(f"{num}. {nombre}")
        
        while True:
            seleccion = input("Elige tu Pokémon (1-4): ")
            if seleccion in self.pokemones_disponibles:
                _, constructor = self.pokemones_disponibles[seleccion]
                self.jugador = constructor(5)  # Nivel inicial 5
                print(f"¡Has elegido a {self.jugador.nombre}!")
                break
            print("¡Selección inválida! Intenta de nuevo.")
        
        self.bucle_batallas()
    
    def bucle_batallas(self):
        while self.jugador.estado != "debilitado":
            # Crear un enemigo aleatorio
            enemigo_num = random.choice(list(self.pokemones_disponibles.keys()))
            _, constructor = self.pokemones_disponibles[enemigo_num]
            nivel_enemigo = max(1, self.jugador.nivel + random.randint(-2, 2))
            enemigo = constructor(nivel_enemigo)
            
            print(f"\n¡Un {enemigo.nombre} salvaje de nivel {enemigo.nivel} apareció!")
            
            batalla = Batalla(self.jugador, enemigo)
            resultado = batalla.iniciar_batalla()
            
            if not resultado:  # El jugador perdió o huyó
                if self.jugador.estado == "debilitado":
                    print("¡Has perdido la batalla!")
                    print("Tu Pokémon ha sido curado en el Centro Pokémon.")
                    self.jugador.hp_actual = self.jugador.hp_max
                    self.jugador.estado = "normal"
                break
            
            input("\nPresiona Enter para continuar...")
        
        print("\nRegresando al menú principal...")

# Iniciar el juego
if __name__ == "__main__":
    juego = JuegoPokemon()
    juego.menu_principal()
