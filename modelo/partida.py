from dataclasses import dataclass
from typing import Sequence

from modelo.jugador import Jugador
from modelo.pista import Pista
from modelo.voto import Voto
from modelo.ronda import Ronda
from modelo.impostor import Impostor
from modelo.enumeraciones import FaseJuego, Ganador
from modelo.excepciones import EstadoInvalidoException
from modelo.palabra_secreta import PalabraSecreta

from servicios.interfaces import (
    IAsignadorRoles,
    IValidadorPista,
    IContadorVotos,
    IRepositorioPalabras
)


@dataclass(frozen=True)
class ConfiguracionPartida:
    max_rondas: int = 5
    tiempo_debate: int = 60
    categoria: str | None = None
    ultima_oportunidad: bool = True
    longitud_maxima_pista: int = 40

    def __post_init__(self):
        if (
            self.max_rondas < 1
            or self.tiempo_debate < 0
            or self.longitud_maxima_pista < 1
        ):
            raise ValueError("Configuración inválida")


@dataclass(frozen=True)
class ResultadoPartida:
    ganador: Ganador
    impostor_descubierto: bool
    palabra_adivinada: bool = False


class Partida:

    def __init__(
        self,
        jugadores: Sequence[Jugador],
        configuracion: ConfiguracionPartida,
        asignador: IAsignadorRoles,
        validador: IValidadorPista,
        contador: IContadorVotos,
        repositorio: IRepositorioPalabras
    ):

        if not 3 <= len(jugadores) <= 10:
            raise ValueError(
                "Se requieren entre 3 y 10 jugadores"
            )

        if len({
            j.nombre.casefold() for j in jugadores
        }) != len(jugadores):
            raise ValueError(
                "Los nombres deben ser únicos"
            )

        if len({
            j.id for j in jugadores
        }) != len(jugadores):
            raise ValueError(
                "Los IDs deben ser únicos"
            )

        self.__jugadores = tuple(jugadores)
        self.__configuracion = configuracion

        self.__asignador = asignador
        self.__validador = validador
        self.__contador = contador
        self.__repositorio = repositorio

        self.__palabra: PalabraSecreta | None = None
        self.__impostor: Jugador | None = None

        self.__rondas: list[Ronda] = []
        self.__resultado: ResultadoPartida | None = None

    @property
    def jugadores(self):
        return self.__jugadores

    @property
    def rondas(self):
        return tuple(self.__rondas)

    @property
    def ronda_actual(self) -> Ronda:
        if not self.__rondas:
            raise EstadoInvalidoException(
                "Partida sin iniciar"
            )

        return self.__rondas[-1]

    @property
    def resultado(self):
        return self.__resultado

    @property
    def finalizada(self):
        return self.__resultado is not None

    @property
    def activos(self):
        return tuple(
            j for j in self.__jugadores
            if j.activo
        )

    def iniciar(self) -> None:

        if self.__rondas:
            raise EstadoInvalidoException(
                "La partida ya inició"
            )

        self.__palabra = (
            self.__repositorio.obtener_palabra_aleatoria(
                self.__configuracion.categoria
            )
        )

        self.__impostor = (
            self.__asignador.asignar_roles(
                self.__jugadores,
                self.__palabra
            )
        )

        self.__rondas.append(Ronda(1))

    def informacion_privada(
        self,
        jugador: Jugador
    ) -> tuple[str, str]:

        if (
            jugador not in self.__jugadores
            or not self.__rondas
            or jugador.rol is None
        ):
            raise EstadoInvalidoException(
                "Jugador no válido"
            )

        return (
            jugador.rol.nombre,
            jugador.rol.obtener_palabra_visible()
        )

    def registrar_pista(
        self,
        autor: Jugador,
        texto: str
    ) -> None:

        if self.finalizada:
            raise EstadoInvalidoException(
                "Partida finalizada"
            )

        self.__validador.validar(
            texto,
            self.__palabra,
            self.__configuracion.longitud_maxima_pista
        )

        self.ronda_actual.registrar_pista(
            Pista(
                autor,
                texto.strip(),
                len(self.ronda_actual.pistas) + 1
            ),
            self.activos
        )

    def iniciar_debate(self):

        if len(self.ronda_actual.pistas) != len(self.activos):
            raise EstadoInvalidoException(
                "Faltan pistas"
            )

        self.ronda_actual.avanzar_fase()

    def iniciar_votacion(self):
        self.ronda_actual.avanzar_fase()

    def registrar_voto(
        self,
        votante: Jugador,
        acusado: Jugador
    ):

        if self.finalizada:
            raise EstadoInvalidoException(
                "Partida finalizada"
            )

        self.ronda_actual.registrar_voto(
            Voto(votante, acusado),
            self.activos
        )

    def resolver_votacion(self) -> list[Jugador]:

        if self.ronda_actual.fase != FaseJuego.VOTACION:
            raise EstadoInvalidoException(
                "No estamos en votación"
            )

        candidatos = self.__contador.contar_votos(
            self.ronda_actual.votos,
            self.activos
        )

        if len(candidatos) > 1:
            # El empate queda pendiente de desempate.
            return candidatos

        acusado = candidatos[0]

        self.ronda_actual.avanzar_fase()

        if acusado is self.__impostor:

            if not self.__configuracion.ultima_oportunidad:
                self.__resultado = ResultadoPartida(
                    Ganador.CIVILES,
                    True
                )

            return candidatos

        acusado.eliminar()

        if (
            len(self.__rondas) >= self.__configuracion.max_rondas
            or len(self.activos) <= 2
        ):
            self.__resultado = ResultadoPartida(
                Ganador.IMPOSTOR,
                False
            )

        else:
            self.__rondas.append(
                Ronda(len(self.__rondas) + 1)
            )

        return candidatos

    def adivinar_palabra(
        self,
        intento: str
    ) -> ResultadoPartida:

        if (
            self.finalizada
            or self.ronda_actual.fase != FaseJuego.RESULTADO
            or not self.__configuracion.ultima_oportunidad
        ):
            raise EstadoInvalidoException(
                "Última oportunidad no disponible"
            )

        candidatos = self.__contador.contar_votos(
            self.ronda_actual.votos,
            self.activos
        )

        if (
            len(candidatos) != 1
            or candidatos[0] is not self.__impostor
        ):
            raise EstadoInvalidoException(
                "El impostor no fue descubierto"
            )

        acierto = self.__impostor.rol.intentar_adivinar(
            intento,
            self.__palabra
        )

        self.__resultado = ResultadoPartida(
            Ganador.IMPOSTOR if acierto else Ganador.CIVILES,
            True,
            acierto
        )

        return self.__resultado