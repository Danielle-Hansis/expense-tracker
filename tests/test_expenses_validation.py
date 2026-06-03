"""
# simulates submitting the HTML form
# checks the backend validation
def test_create_expense_invalid_amount_letters_returns_400(client, any_category_id):
    response = client.post(
        "/expenses",
        data={
            "amount": "abc",
            "description": "test",
            "category_id": str(any_category_id),
        },
    )

    assert response.status_code == 400


def test_create_expense_invalid_amount_negative_returns_400(client, any_category_id):
    response = client.post(
        "/expenses",
        data={
            "amount": "-5",
            "description": "test",
            "category_id": str(any_category_id),
        },
    )

    assert response.status_code == 400


def test_create_expense_valid_returns_redirect(client, any_category_id):
    response = client.post(
        "/expenses",
        data={
            "amount": "12.50",
            "description": "coffee",
            "category_id": str(any_category_id),
        },
    )

    # Most CRUD forms redirect after success
    assert response.status_code in (302, 303)
"""