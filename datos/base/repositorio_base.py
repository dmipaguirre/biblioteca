"""Contrato base para todos los repositorios de datos.

Esta es la "interfaz" de POO que aplicamos como Repository Pattern:
cualquier repositorio concreto (AutoresRepo, LibrosRepo, etc.) debe
heredar de `RepositorioBase` e implementar sus cinco métodos. Si a un
repositorio le falta implementar alguno, Python impide instanciarlo
(TypeError), lo cual fuerza la consistencia entre todos los repos.
"""

from abc import ABC, abstractmethod
from typing import Generic, List, Optional, TypeVar

T = TypeVar("T")


class RepositorioBase(ABC, Generic[T]):
    """Operaciones CRUD mínimas que debe exponer todo repositorio.

    `T` es el tipo de modelo que maneja el repositorio (por ejemplo,
    `RepositorioBase[Autor]` para un repositorio de autores).
    """

    @abstractmethod
    def obtener_por_id(self, id_: int) -> Optional[T]:
        """Devuelve la entidad con ese id, o None si no existe."""
        raise NotImplementedError

    @abstractmethod
    def crear(self, entidad: T) -> T:
        """Inserta la entidad en la base de datos y devuelve la misma
        entidad ya con su `id` asignado."""
        raise NotImplementedError

    @abstractmethod
    def actualizar(self, entidad: T) -> None:
        """Actualiza en base de datos la entidad indicada (por su id)."""
        raise NotImplementedError

    @abstractmethod
    def eliminar(self, id_: int) -> None:
        """Elimina de la base de datos la entidad con ese id."""
        raise NotImplementedError

    @abstractmethod
    def listar_todos(self) -> List[T]:
        """Devuelve todas las entidades almacenadas."""
        raise NotImplementedError