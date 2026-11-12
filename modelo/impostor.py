

from modelo.rol import Rol
from modelo.palabra_secreta import PalabraSecreta

class impostor(Rol):

    @property
    def nombre(self)-> str:
        return "impostor"

    def conoce_palabra(self)-> bool:
        return False 

    def obetener_palabra_visible(self)-> str:
        return "PALABRA OCULTA"

    def intentar_adivinar(self, intento:str, palabra:PalabraSecreta)-> bool:
        return palabra.coincide_con(intento)
           