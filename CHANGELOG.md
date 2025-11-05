# 🧪 Casos de Prueba - Cambios Implementados

## ✅ Cambios Realizados

### 1. **Modelo de Datos** (`app/models.py`)
- ✅ Nuevo modelo `TestCase` con campos:
  - `id`: Identificador único (ej: HU1-TC1)
  - `title`: Título del caso
  - `description`: Descripción detallada
  - `preconditions`: Condiciones previas
  - `steps`: Lista de pasos a seguir
  - `expected_result`: Resultado esperado
  - `test_type`: Tipo de prueba (functional, integration, ui, api, security, performance)
  
- ✅ Actualizado `UserStory` para incluir:
  - `test_cases`: Lista de casos de prueba

---

### 2. **Agente de IA** (`app/services/ai_agent.py`)
- ✅ Prompt del sistema actualizado para generar casos de prueba
- ✅ Instrucciones detalladas sobre:
  - Estructura de casos de prueba
  - Tipos de prueba a generar
  - Cobertura (happy path + casos de error)
  - Formato JSON esperado
  
- ✅ Parser actualizado para procesar casos de prueba del JSON

---

### 3. **Frontend** (`frontend/src/components/UserStoryCard.jsx`)
- ✅ Nueva sección de "Casos de Prueba" en cada tarjeta de HU
- ✅ Visualización de cada caso con:
  - ID y título
  - Descripción
  - Precondiciones
  - Pasos numerados
  - Resultado esperado
  - Badge con tipo de prueba
  
- ✅ Diseño con tarjetas expandibles y borde de color

---

### 4. **Estilos** (`frontend/src/App.css`)
- ✅ Nuevas clases CSS:
  - `.test-case`: Contenedor del caso
  - `.test-case-header`: Encabezado
  - `.test-case-description`: Descripción
  - `.test-case-section`: Secciones del caso
  - `.test-case-steps`: Lista de pasos
  - `.test-case-type`: Badge de tipo

---

### 5. **Exportación** (`app/services/backlog_manager.py`)

**Markdown:**
- ✅ Sección completa de casos de prueba por cada HU
- ✅ Formato legible con encabezados y listas

**CSV:**
- ✅ Nueva columna "Casos de Prueba"
- ✅ Lista compacta de IDs y títulos

**JSON:**
- ✅ Array completo de test_cases con toda la información

---

### 6. **Documentación**
- ✅ `TEST_CASES_GUIDE.md`: Guía completa de casos de prueba
- ✅ `README.md`: Actualizado para mencionar casos de prueba
- ✅ `CHANGELOG.md`: Este archivo con los cambios

---

## 🎯 Ejemplo de Salida

### Historia de Usuario Generada:

```json
{
  "id": "HU1",
  "title": "Registro de usuario",
  "gherkin": "Como usuario nuevo quiero registrarme con correo y contraseña para acceder a la plataforma",
  "acceptance_criteria": [
    "Se envía email de confirmación",
    "Validación de formato email",
    "Contraseña mínimo 8 caracteres con mayúscula y número"
  ],
  "test_cases": [
    {
      "id": "HU1-TC1",
      "title": "Validar registro exitoso con datos válidos",
      "description": "Verificar que un usuario puede registrarse con correo y contraseña válidos",
      "preconditions": "Sistema disponible, no hay usuario registrado con el email de prueba",
      "steps": [
        "Abrir página de registro",
        "Ingresar email válido: test@example.com",
        "Ingresar contraseña válida: Test123!",
        "Hacer clic en botón Registrar"
      ],
      "expected_result": "Usuario registrado exitosamente, se envía email de confirmación, se redirige a página de inicio",
      "test_type": "functional"
    },
    {
      "id": "HU1-TC2",
      "title": "Validar error con email inválido",
      "description": "Verificar que el sistema rechaza emails con formato incorrecto",
      "preconditions": "Sistema disponible",
      "steps": [
        "Abrir página de registro",
        "Ingresar email inválido: test@invalid",
        "Ingresar contraseña válida: Test123!",
        "Hacer clic en botón Registrar"
      ],
      "expected_result": "Se muestra mensaje de error 'Email inválido', no se crea usuario",
      "test_type": "functional"
    },
    {
      "id": "HU1-TC3",
      "title": "Validar error con contraseña débil",
      "description": "Verificar que el sistema rechaza contraseñas que no cumplen requisitos",
      "preconditions": "Sistema disponible",
      "steps": [
        "Abrir página de registro",
        "Ingresar email válido: test@example.com",
        "Ingresar contraseña débil: 123",
        "Hacer clic en botón Registrar"
      ],
      "expected_result": "Se muestra mensaje 'Contraseña debe tener mínimo 8 caracteres', no se crea usuario",
      "test_type": "security"
    }
  ],
  "story_points": 3,
  "priority": "Alta"
}
```

---

## 🎨 Visualización en UI

Antes de los cambios:
```
┌───────────────────────────┐
│ HU1: Registro de usuario  │
├───────────────────────────┤
│ Gherkin: Como usuario...  │
│ ✓ Criterios (3)          │
│ ⚙️ Subtareas (6)          │
└───────────────────────────┘
```

Después de los cambios:
```
┌────────────────────────────────────────┐
│ HU1: Registro de usuario               │
├────────────────────────────────────────┤
│ Gherkin: Como usuario...               │
│ ✓ Criterios (3)                       │
│                                        │
│ 🧪 Casos de Prueba (3) ← NUEVO        │
│ ┌────────────────────────────────────┐│
│ │ HU1-TC1: Registro exitoso          ││
│ │ Descripción: Verificar que...      ││
│ │ Pasos:                             ││
│ │  1. Abrir página                   ││
│ │  2. Ingresar email                 ││
│ │  3. Clic en Registrar              ││
│ │ Resultado: Usuario registrado...   ││
│ │ [functional]                       ││
│ └────────────────────────────────────┘│
│                                        │
│ ⚙️ Subtareas (6)                      │
└────────────────────────────────────────┘
```

---

## 📊 Tipos de Casos de Prueba Generados

1. **functional** - Pruebas funcionales básicas (más común)
2. **integration** - Integración entre componentes
3. **ui** - Interfaz de usuario y UX
4. **api** - Endpoints y servicios REST
5. **security** - Validaciones de seguridad
6. **performance** - Rendimiento y tiempos de respuesta

---

## ✨ Beneficios

### Para el Product Owner:
- ✅ Casos de prueba listos para QA
- ✅ Documentación de comportamiento esperado
- ✅ Base para Definition of Done

### Para el Equipo de Desarrollo:
- ✅ Claridad sobre qué probar
- ✅ Base para tests unitarios y E2E
- ✅ Casos edge identificados automáticamente

### Para QA:
- ✅ Test cases listos para ejecutar
- ✅ Cobertura completa desde el inicio
- ✅ Formato estándar y exportable

---

## 🚀 Cómo Usar

### 1. Generar Backlog
```bash
# Inicia la aplicación
./start.sh

# Navega a http://localhost:5173
# Ingresa requisitos
# Genera backlog
```

### 2. Ver Casos de Prueba
- Navega a la pestaña "📋 Historias de Usuario"
- Expande cualquier historia
- Sección "🧪 Casos de Prueba" muestra todos los casos

### 3. Exportar
```bash
# Desde la UI:
# - Clic en "📄 Exportar Markdown" para documentación
# - Clic en "📊 Exportar CSV" para Excel/Jira
# - Clic en "🔧 Exportar JSON" para integración
```

---

## 📚 Documentación Adicional

- **Guía completa:** `TEST_CASES_GUIDE.md`
- **Ejemplos:** Ver `EJEMPLOS.md` y generar backlog
- **API:** Los casos están en el modelo JSON de cada HU

---

## 🔄 Retrocompatibilidad

- ✅ Los backlogs existentes siguen funcionando
- ✅ `test_cases` es opcional (lista vacía por defecto)
- ✅ No rompe exportaciones anteriores

---

## 🎉 Resultado Final

Ahora cada Historia de Usuario generada incluye:

1. ✅ ID y título
2. ✅ Gherkin (Como... quiero... para...)
3. ✅ Criterios de aceptación
4. ✅ **2-4 Casos de prueba detallados** ← NUEVO
5. ✅ Subtareas técnicas
6. ✅ Story Points y prioridad
7. ✅ Dependencias
8. ✅ Tags

**Total:** Backlog 100% listo para desarrollo y testing! 🚀
