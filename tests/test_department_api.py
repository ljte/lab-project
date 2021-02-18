
def test_get(client):
    resp = client.get(f"/api/departments/")
    assert resp.status_code == 200


def test_get_by_id(client):
    dep = {"name": "testing department"}
    client.post("/api/departments/", data=dep)

    resp = client.get("/api/departments/1")

    assert resp.status_code == 200
    assert resp.json.get("name") == "Testing department"


def test_get_by_invalid_id(client):
    resp = client.get("/api/departments/asga")

    assert resp.status_code == 404

    resp = client.get("/api/departments/12")

    assert resp.status_code == 400


def test_post(client):
    dep = {"name": "Marketing department"}
    resp = client.post("/api/departments/", data=dep)

    assert resp.status_code == 201


def test_invalid_post(client):
    dep = {"name": "12312"}
    resp = client.post("/api/departments/", data=dep)

    assert resp.status_code == 400


def test_put(client):
    dep = {"name": "testing department"}
    client.post("/api/departments/", data=dep)

    resp = client.put("/api/departments/1", data={"name": "good department"})

    assert resp.status_code == 204
    assert client.get("/api/departments/1").json.get("name") == "Good department"


def test_invalid_put(client):
    dep = {"name": "testing department"}
    client.post("/api/departments/", data=dep)

    resp = client.put("/api/departments/1", data={"name": "1231 department"})

    assert resp.status_code == 400
    assert client.get("/api/departments/1").json.get("name") == "Testing department"


def test_delete(client):
    dep = {"name": "testing department"}
    client.post("/api/departments/", data=dep)

    resp = client.delete("/api/departments/1")

    assert resp.status_code == 204
    assert client.get("/api/departments/1").status_code == 400


def test_invalid_delete(client):
    resp = client.delete("/api/departments/1")

    assert resp.status_code == 400