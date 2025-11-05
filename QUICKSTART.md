# Guía de Inicio Rápido

## 🚀 Inicio en 3 Pasos

### 1. Instalar Dependencias

**Backend:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Frontend:**
```bash
cd frontend
npm install
```

### 2. Configurar Credenciales

Las credenciales de Azure OpenAI ya están configuradas en `.env`

### 3. Iniciar Aplicación

```bash
./start.sh
```

O manualmente:

**Terminal 1 - Backend:**
```bash
source venv/bin/activate
uvicorn app.main:app --reload
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

## 📱 Acceder a la Aplicación

- **Frontend:** http://localhost:5173
- **API Docs:** http://localhost:8000/docs
- **API Backend:** http://localhost:8000

## 🎯 Primer Uso

1. Ve a la pestaña "📝 Generar Backlog"
2. Ingresa tus requisitos de negocio (puedes usar un ejemplo de `EJEMPLOS.md`)
3. Define la capacidad de tu equipo (ej: 9 story points)
4. Haz clic en "✨ Generar Backlog con IA"
5. Espera unos segundos mientras la IA genera las historias
6. Explora las pestañas "📋 Historias de Usuario" y "🏃 Sprints"

## 💡 Ejemplo Rápido

**Requisitos:**
```
Los usuarios deben poder registrarse con correo y contraseña, 
recuperar contraseña vía email, y el sistema debe soportar 
roles de admin y usuario estándar.
```

**Capacidad:** 9 SP

Esto generará aproximadamente 3-5 historias de usuario con sus criterios de aceptación, estimaciones y planificación de sprints.

## 📤 Exportar Resultados

Una vez generado el backlog:
- Haz clic en "📄 Exportar Markdown" para documentación completa
- Haz clic en "📊 Exportar CSV" para importar a Excel/Linear/Jira
- Haz clic en "🔧 Exportar JSON" para datos estructurados

Los archivos se guardarán en la carpeta `exports/`

## 📈 Actualizar Velocidad

Después de completar un sprint:
1. Haz clic en "📈 Actualizar Velocidad"
2. Ingresa el número de sprint completado
3. Ingresa los story points realmente completados
4. El sistema ajustará automáticamente la velocidad del equipo

## 🆘 Solución de Problemas

**Error de conexión a Azure OpenAI:**
- Verifica que las credenciales en `.env` sean correctas
- Comprueba que tu suscripción de Azure esté activa

**Puerto en uso:**
- Backend (8000): `lsof -ti:8000 | xargs kill`
- Frontend (5173): `lsof -ti:5173 | xargs kill`

**Módulos no encontrados:**
```bash
# Backend
source venv/bin/activate
pip install -r requirements.txt

# Frontend
cd frontend
rm -rf node_modules package-lock.json
npm install
```

## 📚 Documentación Completa

- `README.md` - Visión general y guía de usuario
- `TECHNICAL_DOCS.md` - Arquitectura y detalles técnicos
- `EJEMPLOS.md` - Ejemplos de requisitos de negocio
- `/docs` (API) - Documentación interactiva de la API

## 🎓 Conceptos Clave

**Story Points:** Unidad de estimación de esfuerzo (1, 2, 3, 5, 8, 13)
- 1-2 SP: Menos de 1 día
- 3 SP: 1-2 días
- 5 SP: 3-4 días
- 8 SP: ~1 semana
- 13 SP: Muy grande, considerar dividir

**Capacidad del Equipo:** Cuántos story points puede completar el equipo por sprint
- Equipo pequeño (2-3 devs): 6-9 SP
- Equipo mediano (4-5 devs): 9-15 SP
- Equipo grande (6+ devs): 15-25 SP

**Velocidad:** Promedio de story points completados en sprints anteriores. El sistema ajusta automáticamente la planificación basándose en la velocidad real.

## ✅ Checklist de Verificación

- [ ] Python 3.9+ instalado
- [ ] Node.js 16+ instalado
- [ ] Dependencias del backend instaladas
- [ ] Dependencias del frontend instaladas
- [ ] Archivo `.env` configurado
- [ ] Backend corriendo en puerto 8000
- [ ] Frontend corriendo en puerto 5173
- [ ] Puedes acceder a http://localhost:5173

¡Listo para generar tu primer backlog! 🚀
