def test_HTTP_200_OK(client):
    response = client.get("/templates/", headers=[("accept", "application/json")])
    assert response.status_code == 200
    content = response.json()
    # assert content["title"] == item.title
    # assert content["description"] == item.description
    # assert content["id"] == item.id
    # assert content["owner_id"] == item.owner_id
