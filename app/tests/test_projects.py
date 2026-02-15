def test_create_project(client):
    payload = {
        "titulo": "Bio-fertilizante",
        "lider": "Ana Gómez",
        "descripcion": "Reducir uso de químicos",
        "fecha_inicio": "2024-03-01",
    }
    response = client.post("/projects/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["titulo"] == "Bio-fertilizante"
    assert data["id"] == 1


def test_read_projects(client):
    # primero creamos uno
    client.post(
        "/projects/",
        json={
            "titulo": "T1",
            "lider": "L1",
            "descripcion": "D1",
            "fecha_inicio": "2024-01-01",
        },
    )
    response = client.get("/projects/")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_delete_project(client):
    # Crear un proyecto
    create_response = client.post(
        "/projects/",
        json={
            "titulo": "T1",
            "lider": "L1",
            "descripcion": "D1",
            "fecha_inicio": "2024-01-01",
        },
    )
    project_id = create_response.json()["id"]

    # Eliminar el proyecto
    delete_response = client.delete(f"/projects/{project_id}")
    assert delete_response.status_code == 204

    # Verificar que el proyecto fue eliminado
    get_response = client.get("/projects/")
    assert len(get_response.json()) == 0


def test_delete_nonexistent_project(client):
    # Intentar eliminar un proyecto que no existe
    delete_response = client.delete("/projects/999")
    assert delete_response.status_code == 404
    data = delete_response.json()
    assert data["detail"] == "El proyecto no existe"
