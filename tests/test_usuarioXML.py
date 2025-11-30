from src.usuarioXML import actualizar_usuario, insertar_usuario, eliminar_usuario

def test_actualizar_usuario():
    datos = {
        "usuarios": [
            {"id": 1, "nombre": "Juan", "edad": 30},
            {"id": 2, "nombre": "Ana", "edad": 25},
        ]
    }

    actualizar_usuario(datos, 1, 31)
    assert datos["usuarios"][0]["edad"] == 31
    assert datos["usuarios"][1]["edad"] == 25
    # Intentar actualizar un ID inexistente no debe añadir ni eliminar usuarios
    actualizar_usuario(datos, 99, 50)
    assert len(datos["usuarios"]) == 2


def test_insertar_usuario():
    datos = {
        "usuarios": [
            {"id": 1, "nombre": "Juan", "edad": 30},
            {"id": 2, "nombre": "Ana", "edad": 25},
        ]
    }

    insertar_usuario(datos, {"id": 3, "nombre": "Pedro", "edad": 40})
    assert len(datos["usuarios"]) == 3
    assert datos["usuarios"][-1]["nombre"] == "Pedro"
    assert datos["usuarios"][-1]["edad"] == 40


def test_eliminar_usuario():
    datos = {
        "usuarios": [
            {"id": 1, "nombre": "Juan", "edad": 30},
            {"id": 2, "nombre": "Ana", "edad": 25},
            {"id": 3, "nombre": "Pedro", "edad": 40},
        ]
    }

    eliminar_usuario(datos, 2)
    assert len(datos["usuarios"]) == 2
    assert not any(u["id"] == 2 for u in datos["usuarios"])
    assert [u["id"] for u in datos["usuarios"]] == [1, 3]