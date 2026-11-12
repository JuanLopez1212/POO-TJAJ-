import json
import random
from pathlib import Path

from modelo.palabra_secreta import PalabraSecreta
from servicios.interfaces import IRepositorioPalabras


class RepositorioPalabrasArchivo(IRepositorioPalabras):

    def __init__ ( 
            self,
            ruta: str | Path,
            rng: random.Random | None = None
            ):
                self._ruta = Path(ruta)
                self._rng = rng or random.Random()

    def obtener_palabra_aleatoria(self,categoria: str | None = None) -> PalabraSecreta:

        with self._ruta.open(encoding="utf-8") as archivo:
            datos = json.load(archivo)

        candidatas = [
            PalabraSecreta(
                item["texto"],
                item["categoria"]
            )
            for item in datos
        ]

        if categoria is not None:
            candidatas = [
                p for p in candidatas
                if p.categoria.casefold()
                == categoria.casefold()
            ]

        if not candidatas:
            raise ValueError("No hay palabras para la categoría indicada")

        return self._rng.choice(candidatas)