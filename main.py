# from pathlib import Path

# from controlador.controlador_partida import ControladorPartida
# from vista.vista_consola import VistaConsola

# from servicios.asignador_roles import AsignadorRolesAleatorio
# from servicios.validador_pistas import ValidadorPistaCompuesto
# from servicios.contador_votos import ContadorVotosMayoria
# from servicios.repositorio_palabras import RepositorioPalabrasArchivo

# def main():
#     ruta = (
#         Path(_file_).resolve().parent
#         /"datos"
#         /"palabras.json"
#     )

#     vista = VistaConsola()
#     vista.titulo("Bienvenidos a el impostor")

#     marcador = {
#         "Civiles": 0,
#         "Impostor": 0
#     }

#     try:
#         while True:
#             controlador = ControladorPartida(
#                 vista,
#                 AsignadorRolesAleatorio(),
#                 ValidadorPistaCompuesto(),
#                 ContadorVotosMayoria(),
#                 RepositorioPalabrasArchivo(ruta)
#             )

#             resultado = controlador.jugar()

#             marcador[resultado.ganador.name] += 1

#             vista.titulo