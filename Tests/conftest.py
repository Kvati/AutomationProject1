import pytest
import uuid

@pytest.fixture
def random_user():
    return {
        "username": "user_" + uuid.uuid4().hex[:6],
        "email": f"{uuid.uuid4().hex[:8]}@test.com",
    }

@pytest.fixture
def existing_user():
    return {
        "username": "Kvati123",
        "email": "KvatiTest@test.com",
        "password": "test123",
        "dob_day": "20",
        "dob_month": "9",
        "dob_year": "2000",
        "first_name": "Kvati",
        "last_name": "Test",
        "company": "TestCompany",
        "address_1": "TestAddress 123 bld. 15",
        "address_2": "TestAddress 456 bld. 43",
        "country": "Australia",
        "state": "TestState",
        "city": "TestCity",
        "zipcode": "TestZIP",
        "mobile_number": "0412 345 678"
    }