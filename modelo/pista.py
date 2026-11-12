Pista:

from dataclasses import dataclass
from modelo.jugador import Jugador


@dataclass(frozen=True)
class Pista:
    autor: Jugador
    texto: str
    numero_turno: int