"""Enumeraciones compartidas por los modelos del sistema.
 
Se centralizan aquí para que ninguna clase dependa de strings sueltos
(por ejemplo "activo" vs "Activo" vs "ACTIVO"), lo cual es una fuente
común de errores en proyectos que representan estados como texto libre.
"""

from enum import Enum

class RolUsuario(str, Enum):
    """Rol de un usuario del sistema"""

    ADMIN = "admin"
    LECTOR = "lector"

class EstadoEjemplar(str, Enum):
    """Estado físico/operativo de un ejemplar (copia) de un libro"""

    DISPONIBLE = "disponible"
    PRESTADO = "prestado"

class EstadoPrestamo(str, Enum):
    """Estado del ciclo de vida de un préstamo"""

    ACTIVO = "activo"
    DEVUELTO = "devuelto"
    ATRARSADO = "atrasado"