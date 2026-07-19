"""Paquete de modelos: clases simples que representan las entidades del sistema.
 
Estas clases definen únicamente la "forma" del dato (atributos y
validaciones básicas de formato). No contienen lógica de negocio ni
acceso a base de datos; eso corresponde a las capas `logica/` y `datos/`
respectivamente.
"""

from modelos.autor import Autor
from modelos.categoria import Categoria
from modelos.ejemplar import Ejemplar
from modelos.enums import EstadoEjemplar, EstadoPrestamo, RolUsuario
from modelos.libro import Libro
from modelos.prestamo import Prestamo
from modelos.usuario import Usuario
 
__all__ = [
    "Autor",
    "Categoria",
    "Libro",
    "Ejemplar",
    "Usuario",
    "Prestamo",
    "RolUsuario",
    "EstadoEjemplar",
    "EstadoPrestamo",
]
 