"""Tiny in-memory order application."""
from dataclasses import dataclass

@dataclass
class Order:
    id: int
    status: str = 'NEW'

ORDERS = {1: Order(1), 2: Order(2, 'SHIPPED')}

def get_order(order_id: int) -> Order:
    if order_id not in ORDERS:
        raise ValueError('Order not found')
    return ORDERS[order_id]
