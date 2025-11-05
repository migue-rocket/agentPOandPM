# Testing del API

Puedes usar estos comandos curl para probar el API directamente.

## 1. Health Check

```bash
curl http://localhost:8000/health
```

## 2. Generar Backlog

```bash
curl -X POST "http://localhost:8000/api/generate-backlog" \
  -H "Content-Type: application/json" \
  -d '{
    "requirements": "Los usuarios deben poder registrarse con correo y contraseña; además, deben poder recuperar contraseña vía email; el sistema debe permitir diferentes roles de usuario (admin, estándar).",
    "team_capacity": 9,
    "additional_context": "Stack: React + FastAPI + PostgreSQL",
    "priority_guidance": "Priorizar autenticación antes que otras funcionalidades"
  }'
```

## 3. Obtener Backlog Actual

```bash
curl http://localhost:8000/api/backlog
```

## 4. Actualizar Velocidad

```bash
curl -X POST "http://localhost:8000/api/update-velocity" \
  -H "Content-Type: application/json" \
  -d '{
    "sprint_number": 1,
    "completed_points": 8,
    "total_points": 10,
    "feedback": "El equipo tuvo algunos bloqueos con la integración de email"
  }'
```

## 5. Replanificar Sprints

```bash
curl -X POST "http://localhost:8000/api/plan-sprints" \
  -H "Content-Type: application/json" \
  -d '{
    "team_capacity": 10,
    "num_sprints": 3
  }'
```

## 6. Exportar Backlog (Markdown)

```bash
curl -O -J http://localhost:8000/api/export/markdown
```

## 7. Exportar Backlog (CSV)

```bash
curl -O -J http://localhost:8000/api/export/csv
```

## 8. Exportar Backlog (JSON)

```bash
curl -O -J http://localhost:8000/api/export/json
```

## 9. Limpiar Backlog

```bash
curl -X DELETE http://localhost:8000/api/backlog
```

## Testing con Python

```python
import requests

# Generar backlog
response = requests.post(
    "http://localhost:8000/api/generate-backlog",
    json={
        "requirements": "Sistema de blog con posts, comentarios y categorías",
        "team_capacity": 9
    }
)

backlog = response.json()
print(f"Generadas {len(backlog['user_stories'])} historias de usuario")
print(f"Planificados {len(backlog['sprints'])} sprints")

# Iterar sobre historias
for story in backlog['user_stories']:
    print(f"\n{story['id']}: {story['title']}")
    print(f"  Story Points: {story['story_points']}")
    print(f"  Prioridad: {story['priority']}")
```

## Testing con JavaScript/Node

```javascript
const axios = require('axios');

async function testAPI() {
  try {
    // Generar backlog
    const response = await axios.post(
      'http://localhost:8000/api/generate-backlog',
      {
        requirements: 'Sistema de gestión de tareas con proyectos y asignaciones',
        team_capacity: 12
      }
    );

    const backlog = response.data;
    console.log(`Generadas ${backlog.user_stories.length} historias`);
    
    // Exportar a Markdown
    await axios.get('http://localhost:8000/api/export/markdown', {
      responseType: 'blob'
    });
    
    console.log('Backlog exportado exitosamente');
  } catch (error) {
    console.error('Error:', error.message);
  }
}

testAPI();
```

## Documentación Interactiva

Visita http://localhost:8000/docs para la documentación interactiva de Swagger/OpenAPI.

Puedes probar todos los endpoints directamente desde el navegador.
