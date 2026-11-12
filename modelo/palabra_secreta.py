from dataclasses import dataclass
import unicodedata


def normalizar(texto: str) -> str:
    texto = unicodedata.normalize(
        "NFKD",
        texto.casefold()
    )

    return "".join(
        c for c in texto
        if not unicodedata.combining(c)
    ).strip()


@dataclass(frozen=True)
class PalabraSecreta:
    texto: str
    categoria: str

    def _post_init_(self):
        if not self.texto.strip() or not self.categoria.strip():
            raise ValueError(
                "La palabra y su categoría son obligatorias"
            )

    def coincide_con(self, texto: str) -> bool:
        return normalizar(self.texto) == normalizar(texto)