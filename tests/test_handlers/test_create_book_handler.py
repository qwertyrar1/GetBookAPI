import json
from tests.conftest import create_test_auth_headers_for_admin
from tests.data_for_tests import book_data_for_reg, admin_data_for_create


async def test_create_book(client, get_book_from_database, create_admin_in_database):
    await create_admin_in_database(**admin_data_for_create)
    resp = client.post("/book/", data=json.dumps(book_data_for_reg),
                       headers=create_test_auth_headers_for_admin(admin_data_for_create["nickname"]))
    assert resp.status_code == 200
    data_from_resp = resp.json()
    assert data_from_resp["name"] == book_data_for_reg["name"]
    assert data_from_resp["download_link"] == book_data_for_reg["download_link"]
    books_from_db = await get_book_from_database(data_from_resp["book_id"])
    assert len(books_from_db) == 1
    book_from_db = dict(books_from_db[0])
    assert book_from_db["name"] == book_data_for_reg["name"]
    assert book_from_db["download_link"] == book_data_for_reg["download_link"]
    assert str(book_from_db["id"]) == data_from_resp["book_id"]