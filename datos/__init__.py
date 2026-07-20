"""Paquete de acceso a datos (capa `datos/`).

Contiene la conexión a MySQL y un repositorio por entidad, cada uno
implementando el contrato `RepositorioBase`. Esta capa ejecuta SQL puro
y no contiene reglas de negocio: solo consulta y persiste datos.
"""

from datos.autores_repo import AutoresRepo
from datos.base import RepositorioBase
from datos.categorias_repo import CategoriasRepo
from datos.ejemplares_repo import EjemplaresRepo
from datos.libros_repo import LibrosRepo
from datos.prestamos_repo import PrestamosRepo
from datos.usuarios_repo import UsuariosRepo

__all__ = [
    "RepositorioBase",
    "AutoresRepo",
    "CategoriasRepo",
    "LibrosRepo",
    "EjemplaresRepo",
    "UsuariosRepo",
    "PrestamosRepo",
]