from modelo.enumeraciones import FaseJuego
from modelo.excepciones import (
    EstadoInvalidoException,
    VotoInvalidoException
)
from modelo.pista import Pista
from modelo.voto import Voto

class Ronda:

    def __init__(self, numero: int):
        if numero < 1:
            raise ValueError( "Número de ronda inválido" )

        self.__numero = numero
        self.__fase = FaseJuego.PISTAS
        self.__pistas: list[Pista] = []
        self.__votos: list[Voto] = []

    @property
    def numero(self):
        return self.__numero

    @property
    def fase(self):
        return self.__fase

    @property
    def pistas(self):
        return tuple(self.__pistas)

    @property
    def votos(self):
        return tuple(self.__votos)

    def avanzar_fase (self) -> None:
        transiciones = {
            FaseJuego.PISTAS: FaseJuego.DEBATE,
            FaseJuego.DEBATE: FaseJuego.VOTACION,
            FaseJuego.VOTACION: FaseJuego.RESULTADO
        }

        if self.__fase not in transiciones:
            raise EstadoInvalidoException(
                "No se puede avanzar de fase"
            )

        self.__fase = transiciones[self.__fase]

    def registrar_pista(
            self,
            pista: Pista,
            jugadores_activos
    ) -> None:
        if self.__fase != FaseJuego.PISTAS:
            raise EstadoInvalidoException(
                "No estamos en fase de pistas"
            )

        if (
            not pista.autor.activo
            or pista.autor not in jugadores_activos
        ):
            raise EstadoInvalidoException(
                "Jugador no activo en esta partida"
            )

        if any(
            p.autor.id == pista.autor.id
            for p in self.__pistas
        ):
            raise EstadoInvalidoException(
                "El jugador ya dio su pista"
            )
        if pista.numero_turno != len(self.__pistas) + 1:
         raise EstadoInvalidoException(
            "Turno incorrecto"
        )
        self.__pistas.append(pista)

    def registrar_voto(
            self,
            voto: Voto,
            jugadores_activos
    ) -> None:
        if self.__fase != FaseJuego.VOTACION:
            raise EstadoInvalidoException(
                "No estamos en votación"
            )

        if(
            voto.votante not in jugadores_activos 
            or voto.acusado not in jugadores_activos
        ):
            raise VotoInvalidoException(
                "Solo pueden participar jugadores activos"
            )
        
        if(
            not voto.votante.activo
            or not voto.acusado.activo
        ):
            raise VotoInvalidoException(
                "Jugador eliminado"
            )

        if voto.votante.id == voto.acusado.id:
            raise VotoInvalidoException(
                "No se permite votar por sí mismo"
            )

        if any(
            v.votante.id == voto.votante.id
            for v in self.__votos
        ):
            raise VotoInvalidoException(
                "Ya emitió su voto"
            )

        self.__votos.append(voto)