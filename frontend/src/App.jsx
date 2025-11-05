import React, { useState, useEffect } from 'react';
import './App.css';
import { api } from './services/api';
import UserStoryCard from './components/UserStoryCard';
import SprintCard from './components/SprintCard';

function App() {
  const [requirements, setRequirements] = useState('');
  const [teamCapacity, setTeamCapacity] = useState(9);
  const [additionalContext, setAdditionalContext] = useState('');
  const [backlog, setBacklog] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  const [activeTab, setActiveTab] = useState('form');
  
  // Cargar backlog existente al montar
  useEffect(() => {
    loadBacklog();
  }, []);

  const loadBacklog = async () => {
    try {
      const data = await api.getBacklog();
      if (data.user_stories && data.user_stories.length > 0) {
        setBacklog(data);
        setActiveTab('backlog');
      }
    } catch (err) {
      console.log('No hay backlog previo');
    }
  };

  const handleGenerateBacklog = async (e) => {
    e.preventDefault();
    
    if (!requirements.trim()) {
      setError('Por favor ingresa los requisitos');
      return;
    }

    setLoading(true);
    setError(null);
    setSuccess(null);

    try {
      const data = await api.generateBacklog(
        requirements,
        teamCapacity,
        additionalContext
      );
      
      setBacklog(data);
      setSuccess('¡Backlog generado exitosamente!');
      setActiveTab('backlog');
      
      // Limpiar formulario
      setRequirements('');
      setAdditionalContext('');
      
    } catch (err) {
      setError('Error al generar backlog: ' + (err.response?.data?.detail || err.message));
    } finally {
      setLoading(false);
    }
  };

  const handleUpdateVelocity = async () => {
    const sprintNumber = prompt('¿Qué sprint fue completado? (número)');
    if (!sprintNumber) return;

    const completedPoints = prompt('¿Cuántos story points se completaron?');
    if (!completedPoints) return;

    const sprint = backlog.sprints.find(s => s.number === parseInt(sprintNumber));
    if (!sprint) {
      setError('Sprint no encontrado');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const data = await api.updateVelocity(
        parseInt(sprintNumber),
        parseInt(completedPoints),
        sprint.total_points
      );
      
      setBacklog(data);
      setSuccess(`Velocidad actualizada. Nueva velocidad promedio: ${data.current_velocity?.toFixed(1)} SP`);
      
    } catch (err) {
      setError('Error al actualizar velocidad: ' + (err.response?.data?.detail || err.message));
    } finally {
      setLoading(false);
    }
  };

  const handleExport = async (format) => {
    setLoading(true);
    try {
      await api.exportBacklog(format);
      setSuccess(`Backlog exportado en formato ${format}`);
    } catch (err) {
      setError('Error al exportar: ' + (err.response?.data?.detail || err.message));
    } finally {
      setLoading(false);
    }
  };

  const handleClearBacklog = async () => {
    if (!confirm('¿Estás seguro de eliminar el backlog actual?')) return;

    setLoading(true);
    try {
      await api.clearBacklog();
      setBacklog(null);
      setSuccess('Backlog eliminado');
      setActiveTab('form');
    } catch (err) {
      setError('Error al eliminar backlog: ' + (err.response?.data?.detail || err.message));
    } finally {
      setLoading(false);
    }
  };

  // Calcular estadísticas
  const stats = backlog ? {
    totalStories: backlog.user_stories.length,
    totalPoints: backlog.user_stories.reduce((sum, story) => sum + story.story_points, 0),
    totalSprints: backlog.sprints.length,
    velocity: backlog.current_velocity
  } : null;

  return (
    <div className="app-container">
      {/* Header */}
      <header className="app-header">
        <h1>🚀 Agente Scrum Master AI</h1>
        <p>Traduce requisitos de negocio en artefactos Scrum completos</p>
      </header>

      {/* Alerts */}
      {error && (
        <div className="alert alert-error">
          {error}
          <button 
            onClick={() => setError(null)}
            style={{ float: 'right', background: 'none', border: 'none', cursor: 'pointer' }}
          >
            ✕
          </button>
        </div>
      )}

      {success && (
        <div className="alert alert-success">
          {success}
          <button 
            onClick={() => setSuccess(null)}
            style={{ float: 'right', background: 'none', border: 'none', cursor: 'pointer' }}
          >
            ✕
          </button>
        </div>
      )}

      {/* Tabs */}
      <div style={{ marginBottom: '2rem' }}>
        <div style={{ display: 'flex', gap: '1rem', borderBottom: '2px solid #e0e0e0' }}>
          <button
            onClick={() => setActiveTab('form')}
            style={{
              padding: '1rem 2rem',
              background: activeTab === 'form' ? 'white' : 'transparent',
              border: 'none',
              borderBottom: activeTab === 'form' ? '3px solid #667eea' : 'none',
              cursor: 'pointer',
              fontWeight: activeTab === 'form' ? 'bold' : 'normal',
              color: activeTab === 'form' ? '#667eea' : '#666'
            }}
          >
            📝 Generar Backlog
          </button>
          {backlog && (
            <>
              <button
                onClick={() => setActiveTab('backlog')}
                style={{
                  padding: '1rem 2rem',
                  background: activeTab === 'backlog' ? 'white' : 'transparent',
                  border: 'none',
                  borderBottom: activeTab === 'backlog' ? '3px solid #667eea' : 'none',
                  cursor: 'pointer',
                  fontWeight: activeTab === 'backlog' ? 'bold' : 'normal',
                  color: activeTab === 'backlog' ? '#667eea' : '#666'
                }}
              >
                📋 Historias de Usuario
              </button>
              <button
                onClick={() => setActiveTab('sprints')}
                style={{
                  padding: '1rem 2rem',
                  background: activeTab === 'sprints' ? 'white' : 'transparent',
                  border: 'none',
                  borderBottom: activeTab === 'sprints' ? '3px solid #667eea' : 'none',
                  cursor: 'pointer',
                  fontWeight: activeTab === 'sprints' ? 'bold' : 'normal',
                  color: activeTab === 'sprints' ? '#667eea' : '#666'
                }}
              >
                🏃 Sprints
              </button>
            </>
          )}
        </div>
      </div>

      {/* Loading */}
      {loading && (
        <div className="loading">
          <div className="spinner"></div>
          <p>Procesando con IA...</p>
        </div>
      )}

      {/* Form Tab */}
      {activeTab === 'form' && !loading && (
        <div className="card">
          <h2>Generar Backlog desde Requisitos</h2>
          <form onSubmit={handleGenerateBacklog}>
            <div className="form-group">
              <label htmlFor="requirements">
                Requisitos de Negocio *
              </label>
              <textarea
                id="requirements"
                value={requirements}
                onChange={(e) => setRequirements(e.target.value)}
                placeholder="Ejemplo: Los usuarios deben poder registrarse con correo y contraseña; además, deben poder recuperar contraseña vía email; el sistema debe permitir diferentes roles de usuario (admin, estándar)..."
                required
              />
              <small>Describe los requisitos en lenguaje natural</small>
            </div>

            <div className="form-group">
              <label htmlFor="capacity">
                Capacidad del Equipo (Story Points por Sprint) *
              </label>
              <input
                type="number"
                id="capacity"
                value={teamCapacity}
                onChange={(e) => setTeamCapacity(parseInt(e.target.value) || 9)}
                min="1"
                max="100"
                required
              />
              <small>¿Cuántos story points puede completar tu equipo por sprint?</small>
            </div>

            <div className="form-group">
              <label htmlFor="context">
                Contexto Adicional (Opcional)
              </label>
              <textarea
                id="context"
                value={additionalContext}
                onChange={(e) => setAdditionalContext(e.target.value)}
                placeholder="Stack tecnológico, restricciones, consideraciones especiales..."
                style={{ minHeight: '100px' }}
              />
            </div>

            <button type="submit" className="btn btn-primary" disabled={loading}>
              ✨ Generar Backlog con IA
            </button>
          </form>
        </div>
      )}

      {/* Backlog Tab */}
      {activeTab === 'backlog' && backlog && !loading && (
        <>
          {/* Stats */}
          <div className="stats-grid">
            <div className="stat-card">
              <div className="stat-value">{stats.totalStories}</div>
              <div className="stat-label">Historias de Usuario</div>
            </div>
            <div className="stat-card">
              <div className="stat-value">{stats.totalPoints}</div>
              <div className="stat-label">Story Points Totales</div>
            </div>
            <div className="stat-card">
              <div className="stat-value">{stats.totalSprints}</div>
              <div className="stat-label">Sprints Planificados</div>
            </div>
            {stats.velocity && (
              <div className="stat-card">
                <div className="stat-value">{stats.velocity.toFixed(1)}</div>
                <div className="stat-label">Velocidad Promedio</div>
              </div>
            )}
          </div>

          {/* Actions */}
          <div className="card">
            <div className="button-group">
              <button 
                onClick={() => handleExport('markdown')} 
                className="btn btn-secondary"
                disabled={loading}
              >
                📄 Exportar Markdown
              </button>
              <button 
                onClick={() => handleExport('csv')} 
                className="btn btn-secondary"
                disabled={loading}
              >
                📊 Exportar CSV
              </button>
              <button 
                onClick={() => handleExport('json')} 
                className="btn btn-secondary"
                disabled={loading}
              >
                🔧 Exportar JSON
              </button>
              <button 
                onClick={handleUpdateVelocity} 
                className="btn btn-primary"
                disabled={loading}
              >
                📈 Actualizar Velocidad
              </button>
              <button 
                onClick={handleClearBacklog} 
                className="btn btn-danger"
                disabled={loading}
              >
                🗑️ Limpiar Backlog
              </button>
            </div>
          </div>

          {/* User Stories */}
          <div className="card">
            <h2>Historias de Usuario ({backlog.user_stories.length})</h2>
            <div className="user-stories-grid">
              {backlog.user_stories.map((story) => (
                <UserStoryCard key={story.id} story={story} />
              ))}
            </div>
          </div>
        </>
      )}

      {/* Sprints Tab */}
      {activeTab === 'sprints' && backlog && !loading && (
        <div className="card">
          <h2>Planificación de Sprints</h2>
          <p style={{ marginBottom: '2rem', color: '#666' }}>
            Capacidad del equipo: <strong>{backlog.team_capacity} SP/sprint</strong>
            {backlog.current_velocity && (
              <> | Velocidad actual: <strong>{backlog.current_velocity.toFixed(1)} SP/sprint</strong></>
            )}
          </p>
          
          <div className="sprints-grid">
            {backlog.sprints.map((sprint) => (
              <SprintCard 
                key={sprint.number} 
                sprint={sprint} 
                userStories={backlog.user_stories}
              />
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
