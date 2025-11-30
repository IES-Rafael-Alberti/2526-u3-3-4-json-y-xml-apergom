import os
import xml.etree.ElementTree as ET


def _safe_int(valor, defecto=None):
    try:
        return int(valor)
    except (TypeError, ValueError):
        return defecto


def cargar_xml(nombre_fichero: str):
    """
    Carga el contenido de un fichero XML y lo convierte a un diccionario similar
    al manejo anterior con JSON.

    Args:
        nombre_fichero (str): Nombre del fichero XML.

    Returns:
        dict | None: Diccionario con la clave "usuarios" que contiene una lista de usuarios,
                     o None si no se pudo cargar.
    """
    try:
        tree = ET.parse(nombre_fichero)
        root = tree.getroot()

        usuarios_list = []
        usuarios_node = root.find("usuarios")
        if usuarios_node is None:
            posibles = root.findall("usuario")
        else:
            posibles = usuarios_node.findall("usuario")

        for u in posibles:
            uid = _safe_int(u.get("id"), None)
            nombre_el = u.find("nombre")
            edad_el = u.find("edad")
            nombre = nombre_el.text if nombre_el is not None else None
            edad = _safe_int(edad_el.text, None) if edad_el is not None else None

            usuarios_list.append({"id": uid, "nombre": nombre, "edad": edad})

        return {"usuarios": usuarios_list}

    except FileNotFoundError:
        print(f"*ERROR* El archivo {nombre_fichero} no existe.")
    except ET.ParseError:
        print(f"*ERROR* El archivo XML '{nombre_fichero}' tiene un formato incorrecto.")
    except Exception as e:
        print(f"*ERROR* Problemas al cargar los datos: {e}")

    return None


def _indent(elem, level=0):
    """
    Añade indentación 'bonita' al árbol XML estableciendo .text y .tail.
    Funciona sin xml.dom; es equivalente a xml.etree.ElementTree.indent en versiones modernas.
    """
    i = "\n" + ("    " * level)
    if len(elem):
        if elem.text is None or not elem.text.strip():
            elem.text = i + "    "
        for child in elem:
            _indent(child, level + 1)
        if elem.tail is None or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (elem.tail is None or not elem.tail.strip()):
            elem.tail = i


def _dict_to_tree(datos: dict) -> ET.Element:
    """
    Convierte el diccionario de datos a un ElementTree.Element (sin escribir a fichero).
    """
    root = ET.Element("datos")
    usuarios_el = ET.SubElement(root, "usuarios")

    for usuario in datos.get("usuarios", []):
        uid = usuario.get("id")
        usuario_el = ET.SubElement(usuarios_el, "usuario")
        if uid is not None:
            usuario_el.set("id", str(uid))

        nombre = usuario.get("nombre")
        edad = usuario.get("edad")

        nombre_el = ET.SubElement(usuario_el, "nombre")
        nombre_el.text = "" if nombre is None else str(nombre)

        edad_el = ET.SubElement(usuario_el, "edad")
        edad_el.text = "" if edad is None else str(edad)

    return root


def guardar_xml(nombre_fichero: str, datos: dict) -> bool:
    """
    Guarda los datos en un fichero XML aplicando indentación sin usar xml.dom.

    Args:
        nombre_fichero (str): Nombre del fichero XML.
        datos (dict): Datos a guardar (estructura esperada como en cargar_xml).

    Returns:
        bool: True si se guardó correctamente, False en caso contrario.
    """
    try:
        root = _dict_to_tree(datos)
        # Aplicar indentación "bonita" manualmente
        try:
            # Preferir la función nativa si está disponible (Python 3.9+)
            ET.indent(root, space="    ")
        except AttributeError:
            # Si no existe, usar nuestra implementación manual
            _indent(root)

        tree = ET.ElementTree(root)
        tree.write(nombre_fichero, encoding="utf-8", xml_declaration=True)
        return True
    except PermissionError:
        print(f"*ERROR* No tienes permisos para escribir en el archivo '{nombre_fichero}'.")
    except Exception as e:
        print(f"*ERROR* Problemas al guardar los datos: {e}")

    return False


def actualizar_usuario(datos: dict, id_usuario: int, nueva_edad: int):
    """
    Actualiza la edad de un usuario dado su ID.
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
    """
    if "usuarios" not in datos:
        datos["usuarios"] = []

    datos["usuarios"].append(nuevo_usuario)
    print(f"Usuario {nuevo_usuario.get('nombre', '<sin nombre>')} añadido con éxito.")


def eliminar_usuario(datos: dict, id_usuario: int):
    """
    Elimina un usuario dado su ID.
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
    """
    usuarios = datos.get("usuarios", [])
    print("\n--- Contenido Actual del XML ---")
    if not usuarios:
        print("No hay usuarios en el archivo.")
    else:
        for usuario in usuarios:
            uid = usuario.get("id", "<sin id>")
            nombre = usuario.get("nombre", "<sin nombre>")
            edad = usuario.get("edad", "<sin edad>")
            print(f"ID: {uid}, Nombre: {nombre}, Edad: {edad}")
    print("--- Fin del Contenido ---\n")


def inicializar_datos(origen: str = "datos_usuarios_orig.xml", destino: str = "datos_usuarios.xml") -> bool:
    """
    Copia el contenido del archivo origen al archivo destino y lo formatea
    usando nuestras funciones (verifica parseo y crea un XML "bonito").
    """
    try:
        tree = ET.parse(origen)
        root = tree.getroot()
    except FileNotFoundError:
        print(f"*ERROR* El archivo origen '{origen}' no existe.")
        return False
    except ET.ParseError:
        print(f"*ERROR* El archivo origen '{origen}' tiene un formato XML inválido.")
        return False
    except Exception as e:
        print(f"*ERROR* Problema leyendo el archivo origen: {e}")
        return False

    datos = {"usuarios": []}
    usuarios_node = root.find("usuarios")
    if usuarios_node is None:
        posibles = root.findall("usuario")
    else:
        posibles = usuarios_node.findall("usuario")

    for u in posibles:
        uid = _safe_int(u.get("id"), None)
        nombre_el = u.find("nombre")
        edad_el = u.find("edad")
        nombre = nombre_el.text if nombre_el is not None else None
        edad = _safe_int(edad_el.text, None) if edad_el is not None else None
        datos["usuarios"].append({"id": uid, "nombre": nombre, "edad": edad})

    if guardar_xml(destino, datos):
        print(f"Datos inicializados desde '{origen}' a '{destino}'.")
        return True
    else:
        print(f"*ERROR* No se pudo crear '{destino}'.")
        return False


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
    Flujo principal: inicializar, cargar, mostrar, modificar y guardar,
    replicando el comportamiento del programa original en JSON.
    """
    origen = "datos_usuarios_orig.xml"
    destino = "datos_usuarios.xml"

    limpiar_consola()

    # 0. Inicializar datos desde el fichero origen
    inicializado = inicializar_datos(origen=origen, destino=destino)
    if not inicializado:
        print("No se pudo inicializar los datos. Se continuará con datos vacíos en memoria.")
    pausa()

    # 1. Cargar datos desde el fichero XML
    datos = cargar_xml(destino)
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

    # 5. Guardar los datos de nuevo en el fichero XML
    if guardar_xml(destino, datos):
        print(f"Datos guardados en '{destino}'.")
    else:
        print("No se pudieron guardar los datos.")

    print("\nOperaciones completadas. Archivo actualizado.\n")


if __name__ == "__main__":
    main()