import pytest

@pytest.fixture
def empty_user():
    return {
        "username": "",
        "email": "",
        "password": "",
        "dob_day": "",
        "dob_month": "",
        "dob_year": "",
        "first_name": "",
        "last_name": "",
        "company": "",
        "address_1": "",
        "address_2": "",
        "country": "India",
        "state": "",
        "city": "",
        "zipcode": "",
        "mobile_number": ""
    }

@pytest.fixture
def one_req_field_missing_user(random_user):
    return {
        "username": random_user["username"],
        "email": random_user["email"],
        "password": "test123",
        "dob_day": "20",
        "dob_month": "9",
        "dob_year": "2000",
        "first_name": "",
        "last_name": "test_last_name",
        "company": "TestCompany1",
        "address_1": "TestAddress 123 bld. 15",
        "address_2": "",
        "country": "Australia",
        "state": "TestState",
        "city": "TestCity",
        "zipcode": "TestZIP",
        "mobile_number": "0412 345 678"
    }
