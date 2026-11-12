import unittest
import random
from pathlib import Path

from modelo.jugador import Jugador
from modelo.partida import Partida, ConfiguracionPartida
from modelo.impostor import Impostor
from modelo.enumeraciones import Ganador, FaseJuego

from modelo.excepciones import (
    VotoInvalidoException,
    EstadoInvalidoException
)

from servicios.asignador_roles import AsignadorRolesAleatorio
from servicios.validador_pistas import ValidadorPistaCompuesto
from servicios.contador_votos import ContadorVotosMayoria
from servicios.repositorio_palabras import RepositorioPalabrasArchivo


class TestPartida(unittest.TestCase):

    def crear(self, ultima=True):

        jugadores = [
            Jugador(i, f"J{i}")
            for i in range(1, 5)
        ]

        ruta = (
            Path(__file__).resolve().parents[1]
            / "datos"
            / "palabras.json"
        )

        partida = Partida(
            jugadores,
            ConfiguracionPartida(
                ultima_oportunidad=ultima,
                categoria="lugares"
            ),
            AsignadorRolesAleatorio(random.Random(1)),
            ValidadorPistaCompuesto(),
            ContadorVotosMayoria(),
            RepositorioPalabrasArchivo(
                ruta,
                random.Random(1)
            )
        )

        partida.iniciar()
        return partida

    def preparar_votacion(self, partida):

        for j in partida.activos:
            partida.registrar_pista(j, "Arena")

        partida.iniciar_debate()
        partida.iniciar_votacion()

    def test_flujo_y_ultima_oportunidad(self):

        partida = self.crear()

        impostor = next(
            j for j in partida.jugadores
            if isinstance(j.rol, Impostor)
        )

        self.assertEqual(
            partida.informacion_privada(impostor)[1],
            "PALABRA OCULTA"
        )

        self.preparar_votacion(partida)

        for j in partida.activos:
            partida.registrar_voto(
                j,
                next(
                    x for x in partida.activos
                    if x is not j
                ) if j is impostor else impostor
            )

        self.assertEqual(
            partida.resolver_votacion(),
            [impostor]
        )

        self.assertEqual(
            partida.ronda_actual.fase,
            FaseJuego.RESULTADO
        )

        self.assertEqual(
            partida.adivinar_palabra("incorrecta").ganador,
            Ganador.CIVILES
        )

    def test_impostor_acierta(self):

        partida = self.crear()

        impostor = next(
            j for j in partida.jugadores
            if isinstance(j.rol, Impostor)
        )

        self.preparar_votacion(partida)

        for j in partida.activos:
            partida.registrar_voto(
                j,
                next(
                    x for x in partida.activos
                    if x is not j
                ) if j is impostor else impostor
            )

        partida.resolver_votacion()

        palabra = next(
            j.rol.obtener_palabra_visible()
            for j in partida.jugadores
            if j is not impostor
        )

        self.assertEqual(
            partida.adivinar_palabra(palabra).ganador,
            Ganador.IMPOSTOR
        )

    def test_voto_duplicado(self):

        partida = self.crear()
        self.preparar_votacion(partida)

        a, b = partida.activos[:2]

        partida.registrar_voto(a, b)

        with self.assertRaises(VotoInvalidoException):
            partida.registrar_voto(a, b)

    def test_no_se_puede_iniciar_dos_veces(self):

        partida = self.crear()

        with self.assertRaises(EstadoInvalidoException):
            partida.iniciar()

    def test_civil_eliminado_nueva_ronda(self):

        partida = self.crear(ultima=False)

        impostor = next(
            j for j in partida.jugadores
            if isinstance(j.rol, Impostor)
        )

        civil = next(
            j for j in partida.jugadores
            if j is not impostor
        )

        self.preparar_votacion(partida)

        for j in partida.activos:
            partida.registrar_voto(
                j,
                next(
                    x for x in partida.activos
                    if x is not j
                ) if j is civil else civil
            )

        partida.resolver_votacion()

        self.assertFalse(civil.activo)

        self.assertEqual(
            len(partida.rondas),
            2
        )


if __name__ == "__main__":
    unittest.main()