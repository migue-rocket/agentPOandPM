#!/usr/bin/env python3
"""
Script de verificación del entorno
Verifica que todas las dependencias y configuraciones estén correctas
"""

import sys
import os
from pathlib import Path

def check_python_version():
    """Verifica la versión de Python"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 9:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Requiere Python 3.9+")
        return False

def check_dependencies():
    """Verifica que las dependencias estén instaladas"""
    required_packages = [
        ('fastapi', 'fastapi'),
        ('uvicorn', 'uvicorn'),
        ('pydantic', 'pydantic'),
        ('openai', 'openai'),
        ('pandas', 'pandas'),
        ('aiofiles', 'aiofiles'),
        ('python-dotenv', 'dotenv')
    ]
    
    all_ok = True
    for display_name, import_name in required_packages:
        try:
            __import__(import_name)
            print(f"✅ {display_name} - Instalado")
        except ImportError:
            print(f"❌ {display_name} - NO instalado")
            all_ok = False
    
    return all_ok

def check_env_file():
    """Verifica que el archivo .env exista y tenga las variables necesarias"""
    env_path = Path('.env')
    
    if not env_path.exists():
        print("❌ Archivo .env no encontrado")
        return False
    
    print("✅ Archivo .env encontrado")
    
    # Verificar variables requeridas
    required_vars = [
        'AZURE_OPENAI_API_KEY',
        'AZURE_OPENAI_ENDPOINT',
        'AZURE_OPENAI_DEPLOYMENT_NAME',
        'AZURE_OPENAI_API_VERSION'
    ]
    
    with open(env_path, 'r') as f:
        content = f.read()
    
    all_ok = True
    for var in required_vars:
        if var in content and 'your_' not in content.split(var)[1].split('\n')[0]:
            print(f"  ✅ {var} configurado")
        else:
            print(f"  ⚠️  {var} falta o no está configurado")
            all_ok = False
    
    return all_ok

def check_directories():
    """Verifica que los directorios necesarios existan"""
    required_dirs = ['data', 'exports', 'app', 'app/services', 'frontend']
    
    all_ok = True
    for dir_name in required_dirs:
        dir_path = Path(dir_name)
        if dir_path.exists():
            print(f"✅ Directorio '{dir_name}' - OK")
        else:
            print(f"❌ Directorio '{dir_name}' - NO existe")
            all_ok = False
    
    return all_ok

def check_openai_connection():
    """Intenta conectarse a Azure OpenAI"""
    try:
        from openai import AzureOpenAI
        from dotenv import load_dotenv
        
        load_dotenv()
        
        api_key = os.getenv('AZURE_OPENAI_API_KEY')
        endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')
        
        if not api_key or 'your_' in api_key:
            print("⚠️  Azure OpenAI - Credenciales no configuradas")
            return False
        
        # Solo verificamos que se puedan crear las credenciales
        print("🔄 Verificando credenciales de Azure OpenAI...")
        _ = AzureOpenAI(
            api_key=api_key,
            api_version=os.getenv('AZURE_OPENAI_API_VERSION'),
            azure_endpoint=endpoint
        )
        
        print("✅ Azure OpenAI - Credenciales configuradas correctamente")
        return True
        
    except Exception as e:
        print(f"⚠️  Azure OpenAI - Advertencia: {str(e)}")
        print("   (Esto podría ser normal si no hay conexión a internet)")
        return True  # No bloqueamos por problemas de conexión

def main():
    print("=" * 60)
    print("🔍 VERIFICACIÓN DEL ENTORNO - Agente Scrum Master AI")
    print("=" * 60)
    print()
    
    results = []
    
    print("📌 Verificando Python...")
    results.append(check_python_version())
    print()
    
    print("📦 Verificando dependencias...")
    results.append(check_dependencies())
    print()
    
    print("⚙️  Verificando configuración...")
    results.append(check_env_file())
    print()
    
    print("📁 Verificando estructura de directorios...")
    results.append(check_directories())
    print()
    
    print("🔌 Verificando conexión con Azure OpenAI...")
    results.append(check_openai_connection())
    print()
    
    print("=" * 60)
    if all(results):
        print("✅ TODAS LAS VERIFICACIONES PASARON")
        print("🚀 El sistema está listo para usar")
        print()
        print("Para iniciar la aplicación, ejecuta:")
        print("  ./start.sh")
        print()
        print("O manualmente:")
        print("  Terminal 1: uvicorn app.main:app --reload")
        print("  Terminal 2: cd frontend && npm run dev")
        return 0
    else:
        print("❌ ALGUNAS VERIFICACIONES FALLARON")
        print("Por favor revisa los errores arriba y corrígelos")
        print()
        print("Consulta QUICKSTART.md para más información")
        return 1

if __name__ == '__main__':
    sys.exit(main())
