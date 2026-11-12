

from collections import Counter
from typing import Sequence

from modelo.jugador import Jugador
from modelo.voto import Voto
from modelo.excepciones import VotoInvalidoException

from servicios.interfaces import IContadorVotos


class ContadorVotosMayoria(IContadorVotos):

    def contar_votos(
        self,
        votos: Sequence[Voto],
        jugadores: Sequence[Jugador]
    ) -> list[Jugador]:

        activos = {
            j.id: j
            for j in jugadores
            if j.activo
        }

        if len(votos) != len(activos):
            raise VotoInvalidoException(
                "Todos los jugadores activos deben votar"
            )

        votantes = set()
        conteo = Counter()

        for voto in votos:
            a = voto.votante.id
            b = voto.acusado.id

            if (
                a not in activos
                or b not in activos
                or a == b
                or a in votantes
            ):
                raise VotoInvalidoException(
                    "Voto inválido o duplicado"
                )

            votantes.add(a)
            conteo[b] += 1

        mayor = max(conteo.values())

        return [
            activos[jid]
            for jid, total in conteo.items()
            if total == mayor
        ]

       