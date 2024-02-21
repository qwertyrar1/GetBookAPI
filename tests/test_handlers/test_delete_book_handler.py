from tests.conftest import create_test_auth_headers_for_admin
from tests.data_for_tests import book_data_for_create, admin_data_for_create


async def test_delete_book(client, get_book_from_database, create_book_in_database, create_admin_in_database):
    await create_book_in_database(**book_data_for_create)
    await create_admin_in_database(**admin_data_for_create)
    resp = client.delete(f"/book/?book_id={book_data_for_create['id']}",
                         headers=create_test_auth_headers_for_admin(admin_data_for_create["nickname"]))
    data_from_resp = resp.json()
    assert resp.status_code == 200
    assert data_from_resp["deleted_id"] == str(book_data_for_create["id"])