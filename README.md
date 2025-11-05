# Agente Scrum Master & Product Owner AI

MVP de un agente inteligente que traduce requisitos de negocio en artefactos Scrum completos: Historias de Usuario, Backlog priorizado, Planificación de Sprints y gestión de velocidad del equipo.

## 🚀 Características

- ✅ Generación automática de Historias de Usuario en formato Gherkin
- ✅ Criterios de aceptación y casos de prueba
- ✅ **Casos de prueba detallados por cada Historia de Usuario**
- ✅ Descomposición en subtareas técnicas
- ✅ Priorización por valor de negocio y dependencias
- ✅ Planificación automática de sprints
- ✅ Ajuste dinámico de velocidad basado en histórico
- ✅ Exportación a Markdown y CSV
- ✅ Interfaz web interactiva

## 📋 Requisitos

- Python 3.9+
- Node.js 16+
- Cuenta de Azure OpenAI

## 🔧 Instalación

### Backend

```bash
# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En macOS/Linux

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus credenciales de Azure OpenAI

# Iniciar servidor
uvicorn app.main:app --reload
```

El backend estará disponible en `http://localhost:8000`

### Frontend

```bash
cd frontend

# Instalar dependencias
npm install

# Iniciar desarrollo
npm run dev
```

El frontend estará disponible en `http://localhost:5173`

## 📖 Uso

### 1. Proporcionar Requisitos

Ingresa los requisitos de negocio en lenguaje natural:

```
Los usuarios deben poder registrarse con correo y contraseña; 
además, deben poder recuperar contraseña vía email; 
el sistema debe permitir diferentes roles de usuario (admin, estándar).
```

### 2. Configurar Capacidad del Equipo

Define la capacidad de tu equipo en story points por sprint (ejemplo: 9 SP)

### 3. Generar Backlog

El agente generará:
- Historias de Usuario completas en Gherkin
- Criterios de aceptación
- Story Points estimados
- Subtareas desglosadas
- Backlog priorizado

### 4. Planificar Sprints

El sistema distribuirá las HU en sprints según:
- Capacidad del equipo
- Valor de negocio
- Dependencias funcionales

### 5. Ajustar Velocidad

Reporta el progreso de sprints completados:
```
Sprint 1: completados 8 de 10 story points
```

El agente ajustará la planificación futura basándose en la velocidad real.

## 🏗️ Estructura del Proyecto

```
agente/
├── app/                    # Backend FastAPI
│   ├── main.py            # Aplicación principal
│   ├── models.py          # Modelos de datos
│   ├── services/          # Lógica de negocio
│   │   ├── ai_agent.py    # Agente IA
│   │   └── backlog.py     # Gestión de backlog
│   └── routers/           # Endpoints API
├── frontend/              # Frontend React
│   ├── src/
│   │   ├── components/    # Componentes React
│   │   ├── services/      # Cliente API
│   │   └── App.jsx        # Componente principal
├── data/                  # Almacenamiento de datos
├── exports/               # Archivos exportados
└── requirements.txt       # Dependencias Python
```

## 🔌 API Endpoints

### POST `/api/generate-backlog`
Genera backlog completo desde requisitos

**Body:**
```json
{
  "requirements": "Los usuarios deben poder...",
  "team_capacity": 9,
  "context": "optional"
}
```

### POST `/api/plan-sprints`
Planifica sprints desde backlog existente

### POST `/api/update-velocity`
Actualiza velocidad del equipo

### GET `/api/backlog`
Obtiene backlog actual

### GET `/api/export/{format}`
Exporta a Markdown o CSV

## 🎯 Ejemplos de Requisitos

**E-commerce básico:**
```
Los usuarios deben poder ver un catálogo de productos, agregar productos 
al carrito, procesar pagos con tarjeta, y recibir confirmación por email.
```

**Sistema de gestión documental:**
```
Los usuarios deben poder subir documentos PDF, clasificarlos por categorías,
buscar por texto completo, y compartir documentos con otros usuarios.
```

## 📊 Formato de Salida

### Markdown
Tablas con: ID, Título, Gherkin, Criterios, Story Points, Prioridad, Sprint, Subtareas

### CSV
Formato compatible con herramientas como Linear, Jira, etc.

## 🤝 Contribuir

Este es un MVP. Contribuciones bienvenidas para:
- Integración con Linear/Jira API
- Más estrategias de priorización
- Templates personalizables
- Dashboard de métricas

## 📄 Licencia

MIT License
