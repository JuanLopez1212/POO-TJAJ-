from pathlib import Path

from controlador.controlador_partida import ControladorPartida
from vista.vista_consola import VistaConsola

from servicios.asignador_roles import AsignadorRolesAleatorio
from servicios.validador_pistas import ValidadorPistaCompuesto
from servicios.contador_votos import ContadorVotosMayoria
from servicios.repositorio_palabras import RepositorioPalabrasArchivo

def main():
    ruta = (
        Path(__file__).resolve().parent
        /"datos"
        /"palabras.json"
    )

    vista = VistaConsola()
    vista.titulo("Bienvenidos a el impostor")

    marcador = {
        "Civiles": 0,
        "Impostor": 0
    }

    try:
        while True:
            controlador = ControladorPartida(
                vista,
                AsignadorRolesAleatorio(),
                ValidadorPistaCompuesto(),
                ContadorVotosMayoria(),
                RepositorioPalabrasArchivo(ruta)
            )

            resultado = controlador.jugar()

            marcador[resultado.ganador.name] += 1

            vista.titulo("Marcador acumulado")
            vista.mensaje(
                f"Civiles: {marcador['Civiles']} | "
                f"Impostor: {marcador['Impostor']}"
            )

            if not vista.pedir_si_no(
                "¿Jugar otra partida? (s/N): ",
                False
            ):
                break
    except ( KeyboardInterrupt, EOFError):
        vista.mensaje(
            "\nJuego interrumpido"
        )

if __name__ == "__main__":
    main()