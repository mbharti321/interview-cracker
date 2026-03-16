import requests

BASE_URL = "https://fakestoreapi.com/carts"
# BASE_URL = "http://localhost:8000/carts"
# BASE_URL = "http://127.0.0.1:8000/carts"

def get_all_carts():
    '''
    Task 1:
    Make a GET request to retrieve all carts.
    Store and return the response in JSON format.

    Example endpoint: GET /carts
    '''
    # pass  # Implementation goes here
    response = requests.get(BASE_URL)
    response.raise_for_status()
    all_carts_response = response.json()
    
    return all_carts_response


def get_carts_with_limit_and_sort(limit=5, sort_order="desc"):
    '''
    Task 2:
    Make a GET request to retrieve carts with a limit and sorting.
    Store and return the response in JSON format.

    Example endpoint: GET /carts?limit={limit}&sort={sort_order}
    '''
    # pass  # Implementation goes here
    params ={
        "limit": limit,
        "sort": sort_order
    }

    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()
    limited_sorted_carts_response = response.json()
    
    return limited_sorted_carts_response




def get_user_carts(user_id):
    '''
    Task 3:
    Make a GET request to retrieve carts for a specific user.
    Store and return the response in JSON format.

    Example endpoint: GET /carts/user/{user_id}
    '''
    # pass  # Implementation goes here
    user_url = f"{BASE_URL}/user/{user_id}"
    response = requests.get(user_url)
    response.raise_for_status()
    user_carts_response = response.json()
    
    return user_carts_response


def add_new_cart(cart_data):
    '''
    Task 4:
    Make a POST request to add a new cart.
    Store and return the response in JSON format.
    Example endpoint: POST /carts
    Example payload:
    {
        "userId": 5,
        "date": "2024-12-12",
        "products": [{"productId": 1, "quantity": 2}]
    }
    '''
    # pass  # Implementation goes here
    response = requests.post(BASE_URL, json=cart_data)
    response.raise_for_status()
    new_carts_response = response.json()
    
    return new_carts_response


def update_cart(cart_id, updated_data):
    '''
    Task 5:
    Make a PUT request to update an existing cart.
    Store and return the response in JSON format.

    Example endpoint: PUT /carts/{cart_id}
    Example payload:
    {
        "userId": 5,
        "date": "2024-12-14",
        "products": [{"productId": 2, "quantity": 4}]
    }
    '''
    # pass  # Implementation goes here
    url = f"{BASE_URL}/{cart_id}"
    response = requests.put(url, json=updated_data)
    response.raise_for_status()
    updated_carts_response = response.json()
    
    return updated_carts_response


def delete_cart(cart_id):
    '''
    Task 6:
    Make a DELETE request to delete a cart by ID.
    Store and return the response status/message.

    Example endpoint: DELETE /carts/{cart_id}
    '''
    # pass  # Implementation goes here
    url = f"{BASE_URL}/{cart_id}"
    response = requests.delete(url)
    response.raise_for_status()
    deleted_cart_response = response.json()
    
    return deleted_cart_response


def main():
    
    all_carts = get_all_carts()
    print("All Carts:", all_carts)

    limited_carts = get_carts_with_limit_and_sort(limit=3, sort_order="asc")
    print("Limited & Sorted Carts:", limited_carts)

    user_carts = get_user_carts(user_id=2)
    print("User Carts:", user_carts)

    new_cart_data = {
        "userId": 5,
        "date": "2024-12-12",
        "products": [{"productId": 1, "quantity": 2}, {"productId": 3, "quantity": 1}]
    }
    new_cart = add_new_cart(cart_data=new_cart_data)
    print("New Cart:", new_cart)

    updated_cart_data = {
        "userId": 5,
        "date": "2024-12-14",
        "products": [{"productId": 2, "quantity": 4}]
    }
    updated_cart = update_cart(cart_id=1, updated_data=updated_cart_data)
    print("Updated Cart:", updated_cart)

    deleted_cart = delete_cart(cart_id=1)
    print("Deleted Cart:", deleted_cart)


if __name__ == "__main__":
    main()
