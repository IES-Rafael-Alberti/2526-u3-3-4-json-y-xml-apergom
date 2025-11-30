import json
import os


def cargar_json(nombre_fichero: str):
    """
    Carga el contenido de un fichero JSON.

    Args:
        nombre_fichero (str): Nombre del fichero JSON.

    Returns:
        dict | None: Contenido del archivo JSON como un diccionario, o None si no se pudo cargar.
    """
    try:
        with open(nombre_fichero, "r", encoding="utf-8") as archivo:
            return json.load(archivo)

    except FileNotFoundError:
        print(f"*ERROR* El archivo {nombre_fichero} no existe.")

    except json.JSONDecodeError:
        print(f"*ERROR* El archivo JSON '{nombre_fichero}' tiene un formato incorrecto.")

    except Exception as e:
        print(f"*ERROR* Problemas al cargar los datos {e}.")

    return None


def guardar_json(nombre_fichero: str, datos: dict) -> bool:
    """
    Guarda los datos en un fichero JSON.

    Args:
        nombre_fichero (str): Nombre del fichero JSON.
        datos (dict): Datos a guardar.

    Returns:
        bool: True si se guardó correctamente, False en caso contrario.
    """
    try:
        with open(nombre_fichero, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, indent=4, ensure_ascii=False)
        return True

    except PermissionError:
        print(f"*ERROR* No tienes permisos para escribir en el archivo '{nombre_fichero}'.")

    except TypeError as e:
        print(f"*ERROR* Los datos no son serializables a JSON. Detalle: {e}")

    except Exception as e:
        print(f"*ERROR* Problemas al guardar los datos: {e}")

    return False


def actualizar_usuario(datos: dict, id_usuario: int, nueva_edad: int):
    """
    Actualiza la edad de un usuario dado su ID.

    Args:
        datos (dict): Diccionario con los datos actuales.
        id_usuario (int): ID del usuario a actualizar.
        nueva_edad (int): Nueva edad del usuario.
    """
    for usuario in datos.get("usuarios", []):
        if usuario.get("id") == id_usuario:
            usuario["edad"] = nueva_edad
            print(f"Usuario con ID {id_usuario} actualizado.")
            return

    print(f"Usuario con ID {id_usuario} no encontrado.")


def insertar_usuario(datos: dict, nuevo_usuario: dict):
    """
    Inserta un nuevo usuario.

    Args:
        datos (dict): Diccionario con los datos actuales.
        nuevo_usuario (dict): Diccionario con los datos del nuevo usuario.
    """
    if "usuarios" not in datos:
        datos["usuarios"] = []

    datos["usuarios"].append(nuevo_usuario)
    print(f"Usuario {nuevo_usuario.get('nombre', '<sin nombre>')} añadido con éxito.")


def eliminar_usuario(datos: dict, id_usuario: int):
    """
    Elimina un usuario dado su ID.

    Args:
        datos (dict): Diccionario con los datos actuales.
        id_usuario (int): ID del usuario a eliminar.
    """
    usuarios = datos.get("usuarios", [])
    for usuario in usuarios:
        if usuario.get("id") == id_usuario:
            usuarios.remove(usuario)
            print(f"Usuario con ID {id_usuario} eliminado.")
            return

    print(f"Usuario con ID {id_usuario} no encontrado.")


def mostrar_datos(datos: dict):
    """
    Muestra de forma organizada el contenido del diccionario recibido.

    Args:
        datos (dict): Diccionario con los datos a mostrar.
    """
    usuarios = datos.get("usuarios", [])
    print("\n--- Contenido Actual del JSON ---")
    if not usuarios:
        print("No hay usuarios en el archivo.")
    else:
        for usuario in usuarios:
            uid = usuario.get("id", "<sin id>")
            nombre = usuario.get("nombre", "<sin nombre>")
            edad = usuario.get("edad", "<sin edad>")
            print(f"ID: {uid}, Nombre: {nombre}, Edad: {edad}")
    print("--- Fin del Contenido ---\n")


def inicializar_datos(origen: str = "datos_usuarios_orig.json", destino: str = "datos_usuarios.json") -> bool:
    """
    Copia el contenido del archivo origen al archivo destino.

    Maneja errores si el archivo origen no existe o tiene formato JSON inválido.
    Si la copia es exitosa muestra un mensaje de confirmación.
    """
    # Intentamos leer el origen
    try:
        with open(origen, "r", encoding="utf-8") as f_origen:
            datos = json.load(f_origen)
    except FileNotFoundError:
        print(f"*ERROR* El archivo origen '{origen}' no existe.")
        return False
    except json.JSONDecodeError:
        print(f"*ERROR* El archivo origen '{origen}' tiene un formato JSON inválido.")
        return False
    except Exception as e:
        print(f"*ERROR* Problema leyendo el archivo origen: {e}")
        return False

    # Intentamos escribir en el destino
    try:
        with open(destino, "w", encoding="utf-8") as f_destino:
            json.dump(datos, f_destino, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"*ERROR* No se pudo inicializar '{destino}': {e}")
        return False

    print(f"Datos inicializados desde '{origen}' a '{destino}'.")
    return True


def limpiar_consola():
    """Limpia la consola del sistema."""
    os.system("cls" if os.name == "nt" else "clear")


def pausa():
    """Pausa hasta que el usuario pulse Enter."""
    try:
        input("Pulse Enter para continuar...")
    except EOFError:
        # En entornos sin stdin disponible, simplemente continuar
        pass


def main():
    """
    Función principal que realiza las operaciones de gestión de un archivo JSON.
    Sigue el flujo requerido en la actividad: inicializar, mostrar, modificar y guardar.
    """
    origen = "datos_usuarios_orig.json"
    destino = "datos_usuarios.json"

    limpiar_consola()

    # 0. Inicializar datos desde el fichero origen
    inicializado = inicializar_datos(origen=origen, destino=destino)
    if not inicializado:
        print("No se pudo inicializar los datos. Se continuará con datos vacíos en memoria.")
    pausa()

    # 1. Cargar datos desde el fichero JSON
    datos = cargar_json(destino)
    if datos is None:
        datos = {"usuarios": []}

    # Mostrar contenido inicial
    mostrar_datos(datos)
    pausa()

    # 2. Actualizar la edad de un usuario (ejemplo: id 1 -> 31)
    actualizar_usuario(datos, id_usuario=1, nueva_edad=31)
    mostrar_datos(datos)
    pausa()

    # 3. Insertar un nuevo usuario
    nuevo_usuario = {"id": 3, "nombre": "Pedro", "edad": 40}
    insertar_usuario(datos, nuevo_usuario)
    mostrar_datos(datos)
    pausa()

    # 4. Eliminar un usuario (ejemplo: id 2)
    eliminar_usuario(datos, id_usuario=2)
    mostrar_datos(datos)
    pausa()

    # 5. Guardar los datos de nuevo en el fichero JSON
    if guardar_json(destino, datos):
        print(f"Datos guardados en '{destino}'.")
    else:
        print("No se pudieron guardar los datos.")

    print("\nOperaciones completadas. Archivo actualizado.\n")


if __name__ == "__main__":
    main()