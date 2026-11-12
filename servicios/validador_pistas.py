import re

from modelo.excepciones import PistaInvalidaException
from modelo.palabra_secreta import (
    PalabraSecreta,
    normalizar
)

from servicios.interfaces import IValidadorPista


class ValidadorLongitud(IValidadorPista):

    def validar(
        self,
        texto: str,
        palabra: PalabraSecreta,
        longitud_maxima: int
    ) -> None:

        if (
            longitud_maxima < 1
            or not texto.strip()
            or len(texto.strip()) > longitud_maxima
        ):
            raise PistaInvalidaException(
                "Pista vacía o demasiado larga"
            )


class ValidadorPalabraProhibida(IValidadorPista):

    def validar(
        self,
        texto: str,
        palabra: PalabraSecreta,
        longitud_maxima: int
    ) -> None:

        secreto = normalizar(palabra.texto)
        pista = normalizar(texto)

        if re.search(
            r"(?<!\w)" + re.escape(secreto) + r"(?!\w)",
            pista
        ):
            raise PistaInvalidaException(
                "La pista contiene la palabra secreta"
            )


class ValidadorPistaCompuesto(IValidadorPista):

    def __init__(
        self,
        validadores: list[IValidadorPista] | None = None
    ):
        self._validadores = (
            validadores
            if validadores is not None
            else [
                ValidadorLongitud(),
                ValidadorPalabraProhibida()
            ]
        )

    def validar(
        self,
        texto: str,
        palabra: PalabraSecreta,
        longitud_maxima: int
    ) -> None:

        for validador in self._validadores:
            validador.validar(
                texto,
                palabra,
                longitud_maxima
            )