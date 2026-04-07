
def test_get_all_products(api_session, base_url):
    response = api_session.get(f"{base_url}/api/productsList")

    assert response.status_code == 200

    body = response.json()
    assert body["responseCode"] == 200
    assert "products" in body
    assert len(body["products"]) > 0
    assert isinstance(body["products"], list)
    ids = [p["id"] for p in body["products"]]
    assert len(ids) == len(set(ids))
    for product in body["products"]:
        assert "id" in product
        assert "name" in product
        assert "price" in product
        assert "category" in product
        assert isinstance(product["name"], str)
        assert isinstance(product["id"], int)
        assert product["name"].strip() != ""


def test_post_product_unsupported(api_session, base_url):
    response = api_session.post(f"{base_url}/api/productsList")

    assert response.status_code == 200
    body = response.json()
    assert body["responseCode"] == 405

def test_get_all_brands(api_session, base_url):
    response = api_session.get(f"{base_url}/api/brandsList")
    expected_brands = {"Polo", "H&M", "Madame", "Mast & Harbour", "Babyhug", "Allen Solly Junior", "Kookie Kids", "Biba"}

    assert response.status_code == 200
    body = response.json()
    assert body["responseCode"] == 200
    assert "brands" in body
    actual_brands = {b["brand"] for b in body["brands"]}
    assert isinstance(body["brands"], list)
    assert len(body["brands"]) > 0
    assert expected_brands.issubset(actual_brands)

    for brand in body["brands"]:
        assert "id" in brand
        assert "brand" in brand
        assert isinstance(brand["brand"], str)
        assert isinstance(brand["id"], int)
        assert brand["id"] > 0
        assert brand["brand"].strip() != ""

def test_put_all_brands_unsupported(api_session, base_url):
    response = api_session.put(f"{base_url}/api/brandsList")

    assert response.status_code == 200
    body = response.json()
    assert body["responseCode"] == 405

def test_search_for_product(api_session, base_url):
    search_query = "jean"

    response = api_session.post(f"{base_url}/api/searchProduct", data={"search_product": search_query})

    assert response.status_code == 200
    body = response.json()
    assert body["responseCode"] == 200
    assert "products" in body
    assert len(body["products"]) > 0
    for product in body["products"]:
        assert search_query.lower() in product["name"].lower()

def test_search_without_search_parameter(api_session, base_url):
    response = api_session.post(f"{base_url}/api/searchProduct")

    assert response.status_code == 200
    body = response.json()
    assert body["responseCode"] == 400

def test_search_no_result(api_session, base_url):
    search_query = "somejibberish"

    response = api_session.post(f"{base_url}/api/searchProduct", data={"search_product": search_query})

    assert response.status_code == 200
    body = response.json()
    if body["responseCode"] == 200:
        assert body["products"] == []
    else:
        assert body["responseCode"] == 404
