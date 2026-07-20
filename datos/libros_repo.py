"""Repositorio de datos para la entidad Libro (tabla `libros`)."""

from typing import List, Optional

from datos.base import RepositorioBase
from datos.conexion import obtener_cursor
from modelos.libro import Libro


class LibrosRepo(RepositorioBase[Libro]):
    """Acceso a datos (SQL puro) para la tabla `libros`."""

    _COLUMNAS = "id, titulo, autor_id, categoria_id, isbn, descripcion"

    def obtener_por_id(self, id_: int) -> Optional[Libro]:
        with obtener_cursor() as cursor:
            cursor.execute(
                f"SELECT {self._COLUMNAS} FROM libros WHERE id = %s", (id_,)
            )
            fila = cursor.fetchone()
        return self._fila_a_libro(fila) if fila else None

    def crear(self, entidad: Libro) -> Libro:
        with obtener_cursor() as cursor:
            cursor.execute(
                """INSERT INTO libros (titulo, autor_id, categoria_id, isbn, descripcion)
                   VALUES (%s, %s, %s, %s, %s)""",
                (
                    entidad.titulo,
                    entidad.autor_id,
                    entidad.categoria_id,
                    entidad.isbn,
                    entidad.descripcion,
                ),
            )
            entidad.id = cursor.lastrowid
        return entidad

    def actualizar(self, entidad: Libro) -> None:
        if entidad.id is None:
            raise ValueError("No se puede actualizar un libro sin id")
        with obtener_cursor() as cursor:
            cursor.execute(
                """UPDATE libros
                   SET titulo = %s, autor_id = %s, categoria_id = %s,
                       isbn = %s, descripcion = %s
                   WHERE id = %s""",
                (
                    entidad.titulo,
                    entidad.autor_id,
                    entidad.categoria_id,
                    entidad.isbn,
                    entidad.descripcion,
                    entidad.id,
                ),
            )

    def eliminar(self, id_: int) -> None:
        with obtener_cursor() as cursor:
            cursor.execute("DELETE FROM libros WHERE id = %s", (id_,))

    def listar_todos(self) -> List[Libro]:
        with obtener_cursor() as cursor:
            cursor.execute(f"SELECT {self._COLUMNAS} FROM libros ORDER BY titulo")
            filas = cursor.fetchall()
        return [self._fila_a_libro(fila) for fila in filas]

    def buscar(
        self,
        titulo: Optional[str] = None,
        autor_id: Optional[int] = None,
        categoria_id: Optional[int] = None,
    ) -> List[Libro]:
        """Busca libros combinando filtros opcionales.

        Cualquier filtro que se omita (None) simplemente no se aplica.
        Útil para el caso de uso "el lector busca libros por título,
        autor o categoría".
        """
        condiciones: List[str] = []
        parametros: List[object] = []

        if titulo:
            condiciones.append("titulo LIKE %s")
            parametros.append(f"%{titulo}%")
        if autor_id is not None:
            condiciones.append("autor_id = %s")
            parametros.append(autor_id)
        if categoria_id is not None:
            condiciones.append("categoria_id = %s")
            parametros.append(categoria_id)

        query = f"SELECT {self._COLUMNAS} FROM libros"
        if condiciones:
            query += " WHERE " + " AND ".join(condiciones)
        query += " ORDER BY titulo"

        with obtener_cursor() as cursor:
            cursor.execute(query, tuple(parametros))
            filas = cursor.fetchall()
        return [self._fila_a_libro(fila) for fila in filas]

    @staticmethod
    def _fila_a_libro(fila: dict) -> Libro:
        """Convierte una fila del cursor (dict) en un objeto Libro."""
        return Libro(
            id=fila["id"],
            titulo=fila["titulo"],
            autor_id=fila["autor_id"],
            categoria_id=fila["categoria_id"],
            isbn=fila["isbn"],
            descripcion=fila.get("descripcion"),
        )