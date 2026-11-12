from enum import Enum, auto


class FaseJuego(Enum):
    REGISTRO = auto()
    ASIGNACION = auto()
    PISTAS = auto()
    DEBATE = auto()
    VOTACION = auto()
    RESULTADO = auto()
    FINALIZADA = auto()


class EstadoJugador(Enum):
    ACTIVO = auto()
    ELIMINADO = auto()


class Ganador(Enum):
    CIVILES = auto()
    IMPOSTOR = auto()