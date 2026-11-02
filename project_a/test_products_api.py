import pytest
import requests

BASE_URL = "https://dummyjson.com"


@pytest.mark.parametrize(
    "product_id",
    [
        pytest.param(1, id="first-product"),
        pytest.param(2, id="second-product"),
        pytest.param(3, id="third-product"),
    ],
)
def test_get_product_by_id(product_id):
    # TODO 1: Send a GET request to /products/{product_id}
    response = requests.get(f"{BASE_URL}/products/{product_id}")
    # TODO 2: Assert that the status code is 200
    assert response.status_code == 200
    # TODO 3: Parse the JSON response
    data = response.json()
    # TODO 4: Assert that the returned ID matches product_id
    assert data.get("id") == product_id
    # TODO 5: Assert that the response contains a title and price
    assert data.get("title")
    assert data.get("price")


@pytest.mark.parametrize(
    "search_term",
    [
        pytest.param("phone", id="search-phone"),
        pytest.param("laptop", id="search-laptop"),
    ],
)
def test_search_products(search_term):
    # TODO: Send GET /products/search with q=search_term
    response = requests.get(f"{BASE_URL}/products/search", params={"q": search_term})
    # TODO: Assert status code and response structure
    assert response.status_code == 200
    data = response.json()
    for key in ("products", "total", "skip", "limit"):
        assert key in data
    assert isinstance(data["products"], list)
    assert len(data["products"]) > 0
    assert data["total"] >= len(data["products"])
    # TODO: Verify the search behavior against the API's documented contract
    for product in data["products"]:
        searchable = " ".join(
            [
                product.get("title") or "",
                product.get("description") or "",
                product.get("category") or "",
                product.get("brand") or "",
                " ".join(product.get("tags") or []),
            ]
        ).lower()
        assert search_term in searchable, (
            f"'{search_term}' not found in product {product.get('id')}: {product.get('title')}"
        )


@pytest.mark.parametrize(
    "limit, skip",
    [
        pytest.param(1, 0, id="one-result"),
        pytest.param(5, 5, id="five-results"),
    ],
)
def test_product_limit(limit, skip):
    # TODO: Send GET /products with the limit query parameter
    response = requests.get(
        f"{BASE_URL}/products", params={"limit": limit, "skip": skip}
    )
    # TODO: Assert status code
    assert response.status_code == 200
    data = response.json()
    # TODO: Assert len(response["products"]) <= limit
    assert len(data["products"]) <= limit
    # TODO: Check the response pagination metadata
    assert data["limit"] == limit
    assert data["skip"] == skip
    assert data["total"] >= len(data["products"])