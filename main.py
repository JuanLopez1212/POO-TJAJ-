from pathlib import Path

from controlador.controlador_partida import ControladorPartida
from vista.vista_consola import VistaConsola

from modelo.enumeraciones import Ganador

from servicios.asignador_roles import AsignadorRolesAleatorio
from servicios.validador_pistas import ValidadorPistaCompuesto
from servicios.contador_votos import ContadorVotosMayoria
from servicios.repositorio_palabras import RepositorioPalabrasArchivo


def main():

    ruta = (
        Path(__file__).resolve().parent
        / "datos"
        / "palabras.json"
    )

    vista = VistaConsola()

    vista.titulo("BIENVENIDOS A EL IMPOSTOR")

    # Marcador acumulado
    marcador = {
        Ganador.CIVILES: 0,
        Ganador.IMPOSTOR: 0
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

            # Ejecutar partida
            resultado = controlador.jugar()

            # Actualizar marcador
            marcador[resultado.ganador] += 1

            # Mostrar marcador
            vista.titulo("MARCADOR ACUMULADO")

            vista.mensaje(
                f"Civiles: {marcador[Ganador.CIVILES]}"
            )

            vista.mensaje(
                f"Impostor: {marcador[Ganador.IMPOSTOR]}"
            )

            # Preguntar si desean jugar otra vez
            if not vista.pedir_si_no(
                "¿Jugar otra partida? (s/N): ",
                False
            ):
                break

    except (KeyboardInterrupt, EOFError):
        vista.mensaje(
            "\nJuego interrumpido. ¡Hasta pronto!"
        )


if __name__ == "__main__":
    main()