#!/bin/bash

# Script de demostración del Agente Scrum Master AI
# Este script ejecuta una demostración completa del sistema

echo "╔════════════════════════════════════════════════════════════╗"
echo "║                                                             ║"
echo "║        🚀 DEMO - Agente Scrum Master AI                    ║"
echo "║                                                             ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Verificar que el entorno esté listo
if [ ! -d "venv" ]; then
    echo "❌ Entorno virtual no encontrado. Ejecuta primero:"
    echo "   python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Activar entorno
source venv/bin/activate

echo "📋 Verificando sistema..."
python verify_setup.py > /dev/null 2>&1

if [ $? -ne 0 ]; then
    echo "⚠️  Hay problemas con la configuración. Ejecuta:"
    echo "   python verify_setup.py"
    echo ""
    echo "Para ver los detalles."
    exit 1
fi

echo "✅ Sistema verificado"
echo ""

echo "═══════════════════════════════════════════════════════════"
echo "  DEMO 1: Generar Backlog desde Requisitos"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "Requisitos de ejemplo:"
echo "───────────────────────────────────────────────────────────"
cat << 'EOF'
Los usuarios deben poder registrarse con correo y contraseña;
además, deben poder recuperar contraseña vía email; 
el sistema debe permitir diferentes roles de usuario (admin, estándar).
EOF
echo "───────────────────────────────────────────────────────────"
echo ""

read -p "Presiona ENTER para generar backlog con IA..." 

# Crear archivo temporal con la request
cat > /tmp/demo_request.json << 'EOF'
{
  "requirements": "Los usuarios deben poder registrarse con correo y contraseña; además, deben poder recuperar contraseña vía email; el sistema debe permitir diferentes roles de usuario (admin, estándar).",
  "team_capacity": 9,
  "additional_context": "Stack: React + FastAPI",
  "priority_guidance": "Priorizar autenticación"
}
EOF

echo "🔄 Iniciando backend temporalmente..."
uvicorn app.main:app --port 8000 > /dev/null 2>&1 &
BACKEND_PID=$!

# Esperar a que el backend esté listo
echo "⏳ Esperando que el backend inicie..."
sleep 5

echo "🤖 Generando backlog con IA..."
echo ""

# Hacer la request
RESPONSE=$(curl -s -X POST "http://localhost:8000/api/generate-backlog" \
  -H "Content-Type: application/json" \
  -d @/tmp/demo_request.json)

# Verificar si hay error
if echo "$RESPONSE" | grep -q "error\|detail"; then
    echo "❌ Error al generar backlog:"
    echo "$RESPONSE" | python -m json.tool
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi

echo "✅ ¡Backlog generado exitosamente!"
echo ""

# Mostrar resumen
echo "═══════════════════════════════════════════════════════════"
echo "  RESUMEN DEL BACKLOG GENERADO"
echo "═══════════════════════════════════════════════════════════"
echo ""

# Extraer información del JSON
NUM_STORIES=$(echo "$RESPONSE" | python -c "import json,sys; data=json.load(sys.stdin); print(len(data['user_stories']))")
TOTAL_POINTS=$(echo "$RESPONSE" | python -c "import json,sys; data=json.load(sys.stdin); print(sum(s['story_points'] for s in data['user_stories']))")
NUM_SPRINTS=$(echo "$RESPONSE" | python -c "import json,sys; data=json.load(sys.stdin); print(len(data['sprints']))")

echo "📊 Estadísticas:"
echo "   • Historias de Usuario: $NUM_STORIES"
echo "   • Story Points Totales: $TOTAL_POINTS"
echo "   • Sprints Planificados: $NUM_SPRINTS"
echo ""

echo "📋 Historias de Usuario:"
echo ""
echo "$RESPONSE" | python -c "
import json
import sys

data = json.load(sys.stdin)
for story in data['user_stories']:
    print(f\"   {story['id']}: {story['title']}\")
    print(f\"   └─ {story['story_points']} SP | Prioridad: {story['priority']}\")
    print()
"

echo "═══════════════════════════════════════════════════════════"
echo ""

# Exportar a Markdown
echo "📄 Exportando a Markdown..."
curl -s -O -J "http://localhost:8000/api/export/markdown"

if [ $? -eq 0 ]; then
    MARKDOWN_FILE=$(ls -t backlog_*.md 2>/dev/null | head -1)
    if [ -n "$MARKDOWN_FILE" ]; then
        echo "✅ Exportado a: $MARKDOWN_FILE"
        echo ""
        echo "Vista previa (primeras 30 líneas):"
        echo "───────────────────────────────────────────────────────────"
        head -30 "$MARKDOWN_FILE"
        echo "───────────────────────────────────────────────────────────"
        echo "... (ver archivo completo para más detalles)"
        
        # Mover a exports
        mv "$MARKDOWN_FILE" exports/ 2>/dev/null
        echo ""
        echo "📁 Archivo movido a: exports/$MARKDOWN_FILE"
    fi
fi

echo ""
echo "═══════════════════════════════════════════════════════════"
echo "  DEMO COMPLETADA"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "✅ El backlog ha sido generado y exportado"
echo ""
echo "💡 Próximos pasos:"
echo "   1. Inicia la interfaz web: ./start.sh"
echo "   2. Abre http://localhost:5173"
echo "   3. Explora las historias de usuario"
echo "   4. Revisa la planificación de sprints"
echo "   5. Exporta en diferentes formatos"
echo ""
echo "📚 Documentación:"
echo "   • Guía rápida: QUICKSTART.md"
echo "   • Guía visual: VISUAL_GUIDE.md"
echo "   • Ejemplos: EJEMPLOS.md"
echo ""

# Limpiar
kill $BACKEND_PID 2>/dev/null
rm /tmp/demo_request.json 2>/dev/null

echo "🎉 ¡Gracias por probar el Agente Scrum Master AI!"
echo ""
