

import random
from typing import Sequence

from modelo.jugador import Jugador
from modelo.civil import Civil
from modelo.impostor import Impostor
from modelo.palabra_secreta import PalabraSecreta

from servicios.interfaces import IAsignadorRoles


class AsignadorRolesAleatorio(IAsignadorRoles):

    def __init__(
        self,
        rng: random.Random | None = None
    ):
        self._rng = rng or random.Random()

    def asignar_roles(
        self,
        jugadores: Sequence[Jugador],
        palabra: PalabraSecreta
    ) -> Jugador:

        if not 3 <= len(jugadores) <= 10:
            raise ValueError(
                "Se requieren entre 3 y 10 jugadores"
            )

        if len({
            j.id for j in jugadores
        }) != len(jugadores):
            raise ValueError(
                "Los identificadores deben ser únicos"
            )

        elegido = self._rng.choice(list(jugadores))

        for jugador in jugadores:
            jugador.asignar_rol(
                Impostor()
                if jugador is elegido
                else Civil(palabra)
            )

        return elegido