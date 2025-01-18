# BlobService - Sistemas Distribuidos

Este repositorio contiene la implementación del servicio **BlobService** como parte del proyecto de laboratorio para la asignatura de Sistemas Distribuidos. El objetivo de este servicio es gestionar el almacenamiento y transferencia de blobs (objetos binarios grandes) en un sistema distribuido que simula funcionalidades similares a las de plataformas como Google Drive o OneDrive.

---

## Descripción General

El sistema distribuido se compone de tres servicios principales:
- **AuthenticationService**: gestión de usuarios y autenticación.
- **DirectoryService**: gestión de estructuras de directorios.
- **BlobService**: gestión del almacenamiento de blobs (asignado a este repositorio).

### Responsabilidades de BlobService
El servicio **BlobService** se encarga de:
1. Almacenar blobs de manera persistente y eficiente.
2. Gestionar identificadores únicos (basados en hash SHA-256) para blobs.
3. Realizar operaciones de enlace (link) y desenlace (unlink) para mantener un conteo de referencias de blobs.
4. Coordinar la transferencia de datos con instancias distribuidas y otros servicios mediante ZeroC Ice.

---

## Requisitos

### Software
- Python 3.x
- Librería [ZeroC Ice](https://zeroc.com/ice)
- Dependencias adicionales (listadas en el archivo `requirements.txt`)

### Hardware
- Sistema operativo compatible con Python y ZeroC Ice.
- Espacio suficiente para la persistencia de blobs.

---

## Instalación

1. Clona este repositorio:
   ```bash
   git clone <URL_DEL_REPOSITORIO>
   cd blobservice
   ```
2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Configura el entorno de persistencia:
   - Define el directorio de almacenamiento en el archivo `config.json` o utiliza el directorio por defecto (`./data`).

---

## Ejecución

1. Ejecuta el servicio:
   ```bash
   python blob_service.py
   ```
   
---

## Interfaz ::IceDrive::BlobService

El servicio implementa los siguientes métodos:

### 1. `String upload(User* user, DataTransfer* blob)`
Sube un nuevo blob al sistema.
- **Parámetros:**
  - `user`: proxy del usuario autenticado que realiza la acción.
  - `blob`: objeto que gestiona la transferencia de datos.
- **Excepciones:**
  - `FailedToReadData`: error al leer los datos del blob.
  - `TemporaryUnavailable`: no se puede procesar temporalmente.
- **Resultado:** retorna un identificador único (blobId) para el blob.

### 2. `DataTransfer* download(User* user, string blobId)`
Descarga un blob del sistema.
- **Parámetros:**
  - `user`: proxy del usuario autenticado.
  - `blobId`: identificador del blob a descargar.
- **Excepciones:**
  - `UnknownBlob`: el blob no existe.
  - `TemporaryUnavailable`: no se puede procesar temporalmente.
- **Resultado:** retorna un objeto `DataTransfer` para la transferencia de datos.

### 3. `void link(string blobId)`
Incrementa el contador de referencias de un blob.
- **Parámetros:**
  - `blobId`: identificador del blob.
- **Excepciones:**
  - `UnknownBlob`: el blob no existe.

### 4. `void unlink(string blobId)`
Decrementa el contador de referencias de un blob y elimina el blob si ya no está enlazado.
- **Parámetros:**
  - `blobId`: identificador del blob.
- **Excepciones:**
  - `UnknownBlob`: el blob no existe.

---

## Resolución Diferida

Cuando el servicio no pueda atender una solicitud de manera inmediata (por ejemplo, un blob no se encuentra localmente), se seguirá el siguiente mecanismo:

1. Se creará un objeto que implemente la interfaz `BlobQueryResponse`.
2. Se enviará un evento en el canal asociado a la interfaz `BlobQuery`.
3. Si se recibe una respuesta en un plazo de 5 segundos:
   - Se procesará la acción.
4. Si no se recibe respuesta:
   - Se retornará un error al cliente.

### Interfaz ::IceDrive::BlobQuery

#### Métodos
- `void downloadBlob(string blobId, BlobQueryResponse* response)`
- `void blobIdExists(string blobId, BlobQueryResponse* response)`
- `void linkBlob(string blobId, BlobQueryResponse* response)`
- `void unlinkBlob(string blobId, BlobQueryResponse* response)`

---

## Persistencia

- Los blobs se almacenan de manera persistente en el directorio configurado.
- Se utiliza el hash SHA-256 como identificador único para blobs.
- Se guarda un registro del contador de referencias para gestionar el ciclo de vida de los blobs.

---

## Colaboración con Otros Servicios

El servicio **BlobService** interactúa con:
- **AuthenticationService**: verifica la autenticidad de los usuarios mediante el método `verifyUser`.
- **DirectoryService**: permite enlazar y desenlazar blobs a archivos en directorios.

---

## Pruebas

Incluye pruebas unitarias para todos los métodos del servicio.

---

## Contribuciones

El desarrollo de este proyecto fomenta el trabajo en equipo. Por favor, sigue las pautas acordadas para commits y revisiones de código.

---

## Autores

Este servicio fue desarrollado por [Adrián Utrilla Sánchez]. Para consultas, contacta a [adrian.utrilla@outlook.es].

