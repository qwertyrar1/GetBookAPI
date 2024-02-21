from tests.conftest import create_test_auth_headers_for_admin
from tests.data_for_tests import book_data_for_create, admin_data_for_create


async def test_get_book(client, get_book_from_database, create_book_in_database, create_admin_in_database):
    await create_admin_in_database(**admin_data_for_create)
    await create_book_in_database(**book_data_for_create)
    resp = client.get(f"/book/?book_id={book_data_for_create['id']}",
                      headers=create_test_auth_headers_for_admin(admin_data_for_create["nickname"]))
    assert resp.status_code == 200
    data_from_resp = resp.json()
    assert data_from_resp["book_id"] == str(book_data_for_create["id"])
    assert data_from_resp["name"] == book_data_for_create["name"]
    assert data_from_resp["download_link"] == book_data_for_create["download_link"]