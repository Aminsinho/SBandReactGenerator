import os
import subprocess
import requests

# Función para descargar el proyecto desde Spring Initializr
def download_spring_boot_project(project_name, build_tool, base_package, install_dir):
    # Configurar la URL de Spring Initializr según la opción de construcción
    if build_tool == "maven":
        build_type = "maven-project"
    else:
        build_type = "gradle-project"

    # Construir la URL sin la dependencia 'docker' ya que no es válida
    url = f"https://start.spring.io/starter.zip?dependencies=web,data-jpa,postgresql&type={build_type}&language=java&name={project_name}&packageName={base_package}&artifactId={project_name}"
    print(f"🔄 Descargando proyecto desde: {url}")

    response = requests.get(url)
    
    # Verificar si la descarga fue exitosa
    if response.status_code == 200:
        zip_path = f"{install_dir}/{project_name}/backend/{project_name.lower()}.zip"
        
        # Guardar el archivo ZIP descargado
        with open(zip_path, "wb") as f:
            f.write(response.content)
        print(f"✅ Proyecto Spring Boot descargado en {zip_path}")
        
        # Intentar descomprimir el archivo ZIP
        try:
            subprocess.run(["unzip", zip_path, "-d", f"{install_dir}/{project_name}/backend"], check=True)
            os.remove(zip_path)  # Eliminar el archivo ZIP después de descomprimirlo
            print("✅ Proyecto Spring Boot descomprimido exitosamente.")
        except subprocess.CalledProcessError as e:
            print(f"❌ Error al descomprimir el archivo ZIP: {e}")
            raise
    else:
        print(f"❌ Error al descargar el proyecto. Código de respuesta: {response.status_code}")
        print(f"Detalles: {response.text}")

def create_project_structure(project_name, install_dir):
    # Crear carpetas principales dentro del directorio de instalación
    os.makedirs(f"{install_dir}/{project_name}/backend", exist_ok=True)
    os.makedirs(f"{install_dir}/{project_name}/frontend", exist_ok=True)
    print(f"📂 Estructura de carpetas creada en {install_dir}/{project_name}")

def generate_react_app(project_name, install_dir):
    frontend_path = f"{install_dir}/{project_name}/frontend"
    print("⚛️ Generando proyecto React...")
    subprocess.run(["npx", "create-react-app", frontend_path])
    print(f"✅ Proyecto React generado en {frontend_path}")

def create_dockerfiles(project_name, install_dir, build_tool):
    # Corregir la cadena de texto que estaba mal cerrada
    backend_dockerfile = f"{install_dir}/{project_name}/backend/Dockerfile"

    if build_tool == "maven":
        with open(backend_dockerfile, "w") as f:
            f.write("""FROM openjdk:17-jdk-slim
WORKDIR /app
COPY ./target/{project_name}.jar /app/{project_name}.jar
CMD ["java", "-jar", "{project_name}.jar"]
""".format(project_name=project_name))
    else:
        with open(backend_dockerfile, "w") as f:
            f.write("""FROM openjdk:17-jdk-slim
WORKDIR /app
COPY ./build/libs/{project_name}.jar /app/{project_name}.jar
CMD ["java", "-jar", "{project_name}.jar"]
""".format(project_name=project_name))

    print(f"✅ Dockerfile para Spring Boot {build_tool} creado en {backend_dockerfile}")

    # Crear Dockerfile para el frontend
    frontend_dockerfile = f"{install_dir}/{project_name}/frontend/Dockerfile"
    with open(frontend_dockerfile, "w") as f:
        f.write("""FROM node:16-alpine
WORKDIR /app
COPY . /app
RUN npm install
CMD ["npm", "start"]
""")
    print(f"✅ Dockerfile para React creado en {frontend_dockerfile}")

def create_docker_compose(project_name, install_dir):
    # Crear archivo docker-compose.yml en el directorio raíz del proyecto
    docker_compose_path = f"{install_dir}/{project_name}/docker-compose.yml"
    with open(docker_compose_path, "w") as f:
        f.write("""version: '3'
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
      POSTGRES_DB: {project_name}
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    ports:
      - "5432:5432"
""".format(project_name=project_name))
    print(f"✅ docker-compose.yml creado en {docker_compose_path}")

# Función principal para crear el proyecto
def create_project(project_name, build_tool, base_package, install_dir):
    # Crear la estructura de carpetas
    create_project_structure(project_name, install_dir)

    # Descargar el proyecto Spring Boot
    download_spring_boot_project(project_name, build_tool, base_package, install_dir)

    # Generar el proyecto React
    generate_react_app(project_name, install_dir)

    # Crear Dockerfiles para el backend y el frontend
    create_dockerfiles(project_name, install_dir, build_tool)

    # Crear el archivo docker-compose.yml
    create_docker_compose(project_name, install_dir)

    print(f"🎉 Proyecto '{project_name}' generado exitosamente.")

if __name__ == "__main__":
    # Pide los parámetros al usuario
    project_name = input("Ingresa el nombre del proyecto: ")
    build_tool = input("Selecciona la herramienta de construcción (maven/gradle): ").lower()
    base_package = input("Ingresa el paquete base (por ejemplo, com.ejemplo): ")
    install_dir = input("Ingresa el directorio donde se instalará el proyecto: ")

    if not install_dir:
        install_dir = os.getcwd()  # Si no se ingresa un directorio, se usa el directorio actual

    create_project(project_name, build_tool, base_package, install_dir)
