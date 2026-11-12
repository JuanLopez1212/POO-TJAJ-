from abc import ABC, abstractmethod
from typing import Sequence

from modelo.jugador import Jugador
from modelo.palabra_secreta import PalabraSecreta
from modelo.voto import Voto


class IAsignadorRoles(ABC):

    @abstractmethod
    def asignar_roles(
        self,
        jugadores: Sequence[Jugador],
        palabra: PalabraSecreta
    ) -> Jugador:
        pass


class IValidadorPista(ABC):

    @abstractmethod
    def validar(
        self,
        texto: str,
        palabra: PalabraSecreta,
        longitud_maxima: int
    ) -> None:
        pass


class IContadorVotos(ABC):

    @abstractmethod
    def contar_votos(
        self,
        votos: Sequence[Voto],
        jugadores: Sequence[Jugador]
    ) -> list[Jugador]:
        pass


class IRepositorioPalabras(ABC):

    @abstractmethod
    def obtener_palabra_aleatoria(
        self,
        categoria: str | None = None
    ) -> PalabraSecreta:
        pass