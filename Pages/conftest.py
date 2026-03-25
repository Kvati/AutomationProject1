import pytest
import uuid

@pytest.fixture
def random_user():
    return {
        "username": "user_" + uuid.uuid4().hex[:6],
        "email": f"{uuid.uuid4().hex[:8]}@test.com",
    }