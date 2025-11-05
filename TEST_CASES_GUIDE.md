# 🧪 Casos de Prueba - Guía Completa

## ¿Qué son los Casos de Prueba?

Los casos de prueba son escenarios específicos que verifican que cada Historia de Usuario funciona correctamente. El agente genera automáticamente 2-4 casos de prueba por cada HU, incluyendo tanto escenarios exitosos (happy path) como casos de error.

---

## 📋 Estructura de un Caso de Prueba

Cada caso de prueba incluye:

### 1. **ID** - Identificador único
Formato: `{HU_ID}-TC{número}`
Ejemplo: `HU1-TC1`, `HU1-TC2`

### 2. **Título** - Descripción corta
Ejemplo: "Validar registro exitoso con datos válidos"

### 3. **Descripción** - Explicación detallada
Ejemplo: "Verificar que un usuario puede registrarse con correo y contraseña válidos"

### 4. **Precondiciones** - Estado requerido antes de ejecutar
Ejemplo: "Sistema disponible, no hay usuario registrado con el email de prueba"

### 5. **Pasos** - Lista ordenada de acciones
Ejemplo:
1. Abrir página de registro
2. Ingresar email válido: test@example.com
3. Ingresar contraseña válida: Test123!
4. Hacer clic en botón Registrar

### 6. **Resultado Esperado** - Qué debe suceder
Ejemplo: "Usuario registrado exitosamente, se envía email de confirmación"

### 7. **Tipo de Prueba** - Categoría del test
Tipos: `functional`, `integration`, `ui`, `api`, `security`, `performance`

---

## 🎯 Ejemplo Completo

### Historia de Usuario: Registro de Usuario

```
HU1: Registro de usuario
Como usuario nuevo
Quiero registrarme con correo y contraseña
Para acceder a la plataforma
```

### Casos de Prueba Generados:

#### **TC1: Registro exitoso con datos válidos**

**ID:** HU1-TC1  
**Tipo:** functional  
**Descripción:** Verificar que un usuario puede registrarse con credenciales válidas

**Precondiciones:**
- Sistema disponible
- No existe usuario con el email test@example.com

**Pasos:**
1. Navegar a `/registro`
2. Ingresar email: test@example.com
3. Ingresar contraseña: Test123!
4. Confirmar contraseña: Test123!
5. Hacer clic en "Registrar"

**Resultado esperado:**
- Usuario creado en la base de datos
- Email de confirmación enviado
- Redirección a página de inicio
- Mensaje de éxito visible

---

#### **TC2: Error con email inválido**

**ID:** HU1-TC2  
**Tipo:** functional  
**Descripción:** Verificar rechazo de emails con formato incorrecto

**Precondiciones:**
- Sistema disponible

**Pasos:**
1. Navegar a `/registro`
2. Ingresar email inválido: test@invalid
3. Ingresar contraseña: Test123!
4. Hacer clic en "Registrar"

**Resultado esperado:**
- Mensaje de error: "Email inválido"
- No se crea usuario
- Formulario permanece en pantalla

---

#### **TC3: Error con contraseña débil**

**ID:** HU1-TC3  
**Tipo:** security  
**Descripción:** Verificar que el sistema rechaza contraseñas débiles

**Precondiciones:**
- Sistema disponible

**Pasos:**
1. Navegar a `/registro`
2. Ingresar email: test@example.com
3. Ingresar contraseña: 123
4. Hacer clic en "Registrar"

**Resultado esperado:**
- Mensaje de error: "Contraseña debe tener mínimo 8 caracteres"
- No se crea usuario

---

#### **TC4: Error con email duplicado**

**ID:** HU1-TC4  
**Tipo:** functional  
**Descripción:** Verificar que no se permiten emails duplicados

**Precondiciones:**
- Usuario con email test@example.com ya existe

**Pasos:**
1. Navegar a `/registro`
2. Ingresar email: test@example.com
3. Ingresar contraseña: Test123!
4. Hacer clic en "Registrar"

**Resultado esperado:**
- Mensaje de error: "Email ya registrado"
- No se crea nuevo usuario

---

## 🎨 Visualización en la Interfaz

Los casos de prueba se muestran en tarjetas expandibles dentro de cada Historia de Usuario:

```
┌─────────────────────────────────────────────────┐
│ HU1: Registro de usuario          [3 SP] [Alta] │
├─────────────────────────────────────────────────┤
│ Como usuario quiero registrarme...              │
│                                                  │
│ ✓ Criterios de Aceptación (3)                   │
│                                                  │
│ 🧪 Casos de Prueba (4)                          │
│                                                  │
│ ┌─────────────────────────────────────────────┐ │
│ │ HU1-TC1: Registro exitoso                   │ │
│ │ Verificar registro con datos válidos        │ │
│ │                                              │ │
│ │ Precondiciones: Sistema disponible...       │ │
│ │                                              │ │
│ │ Pasos:                                       │ │
│ │ 1. Abrir página de registro                 │ │
│ │ 2. Ingresar email válido                    │ │
│ │ 3. Ingresar contraseña válida               │ │
│ │ 4. Hacer clic en Registrar                  │ │
│ │                                              │ │
│ │ Resultado: Usuario registrado, email enviado│ │
│ │                                              │ │
│ │ [functional]                                 │ │
│ └─────────────────────────────────────────────┘ │
│                                                  │
│ ┌─────────────────────────────────────────────┐ │
│ │ HU1-TC2: Error con email inválido           │ │
│ │ ...                                          │ │
│ └─────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────┘
```

---

## 📤 Exportación de Casos de Prueba

### Formato Markdown

```markdown
#### HU1-TC1: Registro exitoso con datos válidos

**Descripción:** Verificar que un usuario puede registrarse...

**Precondiciones:** Sistema disponible, no hay usuario...

**Pasos:**
1. Abrir página de registro
2. Ingresar email válido: test@example.com
3. Ingresar contraseña válida: Test123!
4. Hacer clic en botón Registrar

**Resultado esperado:** Usuario registrado exitosamente...

**Tipo:** `functional`
```

### Formato CSV

```csv
ID,Título,Casos de Prueba
HU1,Registro de usuario,"HU1-TC1: Registro exitoso; HU1-TC2: Error email inválido; HU1-TC3: Error contraseña débil; HU1-TC4: Error email duplicado"
```

### Formato JSON

```json
{
  "id": "HU1",
  "title": "Registro de usuario",
  "test_cases": [
    {
      "id": "HU1-TC1",
      "title": "Registro exitoso con datos válidos",
      "description": "Verificar que un usuario puede registrarse...",
      "preconditions": "Sistema disponible...",
      "steps": [
        "Abrir página de registro",
        "Ingresar email válido: test@example.com",
        "Ingresar contraseña válida: Test123!",
        "Hacer clic en botón Registrar"
      ],
      "expected_result": "Usuario registrado exitosamente...",
      "test_type": "functional"
    }
  ]
}
```

---

## 🏷️ Tipos de Prueba

### **functional** (Funcional)
- Pruebas de funcionalidad básica
- Happy path y casos de error
- Más común para la mayoría de HU

**Ejemplo:** Verificar que el login funciona con credenciales válidas

---

### **integration** (Integración)
- Pruebas de integración entre componentes
- Flujos que cruzan múltiples sistemas

**Ejemplo:** Verificar que después del registro se envía email y se crea sesión

---

### **ui** (Interfaz de Usuario)
- Pruebas de elementos visuales
- Responsive, accesibilidad, UX

**Ejemplo:** Verificar que el formulario es responsive en móvil

---

### **api** (API)
- Pruebas de endpoints
- Request/response, status codes

**Ejemplo:** POST /api/register retorna 201 con usuario creado

---

### **security** (Seguridad)
- Pruebas de vulnerabilidades
- Validaciones, sanitización, autenticación

**Ejemplo:** Verificar que las contraseñas se almacenan hasheadas

---

### **performance** (Rendimiento)
- Pruebas de velocidad y escalabilidad
- Tiempos de respuesta, carga

**Ejemplo:** Registro debe completarse en menos de 2 segundos

---

## 💡 Mejores Prácticas

### ✅ Hacer:
- Incluir tanto casos de éxito como de error
- Usar datos específicos en los pasos (no "ingresar email válido" sino "ingresar test@example.com")
- Resultado esperado debe ser verificable
- Variar los tipos de prueba según funcionalidad

### ❌ Evitar:
- Casos de prueba vagos o ambiguos
- Omitir precondiciones importantes
- Pasos demasiado genéricos
- No especificar el resultado esperado

---

## 🎓 Cobertura de Pruebas

El agente genera automáticamente casos que cubren:

1. **Happy Path** - Caso exitoso principal
2. **Validaciones** - Datos inválidos, formatos incorrectos
3. **Edge Cases** - Valores límite, casos extremos
4. **Errores** - Manejo de errores esperados
5. **Seguridad** - Validaciones de seguridad básicas

---

## 🔄 Integración con Herramientas

Los casos de prueba exportados pueden usarse con:

- **Jira/Linear:** Importar como sub-tareas de testing
- **TestRail:** Importar como casos de prueba
- **Cypress/Playwright:** Base para tests E2E
- **Postman:** Base para tests de API
- **Manual Testing:** Guías para QA manual

---

## 📊 Ejemplo Real Completo

**Requisito de Negocio:**
```
Los usuarios deben poder recuperar su contraseña mediante un enlace enviado por email
```

**HU Generada:**
```
HU2: Recuperar contraseña
Como usuario registrado
Quiero recuperar mi contraseña mediante email
Para poder acceder si la olvido

Story Points: 3
Prioridad: Alta
```

**Casos de Prueba Generados:**

1. **HU2-TC1:** Recuperación exitosa con email válido (functional)
2. **HU2-TC2:** Error con email no registrado (functional)
3. **HU2-TC3:** Token expira después de 24 horas (security)
4. **HU2-TC4:** Link solo puede usarse una vez (security)
5. **HU2-TC5:** Email se envía en menos de 5 segundos (performance)

---

## 🎉 Ventajas

- ✅ **Ahorro de tiempo:** No escribir casos manualmente
- ✅ **Cobertura completa:** IA identifica casos que podrías olvidar
- ✅ **Consistencia:** Formato estándar en todo el backlog
- ✅ **Documentación:** Casos sirven como documentación de comportamiento
- ✅ **Automatización:** Base para tests automatizados

---

¡Genera tu primer backlog con casos de prueba completos! 🚀
