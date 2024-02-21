from uuid import uuid4
from tests.conftest import create_test_auth_headers_for_admin
from tests.data_for_tests import superadmin_data_for_auth, admin_data_for_create


async def test_delete_admin(client, create_admin_in_database):
    await create_admin_in_database(**superadmin_data_for_auth)
    await create_admin_in_database(**admin_data_for_create)
    resp = client.delete(f"/admin/?admin_id={admin_data_for_create['id']}",
                         headers=create_test_auth_headers_for_admin(superadmin_data_for_auth["nickname"]))
    data_from_resp = resp.json()
    print(data_from_resp)
    assert resp.status_code == 200
    assert data_from_resp["deleted_id"] == str(admin_data_for_create["id"])


async def test_delete_admin_not_found(client, create_admin_in_database):
    await create_admin_in_database(**admin_data_for_create)
    await create_admin_in_database(**superadmin_data_for_auth)
    admin_id_not_exists_admin = uuid4()
    resp = client.delete(
        f"/admin/?admin_id={admin_id_not_exists_admin}",
        headers=create_test_auth_headers_for_admin(superadmin_data_for_auth["nickname"]),
    )
    assert resp.status_code == 404
    assert resp.json() == {
        "detail": f"Admin with id {admin_id_not_exists_admin} not found."
    }


async def test_delete_admin_id_validation_error(client, create_admin_in_database):
    await create_admin_in_database(**superadmin_data_for_auth)
    resp = client.delete(
        "/admin/?admin_id=123",
        headers=create_test_auth_headers_for_admin(superadmin_data_for_auth["nickname"]),
    )
    assert resp.status_code == 422


async def test_delete_admin_bad_cred(client, create_admin_in_database):
    await create_admin_in_database(**superadmin_data_for_auth)
    admin_id = uuid4()
    resp = client.delete(
        f"/admin/?admin_id={admin_id}",
        headers=create_test_auth_headers_for_admin(superadmin_data_for_auth["nickname"] + "a"),
    )
    assert resp.status_code == 401
    assert resp.json() == {"detail": "Could not validate credentials"}


async def test_delete_admin_no_jwt(client, create_admin_in_database):
    await create_admin_in_database(**superadmin_data_for_auth)
    admin_id = uuid4()
    resp = client.delete(
        f"/admin/?admin_id={admin_id}",
    )
    assert resp.status_code == 401
    assert resp.json() == {"detail": "Not authenticated"}



