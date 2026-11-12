#Jugador
from modelo.rol import Rol
from modelo.enumeraciones import EstadoJugador
from modelo.excepciones import EstadoInvalidoException


class Jugador:

    def __init__(self, identificador: int, nombre: str):
        if identificador < 1 or not nombre.strip():
            raise ValueError(
                "Identificador y nombre válidos son obligatorios"
            )

        self.__id = identificador
        self.__nombre = nombre.strip()
        self.__rol: Rol | None = None
        self.__estado = EstadoJugador.ACTIVO

    @property
    def id(self) -> int:
        return self.__id

    @property
    def nombre(self) -> str:
        return self.__nombre

    @property
    def rol(self) -> Rol | None:
        return self.__rol

    @property
    def estado(self) -> EstadoJugador:
        return self.__estado

    @property
    def activo(self) -> bool:
        return self.__estado == EstadoJugador.ACTIVO

    def asignar_rol(self, rol: Rol) -> None:
        if not isinstance(rol, Rol):
            raise TypeError("El rol debe implementar Rol")

        self.__rol = rol

    def eliminar(self) -> None:
        if not self.activo:
            raise EstadoInvalidoException(
                "El jugador ya está eliminado"
            )

        self.__estado = EstadoJugador.ELIMINADO

    def reiniciar(self) -> None:
        self.__estado = EstadoJugador.ACTIVO
        self.__rol = None