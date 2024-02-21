import json
from tests.conftest import create_test_auth_headers_for_admin
from tests.data_for_tests import superadmin_data_for_auth, admin_data_for_reg, admin_data_same


async def test_create_admin(client, get_admin_from_database, create_admin_in_database):
    await create_admin_in_database(**superadmin_data_for_auth)
    resp = client.post("/admin/", data=json.dumps(admin_data_for_reg),
                       headers=create_test_auth_headers_for_admin(superadmin_data_for_auth["nickname"]))
    assert resp.status_code == 200
    data_from_resp = resp.json()
    assert data_from_resp["nickname"] == admin_data_for_reg["nickname"]
    admin_from_db = await get_admin_from_database(data_from_resp["admin_id"])
    assert len(admin_from_db) == 1
    admin_from_db = dict(admin_from_db[0])
    assert admin_from_db["nickname"] == admin_data_for_reg["nickname"]
    assert str(admin_from_db["id"]) == data_from_resp["admin_id"]


async def test_create_admin_duplicate_nickname_error(client, get_admin_from_database, create_admin_in_database):
    await create_admin_in_database(**superadmin_data_for_auth)
    resp = client.post(
        "/admin/", data=json.dumps(admin_data_for_reg),
        headers=create_test_auth_headers_for_admin(superadmin_data_for_auth["nickname"])
    )
    assert resp.status_code == 200
    data_from_resp = resp.json()
    assert data_from_resp["nickname"] == admin_data_for_reg["nickname"]
    admin_from_db = await get_admin_from_database(data_from_resp["admin_id"])
    assert len(admin_from_db) == 1
    admin_from_db = dict(admin_from_db[0])
    assert admin_from_db["nickname"] == admin_data_for_reg["nickname"]
    assert str(admin_from_db["id"]) == data_from_resp["admin_id"]
    resp = client.post(
        "/admin/", data=json.dumps(admin_data_same),
        headers=create_test_auth_headers_for_admin(superadmin_data_for_auth["nickname"])
    )
    assert resp.status_code == 503
    assert (
            'duplicate key value violates unique constraint "admins_nickname_key"'
            in resp.json()["detail"]
    )
