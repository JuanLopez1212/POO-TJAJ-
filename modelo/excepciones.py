class JuegoError(Exception):
    """Error de regla de negocio."""


class PistaInvalidaException(JuegoError):
    pass


class VotoInvalidoException(JuegoError):
    pass


class EstadoInvalidoException(JuegoError):
    pass