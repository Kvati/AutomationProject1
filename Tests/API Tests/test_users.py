import pytest

# the fixture register_user creates a random email, which I need for deletion so for the sake of sending a
# parameter I save email in a separate static variable

def test_create_user(api_session, base_url, register_user):
    email = register_user["email"]

    response = api_session.post(f"{base_url}/api/createAccount", data = {"name": register_user["username"],
    "password": register_user["password"], "email": email,
    "dob_day": register_user["dob_day"], "dob_month": register_user["dob_month"],
    "dob_year": register_user["dob_year"], "firstname": register_user["first_name"],
    "lastname": register_user["last_name"], "company": register_user["company"],
    "address1": register_user["address_1"], "address2": register_user["address_2"],
    "country": register_user["country"], "city": register_user["city"],
    "state": register_user["state"], "zipcode": register_user["zipcode"],
    "mobile_number": register_user["mobile_number"]})

    assert response.status_code == 200
    body = response.json()
    assert body["responseCode"] == 201
    assert body["message"] == "User created!"

    api_session.delete(f"{base_url}/api/deleteAccount", data={"email": register_user["email"],"password": register_user["password"]})

@pytest.mark.xfail(reason="Known issue: API does not validate fields JIRA-123")
def test_create_user_with_missing_field(api_session, base_url, register_user):

    response = api_session.post(f"{base_url}/api/createAccount", data = {"name": register_user["username"],
    "password": "", "email": register_user["email"],
    "dob_day": register_user["dob_day"], "dob_month": register_user["dob_month"],
    "dob_year": register_user["dob_year"], "firstname": "",
    "lastname": register_user["last_name"], "company": register_user["company"],
    "address1": "", "address2": register_user["address_2"],
    "country": register_user["country"], "city": register_user["city"],
    "state": register_user["state"], "zipcode": register_user["zipcode"],
    "mobile_number": register_user["mobile_number"]})

    assert response.status_code == 200
    body = response.json()
    assert body["responseCode"] == 400

    api_session.delete(f"{base_url}/api/deleteAccount", data={"email": register_user["email"], "password": register_user["password"]})

def test_delete_user(api_session, base_url, register_user):
    email = register_user["email"]

    response_setup = api_session.post(f"{base_url}/api/createAccount", data={"name": register_user["username"],
    "password": register_user["password"], "email": email,
    "dob_day": register_user["dob_day"], "dob_month": register_user["dob_month"],
    "dob_year": register_user["dob_year"], "firstname": register_user["first_name"],
    "lastname": register_user["last_name"], "company": register_user["company"],
    "address1": register_user["address_1"], "address2": register_user["address_2"],
    "country": register_user["country"], "city": register_user["city"],
    "state": register_user["state"], "zipcode": register_user["zipcode"],
    "mobile_number": register_user["mobile_number"]})

    assert response_setup.status_code == 200
    body_setup = response_setup.json()
    assert body_setup["responseCode"] == 200

    response = api_session.delete(f"{base_url}/api/deleteAccount", data={"email": email, "password": register_user["password"]})

    assert response.status_code == 200
    body = response.json()
    assert body["responseCode"] == 200
    assert body["message"] == "Account deleted!"

def test_update_user_information(api_session, base_url, register_user):
    name = register_user["username"]
    email = register_user["email"]

    response_setup = api_session.post(f"{base_url}/api/createAccount", data={"name": name,
    "password": register_user["password"], "email": email,
    "dob_day": register_user["dob_day"], "dob_month": register_user["dob_month"],
    "dob_year": register_user["dob_year"], "firstname": register_user["first_name"],
    "lastname": register_user["last_name"], "company": register_user["company"],
    "address1": register_user["address_1"], "address2": register_user["address_2"],
    "country": register_user["country"], "city": register_user["city"],
    "state": register_user["state"], "zipcode": register_user["zipcode"],
    "mobile_number": register_user["mobile_number"]})

    assert response_setup.status_code == 200
    body_setup = response_setup.json()
    assert body_setup["responseCode"] == 200

    response = api_session.put(f"{base_url}/api/updateAccount", data={"name": register_user["username"],
    "password": register_user["password"], "email": register_user["email"],
    "dob_day": register_user["dob_day"], "dob_month": register_user["dob_month"],
    "dob_year": register_user["dob_year"], "firstname": register_user["first_name"],
    "lastname": "new_last_name", "company": register_user["company"],
    "address1": "new_address", "address2": register_user["address_2"],
    "country": "India", "city": register_user["city"],
    "state": register_user["state"], "zipcode": "1523",
    "mobile_number": register_user["mobile_number"]})

    assert response.status_code == 200
    body = response.json()
    assert body["responseCode"] == 200
    assert body["message"] == "User updated!"

    verify = api_session.get(f"{base_url}/api/getUserDetailByEmail", params={"email": register_user["email"]})
    assert verify.json["user"]["lastname"] == "new_last_name"

    api_session.delete(f"{base_url}/api/deleteAccount", data={"email": register_user["email"],"password": register_user["password"]})

def test_get_user_account_detail_by_email(api_session, base_url, existing_user):
    response = api_session.get(f"{base_url}/api/getUserDetailByEmail", params = {"email": existing_user["email"]})

    assert response.status_code == 200
    body = response.json()
    assert body["responseCode"] == 200
    assert body["user"]["name"] == existing_user["username"]
    assert body["user"]["email"] == existing_user["email"]

def test_get_user_account_detail_by_invalid_email(api_session,base_url):
    response = api_session.get(f"{base_url}/api/getUserDetailByEmail", params={"email": "random123email@123emailtest.com"})

    assert response.status_code == 200
    body = response.json()
    assert body["responseCode"] == 404
    assert body["message"] == "Account not found with this email, try another email!"

def test_get_user_account_detail_by_no_email(api_session,base_url):
    response = api_session.get(f"{base_url}/api/getUserDetailByEmail")

    assert response.status_code == 200
    body = response.json()
    assert body["responseCode"] == 400
    assert body["message"] == "Bad request, email parameter is missing in GET request."

def test_create_duplicate_user(api_session, base_url, existing_user):

    response = api_session.post(f"{base_url}/api/createAccount", data = {"name": existing_user["username"],
    "password": existing_user["password"], "email": existing_user["email"],
    "dob_day": existing_user["dob_day"], "dob_month": existing_user["dob_month"],
    "dob_year": existing_user["dob_year"], "firstname": existing_user["first_name"],
    "lastname": existing_user["last_name"], "company": existing_user["company"],
    "address1": existing_user["address_1"], "address2": existing_user["address_2"],
    "country": existing_user["country"], "city": existing_user["city"],
    "state": existing_user["state"], "zipcode": existing_user["zipcode"],
    "mobile_number": existing_user["mobile_number"]})

    assert response.status_code == 200
    body = response.json()
    assert body["responseCode"] == 400
    assert body["message"] == "Email already exists!"