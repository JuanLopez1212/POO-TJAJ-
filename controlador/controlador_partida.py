from modelo.jugador import Jugador
from modelo.partida import Partida, ConfiguracionPartida
from modelo.impostor import Impostor
from modelo.excepciones import (
    PistaInvalidaException,
    VotoInvalidoException
)

from servicios.interfaces import (
    IAsignadorRoles,
    IValidadorPista,
    IContadorVotos,
    IRepositorioPalabras
)


class ControladorPartida:

    def __init__(
        self,
        vista,
        asignador: IAsignadorRoles,
        validador: IValidadorPista,
        contador: IContadorVotos,
        repositorio: IRepositorioPalabras
    ):
        self._vista = vista
        self._asignador = asignador
        self._validador = validador
        self._contador = contador
        self._repositorio = repositorio

    def _registrar_jugadores(self):
        vista = self._vista
        vista.titulo("EL IMPOSTOR - REGISTRO")

        cantidad = vista.pedir_entero(
            "Número de jugadores (3-10): ", 3, 10
        )

        jugadores = []
        nombres = set()

        for numero in range(1, cantidad + 1):
            while True:
                nombre = vista.pedir_texto(
                    f"Nombre del jugador {numero}: "
                )

                if not nombre or nombre.casefold() in nombres:
                    vista.mensaje(
                        "Escribe un nombre único y no vacío."
                    )
                    continue

                nombres.add(nombre.casefold())
                jugadores.append(Jugador(numero, nombre))
                break

        return jugadores

    def _configurar(self):
        vista = self._vista
        vista.titulo("CONFIGURACIÓN")

        categoria = vista.pedir_texto(
            "Categoría (lugares, animales, objetos; "
            "ENTER = cualquiera): "
        ) or None

        rondas = vista.pedir_entero(
            "Máximo de rondas (1-20): ", 1, 20
        )

        segundos = vista.pedir_entero(
            "Debate en segundos (0-180): ", 0, 180
        )

        ultima = vista.pedir_si_no(
            "¿Última oportunidad del impostor? (S/n): "
        )

        return ConfiguracionPartida(
            max_rondas=rondas,
            tiempo_debate=segundos,
            categoria=categoria,
            ultima_oportunidad=ultima,
            longitud_maxima_pista=40
        )

    def jugar(self):
        vista = self._vista
        jugadores = self._registrar_jugadores()

        while True:
            config = self._configurar()

            partida = Partida(
                jugadores,
                config,
                self._asignador,
                self._validador,
                self._contador,
                self._repositorio
            )

            try:
                partida.iniciar()
                break
            except (ValueError, FileNotFoundError) as error:
                vista.mensaje(
                    f"No se puede iniciar: {error}"
                )
                vista.mensaje(
                    "Vuelve a configurar la partida."
                )

        # Mostrar información individual.
        for jugador in partida.jugadores:
            rol, palabra = partida.informacion_privada(
                jugador
            )

            vista.mostrar_rol_privado(
                jugador.nombre, rol, palabra
            )

        # Ejecutar rondas hasta finalizar.
        while not partida.finalizada:
            self._jugar_ronda(partida, config)

        self._mostrar_final(partida)
        return partida.resultado

    def _jugar_ronda(self, partida, config):
        vista = self._vista
        numero = partida.ronda_actual.numero

        vista.titulo(f"RONDA {numero} - PISTAS")

        # Registrar pistas.
        for jugador in partida.activos:
            while True:
                texto = vista.pedir_texto(
                    f"{jugador.nombre}, escribe tu pista: "
                )

                try:
                    partida.registrar_pista(
                        jugador, texto
                    )
                    break
                except PistaInvalidaException as error:
                    vista.mensaje(
                        f"Pista rechazada: {error}"
                    )

        # Debate.
        partida.iniciar_debate()
        vista.mostrar_pistas(
            partida.ronda_actual.pistas
        )
        vista.esperar_debate(
            config.tiempo_debate
        )
        partida.iniciar_votacion()

        # Votación y posible desempate.
        while (
            not partida.finalizada
            and partida.ronda_actual.numero == numero
        ):
            candidatos = (
                partida.ronda_actual.candidatos_desempate
                or partida.activos
            )

            vista.titulo("VOTACIÓN")

            for votante in partida.activos:
                while True:
                    acusado = vista.pedir_voto(
                        votante, candidatos
                    )

                    try:
                        partida.registrar_voto(
                            votante, acusado
                        )
                        break
                    except VotoInvalidoException as error:
                        vista.mensaje(
                            f"Voto rechazado: {error}"
                        )

                vista.limpiar()

            mas_votados = partida.resolver_votacion()

            if len(mas_votados) > 1:
                nombres = ", ".join(
                    j.nombre for j in mas_votados
                )
                vista.mensaje(
                    f"Empate entre: {nombres}."
                )

                if (
                    partida.ronda_actual.numero == numero
                    and not partida.finalizada
                ):
                    vista.mensaje(
                        "Se repetirá la votación "
                        "entre los empatados."
                    )
                else:
                    vista.mensaje(
                        "Persiste el empate: "
                        "ronda sin eliminación."
                    )

                continue

            acusado = mas_votados[0]

            if isinstance(acusado.rol, Impostor):
                vista.mensaje(
                    f"¡{acusado.nombre} era el impostor!"
                )

                if not partida.finalizada:
                    intento = vista.pedir_texto(
                        "Impostor, ¿cuál era la palabra?: "
                    )
                    partida.adivinar_palabra(intento)

            else:
                vista.mensaje(
                    f"{acusado.nombre} era civil "
                    "y queda eliminado."
                )

                if not partida.finalizada:
                    vista.mensaje(
                        "Comienza otra ronda."
                    )

            vista.pausar()

    def _mostrar_final(self, partida):
        vista = self._vista
        vista.titulo("RESULTADO FINAL")

        vista.mensaje(
            f"GANARON: {partida.resultado.ganador.name}"
        )

        palabra, impostor = partida.informacion_final()

        vista.mensaje(
            f"La palabra secreta era: {palabra}"
        )
        vista.mensaje(
            f"El impostor era: {impostor}"
        )

        vista.mensaje("\nROLES DE LOS JUGADORES:")

        for jugador in partida.jugadores:
            vista.mensaje(
                f"- {jugador.nombre}: "
                f"{jugador.rol.nombre} "
                f"({jugador.estado.name})"
            )