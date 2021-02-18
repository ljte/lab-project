

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