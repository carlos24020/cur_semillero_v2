def test_create_leader(client):
    payload = {
        "nombre": "Carlos",
        "email": "carlos@example.com",
        "departamento": "Desarrollo",
    }
    response = client.post("/leaders/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["nombre"] == "Carlos"
    assert data["id"] == 1


def test_read_leaders(client):
    client.post(
        "/leaders/",
        json={
            "nombre": "Ana",
            "email": "ana@example.com",
            "departamento": "Diseño",
        },
    )
    response = client.get("/leaders/")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_leader_by_id(client):
    create_response = client.post(
        "/leaders/",
        json={
            "nombre": "Pedro",
            "email": "pedro@example.com",
            "departamento": "QA",
        },
    )
    leader_id = create_response.json()["id"]
    
    response = client.get(f"/leaders/{leader_id}")
    assert response.status_code == 200
    assert response.json()["nombre"] == "Pedro"


def test_delete_leader(client):
    create_response = client.post(
        "/leaders/",
        json={
            "nombre": "María",
            "email": "maria@example.com",
            "departamento": "Marketing",
        },
    )
    leader_id = create_response.json()["id"]
    
    delete_response = client.delete(f"/leaders/{leader_id}")
    assert delete_response.status_code == 204
    
    get_response = client.get("/leaders/")
    assert len(get_response.json()) == 0
