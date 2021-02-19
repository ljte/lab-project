

def test_get(client):
    resp = client.get(f"/api/employees/")
    assert resp.status_code == 200


def test_get_by_id(client):
    dep = {"first_name": "Testing", "second_name": "Employee",
           "bday": "2000-12-31", "department_id": 1} 
    r = client.post("/api/employees/", data=dep)
    print(r, r.json)

    resp = client.get("/api/employees/1")
    print(resp.json)

    print(client.get("/api/employees/").json)
    assert resp.status_code == 200
    assert resp.json.get("first_name") == "Testing"


def test_get_by_invalid_id(client):
    resp = client.get("/api/employees/asga")

    assert resp.status_code == 404

    resp = client.get("/api/employees/12")

    assert resp.status_code == 400


def test_post(client):
    emp = {"first_name": "Testing", "second_name": "Employee",
           "bday": "2000-12-31", "department_id": 1} 
    resp = client.post("/api/employees/", data=emp)

    assert resp.status_code == 201


def test_invalid_post(client):
    emp = {"first_name": "123123", "second_name": "Employee",
           "bday": "2000-12-31", "department_id": 1} 
    resp = client.post("/api/employees/", data=emp)

    assert resp.status_code == 400

    emp = {"first_name": "123123", "second_name": "Employee",
           "department_id": 1} 
    resp = client.post("/api/employees/", data=emp)

    assert resp.status_code == 400


def test_put(client):
    emp = {"first_name": "Testing", "second_name": "Employee",
           "bday": "2000-12-31", "department_id": 1} 
    resp = client.post("/api/employees/", data=emp)

    resp = client.put("/api/employees/1", data={"first_name": "Good"})

    assert resp.status_code == 201
    assert client.get("/api/employees/1").json.get("first_name") == "Good"


def test_invalid_put(client):
    emp = {"first_name": "Testing", "second_name": "Employee",
           "bday": "2000-12-31", "department_id": 1} 
    resp = client.post("/api/employees/", data=emp)

    resp = client.put("/api/employees/1", data={"first_name": "1231"})

    assert resp.status_code == 400
    assert client.get("/api/employees/1").json.get("first_name") == "Testing"
