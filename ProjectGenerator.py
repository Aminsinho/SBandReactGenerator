import os
import subprocess
import requests
import zipfile

# Instalar dependencias necesarias si no están presentes
def install_dependencies():
    print("Instalando dependencias necesarias...")
    try:
        subprocess.run(["python3", "-m", "pip", "install", "requests"], check=True)
        print("Dependencias instaladas correctamente.")
    except subprocess.CalledProcessError as e:
        print(f"Error al instalar dependencias: {e}")
        exit(1)

# Descargar y descomprimir proyecto Spring Boot desde Spring Initializr
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
            
            with zipfile.ZipFile(project_path, 'r') as zip_ref:
                zip_ref.extractall(project_dir)
            print(f"Proyecto Spring Boot descomprimido en {project_dir}")
        else:
            print(f"Error al descargar el proyecto. Código de respuesta: {response.status_code}")
            exit(1)
    except Exception as e:
        print(f"Error durante la descarga del proyecto: {e}")
        exit(1)

# Crear proyecto React con create-react-app
def create_react_project(name, install_dir):
    try:
        frontend_dir = os.path.join(install_dir, name, 'frontend')
        
        if not os.path.exists(frontend_dir):
            print(f"Creando directorio de frontend: {frontend_dir}")
            os.makedirs(frontend_dir)

        print(f"Creando proyecto React en {frontend_dir}...")
        subprocess.run(["npx", "create-react-app", "."], cwd=frontend_dir, check=True)
        
        print(f"Proyecto React creado en {frontend_dir}")
    except subprocess.CalledProcessError as e:
        print(f"Error al crear el proyecto React: {e}")
        exit(1)

# Crear Dockerfile para backend Spring Boot
def create_spring_dockerfile(name, install_dir, maven_or_gradle):
    print("Creando Dockerfile para Spring Boot...")
    dockerfile_content = f"""
FROM gradle:8.5-jdk17 AS builder

WORKDIR /app

COPY . .

RUN gradle build -x test

FROM openjdk:17-jdk-slim

WORKDIR /app

COPY ./build/libs/{name}-0.0.1-SNAPSHOT.jar /app/{name}.jar

ENTRYPOINT ["java", "-jar", "{name}.jar"]
"""
    dockerfile_path = os.path.join(install_dir, name, 'backend', 'Dockerfile')
    with open(dockerfile_path, 'w') as f:
        f.write(dockerfile_content)
    print(f"Dockerfile de Spring Boot creado en {dockerfile_path}")

# Modificar el application.properties para usar PostgreSQL
def modify_application_properties(install_dir, name):
    properties_path = os.path.join(install_dir, name, 'backend', 'src', 'main', 'resources', 'application.properties')
    
    if not os.path.exists(properties_path):
        print(f"No se encontró el archivo application.properties en {properties_path}")
        return
    
    with open(properties_path, 'a') as f:
        f.write("\n# Configuración de PostgreSQL\n")
        f.write("spring.datasource.url=jdbc:postgresql://db:5432/springbootdb\n")
        f.write("spring.datasource.username=admin\n")
        f.write("spring.datasource.password=admin\n")
        f.write("spring.jpa.hibernate.ddl-auto=update\n")
        f.write("spring.jpa.show-sql=true\n")
        f.write("\n# Configuración JPA / Hibernate\n")
        f.write("spring.jpa.hibernate.ddl-auto=update\n")
        f.write("spring.jpa.show-sql=true\n")
        f.write("spring.jpa.properties.hibernate.dialect=org.hibernate.dialect.PostgreSQLDialect\n")
        f.write("\n# Opcional: logging para debug\n")
        f.write("logging.level.org.hibernate.SQL=DEBUG\n")
        f.write("logging.level.org.hibernate.type.descriptor.sql.BasicBinder=TRACE\n")
    
    print(f"application.properties modificado para usar PostgreSQL en {properties_path}")

# Crear Dockerfile para frontend React
def create_react_dockerfile(name, install_dir):
    print("Creando Dockerfile para React...")
    dockerfile_content = f"""
FROM node:16-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 3000

CMD ["npm", "start"]
"""
    dockerfile_path = os.path.join(install_dir, name, 'frontend', 'Dockerfile')
    with open(dockerfile_path, 'w') as f:
        f.write(dockerfile_content)
    print(f"Dockerfile de React creado en {dockerfile_path}")

# Crear archivo docker-compose.yml con backend, frontend y base de datos
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

# Compilar el backend (usa Maven o Gradle, con gradlew si está disponible)
def build_backend_project(maven_or_gradle, install_dir, name):
    backend_dir = os.path.join(install_dir, name, 'backend')

    try:
        if maven_or_gradle == 'maven':
            print("Compilando el proyecto Spring Boot con Maven (omitiendo tests)...")
            subprocess.run(["mvn", "clean", "install", "-DskipTests"], cwd=backend_dir, check=True)
            print("Proyecto Spring Boot compilado correctamente con Maven.")
        elif maven_or_gradle == 'gradle':
            print("Compilando el proyecto Spring Boot con Gradle (omitiendo tests)...")
            gradlew_path = os.path.join(backend_dir, "gradlew")

            if os.path.exists(gradlew_path):
                subprocess.run(["chmod", "+x", gradlew_path], cwd=backend_dir, check=True)
                subprocess.run(["./gradlew", "build", "-x", "test"], cwd=backend_dir, check=True)
                print("Proyecto Spring Boot compilado correctamente con gradlew.")
            else:
                print("No se encontró gradlew, intentando con Gradle global...")
                subprocess.run(["gradle", "build", "-x", "test"], cwd=backend_dir, check=True)
                print("Proyecto Spring Boot compilado correctamente con Gradle global.")
        else:
            print(f"Tipo de proyecto desconocido: {maven_or_gradle}")
            exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Error al compilar el proyecto Spring Boot: {e}")
        exit(1)

# Main: flujo general del generador
def main():
    project_name = input("Ingresa el nombre del proyecto: ")
    package_name = input("Ingresa el paquete base (ej. com.amin): ")
    maven_or_gradle = input("Elige el tipo de proyecto (maven/gradle): ") or 'maven'
    dependencies = "web,data-jpa,postgresql"
    install_dir = os.getcwd()

    print(f"\n🛠 Generando el proyecto '{project_name}'...\n")
    
    download_spring_project(project_name, package_name, maven_or_gradle, dependencies, install_dir)
    build_backend_project(maven_or_gradle, install_dir, project_name)
    modify_application_properties(install_dir, project_name)
    create_react_project(project_name, install_dir)
    create_spring_dockerfile(project_name, install_dir, maven_or_gradle)
    create_react_dockerfile(project_name, install_dir)
    create_docker_compose(install_dir, project_name)
    
    print(f"\n✅ ¡Proyecto '{project_name}' generado con éxito!")

if __name__ == "__main__":
    install_dependencies()
    main()
