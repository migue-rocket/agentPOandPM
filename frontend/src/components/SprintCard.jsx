import React from 'react';

export default function SprintCard({ sprint, userStories }) {
  const utilizationPercent = (sprint.total_points / sprint.capacity) * 100;
  const completionPercent = sprint.completed_points > 0 
    ? (sprint.completed_points / sprint.total_points) * 100 
    : 0;

  return (
    <div className="sprint-card">
      <div className="sprint-header">
        <h3 className="sprint-title">{sprint.name}</h3>
        <div className="sprint-capacity">
          <strong>{sprint.total_points}</strong> / {sprint.capacity} SP
          <span style={{ 
            marginLeft: '1rem', 
            color: utilizationPercent > 90 ? '#e53e3e' : '#48bb78' 
          }}>
            ({utilizationPercent.toFixed(0)}%)
          </span>
        </div>
      </div>

      {sprint.status === 'Completado' && (
        <div className="alert alert-success">
          ✓ Completado: {sprint.completed_points} de {sprint.total_points} SP
        </div>
      )}

      <div className="progress-bar">
        <div 
          className="progress-fill" 
          style={{ 
            width: `${sprint.status === 'Completado' ? completionPercent : utilizationPercent}%` 
          }}
        />
      </div>

      <div className="sprint-stories">
        {sprint.user_stories.map((storyId) => {
          const story = userStories.find(s => s.id === storyId);
          if (!story) return null;
          
          return (
            <div key={storyId} className="sprint-story-item">
              <div>
                <strong>{story.id}</strong>: {story.title}
              </div>
              <div className="story-badges">
                <span className="badge badge-points">{story.story_points} SP</span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
