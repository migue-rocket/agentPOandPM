import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

export const api = {
  // Generar backlog completo desde requisitos
  generateBacklog: async (requirements, teamCapacity = 9, additionalContext = '', priorityGuidance = '') => {
    const response = await axios.post(`${API_BASE_URL}/generate-backlog`, {
      requirements,
      team_capacity: teamCapacity,
      additional_context: additionalContext || null,
      priority_guidance: priorityGuidance || null
    });
    return response.data;
  },

  // Obtener backlog actual
  getBacklog: async () => {
    const response = await axios.get(`${API_BASE_URL}/backlog`);
    return response.data;
  },

  // Replanificar sprints
  planSprints: async (teamCapacity, numSprints = null) => {
    const response = await axios.post(`${API_BASE_URL}/plan-sprints`, {
      team_capacity: teamCapacity,
      num_sprints: numSprints
    });
    return response.data;
  },

  // Actualizar velocidad del equipo
  updateVelocity: async (sprintNumber, completedPoints, totalPoints, feedback = '') => {
    const response = await axios.post(`${API_BASE_URL}/update-velocity`, {
      sprint_number: sprintNumber,
      completed_points: completedPoints,
      total_points: totalPoints,
      feedback: feedback || null
    });
    return response.data;
  },

  // Exportar backlog
  exportBacklog: async (format) => {
    const response = await axios.get(`${API_BASE_URL}/export/${format}`, {
      responseType: 'blob'
    });
    
    // Crear link de descarga
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
    
    const extension = format === 'markdown' ? 'md' : format;
    link.setAttribute('download', `backlog_${Date.now()}.${extension}`);
    
    document.body.appendChild(link);
    link.click();
    link.remove();
    
    return true;
  },

  // Limpiar backlog
  clearBacklog: async () => {
    const response = await axios.delete(`${API_BASE_URL}/backlog`);
    return response.data;
  }
};
