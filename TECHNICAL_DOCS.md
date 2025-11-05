# Agente Scrum Master & Product Owner AI

**Versión:** 1.0.0  
**Fecha:** 30 de octubre de 2025

## 📋 Resumen del Proyecto

MVP de un agente inteligente que traduce requisitos de negocio en artefactos Scrum completos utilizando Azure OpenAI GPT-4o.

## ✨ Características Implementadas

### Core Features
- ✅ Generación automática de Historias de Usuario en formato Gherkin
- ✅ Criterios de aceptación detallados y casos de prueba
- ✅ Descomposición automática en subtareas técnicas
- ✅ Estimación de Story Points (escala Fibonacci)
- ✅ Priorización por valor de negocio y dependencias
- ✅ Planificación automática de sprints
- ✅ Ajuste dinámico de velocidad del equipo
- ✅ Gestión de histórico de velocidad

### Exportación
- ✅ Formato Markdown (documentación completa)
- ✅ Formato CSV (compatible con Excel, Linear, Jira)
- ✅ Formato JSON (datos estructurados)

### Interfaz
- ✅ Frontend React con diseño moderno
- ✅ Vista de Historias de Usuario con detalles
- ✅ Vista de Planificación de Sprints
- ✅ Dashboard con estadísticas
- ✅ Sistema de pestañas intuitivo

## 🏗️ Arquitectura

```
┌─────────────────────────────────────────────────┐
│                  Frontend React                  │
│              (Vite + React 18)                   │
│  - Formulario de requisitos                      │
│  - Visualización de backlog                      │
│  - Gestión de sprints                            │
│  - Exportación de datos                          │
└───────────────┬─────────────────────────────────┘
                │ HTTP/REST API
┌───────────────▼─────────────────────────────────┐
│              Backend FastAPI                     │
│          (Python 3.9+ async)                     │
│  - Endpoints REST                                │
│  - Validación con Pydantic                       │
│  - Manejo de estado                              │
└───────────────┬─────────────────────────────────┘
                │
        ┌───────┴────────┐
        ▼                ▼
┌───────────────┐  ┌────────────────┐
│   AI Agent    │  │ Backlog Manager│
│ (Azure OpenAI)│  │ (Persistencia) │
│               │  │                │
│ - GPT-4o      │  │ - JSON Storage │
│ - Generación  │  │ - Exportación  │
│   de HU       │  │ - Métricas     │
│ - Prioriza-   │  └────────────────┘
│   ción        │
│ - Planning    │
└───────────────┘
```

## 📊 Modelo de Datos

### UserStory
```python
- id: str (HU1, HU2, ...)
- title: str
- gherkin: str
- acceptance_criteria: List[str]
- story_points: int (1-13)
- priority: Priority (Alta, Media, Baja)
- dependencies: List[str]
- subtasks: List[SubTask]
- sprint_assigned: Optional[int]
- tags: List[str]
```

### Sprint
```python
- number: int
- name: str
- capacity: int
- user_stories: List[str]
- total_points: int
- completed_points: int
- status: str
```

### Backlog
```python
- user_stories: List[UserStory]
- sprints: List[Sprint]
- team_capacity: int
- velocity_history: List[int]
- current_velocity: Optional[float]
```

## 🔧 Tecnologías Utilizadas

### Backend
- **FastAPI** 0.115.0 - Framework web moderno y rápido
- **Pydantic** 2.9.2 - Validación de datos y serialización
- **Azure OpenAI** (openai 1.54.3) - GPT-4o para generación de contenido
- **Uvicorn** 0.32.0 - Servidor ASGI

### Frontend
- **React** 18.3.1 - Biblioteca de UI
- **Vite** 5.4.10 - Build tool y dev server
- **Axios** 1.7.7 - Cliente HTTP
- **Lucide React** 0.454.0 - Iconos

### AI/ML
- **Azure OpenAI Service**
- **Model:** gpt-4o
- **API Version:** 2025-01-01-preview

## 📁 Estructura de Archivos

```
agente/
├── app/
│   ├── main.py                 # FastAPI app + endpoints
│   ├── models.py               # Modelos Pydantic
│   ├── config.py               # Configuración y settings
│   └── services/
│       ├── ai_agent.py         # Lógica de IA (OpenAI)
│       └── backlog_manager.py  # Gestión de backlog
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx             # Componente principal
│   │   ├── App.css             # Estilos globales
│   │   ├── main.jsx            # Entry point
│   │   ├── components/
│   │   │   ├── UserStoryCard.jsx
│   │   │   └── SprintCard.jsx
│   │   └── services/
│   │       └── api.js          # Cliente API
│   ├── index.html
│   ├── vite.config.js
│   └── package.json
│
├── data/                       # Almacenamiento local
│   └── backlog.json           # Estado del backlog
│
├── exports/                    # Archivos exportados
│   ├── backlog_*.md
│   ├── backlog_*.csv
│   └── backlog_*.json
│
├── .env                        # Variables de entorno
├── requirements.txt            # Dependencias Python
├── README.md                   # Documentación principal
├── EJEMPLOS.md                 # Ejemplos de requisitos
├── TECHNICAL_DOCS.md          # Este archivo
└── start.sh                    # Script de inicio rápido
```

## 🚀 Instalación y Configuración

### Prerrequisitos
- Python 3.9 o superior
- Node.js 16 o superior
- Cuenta de Azure OpenAI

### Paso 1: Clonar y Configurar Backend

```bash
# Navegar al directorio
cd agente

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate  # Windows

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno (.env ya está configurado)
# AZURE_OPENAI_API_KEY=...
# AZURE_OPENAI_ENDPOINT=...
# AZURE_OPENAI_DEPLOYMENT_NAME=...
# AZURE_OPENAI_API_VERSION=...
```

### Paso 2: Configurar Frontend

```bash
cd frontend
npm install
```

### Paso 3: Iniciar Aplicación

**Opción A: Script automático (recomendado)**
```bash
chmod +x start.sh
./start.sh
```

**Opción B: Manual**

Terminal 1 - Backend:
```bash
source venv/bin/activate
uvicorn app.main:app --reload
```

Terminal 2 - Frontend:
```bash
cd frontend
npm run dev
```

## 🔌 API Endpoints

### `POST /api/generate-backlog`
Genera backlog completo desde requisitos.

**Request:**
```json
{
  "requirements": "Los usuarios deben poder...",
  "team_capacity": 9,
  "additional_context": "Stack: React + Node.js",
  "priority_guidance": "Priorizar autenticación"
}
```

**Response:** `Backlog`

### `GET /api/backlog`
Obtiene el backlog actual almacenado.

**Response:** `Backlog`

### `POST /api/plan-sprints`
Replanifica sprints con nueva capacidad o velocidad.

**Request:**
```json
{
  "team_capacity": 10,
  "num_sprints": 3
}
```

**Response:** `Backlog`

### `POST /api/update-velocity`
Actualiza velocidad del equipo con datos de sprint completado.

**Request:**
```json
{
  "sprint_number": 1,
  "completed_points": 8,
  "total_points": 10,
  "feedback": "Algunas tareas fueron más complejas"
}
```

**Response:** `Backlog` (con velocidad actualizada)

### `GET /api/export/{format}`
Exporta backlog en formato especificado.

**Params:** `format` = `markdown` | `csv` | `json`

**Response:** Archivo descargable

### `DELETE /api/backlog`
Elimina el backlog actual.

**Response:**
```json
{
  "message": "Backlog eliminado exitosamente"
}
```

## 🤖 Lógica del Agente IA

### Prompt Engineering

El agente utiliza un system prompt detallado que instruye a GPT-4o para:

1. **Formato Gherkin:** "Como [rol] quiero [funcionalidad] para [beneficio]"
2. **Criterios SMART:** Específicos, Medibles, Alcanzables, Relevantes, Temporales
3. **Estimación Fibonacci:** 1, 2, 3, 5, 8, 13 story points
4. **Priorización:** Alta (core/habilitadores), Media (importante), Baja (nice-to-have)
5. **Dependencias:** Identificar HU que habilitan otras
6. **Subtareas:** Análisis, Diseño, Backend, Frontend, Testing, Docs

### Algoritmo de Priorización

```python
def _prioritize_stories(stories):
    # 1. Ordenar por prioridad de negocio
    # 2. Luego por dependencias (habilitadores primero)
    # 3. Finalmente por ID para estabilidad
    
    priority_order = {Alta: 0, Media: 1, Baja: 2}
    
    def get_score(story):
        dependent_count = count_dependents(story)
        return (
            priority_order[story.priority],  # Prioridad primero
            -dependent_count,                 # Habilitadores antes
            story.id                          # Estabilidad
        )
    
    return sorted(stories, key=get_score)
```

### Algoritmo de Planning

```python
def suggest_sprint_planning(stories, capacity):
    sprints = []
    current_sprint = 1
    current_capacity = 0
    current_stories = []
    
    for story in prioritized_stories:
        if current_capacity + story.points <= capacity:
            # Cabe en sprint actual
            current_capacity += story.points
            current_stories.append(story)
        else:
            # Crear nuevo sprint
            sprints.append(Sprint(...))
            current_sprint += 1
            current_capacity = story.points
            current_stories = [story]
    
    return sprints
```

### Ajuste de Velocidad

```python
def update_velocity(sprint_completed):
    # Agregar a histórico
    velocity_history.append(sprint_completed.points)
    
    # Calcular promedio móvil (últimos 3 sprints)
    recent = velocity_history[-3:]
    current_velocity = sum(recent) / len(recent)
    
    # Ajustar capacidad del equipo
    if len(recent) >= 3:
        team_capacity = int(current_velocity)
    
    return current_velocity
```

## 🎨 Componentes Frontend

### App.jsx
Componente principal que maneja:
- Estado global de la aplicación
- Navegación por pestañas
- Llamadas a la API
- Gestión de errores y loading

### UserStoryCard.jsx
Tarjeta visual para cada Historia de Usuario mostrando:
- ID y título
- Gherkin
- Badges de prioridad y story points
- Criterios de aceptación
- Subtareas
- Tags

### SprintCard.jsx
Tarjeta de sprint con:
- Nombre y número
- Capacidad y utilización
- Barra de progreso
- Lista de HU asignadas
- Estado de completitud

## 🔒 Seguridad

- ✅ Variables de entorno para credenciales
- ✅ CORS configurado para localhost
- ✅ Validación de entrada con Pydantic
- ✅ Manejo seguro de errores
- ⚠️ No implementado: autenticación de usuarios (MVP)

## 📈 Métricas y Analytics

El sistema rastrea:
- Total de historias de usuario
- Total de story points
- Número de sprints
- Histórico de velocidad
- Velocidad promedio actual
- Utilización de capacidad por sprint

## 🧪 Testing

**Estado actual:** No implementado en MVP

**Recomendaciones para producción:**
- Unit tests con pytest (backend)
- Tests de integración para API
- Tests E2E con Playwright/Cypress (frontend)
- Tests de prompts con diferentes requisitos

## 🚀 Mejoras Futuras

### Corto Plazo
- [ ] Autenticación y usuarios múltiples
- [ ] Persistencia en base de datos (PostgreSQL)
- [ ] Edición manual de historias de usuario
- [ ] Drag & drop para reordenar prioridades
- [ ] Vista Kanban

### Mediano Plazo
- [ ] Integración con Linear API
- [ ] Integración con Jira API
- [ ] Templates personalizables
- [ ] Múltiples backlogs por proyecto
- [ ] Colaboración en tiempo real

### Largo Plazo
- [ ] Dashboard de métricas avanzadas
- [ ] Predicción de sprint con ML
- [ ] Análisis de sentimiento en feedback
- [ ] Generación de documentación técnica
- [ ] Sugerencias de refactoring de HU

## 🐛 Issues Conocidos

1. **Lint warnings:** Algunos warnings de linter por props validation en React (no afecta funcionalidad)
2. **Contraste de colores:** Algunos warnings de accesibilidad en CSS (mejora futura)
3. **Persistencia:** Solo en archivo local JSON (mejorar con BD)

## 📞 Soporte

Para problemas o preguntas:
1. Revisar logs del backend en terminal
2. Verificar consola del navegador (DevTools)
3. Verificar que Azure OpenAI esté funcionando
4. Revisar que las credenciales en `.env` sean correctas

## 📄 Licencia

MIT License - Uso libre para proyectos personales y comerciales.

---

**Desarrollado con ❤️ usando Azure OpenAI GPT-4o**
