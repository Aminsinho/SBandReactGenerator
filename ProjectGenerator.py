import os
import subprocess
import requests
import zipfile

# Verificar si es necesario instalar alguna dependencia
def install_dependencies():
    print("Instalando dependencias necesarias...")
    try:
        subprocess.run(["python3", "-m", "pip", "install", "requests"], check=True)
        print("Dependencias instaladas correctamente.")
    except subprocess.CalledProcessError as e:
        print(f"Error al instalar dependencias: {e}")
        exit(1)

# Descargar proyecto desde Spring Initializr
def download_spring_project(name, package_name, maven_or_gradle, dependencies, install_dir):
    url = f"https://start.spring.io/starter.zip?dependencies={dependencies}&type={maven_or_gradle}-project&language=java&name={name}&packageName={package_name}&artifactId={name}"
    
    print(f"Descargando proyecto Spring Boot desde: {url}")
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            project_dir = os.path.join(install_dir, name, 'backend')
            if not os.path.exists(project_dir):
                print(f"Creando directorio de backend: {project_dir}")
                os.makedirs(project_dir)

            project_path = os.path.join(project_dir, f'{name}.zip')
            
            with open(project_path, 'wb') as f:
                f.write(response.content)
            
            print(f"Proyecto Spring Boot descargado en {project_path}")
            # Descomprimir el archivo ZIP descargado
            with zipfile.ZipFile(project_path, 'r') as zip_ref:
                zip_ref.extractall(project_dir)
            print(f"Proyecto Spring Boot descomprimido en {project_dir}")
        else:
            print(f"Error al descargar el proyecto. Código de respuesta: {response.status_code}")
            exit(1)
    except Exception as e:
        print(f"Error durante la descarga del proyecto: {e}")
        exit(1)

# Crear proyecto React
def create_react_project(name, install_dir):
    try:
        # Definimos el directorio para el frontend directamente sin subdirectorio adicional
        frontend_dir = os.path.join(install_dir, name, 'frontend')
        
        # Verificamos si el directorio de frontend ya existe, si no, lo creamos
        if not os.path.exists(frontend_dir):
            print(f"Creando directorio de frontend: {frontend_dir}")
            os.makedirs(frontend_dir)

        # Creamos el proyecto de React directamente en el directorio frontend
        print(f"Creando proyecto React en {frontend_dir}...")
        subprocess.run(["npx", "create-react-app", "."], cwd=frontend_dir, check=True)
        
        print(f"Proyecto React creado en {frontend_dir}")
    except subprocess.CalledProcessError as e:
        print(f"Error al crear el proyecto React: {e}")
        exit(1)

# Crear Dockerfile para Spring Boot
def create_spring_dockerfile(name, install_dir, maven_or_gradle):
    print("Creando Dockerfile para Spring Boot...")
    dockerfile_content = f"""
FROM openjdk:17-jdk-slim

WORKDIR /app

COPY ./target/{name}.jar /app/{name}.jar

ENTRYPOINT ["java", "-jar", "{name}.jar"]
"""
    dockerfile_path = os.path.join(install_dir, name, 'backend', 'Dockerfile')
    with open(dockerfile_path, 'w') as f:
        f.write(dockerfile_content)
    print(f"Dockerfile de Spring Boot creado en {dockerfile_path}")

# Crear Dockerfile para React
def create_react_dockerfile(name, install_dir):
    print("Creando Dockerfile para React...")
    dockerfile_content = f"""
# Usar la imagen oficial de Node.js
FROM node:16-alpine

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar el package.json y package-lock.json
COPY package*.json ./

# Instalar las dependencias de React
RUN npm install

# Copiar todo el código fuente
COPY . .

# Exponer el puerto en el que React se ejecuta
EXPOSE 3000

# Iniciar la aplicación
CMD ["npm", "start"]
"""
    dockerfile_path = os.path.join(install_dir, name, 'frontend', 'Dockerfile')
    with open(dockerfile_path, 'w') as f:
        f.write(dockerfile_content)
    print(f"Dockerfile de React creado en {dockerfile_path}")

# Crear el archivo docker-compose.yml
def create_docker_compose(install_dir, project_name):
    print("Creando docker-compose.yml...")
    docker_compose_content = f"""
version: '3.8'

services:
  backend:
    build:
      context: ./backend
    ports:
      - "8080:8080"
    depends_on:
      - db

  frontend:
    build:
      context: ./frontend
    ports:
      - "3000:3000"

  db:
    image: postgres:latest
    environment:
      POSTGRES_DB: springbootdb
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: admin
    ports:
      - "5432:5432"
"""
    docker_compose_path = os.path.join(install_dir, project_name, 'docker-compose.yml')
    with open(docker_compose_path, 'w') as f:
        f.write(docker_compose_content)
    print(f"docker-compose.yml creado en {docker_compose_path}")

def main():
    # Obtener detalles del proyecto
    project_name = input("Ingresa el nombre del proyecto: ")
    package_name = input("Ingresa el paquete base (ej. com.amin): ")
    maven_or_gradle = input("Elige el tipo de proyecto (maven/gradle): ") or 'maven'
    dependencies = "web,data-jpa,postgresql"  # Esto puede ser personalizado
    install_dir = os.getcwd()

    # Llamar las funciones
    print(f"Generando el proyecto {project_name}...")
    download_spring_project(project_name, package_name, maven_or_gradle, dependencies, install_dir)
    create_react_project(project_name, install_dir)
    create_spring_dockerfile(project_name, install_dir, maven_or_gradle)
    create_react_dockerfile(project_name, install_dir)
    create_docker_compose(install_dir, project_name)
    print(f"¡Proyecto '{project_name}' generado con éxito!")

if __name__ == "__main__":
    install_dependencies()
    main()
