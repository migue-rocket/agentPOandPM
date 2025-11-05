from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum


class Priority(str, Enum):
    ALTA = "Alta"
    MEDIA = "Media"
    BAJA = "Baja"


class SubTask(BaseModel):
    """Subtarea de una Historia de Usuario"""
    id: str
    title: str
    description: Optional[str] = None
    estimated_hours: Optional[float] = None
    status: str = "Pendiente"


class TestCase(BaseModel):
    """Caso de prueba para una Historia de Usuario"""
    id: str
    title: str
    description: str
    preconditions: Optional[str] = None
    steps: List[str]
    expected_result: str
    test_type: str = Field(default="functional", description="functional, integration, ui, api, etc.")


class UserStory(BaseModel):
    """Historia de Usuario en formato Scrum"""
    id: str = Field(..., description="ID único de la HU (ej: HU1)")
    title: str = Field(..., description="Título corto de la historia")
    gherkin: str = Field(..., description="Formato: Como [rol] quiero [funcionalidad] para [beneficio]")
    acceptance_criteria: List[str] = Field(..., description="Lista de criterios de aceptación")
    test_cases: List[TestCase] = Field(default_factory=list, description="Casos de prueba")
    story_points: int = Field(..., ge=1, le=13, description="Estimación en story points (1-13)")
    priority: Priority = Field(..., description="Prioridad de negocio")
    dependencies: List[str] = Field(default_factory=list, description="IDs de HU dependientes")
    subtasks: List[SubTask] = Field(default_factory=list, description="Subtareas técnicas")
    sprint_assigned: Optional[int] = None
    status: str = "Backlog"
    tags: List[str] = Field(default_factory=list)
    
    class Config:
        use_enum_values = True


class Sprint(BaseModel):
    """Sprint de Scrum"""
    number: int
    name: str
    capacity: int = Field(..., description="Capacidad en story points")
    user_stories: List[str] = Field(default_factory=list, description="IDs de HU asignadas")
    total_points: int = 0
    completed_points: int = 0
    status: str = "Planificado"
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class Backlog(BaseModel):
    """Backlog completo del producto"""
    user_stories: List[UserStory] = Field(default_factory=list)
    sprints: List[Sprint] = Field(default_factory=list)
    team_capacity: int = Field(default=9, description="Capacidad del equipo por sprint")
    velocity_history: List[int] = Field(default_factory=list, description="Histórico de story points completados")
    current_velocity: Optional[float] = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class GenerateBacklogRequest(BaseModel):
    """Request para generar backlog desde requisitos"""
    requirements: str = Field(..., description="Requisitos de negocio en lenguaje ubicuo")
    team_capacity: int = Field(default=9, ge=1, le=100, description="Capacidad del equipo en story points por sprint")
    additional_context: Optional[str] = None
    priority_guidance: Optional[str] = None


class PlanSprintsRequest(BaseModel):
    """Request para planificar sprints"""
    backlog_id: Optional[str] = None
    team_capacity: int = Field(default=9)
    num_sprints: Optional[int] = Field(default=None, description="Número de sprints a planificar")


class UpdateVelocityRequest(BaseModel):
    """Request para actualizar velocidad del equipo"""
    sprint_number: int
    completed_points: int
    total_points: int
    feedback: Optional[str] = None


class ExportFormat(str, Enum):
    MARKDOWN = "markdown"
    CSV = "csv"
    JSON = "json"
