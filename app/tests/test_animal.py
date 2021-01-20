def test_animal(client):
    resp = client.get("/animals")
    assert resp.status_code == 200, resp.text
