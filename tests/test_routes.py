def test_get_all_books_no_records(client):
    #ACT
    response = client.get("/books")
    response_body = response.get_json()

    #ASSERT
    assert response.status_code == 200
    assert response_body == []

def test_get_one_book(client, two_saved_books):
    #ACT
    response = client.get("/books/1")
    response_body = response.get_json()

    #ASSERT
    assert response.status_code == 200
    assert response_body == {
        'id': 1,
        'title': 'Ocean Book',
        'description': 'about water'
    }

def test_create_one_book(client):
    #ACT
    response = client.post("/books", json={
        "title": "A New Book",
        "description": "wow we love books!"
    })
    response_body = response.get_json()
    #ASSERT
    assert response.status_code == 201
    assert response_body == "Book A New Book successfully created"