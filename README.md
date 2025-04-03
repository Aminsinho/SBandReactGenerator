# ProjectGen

Este proyecto tiene como objetivo generar la estructura básica para proyectos que combinan **React** en el frontend y **Spring Boot** en el backend, utilizando **PostgreSQL** como base de datos. Todo esto se configura para ejecutarse dentro de contenedores **Docker**.

## Características

- Generación automática de la estructura de un proyecto React.
- Configuración inicial de un backend con Spring Boot.
- Integración con PostgreSQL como base de datos.
- Configuración lista para ejecutar en contenedores Docker.

## Requisitos previos

Antes de usar este proyecto, asegúrate de tener instalados los siguientes programas:

- [Docker](https://www.docker.com/)
- [Node.js](https://nodejs.org/) (para React)
- [Java JDK](https://www.oracle.com/java/technologies/javase-downloads.html) (para Spring Boot)

## Uso

1. Clona este repositorio en tu máquina local:
   ```bash
   git clone <URL_DEL_REPOSITORIO>
   ```

2. Ejecuta el script de generación para crear la estructura del proyecto.

3. Construye y levanta los contenedores Docker:
   ```bash
   docker-compose up --build
   ```

4. Accede a la aplicación:
   - Frontend: `http://localhost:3000`
   - Backend: `http://localhost:8080`

## Estructura del proyecto

El proyecto generado tendrá la siguiente estructura:

```
project-root/
├── frontend/   # Proyecto React
├── backend/    # Proyecto Spring Boot
└── docker/     # Configuración de Docker
```

## Contribuciones

Si deseas contribuir a este proyecto, por favor abre un issue o envía un pull request.



---

# ProjectGen

This project aims to generate the basic structure for projects that combine **React** on the frontend and **Spring Boot** on the backend, using **PostgreSQL** as the database. Everything is configured to run inside **Docker** containers.

## Features

- Automatic generation of a React project structure.
- Initial setup for a Spring Boot backend.
- Integration with PostgreSQL as the database.
- Ready-to-run Docker container configuration.

## Prerequisites

Before using this project, make sure you have the following programs installed:

- [Docker](https://www.docker.com/)
- [Node.js](https://nodejs.org/) (for React)
- [Java JDK](https://www.oracle.com/java/technologies/javase-downloads.html) (for Spring Boot)

## Usage

1. Clone this repository to your local machine:
   ```bash
   git clone <REPOSITORY_URL>
   ```

2. Run the generation script to create the project structure.

3. Build and start the Docker containers:
   ```bash
   docker-compose up --build
   ```

4. Access the application:
   - Frontend: `http://localhost:3000`
   - Backend: `http://localhost:8080`

## Project Structure

The generated project will have the following structure:

```
project-root/
├── frontend/   # React project
├── backend/    # Spring Boot project
└── docker/     # Docker configuration
```

## Contributions

If you want to contribute to this project, please open an issue or submit a pull request.

