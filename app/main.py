from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from app.config import get_settings
from app.models import (
    GenerateBacklogRequest, 
    PlanSprintsRequest,
    UpdateVelocityRequest,
    Backlog,
    Sprint,
    ExportFormat
)
from app.services.ai_agent import AIAgent
from app.services.backlog_manager import BacklogManager


# Inicializar aplicación
settings = get_settings()
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Agente Scrum Master & Product Owner asistido por IA"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Servicios
ai_agent = AIAgent()
backlog_manager = BacklogManager()


@app.get("/")
async def root():
    """Endpoint de bienvenida"""
    return {
        "message": "Agente Scrum Master & Product Owner AI",
        "version": settings.APP_VERSION,
        "status": "online"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.post("/api/generate-backlog", response_model=Backlog)
async def generate_backlog(request: GenerateBacklogRequest):
    """
    Genera un backlog completo desde requisitos de negocio.
    
    Incluye:
    - Historias de Usuario en formato Gherkin
    - Criterios de aceptación
    - Estimación en story points
    - Priorización
    - Subtareas técnicas
    - Planificación inicial de sprints
    """
    try:
        # Generar historias de usuario
        user_stories = ai_agent.generate_user_stories(
            requirements=request.requirements,
            additional_context=request.additional_context,
            priority_guidance=request.priority_guidance
        )
        
        # Crear backlog
        backlog = Backlog(
            user_stories=user_stories,
            team_capacity=request.team_capacity
        )
        
        # Planificar sprints
        sprint_plan = ai_agent.suggest_sprint_planning(
            user_stories=user_stories,
            team_capacity=request.team_capacity
        )
        
        # Agregar sprints al backlog
        backlog.sprints = [
            Sprint(
                number=s["number"],
                name=s["name"],
                capacity=s["capacity"],
                user_stories=s["user_stories"],
                total_points=s["total_points"]
            )
            for s in sprint_plan["sprints"]
        ]
        
        # Guardar backlog
        backlog_manager.save_backlog(backlog)
        
        return backlog
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generando backlog: {str(e)}")


@app.post("/api/plan-sprints", response_model=Backlog)
async def plan_sprints(request: PlanSprintsRequest):
    """
    Replanifica sprints del backlog existente.
    
    Útil cuando:
    - Cambia la capacidad del equipo
    - Se ajusta la priorización
    - Se actualiza la velocidad
    """
    try:
        backlog = backlog_manager.load_backlog()
        
        if not backlog.user_stories:
            raise HTTPException(status_code=404, detail="No hay historias de usuario en el backlog")
        
        # Actualizar capacidad si se proporciona
        if request.team_capacity:
            backlog.team_capacity = request.team_capacity
        
        # Usar velocidad actual si está disponible
        capacity = backlog.current_velocity or backlog.team_capacity
        
        # Replanificar sprints
        sprint_plan = ai_agent.suggest_sprint_planning(
            user_stories=backlog.user_stories,
            team_capacity=int(capacity),
            num_sprints=request.num_sprints
        )
        
        # Actualizar sprints
        backlog.sprints = [
            Sprint(
                number=s["number"],
                name=s["name"],
                capacity=s["capacity"],
                user_stories=s["user_stories"],
                total_points=s["total_points"]
            )
            for s in sprint_plan["sprints"]
        ]
        
        # Guardar
        backlog_manager.save_backlog(backlog)
        
        return backlog
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error planificando sprints: {str(e)}")


@app.post("/api/update-velocity", response_model=Backlog)
async def update_velocity(request: UpdateVelocityRequest):
    """
    Actualiza la velocidad del equipo basado en un sprint completado.
    
    El sistema ajustará automáticamente:
    - Velocidad promedio del equipo
    - Capacidad futura de sprints
    - Replanificación si es necesario
    """
    try:
        backlog = backlog_manager.update_velocity(request)
        return backlog
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error actualizando velocidad: {str(e)}")


@app.get("/api/backlog", response_model=Backlog)
async def get_backlog():
    """Obtiene el backlog actual"""
    try:
        backlog = backlog_manager.load_backlog()
        return backlog
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo backlog: {str(e)}")


@app.get("/api/export/{format}")
async def export_backlog(format: ExportFormat):
    """
    Exporta el backlog en el formato especificado.
    
    Formatos soportados:
    - markdown: Documento Markdown con tablas y detalles
    - csv: CSV compatible con herramientas como Excel, Linear, Jira
    - json: JSON estructurado completo
    """
    try:
        filepath = backlog_manager.export(format)
        
        # Determinar media type
        media_type = {
            ExportFormat.MARKDOWN: "text/markdown",
            ExportFormat.CSV: "text/csv",
            ExportFormat.JSON: "application/json"
        }.get(format, "text/plain")
        
        return FileResponse(
            filepath,
            media_type=media_type,
            filename=filepath.split('/')[-1]
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error exportando backlog: {str(e)}")


@app.delete("/api/backlog")
async def clear_backlog():
    """Elimina el backlog actual"""
    try:
        backlog_manager.backlog_file.unlink(missing_ok=True)
        return {"message": "Backlog eliminado exitosamente"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error eliminando backlog: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
