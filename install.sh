#!/bin/bash

# Actualizar Homebrew
echo "🔄 Actualizando Homebrew..."
brew update

# Instalar Python si no está instalado
echo "🐍 Verificando instalación de Python..."
if ! command -v python3 &> /dev/null
then
    echo "Python no está instalado. Instalando Python..."
    brew install python
else
    echo "Python ya está instalado"
fi

# Verificar si pip está instalado
echo "🔧 Verificando pip..."
if ! command -v pip3 &> /dev/null
then
    echo "pip no está instalado. Instalando pip..."
    brew install python
else
    echo "pip ya está instalado"
fi

# Instalar dependencias necesarias de Python
echo "🔄 Instalando dependencias de Python..."
pip3 install requests  # Solo instala requests, sin necesidad de requirements.txt

# Instalar pip más reciente (si es necesario)
echo "🔧 Actualizando pip..."
python3 -m pip install --upgrade pip

echo "✅ Dependencias de Python instaladas exitosamente."

# Ahora ejecutamos el script generador.py para crear el proyecto
echo "🚀 Ejecutando ProjectGenerator.py para crear el proyecto..."
python3 ProjectGenerator.py  # Ejecuta el generador de proyectos en Python

echo "🎉 Proyecto generado exitosamente"
