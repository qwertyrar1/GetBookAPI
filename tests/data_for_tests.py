from uuid import uuid4
from db.models import PortalRole


superadmin_data_for_auth = {
        "id": uuid4(),
        "nickname": "super_sample1",
        "hashed_password": "super_sample",
        "roles": [PortalRole.ROLE_PORTAL_ADMIN, PortalRole.ROLE_PORTAL_SUPERADMIN, ],
    }

admin_data_for_reg = {
        "nickname": "sample1",
        "password": "sample",
    }

admin_data_for_create = {
        "id": uuid4(),
        "nickname": "sample1",
        "hashed_password": "sample",
        "roles": [PortalRole.ROLE_PORTAL_ADMIN, ],
    }

admin_data_same = {
        "nickname": "sample1",
        "password": "sample",
    }

book_data_for_reg = {
        "name": "qwerty1",
        "download_link": "qwerty",
    }

book_data_for_create = {
        "id": uuid4(),
        "name": "qwerty3",
        "download_link": "qwerty",
    }
