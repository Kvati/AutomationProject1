import pytest
import requests

BASE_URL = "https://automationexercise.com"

@pytest.fixture(scope = "session")
def base_url():
    return BASE_URL

@pytest.fixture(scope = "session")
def api_session():
    session = requests.Session()
    yield session
    session.close()

@pytest.fixture()
def existing_user():
    return {"username": "Kvati123",
          "email": "KvatiTest@test.com",
          "password": "test123",
          "first_name": "Kvati",
          "last_name": "Test",
          "company": "TestCompany",
          "address_1": "TestAddress 123 bld. 15",
          "address_2": "TestAddress 456 bld. 43",
          "country": "Australia",
          "state": "TestState",
          "city": "TestCity",
          "zipcode": "TestZIP",
          "mobile_number": "0412 345 678",
          "title": "Mr",
          "dob_day": "20",
          "dob_month": "9",
          "dob_year": "2000",
    }

@pytest.fixture()
def register_user(random_user):
    return {
        "username": random_user["username"],
        "email": random_user["email"],
        "password": "test123",
        "dob_day": "20",
        "dob_month": "9",
        "dob_year": "2000",
        "first_name": "test_first_name",
        "last_name": "test_last_name",
        "company": "TestCompany1",
        "address_1": "TestAddress 123 bld. 15",
        "address_2": "TestAddress 456 bld. 43",
        "country": "Australia",
        "state": "TestState",
        "city": "TestCity",
        "zipcode": "TestZIP",
        "mobile_number": "0412 345 678"
    }