#!/bin/bash

# Función para verificar la instalación de un programa
function check_and_install() {
    if ! command -v $1 &> /dev/null
    then
        echo "$1 no encontrado. Instalando..."
        $2
    else
        echo "$1 ya está instalado."
    fi
}

# Instalación de Homebrew si no está presente
check_and_install "brew" "/bin/bash -c \"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""

# Instalación de Python y pip si no están presentes
check_and_install "python3" "brew install python"
check_and_install "pip" "python3 -m ensurepip --upgrade"

# Instalación de Maven si no está presente
check_and_install "mvn" "brew install maven"

# Instalación de Docker si no está presente
check_and_install "docker" "brew install --cask docker"

# Verificación de las dependencias de Python
echo "Instalando dependencias de Python..."
python3 -m pip install requests

echo "Instalación completada. Ahora se ejecutará el generador de proyectos."

# Llamar al generador.py
python3 ProjectGenerator.py
