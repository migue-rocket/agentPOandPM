# Ejemplos de Requisitos de Negocio

## Ejemplo 1: Sistema de Autenticación Básico

```
Los usuarios deben poder registrarse con correo electrónico y contraseña.
El sistema debe validar el formato del correo y la fortaleza de la contraseña (mínimo 8 caracteres, una mayúscula, un número).
Los usuarios deben poder iniciar sesión con sus credenciales.
Se debe enviar un correo de confirmación después del registro.
Los usuarios deben poder recuperar su contraseña mediante un enlace enviado por correo.
El sistema debe soportar diferentes roles: admin y usuario estándar.
Los admins pueden ver y gestionar todos los usuarios.
```

**Capacidad sugerida:** 9 story points por sprint

---

## Ejemplo 2: E-commerce Simple

```
Los usuarios deben poder ver un catálogo de productos con imagen, nombre, descripción y precio.
Los productos deben poder filtrarse por categoría y ordenarse por precio.
Los usuarios deben poder buscar productos por nombre o descripción.
Los usuarios deben poder agregar productos a un carrito de compras.
El carrito debe mostrar el total y permitir modificar cantidades o eliminar productos.
Los usuarios deben poder procesar el pago ingresando datos de tarjeta de crédito.
Después de un pago exitoso, se debe enviar un correo de confirmación con el detalle del pedido.
Los usuarios deben poder ver el historial de sus pedidos.
Los administradores deben poder crear, editar y eliminar productos.
```

**Capacidad sugerida:** 12 story points por sprint

---

## Ejemplo 3: Sistema de Gestión de Tareas

```
Los usuarios deben poder crear tareas con título, descripción, fecha límite y prioridad.
Las tareas deben poder organizarse en proyectos.
Los usuarios deben poder asignar tareas a otros miembros del equipo.
El sistema debe mostrar un dashboard con tareas pendientes, en progreso y completadas.
Los usuarios deben recibir notificaciones cuando se les asigne una tarea.
Las tareas deben poder tener comentarios y archivos adjuntos.
Los usuarios deben poder filtrar y buscar tareas.
Se debe generar un reporte de productividad por usuario y proyecto.
```

**Capacidad sugerida:** 10 story points por sprint

---

## Ejemplo 4: Blog con CMS

```
Los usuarios deben poder leer artículos del blog sin necesidad de registrarse.
Los artículos deben mostrar título, contenido, autor, fecha y categoría.
Los usuarios registrados deben poder comentar en los artículos.
Los autores deben poder crear, editar y eliminar sus propios artículos.
Los artículos deben soportar formato Markdown e imágenes.
Los administradores deben poder moderar comentarios.
El sistema debe tener un sistema de categorías y etiquetas.
Los usuarios deben poder buscar artículos por título, contenido o etiquetas.
Se debe implementar paginación para la lista de artículos.
```

**Capacidad sugerida:** 8 story points por sprint

---

## Ejemplo 5: Plataforma de Cursos Online

```
Los usuarios deben poder ver un catálogo de cursos disponibles.
Cada curso debe mostrar descripción, instructor, duración y precio.
Los usuarios deben poder inscribirse en cursos gratuitos o de pago.
Los estudiantes deben poder ver el contenido del curso organizado en módulos y lecciones.
Las lecciones pueden ser videos, textos o cuestionarios.
Los estudiantes deben poder marcar lecciones como completadas.
El sistema debe mostrar el progreso del estudiante en cada curso.
Los instructores deben poder crear y gestionar sus cursos.
Los administradores deben poder aprobar o rechazar cursos antes de publicarlos.
Se deben generar certificados de finalización automáticamente.
```

**Capacidad sugerida:** 15 story points por sprint

---

## Consejos para Escribir Requisitos

1. **Sé específico pero conciso**: Describe claramente qué debe hacer el sistema
2. **Incluye validaciones**: Menciona reglas de negocio importantes
3. **Define roles**: Especifica qué tipo de usuarios existen
4. **Menciona integraciones**: Si hay emails, pagos, notificaciones, etc.
5. **Usa lenguaje ubicuo**: Términos que el equipo y el negocio entiendan

## Contexto Adicional Útil

Puedes agregar información como:
- Stack tecnológico: "React + Node.js + MongoDB"
- Restricciones: "Debe ser compatible con IE11"
- Prioridades: "La funcionalidad de pago es crítica para el lanzamiento"
- Referencias: "Similar a como funciona en [otra aplicación]"
