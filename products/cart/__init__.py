import json
from typing import List
import products
from cart import dao
from products import Product


class Cart:
    def _init_(self, id: int, username: str, contents: List[Product], cost: float):
        self.id = id
        self.username = username
        self.contents = contents
        self.cost = cost

    @staticmethod
    def load(data: dict) -> "Cart":
        return Cart(
            id=data['id'],
            username=data['username'],
            contents=[products.get_product(prod_id) for prod_id in data.get('contents', [])],
            cost=data['cost']
        )


def get_cart(username: str) -> List[Product]:
    cart_details = dao.get_cart(username)
    if not cart_details:
        return []

    products_in_cart = []
    for cart_detail in cart_details:
        try:
            contents = json.loads(cart_detail['contents'])
            products_in_cart.extend(
                products.get_product(prod_id) for prod_id in contents
            )
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error loading cart contents: {e}")
            continue
    return products_in_cart


def add_to_cart(username: str, product_id: int) -> None:
    dao.add_to_cart(username, product_id)


def remove_from_cart(username: str, product_id: int) -> None:
    dao.remove_from_cart(username, product_id)


def delete_cart(username: str) -> None:
    dao.delete_cart(username)
