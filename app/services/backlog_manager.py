import json
import csv
from typing import List
from pathlib import Path
from datetime import datetime
from app.models import Backlog, UserStory, Sprint, UpdateVelocityRequest, ExportFormat
from app.config import get_settings


class BacklogManager:
    """Gestiona el backlog, sprints y velocidad del equipo"""
    
    def __init__(self):
        self.settings = get_settings()
        self.data_dir = Path(self.settings.DATA_DIR)
        self.exports_dir = Path(self.settings.EXPORTS_DIR)
        self.data_dir.mkdir(exist_ok=True)
        self.exports_dir.mkdir(exist_ok=True)
        self.backlog_file = self.data_dir / "backlog.json"
    
    def save_backlog(self, backlog: Backlog) -> None:
        """Guarda el backlog en disco"""
        backlog.updated_at = datetime.now()
        with open(self.backlog_file, 'w', encoding='utf-8') as f:
            json.dump(backlog.model_dump(mode='json'), f, indent=2, default=str, ensure_ascii=False)
    
    def load_backlog(self) -> Backlog:
        """Carga el backlog desde disco"""
        if not self.backlog_file.exists():
            return Backlog()
        
        with open(self.backlog_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return Backlog(**data)
    
    def update_velocity(self, request: UpdateVelocityRequest) -> Backlog:
        """Actualiza la velocidad del equipo basado en sprint completado"""
        backlog = self.load_backlog()
        
        # Actualizar sprint
        for sprint in backlog.sprints:
            if sprint.number == request.sprint_number:
                sprint.completed_points = request.completed_points
                sprint.status = "Completado"
                break
        
        # Agregar a historial de velocidad
        backlog.velocity_history.append(request.completed_points)
        
        # Calcular velocidad promedio (últimos 3 sprints)
        recent_velocity = backlog.velocity_history[-3:]
        backlog.current_velocity = sum(recent_velocity) / len(recent_velocity)
        
        # Ajustar capacidad del equipo si es necesario
        if len(recent_velocity) >= 3:
            backlog.team_capacity = int(backlog.current_velocity)
        
        self.save_backlog(backlog)
        return backlog
    
    def export_markdown(self, backlog: Backlog) -> str:
        """Exporta el backlog a formato Markdown"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = self.exports_dir / f"backlog_{timestamp}.md"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("# Product Backlog\n\n")
            f.write(f"**Generado:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"**Capacidad del Equipo:** {backlog.team_capacity} story points/sprint\n\n")
            
            if backlog.current_velocity:
                f.write(f"**Velocidad Actual:** {backlog.current_velocity:.1f} story points/sprint\n\n")
            
            # Tabla de historias de usuario
            f.write("## Historias de Usuario\n\n")
            f.write("| ID | Título | Gherkin | Criterios de Aceptación | Story Points | Prioridad | Sprint | Subtareas |\n")
            f.write("|---|---|---|---|---|---|---|---|\n")
            
            for story in backlog.user_stories:
                criteria_text = "; ".join(story.acceptance_criteria[:3])
                if len(story.acceptance_criteria) > 3:
                    criteria_text += "..."
                
                subtasks_text = ", ".join([st.title for st in story.subtasks[:3]])
                if len(story.subtasks) > 3:
                    subtasks_text += f" (+{len(story.subtasks)-3} más)"
                
                sprint_text = f"Sprint {story.sprint_assigned}" if story.sprint_assigned else "Backlog"
                
                f.write(f"| {story.id} | {story.title} | {story.gherkin[:50]}... | {criteria_text} | "
                       f"{story.story_points} | {story.priority} | {sprint_text} | {subtasks_text} |\n")
            
            # Detalle de historias
            f.write("\n## Detalle de Historias de Usuario\n\n")
            for story in backlog.user_stories:
                f.write(f"### {story.id}: {story.title}\n\n")
                f.write(f"**Gherkin:** {story.gherkin}\n\n")
                f.write(f"**Story Points:** {story.story_points} | **Prioridad:** {story.priority}\n\n")
                
                if story.dependencies:
                    f.write(f"**Dependencias:** {', '.join(story.dependencies)}\n\n")
                
                f.write("**Criterios de Aceptación:**\n")
                for i, criterion in enumerate(story.acceptance_criteria, 1):
                    f.write(f"{i}. {criterion}\n")
                f.write("\n")
                
                # Casos de prueba
                if story.test_cases:
                    f.write("**Casos de Prueba:**\n\n")
                    for tc in story.test_cases:
                        f.write(f"#### {tc.id}: {tc.title}\n\n")
                        f.write(f"**Descripción:** {tc.description}\n\n")
                        if tc.preconditions:
                            f.write(f"**Precondiciones:** {tc.preconditions}\n\n")
                        f.write("**Pasos:**\n")
                        for i, step in enumerate(tc.steps, 1):
                            f.write(f"{i}. {step}\n")
                        f.write(f"\n**Resultado esperado:** {tc.expected_result}\n\n")
                        f.write(f"**Tipo:** `{tc.test_type}`\n\n")
                        f.write("---\n\n")
                
                f.write("**Subtareas:**\n")
                for subtask in story.subtasks:
                    hours_text = f" ({subtask.estimated_hours}h)" if subtask.estimated_hours else ""
                    f.write(f"- {subtask.title}{hours_text}\n")
                f.write("\n")
                
                if story.tags:
                    f.write(f"**Tags:** {', '.join(story.tags)}\n\n")
                
                f.write("---\n\n")
            
            # Planificación de sprints
            if backlog.sprints:
                f.write("## Planificación de Sprints\n\n")
                for sprint in backlog.sprints:
                    f.write(f"### {sprint.name}\n\n")
                    f.write(f"**Capacidad:** {sprint.capacity} SP | **Total Asignado:** {sprint.total_points} SP | "
                           f"**Utilización:** {(sprint.total_points/sprint.capacity*100):.0f}%\n\n")
                    
                    if sprint.completed_points > 0:
                        f.write(f"**Completado:** {sprint.completed_points} SP | **Estado:** {sprint.status}\n\n")
                    
                    f.write("**Historias Asignadas:**\n")
                    for story_id in sprint.user_stories:
                        story = next((s for s in backlog.user_stories if s.id == story_id), None)
                        if story:
                            f.write(f"- {story.id}: {story.title} ({story.story_points} SP)\n")
                    f.write("\n")
            
            # Historial de velocidad
            if backlog.velocity_history:
                f.write("## Historial de Velocidad\n\n")
                f.write("| Sprint | Story Points Completados |\n")
                f.write("|---|---|\n")
                for i, velocity in enumerate(backlog.velocity_history, 1):
                    f.write(f"| Sprint {i} | {velocity} |\n")
                f.write("\n")
        
        return str(filename)
    
    def export_csv(self, backlog: Backlog) -> str:
        """Exporta el backlog a formato CSV"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = self.exports_dir / f"backlog_{timestamp}.csv"
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Encabezados
            writer.writerow([
                'ID', 'Título', 'Gherkin', 'Criterios de Aceptación', 
                'Story Points', 'Prioridad', 'Sprint Asignado', 'Dependencias',
                'Subtareas', 'Casos de Prueba', 'Tags', 'Estado'
            ])
            
            # Datos
            for story in backlog.user_stories:
                # Formatear casos de prueba para CSV
                test_cases_str = ""
                if story.test_cases:
                    test_cases_list = [f"{tc.id}: {tc.title}" for tc in story.test_cases]
                    test_cases_str = '; '.join(test_cases_list)
                
                writer.writerow([
                    story.id,
                    story.title,
                    story.gherkin,
                    '; '.join(story.acceptance_criteria),
                    story.story_points,
                    story.priority,
                    f"Sprint {story.sprint_assigned}" if story.sprint_assigned else "Backlog",
                    ', '.join(story.dependencies),
                    ', '.join([st.title for st in story.subtasks]),
                    test_cases_str,
                    ', '.join(story.tags),
                    story.status
                ])
        
        return str(filename)
    
    def export_json(self, backlog: Backlog) -> str:
        """Exporta el backlog a formato JSON"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = self.exports_dir / f"backlog_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(backlog.model_dump(mode='json'), f, indent=2, default=str, ensure_ascii=False)
        
        return str(filename)
    
    def export(self, format: ExportFormat) -> str:
        """Exporta el backlog en el formato especificado"""
        backlog = self.load_backlog()
        
        if format == ExportFormat.MARKDOWN:
            return self.export_markdown(backlog)
        elif format == ExportFormat.CSV:
            return self.export_csv(backlog)
        elif format == ExportFormat.JSON:
            return self.export_json(backlog)
        else:
            raise ValueError(f"Formato no soportado: {format}")
