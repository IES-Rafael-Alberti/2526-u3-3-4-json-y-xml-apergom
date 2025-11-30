# Práctica 3.4: JSON y XML

[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/MNhzxJmi)

Apóyate en los siguientes recursos para realizar la práctica:

- U3: JSON — https://revilofe.github.io/section1/u03/practica/PROG-U3.-Practica004/
- U3: XML  — https://revilofe.github.io/section1/u03/practica/PROG-U3.-Practica005/

---

## Entrega
1. Programas en la carpeta `src`:
   - JSON: src/usuario.py
   - XML: src/usuarioXML.py (módulo con las funciones)
   - Script de ejemplo para XML (CLI): src/programa_xml_sin_minidom.py
2. Pruebas unitarias en la carpeta `tests`: tests/test_usuario.py
3. Ficheros de datos de ejemplo:
   - src/datos_usuarios_orig.json
   - src/datos_usuarios.json (archivo destino generado por el programa JSON)
   - src/datos_usuarios_orig.xml
   - src/datos_usuarios.xml (archivo destino generado por el programa XML)

---

# Título de la Actividad

## Identificación de la Actividad
- **ID de la Actividad:** [ID de la actividad]
- **Módulo:** PROG
- **Unidad de Trabajo:** [Número y nombre de la unidad de trabajo]
- **Fecha de Creación:** 2025-11-30
- **Fecha de Entrega:** 2025-11-30
- **Alumno(s):** 
  - **Nombre y Apellidos:** Antonio Manuel Perez Gomez
  - **Correo electrónico:** apergom459w@g.educaand.es
  - **Iniciales del Alumno/Grupo:** AMP G

---

## Descripción de la Actividad
Implementar operaciones básicas de gestión de usuarios almacenados en ficheros (JSON y XML).  
Objetivos principales:
- Aprender a leer y escribir JSON y XML.
- Implementar operaciones CRUD simples sobre la estructura de datos en memoria.
- Escribir pruebas unitarias para las funciones de manipulación de usuarios.

---

## Estructura del Repositorio (relevante)
- src/
  - usuario.py                # Implementación original usando JSON
  - usuarioXML.py             # Implementación de las funciones para uso con XML (mismo API)
  - programa_xml_sin_minidom.py  # Script ejemplo que usa usuarioXML y guarda/lee XML sin xml.dom.minidom
  - datos_usuarios_orig.json
  - datos_usuarios.json
  - datos_usuarios_orig.xml
  - datos_usuarios.xml
- tests/
  - test_usuario.py           # Pruebas pytest para actualizar/insertar/eliminar usuarios

---

## Parte: JSON
(Resumen ya incluido en la entrega)
- Fichero principal: src/usuario.py
- Objetivo: operaciones de carga/guardado, mostrar, inicializar, actualizar, insertar, eliminar usuarios usando JSON.
- Ejemplo de origen JSON (src/datos_usuarios_orig.json):
```json
{
    "usuarios": [
        {"id": 1, "nombre": "Juan", "edad": 30},
        {"id": 2, "nombre": "Ana", "edad": 25}
    ]
}
```
- Ejecución (script JSON):
```bash
python src/usuario.py
```

---

## Parte: XML (nuevo apartado añadido)
Se ha añadido la versión equivalente para trabajar con XML manteniendo el mismo flujo de operaciones que en la versión JSON: inicializar desde un origen, cargar, mostrar, actualizar, insertar, eliminar y guardar.

- Módulo con funciones (API compatible):
  - src/usuarioXML.py
  - Contiene las mismas funciones que las usadas en la parte JSON:
    - actualizar_usuario(datos, id_usuario, nueva_edad)
    - insertar_usuario(datos, nuevo_usuario)
    - eliminar_usuario(datos, id_usuario)
  - Estas funciones trabajan sobre un diccionario en memoria con la clave "usuarios" (mismo formato que en JSON), de modo que las pruebas unitarias se pueden aplicar sin cambios en la lógica.

- Script de ejemplo (CLI) que demuestra el flujo completo y maneja lectura/escritura de XML sin usar xml.dom:
  - src/programa_xml_sin_minidom.py
  - Características:
    - Usa xml.etree.ElementTree para parsear y construir XML.
    - Implementa una función de indentación propia para producir un XML legible (compatible con entornos que no disponen de xml.dom.minidom o ET.indent).
    - Maneja errores comunes: fichero no encontrado, parse error, permisos.
    - Lee datos de `datos_usuarios_orig.xml` (si existe), inicializa `datos_usuarios.xml`, realiza operaciones de ejemplo (actualizar id=1, insertar id=3, eliminar id=2) y guarda el resultado.

- Estructura XML esperada (ejemplo src/datos_usuarios_orig.xml):
```xml
<?xml version="1.0" encoding="utf-8"?>
<datos>
    <usuarios>
        <usuario id="1">
            <nombre>Juan</nombre>
            <edad>30</edad>
        </usuario>
        <usuario id="2">
            <nombre>Ana</nombre>
            <edad>25</edad>
        </usuario>
    </usuarios>
</datos>
```

- Ejecución (script XML):
```bash
python src/programa_xml_sin_minidom.py
```

- Salida esperada (resumen):
  - Se muestra por consola el contenido antes y después de las operaciones.
  - Se genera/actualiza `src/datos_usuarios.xml` con los cambios realizados.

---

## Pruebas Unitarias
- Archivo de tests: tests/test_usuario.py
- Contenido: pruebas para las funciones de manipulación de usuarios:
  - test_actualizar_usuario
  - test_insertar_usuario
  - test_eliminar_usuario

Ejecutar tests:
```bash
# Instalar pytest si es necesario
pip install pytest

# Ejecutar desde la raíz del repositorio
pytest -q
```

Notas sobre imports en las pruebas:
- Las pruebas importan las funciones desde el módulo `src.usuarioXML`:
  from src.usuarioXML import actualizar_usuario, insertar_usuario, eliminar_usuario

Esto mantiene la misma lógica de tests que se usó originalmente para JSON, simplemente apuntando al módulo que contiene las funciones (ahora llamado usuarioXML).

---

## Descripción de las funciones principales (mismo API para JSON y XML)
- cargar_json(nombre_fichero): lee y devuelve un diccionario desde un archivo JSON (solo en la parte JSON).
- guardar_json(nombre_fichero, datos): guarda un diccionario en un fichero JSON.
- cargar_xml(nombre_fichero): (implementado en el script XML) parsea el XML y devuelve un diccionario con la clave "usuarios".
- guardar_xml(nombre_fichero, datos): (implementado en el script XML) guarda el diccionario como XML legible sin usar xml.dom.minidom.
- mostrar_datos(datos): imprime por consola la lista de usuarios.
- inicializar_datos(origen, destino): copia un fichero origen al destino realizando parseo/validación y formateo.
- actualizar_usuario(datos, id_usuario, nueva_edad): modifica la edad del usuario con el id indicado.
- insertar_usuario(datos, nuevo_usuario): añade el nuevo usuario al final de la lista.
- eliminar_usuario(datos, id_usuario): elimina el usuario con el id indicado.

---

## Flujo del programa (comportamiento general)
1. Limpia la consola.
2. Inicializa datos desde `datos_usuarios_orig.*` (JSON o XML) a `datos_usuarios.*` (destino).
   - Si no existe o es inválido el origen, continúa con datos vacíos en memoria.
3. Carga los datos desde el fichero destino.
4. Muestra los datos.
5. Realiza operaciones de ejemplo: actualizar edad de id=1, insertar usuario id=3, eliminar id=2.
6. Guarda los datos actualizados.
7. Finaliza mostrando confirmación.

---

## Ejemplos de Archivos de Origen
- JSON: src/datos_usuarios_orig.json (ver ejemplo arriba)
- XML: src/datos_usuarios_orig.xml (ver ejemplo arriba)

---

## Resultados esperados de las pruebas
Al ejecutar `pytest -q` se esperan que las 3 pruebas definidas en `tests/test_usuario.py` pasen correctamente:
- actualizar, insertar y eliminar usuarios funcionan como se espera sobre la estructura en memoria.

---

## Instrucciones de Compilación y Ejecución
1. Requisitos:
   - Python 3.8+ (recomendado)
   - pytest para ejecutar tests: pip install pytest
2. Ejecutar programa JSON:
   ```bash
   python src/usuario.py
   ```
3. Ejecutar programa XML:
   ```bash
   python src/programa_xml_sin_minidom.py
   ```
4. Ejecutar tests:
   ```bash
   pytest -q
   ```

---

## Desarrollo y Notas Técnicas
- La versión XML mantiene la misma API para las funciones de manipulación de usuarios, lo que facilita reutilizar tests.
- Para crear XML "bonito" se usó:
  - ET.indent cuando está disponible (Python 3.9+), o
  - una función _indent propia que ajusta text/tail para producir indentación legible.
- Se evitó el uso de xml.dom.minidom a petición para mantener el código más ligero y con dependencias estándar mínimas.
- La representación interna en memoria sigue siendo un diccionario Python con la clave `"usuarios"` para homogeneidad entre JSON y XML.

---

## Documentación Adicional
- Manual de usuario: Ejecutar el script correspondiente y seguir las pausas por consola.
- Si quieres que incluya un fichero `src/usuario.py` que reexporte desde `src.usuarioXML` para compatibilidad (o viceversa), puedo añadir un pequeño stub. Actualmente las pruebas importan desde `src.usuarioXML`.