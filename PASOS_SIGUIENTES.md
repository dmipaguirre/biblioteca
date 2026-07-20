# Próximos pasos del proyecto

Este documento convierte los requerimientos de `DOC.docx` en un plan de
implementación para completar el MVP del sistema de gestión de biblioteca.
Parte del estado real del repositorio al 20 de julio de 2026.

## 1. Estado actual

### Completado

- Modelos de dominio: `Autor`, `Categoria`, `Libro`, `Ejemplar`, `Usuario` y
  `Prestamo`.
- Enumeraciones para roles y estados.
- Validaciones básicas en los modelos.
- Contrato abstracto `RepositorioBase`.
- Repositorios CRUD para las seis entidades.
- Búsqueda de libros por título, autor y categoría.
- Consultas de disponibilidad, historial y préstamos activos.
- Conexión a MySQL mediante variables de entorno.
- Transacciones por operación de repositorio con `commit` y `rollback`.

### Pendiente

- Script de creación y datos iniciales de MySQL.
- Configuración centralizada de las reglas de negocio.
- Servicios de usuarios, libros y préstamos.
- Registro e inicio de sesión.
- Hash seguro de contraseñas.
- Interfaz gráfica con Tkinter.
- Logging y mensajes de error para el usuario.
- Pruebas unitarias y de integración.
- Integración de las capas desde `main.py`.

## 2. Prioridades inmediatas

Antes de añadir nuevas funcionalidades, se deben corregir estas diferencias
entre la especificación y el código actual:

1. Añadir `.env` a `.gitignore` para evitar publicar credenciales.
2. Corregir `EstadoPrestamo.ATRARSADO` a `EstadoPrestamo.ATRASADO` y actualizar
   sus referencias.
3. Declarar en `pyproject.toml` las dependencias reales: `pymysql`,
   `python-dotenv`, `pytest` y una biblioteca de hash de contraseñas.
4. Sustituir la descripción provisional de `pyproject.toml` por la descripción
   del proyecto.
5. Crear `config/configuracion.py` con constantes como
   `MAX_PRESTAMOS_ACTIVOS = 4` y `DURACION_PRESTAMO_DIAS = 15`.
6. Definir cómo se coordinarán las operaciones que afectan a varias tablas.
   Crear un préstamo y marcar el ejemplar como prestado debe ser una sola
   transacción; lo mismo se aplica a una devolución.

## 3. Plan de implementación

### Fase 1 — Preparar la infraestructura

**Objetivo:** conseguir un entorno reproducible y una base de datos válida.

- Completar `pyproject.toml` y documentar la instalación.
- Crear `.env.example` sin secretos.
- Crear `config/configuracion.py`.
- Añadir `sql/schema.sql` con las tablas, claves foráneas e índices.
- Añadir `sql/seed.sql` con categorías de ejemplo y el administrador inicial,
  sin incluir una contraseña en texto plano.
- Establecer restricciones únicas para `usuarios.correo`, `libros.isbn` y
  `ejemplares.codigo`.
- Definir los valores permitidos para roles y estados de forma consistente con
  las enumeraciones de Python.
- Añadir una prueba sencilla de conexión a MySQL.

**Criterio de finalización:** una persona puede clonar el proyecto, configurar
su `.env`, instalar las dependencias y crear la base de datos siguiendo solo la
documentación.

### Fase 2 — Implementar la lógica de negocio

**Objetivo:** mantener las reglas fuera de Tkinter y de los repositorios.

Crear, como mínimo:

- `logica/servicio_usuarios.py`
  - registrar lectores;
  - normalizar y validar el correo;
  - generar el hash de la contraseña;
  - autenticar por correo y contraseña;
  - impedir el autoregistro como administrador.
- `logica/servicio_libros.py`
  - buscar el catálogo;
  - crear, editar y eliminar libros;
  - administrar autores, categorías y ejemplares;
  - impedir eliminaciones que rompan relaciones existentes.
- `logica/servicio_prestamos.py`
  - comprobar que el lector tenga menos de cuatro préstamos activos;
  - seleccionar un ejemplar disponible;
  - calcular la fecha límite como fecha de préstamo más 15 días;
  - crear el préstamo y marcar el ejemplar como prestado atómicamente;
  - devolver un préstamo y liberar el ejemplar atómicamente;
  - impedir devolver dos veces el mismo préstamo;
  - identificar préstamos atrasados.

Para préstamo y devolución conviene introducir una unidad de trabajo o permitir
que varios repositorios compartan una misma conexión. Las operaciones actuales
abren una transacción independiente por llamada y no garantizan consistencia si
la segunda actualización falla. Al solicitar un ejemplar también debe
controlarse la concurrencia, por ejemplo bloqueando la fila seleccionada dentro
de la transacción.

**Criterio de finalización:** todas las reglas descritas en `DOC.docx` pueden
ejecutarse desde servicios de Python sin depender de la interfaz gráfica.

### Fase 3 — Añadir pruebas automatizadas

**Objetivo:** validar la lógica antes de construir las pantallas.

- Configurar `pytest`.
- Crear repositorios simulados o mocks para las pruebas unitarias.
- Probar los modelos y sus validaciones.
- Probar el registro y la autenticación.
- Probar que el quinto préstamo sea rechazado.
- Probar el rechazo cuando no haya ejemplares disponibles.
- Probar el cálculo exacto de la fecha límite a 15 días.
- Probar la creación correcta del préstamo y el cambio de estado del ejemplar.
- Probar la devolución y el intento de devolución duplicada.
- Probar la detección de préstamos atrasados.
- Añadir pruebas de integración separadas para repositorios y MySQL.

**Criterio de finalización:** las reglas principales tienen pruebas unitarias y
la capa de datos tiene al menos una prueba CRUD por repositorio.

### Fase 4 — Crear la base de la interfaz Tkinter

**Objetivo:** implementar la navegación por frames definida en el documento.

- Crear `interfaz/ventana_principal.py`.
- Crear un controlador de navegación que intercambie frames en un área central.
- Mantener la sesión del usuario autenticado y su rol.
- Crear componentes compartidos para formularios, tablas, validaciones y
  diálogos.
- Implementar los frames comunes de login y registro.
- Mostrar menús diferentes para lector y administrador.
- Hacer que `main.py` cargue configuración, logging y la ventana principal.

**Criterio de finalización:** un lector y el administrador pueden iniciar
sesión, cerrar sesión y acceder únicamente a las opciones de su rol.

### Fase 5 — Implementar la experiencia del lector

- Catálogo con filtros por título, autor y categoría.
- Detalle del libro y cantidad de ejemplares disponibles.
- Acción para solicitar un préstamo y mostrar el resultado de la validación.
- Vista “Mis préstamos” con activos e historial.
- Acción de devolución en los préstamos activos.
- Mensajes claros para falta de disponibilidad, límite alcanzado y errores.

**Criterio de finalización:** el flujo buscar → solicitar → consultar → devolver
puede completarse íntegramente desde la interfaz.

### Fase 6 — Implementar la experiencia del administrador

- Dashboard básico de navegación, sin estadísticas fuera del alcance del MVP.
- CRUD de autores y categorías.
- CRUD de libros.
- Alta y baja de ejemplares.
- Listado de préstamos activos y atrasados con usuario, libro, ejemplar y fecha
  límite.
- Confirmaciones antes de eliminar información.

**Criterio de finalización:** el administrador puede mantener todo el catálogo
y consultar el estado operativo de los préstamos.

### Fase 7 — Logging, errores y cierre del MVP

- Configurar `logging` con salida a `logs/biblioteca.log` y rotación de archivo.
- Registrar inicios de sesión fallidos, préstamos, devoluciones, rechazos y
  errores de base de datos sin guardar contraseñas ni hashes.
- Traducir excepciones técnicas a mensajes comprensibles mediante
  `tkinter.messagebox`.
- Validar los formularios y desactivar acciones inválidas.
- Ejecutar una prueba manual completa con ambos roles.
- Actualizar README, esquema y decisiones arquitectónicas.

**Criterio de finalización:** el MVP funciona de extremo a extremo, los fallos
se manejan sin cerrar inesperadamente la aplicación y los eventos relevantes
quedan registrados.

## 4. Orden recomendado de entregas

1. **Base ejecutable:** configuración, dependencias, esquema SQL y conexión.
2. **Núcleo probado:** servicios de usuarios y préstamos con pruebas unitarias.
3. **Acceso inicial:** login, registro, sesión y navegación por rol.
4. **Flujo del lector:** catálogo, préstamo, historial y devolución.
5. **Gestión administrativa:** mantenimiento del catálogo y control de
   préstamos.
6. **Estabilización:** integración, logging, manejo de errores y documentación.

Cada entrega debe ser pequeña, ejecutable y acompañada de sus pruebas. No se
recomienda construir todas las pantallas antes de validar los servicios, porque
eso trasladaría reglas de negocio a la interfaz y dificultaría las pruebas.

## 5. Definición de terminado del MVP

El MVP se considera completo cuando se cumplen todas estas condiciones:

- El administrador fijo y los lectores pueden autenticarse con contraseñas
  almacenadas mediante hash seguro.
- Un lector puede registrarse, buscar libros y consultar disponibilidad.
- Un lector puede tener como máximo cuatro préstamos activos.
- Cada préstamo vence exactamente 15 días después de su creación.
- Un ejemplar no puede estar en dos préstamos activos simultáneamente.
- Préstamo y devolución actualizan préstamo y ejemplar en una sola transacción.
- El lector puede consultar su historial y devolver ejemplares.
- El administrador puede gestionar catálogo y ejemplares.
- El administrador puede consultar préstamos activos y atrasados.
- La interfaz no ejecuta SQL ni contiene reglas de negocio.
- Las consultas SQL usan parámetros.
- Los errores se registran y se muestran al usuario de forma comprensible.
- Las reglas críticas cuentan con pruebas automatizadas.
- No se incluyen credenciales ni contraseñas en el repositorio o en los logs.

## 6. Funcionalidades que permanecen fuera del MVP

Según las decisiones de `DOC.docx`, no se deben incluir todavía:

- recuperación de contraseña;
- multas por retrasos;
- reportes o estadísticas;
- bloqueo administrativo de usuarios;
- múltiples administradores;
- autoregistro de administradores.

Estas funcionalidades pueden planificarse después de cerrar y probar el MVP.
