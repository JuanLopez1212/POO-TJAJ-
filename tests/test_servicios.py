import random
import unittest
from pathlib import Path

from modelo.jugador import Jugador
from modelo.civil import Civil
from modelo.impostor import Impostor
from modelo.palabra_secreta import PalabraSecreta
from modelo.voto import Voto

from modelo.excepciones import (
    PistaInvalidaException,
    VotoInvalidoException
)

from servicios.asignador_roles import AsignadorRolesAleatorio
from servicios.validador_pistas import ValidadorPistaCompuesto
from servicios.contador_votos import ContadorVotosMayoria
from servicios.repositorio_palabras import RepositorioPalabrasArchivo


class TestServicios(unittest.TestCase):

    def setUp(self):
        self.jugadores = [
            Jugador(i, f"Jugador {i}")
            for i in range(1, 6)
        ]

        self.palabra = PalabraSecreta(
            "Playa",
            "lugares"
        )

    def test_unico_impostor(self):

        elegido = AsignadorRolesAleatorio(
            random.Random(7)
        ).asignar_roles(
            self.jugadores,
            self.palabra
        )

        self.assertEqual(
            sum(
                isinstance(j.rol, Impostor)
                for j in self.jugadores
            ),
            1
        )

        self.assertIsInstance(
            elegido.rol,
            Impostor
        )

        self.assertEqual(
            sum(
                isinstance(j.rol, Civil)
                for j in self.jugadores
            ),
            4
        )

    def test_rol_oculta_palabra(self):

        AsignadorRolesAleatorio(
            random.Random(3)
        ).asignar_roles(
            self.jugadores,
            self.palabra
        )

        for jugador in self.jugadores:

            self.assertEqual(
                jugador.rol.conoce_palabra(),
                isinstance(jugador.rol, Civil)
            )

            if isinstance(jugador.rol, Impostor):
                self.assertNotIn(
                    "playa",
                    jugador.rol.obtener_palabra_visible().lower()
                )

    def test_pista_valida(self):

        ValidadorPistaCompuesto().validar(
            "Arena",
            self.palabra,
            40
        )

    def test_pista_con_palabra_prohibida(self):

        with self.assertRaises(PistaInvalidaException):
            ValidadorPistaCompuesto().validar(
                "La PLÁYA es bonita",
                self.palabra,
                40
            )

    def test_pista_demasiado_larga(self):

        with self.assertRaises(PistaInvalidaException):
            ValidadorPistaCompuesto().validar(
                "a" * 41,
                self.palabra,
                40
            )

    def test_pista_vacia(self):

        with self.assertRaises(PistaInvalidaException):
            ValidadorPistaCompuesto().validar(
                "  ",
                self.palabra,
                40
            )

    def test_conteo_mayoria(self):

        a, b, c, d, e = self.jugadores

        votos = [
            Voto(a, b),
            Voto(b, a),
            Voto(c, b),
            Voto(d, b),
            Voto(e, a)
        ]

        self.assertEqual(
            ContadorVotosMayoria().contar_votos(
                votos,
                self.jugadores
            ),
            [b]
        )

    def test_empate(self):

        a, b, c, d, e = self.jugadores

        votos = [
            Voto(a, b),
            Voto(b, a),
            Voto(c, b),
            Voto(d, a),
            Voto(e, c)
        ]

        self.assertEqual(
            set(
                ContadorVotosMayoria().contar_votos(
                    votos,
                    self.jugadores
                )
            ),
            {a, b}
        )

    def test_voto_propio_invalido(self):

        a, b, c, d, e = self.jugadores

        votos = [
            Voto(a, a),
            Voto(b, a),
            Voto(c, b),
            Voto(d, b),
            Voto(e, b)
        ]

        with self.assertRaises(VotoInvalidoException):
            ContadorVotosMayoria().contar_votos(
                votos,
                self.jugadores
            )

    def test_votos_incompletos(self):

        with self.assertRaises(VotoInvalidoException):
            ContadorVotosMayoria().contar_votos(
                [],
                self.jugadores
            )

    def test_repositorio_categoria(self):

        ruta = (
            Path(__file__).resolve().parents[1]
            / "datos"
            / "palabras.json"
        )

        palabra = RepositorioPalabrasArchivo(
            ruta,
            random.Random(2)
        ).obtener_palabra_aleatoria("animales")

        self.assertEqual(
            palabra.categoria,
            "animales"
        )


if __name__ == "__main__":
    unittest.main()