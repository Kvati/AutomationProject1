import pytest

@pytest.mark.smoke
def test_user_verify_login(api_session, base_url, existing_user):

    response = api_session.post(f"{base_url}/api/verifyLogin", data={"email": existing_user["email"], "password": existing_user["password"]})

    assert response.status_code == 200
    body = response.json()
    assert body["responseCode"] == 200
    assert body["message"] == "User exists!"

@pytest.mark.regression
def test_user_verify_login_without_email(api_session, base_url, existing_user):

    response = api_session.post(f"{base_url}/api/verifyLogin", data={"password": existing_user["password"]})

    assert response.status_code == 200
    body = response.json()
    assert body["responseCode"] == 400
    assert body["message"] == "Bad request, email or password parameter is missing in POST request."

@pytest.mark.regression
def test_user_verify_login_without_password(api_session, base_url, existing_user):

    response = api_session.post(f"{base_url}/api/verifyLogin", data={"email": existing_user["email"]})

    assert response.status_code == 200
    body = response.json()
    assert body["responseCode"] == 400
    assert body["message"] == "Bad request, email or password parameter is missing in POST request."

@pytest.mark.regression
def test_user_verify_delete(api_session, base_url, existing_user):

    response = api_session.delete(f"{base_url}/api/verifyLogin")

    assert response.status_code == 200
    body = response.json()
    assert body["responseCode"] == 405
    assert body["message"] == "This request method is not supported."

@pytest.mark.regression
def test_user_verify_invalid_user(api_session, base_url):

    response = api_session.post(f"{base_url}/api/verifyLogin", data = {"email": "asd@test123.com", "password": "somepassword"})

    assert response.status_code == 200
    body = response.json()
    assert body["responseCode"] == 404
    assert body["message"] == "User not found!"