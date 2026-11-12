from modelo.rol import Rol
from modelo.palabra_secreta import PalabraSecreta


class Civil(Rol):

    def _init_(self, palabra: PalabraSecreta):
        self.__palabra = palabra

    @property
    def nombre(self) -> str:
        return "Civil"

    def conoce_palabra(self) -> bool:
        return True

    def obtener_palabra_visible(self) -> str:
        return self.__palabra.texto