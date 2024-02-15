import json
from uuid import uuid4


async def test_create_book(client, get_book_from_database):
    book_data = {
        "name": "qwerty",
        "download_link": "qwerty",
    }
    resp = client.post("/book/", data=json.dumps(book_data))
    data_from_resp = resp.json()
    assert resp.status_code == 200
    assert data_from_resp["name"] == book_data["name"]
    assert data_from_resp["download_link"] == book_data["download_link"]
    books_from_db = await get_book_from_database(data_from_resp["book_id"])
    assert len(books_from_db) == 1
    book_from_db = dict(books_from_db[0])
    assert book_from_db["name"] == book_data["name"]
    assert book_from_db["download_link"] == book_data["download_link"]
    assert str(book_from_db["id"]) == data_from_resp["book_id"]


async def test_delete_book(client, get_book_from_database, create_book_in_database):
    book_data = {
        "id": uuid4(),
        "name": "qwerty123",
        "download_link": "qwerty",
    }
    await create_book_in_database(**book_data)
    resp = client.delete(f"/book/?book_id={book_data['id']}")
    data_from_resp = resp.json()
    assert resp.status_code == 200
    assert data_from_resp["deleted_book_id"] == str(book_data["id"])


async def test_get_book(client, get_book_from_database, create_book_in_database):
    book_data = {
        "id": uuid4(),
        "name": "qwerty123",
        "download_link": "qwerty",
    }
    await create_book_in_database(**book_data)
    resp = client.get(f"/book/?book_id={book_data['id']}")
    data_from_resp = resp.json()
    assert resp.status_code == 200
    assert data_from_resp["id"] == book_data["id"]
    assert data_from_resp["name"] == book_data["name"]
    assert data_from_resp["download_link"] == book_data["download_link"]