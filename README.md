# Flask API RESTful

Esta es una API RESTful creada con Flask. La API permite la gestión de usuarios y autenticación utilizando JWT.

## Tabla de Contenidos

- [Instalación](#instalación)
- [Uso](#uso)
  - [Rutas](#rutas)
    - [Registrar Usuario](#registrar-usuario)
    - [Iniciar Sesión](#iniciar-sesión)
    - [Obtener Usuario](#obtener-usuario)
    - [Actualizar Usuario](#actualizar-usuario)
    - [Eliminar Usuario](#eliminar-usuario)


## Instalación
### Requisitos Previos

- Python 3.10.8

- Se necesita crear una base de datos en Firestore.  Puedes crearla acá: https://console.firebase.google.com. Una vez creado el proyecto y la base de datos, descargamos las credenciales en formato json. 

- Configuración del proyecto -> Cuentas de servicio -> Generar nueva clave privada.

*NOTA*: Colocar la clave privada en la raíz del proyecto y añadir el nombre del archivo en el .env del proyecto.

### Paso a Paso

1. **Clonar el repositorio**
2. **Crear un entorno virtual**
    - python -m venv venv
    - venv\Scripts\activate  # En Windows
    - source venv/bin/activate  # En macOS/Linux
3. **Instalar las dependencias**
    - pip install -r requirements.txt
4. **Configurar las variables de entorno**
    - FIREBASE_AUTH=path/to/your/firebase-credentials.json
    - JWT_SECRET_KEY=your_jwt_secret_key
5. **Ejecutar los tests**
    - pytest
6. **Ejecutar la aplicación**
    - flask run


## Uso
### Rutas
#### Registrar Usuario

`POST register`

  ```json
  {
    "username": "john_doe",
    "email": "john@example.com",
    "password_hash": "your_password"
  }```

  ```curl -X POST http://127.0.0.1:5000/api/register -H "Content-Type: application/json" -d '{"username": "john_doe", "email": "john@example.com", "password_hash": "your_password"}'```

#### Respuesta

```json
{
  "id": "generated_user_id",
  "username": "john_doe",
  "email": "john@example.com",
  "password_hash": "hashed_password",
  "created_at": "2023-07-07T12:34:56.789Z"
}```
