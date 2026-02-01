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
