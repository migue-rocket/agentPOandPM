import json
from typing import List, Dict
from openai import AzureOpenAI
from app.config import get_settings
from app.models import UserStory, SubTask, TestCase, Priority, Backlog


class AIAgent:
    """Agente de IA para generar artefactos Scrum"""
    
    def __init__(self):
        self.settings = get_settings()
        self.client = AzureOpenAI(
            api_key=self.settings.AZURE_OPENAI_API_KEY,
            api_version=self.settings.AZURE_OPENAI_API_VERSION,
            azure_endpoint=self.settings.AZURE_OPENAI_ENDPOINT
        )
        
    def generate_user_stories(
        self, 
        requirements: str, 
        additional_context: str = None,
        priority_guidance: str = None
    ) -> List[UserStory]:
        """Genera Historias de Usuario desde requisitos de negocio"""
        
        system_prompt = self._build_system_prompt()
        user_prompt = self._build_user_prompt(requirements, additional_context, priority_guidance)
        
        response = self.client.chat.completions.create(
            model=self.settings.AZURE_OPENAI_DEPLOYMENT_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            response_format={"type": "json_object"}
        )
        
        content = response.choices[0].message.content
        data = json.loads(content)
        
        user_stories = []
        for hu_data in data.get("user_stories", []):
            # Convertir subtareas
            subtasks = [
                SubTask(
                    id=st.get("id", f"{hu_data['id']}-ST{i+1}"),
                    title=st.get("title", ""),
                    description=st.get("description"),
                    estimated_hours=st.get("estimated_hours")
                )
                for i, st in enumerate(hu_data.get("subtasks", []))
            ]
            
            # Convertir casos de prueba
            test_cases = [
                TestCase(
                    id=tc.get("id", f"{hu_data['id']}-TC{i+1}"),
                    title=tc.get("title", ""),
                    description=tc.get("description", ""),
                    preconditions=tc.get("preconditions"),
                    steps=tc.get("steps", []),
                    expected_result=tc.get("expected_result", ""),
                    test_type=tc.get("test_type", "functional")
                )
                for i, tc in enumerate(hu_data.get("test_cases", []))
            ]
            
            user_story = UserStory(
                id=hu_data["id"],
                title=hu_data["title"],
                gherkin=hu_data["gherkin"],
                acceptance_criteria=hu_data["acceptance_criteria"],
                test_cases=test_cases,
                story_points=hu_data["story_points"],
                priority=Priority(hu_data["priority"]),
                dependencies=hu_data.get("dependencies", []),
                subtasks=subtasks,
                tags=hu_data.get("tags", [])
            )
            user_stories.append(user_story)
        
        # Ordenar por prioridad y dependencias
        return self._prioritize_stories(user_stories)
    
    def _build_system_prompt(self) -> str:
        return """Eres un experto Scrum Master y Product Owner asistido por IA.

Tu objetivo es traducir requisitos de negocio en Historias de Usuario (HU) completas y listas para desarrollo.

INSTRUCCIONES:

1. **Formato Gherkin**: Cada HU debe usar: "Como [rol] quiero [funcionalidad] para [beneficio]"

2. **Criterios de Aceptación**: Mínimo 2-3 criterios específicos, medibles y verificables por cada HU

3. **Casos de Prueba**: Genera 2-4 casos de prueba por cada HU que incluyan:
   - ID único (ej: HU1-TC1, HU1-TC2)
   - Título descriptivo del caso
   - Descripción clara del escenario a probar
   - Precondiciones (si aplica)
   - Pasos a seguir (lista ordenada)
   - Resultado esperado
   - Tipo de prueba (functional, integration, ui, api, security, performance)

4. **Story Points**: Estima usando la escala de Fibonacci (1, 2, 3, 5, 8, 13)
   - 1-2: Tarea simple, menos de 1 día
   - 3: Tarea moderada, 1-2 días
   - 5: Tarea compleja, 3-4 días
   - 8: Muy compleja, 5+ días
   - 13: Épica que debe dividirse

5. **Prioridad**: 
   - Alta: Funcionalidad core, habilitadores arquitectónicos, dependencias
   - Media: Funcionalidad importante no crítica
   - Baja: Mejoras, nice-to-have

6. **Dependencias**: Identifica HU que dependen de otras (ej: login antes de perfil de usuario)

7. **Subtareas**: Desglosa cada HU en:
   - Análisis técnico
   - Diseño de interfaz (si aplica)
   - Backend/API
   - Frontend (si aplica)
   - Pruebas unitarias
   - Pruebas de integración
   - Documentación

8. **Tags**: Agrega etiquetas relevantes (backend, frontend, auth, database, etc.)

FORMATO DE SALIDA JSON:
{
  "user_stories": [
    {
      "id": "HU1",
      "title": "Título corto",
      "gherkin": "Como [rol] quiero [funcionalidad] para [beneficio]",
      "acceptance_criteria": ["criterio 1", "criterio 2", "criterio 3"],
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
        }
      ],
      "story_points": 3,
      "priority": "Alta",
      "dependencies": [],
      "subtasks": [
        {
          "id": "HU1-ST1",
          "title": "Análisis técnico",
          "description": "Descripción detallada",
          "estimated_hours": 2
        }
      ],
      "tags": ["backend", "auth"]
    }
  ]
}

IMPORTANTE: 
- Genera casos de prueba realistas y completos
- Incluye tanto casos de éxito (happy path) como casos de error
- Los pasos deben ser claros y ejecutables
- El resultado esperado debe ser específico y verificable
- Varía los tipos de prueba según la funcionalidad (functional, ui, api, integration, security)

Genera HU completas, atómicas y accionables con casos de prueba exhaustivos."""

    def _build_user_prompt(
        self, 
        requirements: str, 
        additional_context: str = None,
        priority_guidance: str = None
    ) -> str:
        prompt = f"""REQUISITOS DE NEGOCIO:
{requirements}"""
        
        if additional_context:
            prompt += f"\n\nCONTEXTO ADICIONAL:\n{additional_context}"
        
        if priority_guidance:
            prompt += f"\n\nGUÍA DE PRIORIZACIÓN:\n{priority_guidance}"
        
        prompt += """

Genera TODAS las Historias de Usuario necesarias para cubrir estos requisitos.
Incluye HU para autenticación, autorización, CRUD, validaciones, manejo de errores, etc.
Asegúrate de que las HU estén priorizadas correctamente y tengan dependencias claras.

Responde ÚNICAMENTE con el JSON solicitado, sin texto adicional."""
        
        return prompt
    
    def _prioritize_stories(self, stories: List[UserStory]) -> List[UserStory]:
        """Ordena historias por prioridad y dependencias"""
        
        # Diccionario de prioridad
        priority_order = {Priority.ALTA: 0, Priority.MEDIA: 1, Priority.BAJA: 2}
        
        def get_priority_score(story: UserStory) -> tuple:
            # Primero por prioridad, luego por número de dependencias hacia esta HU
            dependent_count = sum(1 for s in stories if story.id in s.dependencies)
            return (priority_order[story.priority], -dependent_count, story.id)
        
        # Ordenar
        sorted_stories = sorted(stories, key=get_priority_score)
        
        return sorted_stories
    
    def suggest_sprint_planning(
        self, 
        user_stories: List[UserStory], 
        team_capacity: int,
        num_sprints: int = None
    ) -> Dict:
        """Sugiere distribución de HU en sprints"""
        
        sprints = []
        current_sprint = 1
        current_capacity = 0
        current_stories = []
        
        for story in user_stories:
            # Si la historia cabe en el sprint actual
            if current_capacity + story.story_points <= team_capacity:
                current_capacity += story.story_points
                current_stories.append(story.id)
                story.sprint_assigned = current_sprint
            else:
                # Guardar sprint actual si tiene historias
                if current_stories:
                    sprints.append({
                        "number": current_sprint,
                        "name": f"Sprint {current_sprint}",
                        "capacity": team_capacity,
                        "user_stories": current_stories,
                        "total_points": current_capacity
                    })
                    current_sprint += 1
                    
                    # Si hay límite de sprints
                    if num_sprints and current_sprint > num_sprints:
                        break
                
                # Comenzar nuevo sprint
                current_stories = [story.id]
                current_capacity = story.story_points
                story.sprint_assigned = current_sprint
        
        # Agregar último sprint si tiene historias
        if current_stories:
            sprints.append({
                "number": current_sprint,
                "name": f"Sprint {current_sprint}",
                "capacity": team_capacity,
                "user_stories": current_stories,
                "total_points": current_capacity
            })
        
        return {
            "sprints": sprints,
            "total_sprints": len(sprints),
            "total_points": sum(s["total_points"] for s in sprints)
        }
