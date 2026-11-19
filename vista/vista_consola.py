import os
import time


class VistaConsola:

    def limpiar(self):
        os.system("cls" if os.name == "nt" else "clear")
        print("\n" * 3)

    def mensaje(self, texto=""):
        print(texto)

    def titulo(self, texto):
        print(f"\n{'=' * 48}")
        print(texto.center(48))
        print("=" * 48)

    def pausar(self, texto="Presiona ENTER para continuar..."):
        input(texto)

    def pedir_entero(self, mensaje, minimo, maximo):
        while True:
            try:
                numero = int(input(mensaje).strip())
                if minimo <= numero <= maximo:
                    return numero
            except ValueError:
                pass

            self.mensaje(
                f"Introduce un número entre {minimo} y {maximo}."
            )

    def pedir_si_no(self, mensaje, predeterminado=True):
        while True:
            opcion = input(mensaje).strip().lower()

            if not opcion:
                return predeterminado
            if opcion in ("s", "si", "sí"):
                return True
            if opcion in ("n", "no"):
                return False

            self.mensaje("Responde S o N.")

    def pedir_texto(self, mensaje):
        return input(mensaje).strip()

    def mostrar_rol_privado(self, nombre, rol, palabra):
        self.limpiar()
        self.pausar(
            f"Turno privado de {nombre}. "
            "Solo esta persona debe mirar. ENTER..."
        )
        self.limpiar()

        self.titulo(f"INFORMACIÓN DE {nombre.upper()}")
        self.mensaje(f"ROL: {rol}")
        self.mensaje(f"PALABRA: {palabra}")

        self.pausar(
            "Memoriza tu información y pulsa "
            "ENTER para ocultarla..."
        )
        self.limpiar()

    def mostrar_pistas(self, pistas):
        self.titulo("PISTAS DE LA RONDA")

        for pista in pistas:
            self.mensaje(
                f"{pista.autor.nombre}: {pista.texto}"
            )

    def esperar_debate(self, segundos):
        self.titulo("DEBATE")
        self.mensaje(
            "Discutan quién podría ser el impostor."
        )

        for restantes in range(segundos, 0, -1):
            print(
                f"\rTiempo restante: {restantes:3d} segundos",
                end="",
                flush=True
            )
            time.sleep(1)

        print("\n¡Terminó el debate!")

    def pedir_voto(self, votante, candidatos):
        elegibles = [
            jugador for jugador in candidatos
            if jugador.id != votante.id
        ]

        self.titulo(
            f"VOTACIÓN DE {votante.nombre.upper()}"
        )

        for jugador in elegibles:
            self.mensaje(
                f"{jugador.id}. {jugador.nombre}"
            )

        while True:
            try:
                elegido = int(
                    input("Número del jugador acusado: ").strip()
                )
            except ValueError:
                self.mensaje("Escribe un número válido.")
                continue

            for jugador in elegibles:
                if jugador.id == elegido:
                    return jugador

            self.mensaje(
                "Debes elegir uno de los jugadores mostrados."
            )