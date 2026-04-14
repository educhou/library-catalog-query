#!/bin/bash
# Start script for Library Catalog Query Application
# Aplicação de Consulta de Catálogo para Bibliotecários

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║     📚 Sistema de Consulta de Catálogo para Bibliotecários     ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Check if Flask is installed
if ! python -c "import flask" 2>/dev/null; then
    echo "⚠️  Flask não está instalado. Instalando dependências..."
    pip install -r requirements.txt -q
    echo "✅ Dependências instaladas!"
    echo ""
fi

# Display startup information
echo "🚀 Iniciando aplicação..."
echo ""
echo "📍 A aplicação estará disponível em:"
echo "   👉 http://localhost:5000"
echo ""
echo "📊 Função: Consultar dados de livros por ISBN, Título ou Autor"
echo "🔗 Fonte: Open Library API"
echo ""
echo "⌨️  Pressione Ctrl+C para parar a aplicação"
echo ""
echo "════════════════════════════════════════════════════════════════"
echo ""

# Run the Flask app
python app.py
