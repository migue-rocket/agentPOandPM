import React from 'react';

export default function UserStoryCard({ story }) {
  const priorityColors = {
    'Alta': 'badge-priority-alta',
    'Media': 'badge-priority-media',
    'Baja': 'badge-priority-baja'
  };

  return (
    <div className="user-story-card">
      <div className="story-header">
        <div>
          <span style={{ fontSize: '0.9rem', color: '#667eea', fontWeight: 'bold' }}>
            {story.id}
          </span>
          <h3 className="story-title">{story.title}</h3>
        </div>
        <div className="story-badges">
          <span className={`badge ${priorityColors[story.priority]}`}>
            {story.priority}
          </span>
          <span className="badge badge-points">
            {story.story_points} SP
          </span>
          {story.sprint_assigned && (
            <span className="badge" style={{ background: '#e6f2ff', color: '#2563eb' }}>
              Sprint {story.sprint_assigned}
            </span>
          )}
        </div>
      </div>

      <div className="story-gherkin">
        {story.gherkin}
      </div>

      {story.dependencies && story.dependencies.length > 0 && (
        <div className="story-section">
          <h4>Dependencias</h4>
          <div style={{ color: '#e53e3e', fontSize: '0.9rem' }}>
            {story.dependencies.join(', ')}
          </div>
        </div>
      )}

      <div className="story-section">
        <h4>Criterios de Aceptación</h4>
        <ul>
          {story.acceptance_criteria.map((criterion, idx) => (
            <li key={idx}>{criterion}</li>
          ))}
        </ul>
      </div>

      {story.subtasks && story.subtasks.length > 0 && (
        <div className="story-section">
          <h4>Subtareas</h4>
          <ul>
            {story.subtasks.map((subtask, idx) => (
              <li key={idx}>
                {subtask.title}
                {subtask.estimated_hours && (
                  <span style={{ color: '#666', fontSize: '0.875rem' }}>
                    {' '}({subtask.estimated_hours}h)
                  </span>
                )}
              </li>
            ))}
          </ul>
        </div>
      )}

      {story.test_cases && story.test_cases.length > 0 && (
        <div className="story-section">
          <h4>Casos de Prueba ({story.test_cases.length})</h4>
          {story.test_cases.map((testCase, idx) => (
            <div key={idx} style={{ 
              marginBottom: '1rem', 
              padding: '0.75rem', 
              background: '#f7fafc',
              borderRadius: '6px',
              borderLeft: '3px solid #667eea'
            }}>
              <div style={{ fontWeight: '600', marginBottom: '0.5rem', color: '#333' }}>
                {testCase.id}: {testCase.title}
              </div>
              <div style={{ fontSize: '0.875rem', color: '#666', marginBottom: '0.5rem' }}>
                {testCase.description}
              </div>
              {testCase.preconditions && (
                <div style={{ fontSize: '0.875rem', marginBottom: '0.5rem' }}>
                  <strong>Precondiciones:</strong> {testCase.preconditions}
                </div>
              )}
              <div style={{ fontSize: '0.875rem', marginBottom: '0.5rem' }}>
                <strong>Pasos:</strong>
                <ol style={{ marginLeft: '1.5rem', marginTop: '0.25rem' }}>
                  {testCase.steps.map((step, stepIdx) => (
                    <li key={stepIdx}>{step}</li>
                  ))}
                </ol>
              </div>
              <div style={{ fontSize: '0.875rem', marginBottom: '0.5rem' }}>
                <strong>Resultado esperado:</strong> {testCase.expected_result}
              </div>
              <span style={{ 
                fontSize: '0.75rem', 
                padding: '0.25rem 0.5rem', 
                background: '#e6f2ff', 
                color: '#2563eb',
                borderRadius: '8px',
                fontWeight: '600'
              }}>
                {testCase.test_type}
              </span>
            </div>
          ))}
        </div>
      )}

      {story.tags && story.tags.length > 0 && (
        <div className="story-tags">
          {story.tags.map((tag, idx) => (
            <span key={idx} className="tag">{tag}</span>
          ))}
        </div>
      )}
    </div>
  );
}
