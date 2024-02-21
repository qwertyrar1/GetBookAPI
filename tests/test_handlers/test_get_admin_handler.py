from uuid import uuid4
from tests.conftest import create_test_auth_headers_for_admin
from tests.data_for_tests import superadmin_data_for_auth, admin_data_for_create


async def test_get_admin(client, create_admin_in_database):
    await create_admin_in_database(**admin_data_for_create)
    await create_admin_in_database(**superadmin_data_for_auth)
    resp = client.get(f"/admin/?admin_id={admin_data_for_create['id']}",
                      headers=create_test_auth_headers_for_admin(superadmin_data_for_auth["nickname"]))
    assert resp.status_code == 200
    data_from_resp = resp.json()
    assert data_from_resp["admin_id"] == str(admin_data_for_create["id"])
    assert data_from_resp["nickname"] == admin_data_for_create["nickname"]


async def test_get_admin_id_validation_error(client, create_admin_in_database, get_admin_from_database):
    await create_admin_in_database(**superadmin_data_for_auth)
    resp = client.get(
        "/admin/?admin_id=123",
        headers=create_test_auth_headers_for_admin(superadmin_data_for_auth["nickname"]),
    )
    assert resp.status_code == 422


async def test_get_admin_not_found(client, create_admin_in_database):
    await create_admin_in_database(**superadmin_data_for_auth)
    admin_id_not_exists_admin = uuid4()
    resp = client.get(f"/admin/?admin_id={admin_id_not_exists_admin}",
                      headers=create_test_auth_headers_for_admin(superadmin_data_for_auth["nickname"]))
    assert resp.status_code == 404
    assert resp.json() == {"detail": f"Admin with id {admin_id_not_exists_admin} not found."}


async def test_get_admin_unauth(client, create_admin_in_database):
    await create_admin_in_database(**admin_data_for_create)
    resp = client.get(f"/admin/?admin_id={admin_data_for_create['id']}")
    assert resp.status_code == 401
    assert resp.json() == {"detail": "Not authenticated"}


async def test_get_admin_bad_cred(client, create_admin_in_database):
    await create_admin_in_database(**superadmin_data_for_auth)
    user_id = uuid4()
    resp = client.get(
        f"/admin/?admin_id={user_id}",
        headers=create_test_auth_headers_for_admin(superadmin_data_for_auth["nickname"] + "a"),
    )
    assert resp.status_code == 401
    assert resp.json() == {"detail": "Could not validate credentials"}

