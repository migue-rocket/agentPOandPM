#!/bin/bash

echo "🚀 Iniciando Agente Scrum Master AI..."
echo ""

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 no está instalado"
    exit 1
fi

# Verificar Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js no está instalado"
    exit 1
fi

# Activar entorno virtual si existe
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "⚠️  No se encontró entorno virtual. Creando..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
fi

# Verificar que las dependencias del backend estén instaladas
echo "📦 Verificando dependencias del backend..."
pip install -q -r requirements.txt

# Iniciar backend en background
echo "🔧 Iniciando backend (puerto 8000)..."
cd "$(dirname "$0")"
uvicorn app.main:app --reload --port 8000 &
BACKEND_PID=$!

# Esperar a que el backend esté listo
sleep 3

# Iniciar frontend
echo "🎨 Iniciando frontend (puerto 5173)..."
cd frontend

# Instalar dependencias si es necesario
if [ ! -d "node_modules" ]; then
    echo "📦 Instalando dependencias del frontend..."
    npm install
fi

# Iniciar frontend
npm run dev &
FRONTEND_PID=$!

echo ""
echo "✅ Aplicación iniciada!"
echo "📊 Backend: http://localhost:8000"
echo "🌐 Frontend: http://localhost:5173"
echo "📚 Docs API: http://localhost:8000/docs"
echo ""
echo "Presiona Ctrl+C para detener ambos servicios"

# Función para limpiar procesos al salir
cleanup() {
    echo ""
    echo "🛑 Deteniendo servicios..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    exit 0
}

trap cleanup INT TERM

# Mantener el script corriendo
wait
