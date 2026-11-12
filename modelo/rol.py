from abc import ABC, abstractmethod


class Rol(ABC):

    @property
    @abstractmethod
    def nombre(self) -> str:
        ...

    @abstractmethod
    def conoce_palabra(self) -> bool:
        ...

    @abstractmethod
    def obtener_palabra_visible(self) -> str:
        ...