import unittest
from main import (
    get_all_carts,
    get_carts_with_limit_and_sort,
    get_user_carts,
    add_new_cart,
    update_cart,
    delete_cart,
)

class TestCartManagementSystem(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Setup any reusable data
        cls.new_cart_data = {
            "userId": 5,
            "date": "2024-12-12",
            "products": [{"productId": 1, "quantity": 2}, {"productId": 3, "quantity": 1}],
        }
        cls.updated_cart_data = {
            "userId": 5,
            "date": "2024-12-14",
            "products": [{"productId": 2, "quantity": 4}],
        }
        cls.test_cart_id = None  # To be updated after creating a cart

    def test_1_get_all_carts(self):
        """Test retrieving all carts."""
        carts = get_all_carts()
        self.assertIsInstance(carts, list)
        self.assertGreater(len(carts), 0, "No carts were returned")
        self.assertIn("id", carts[0], "Cart data is missing 'id'")
        self.assertIn("userId", carts[0], "Cart data is missing 'userId'")

    def test_2_get_carts_with_limit_and_sort(self):
        """Test retrieving carts with a limit and sorting."""
        carts = get_carts_with_limit_and_sort(limit=3, sort_order="asc")
        self.assertIsInstance(carts, list)
        self.assertEqual(len(carts), 3, "Carts returned do not match the limit")
        self.assertLessEqual(carts[0]["id"], carts[1]["id"], "Carts are not sorted in ascending order")


if __name__ == "__main__":
    unittest.main()
