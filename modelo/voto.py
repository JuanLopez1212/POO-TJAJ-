

from dataclasses import dataclass
from modelo.jugador import Jugador

@dataclass(frozen=True)
class Voto:
    votante: Jugador
    acusado: Jugador