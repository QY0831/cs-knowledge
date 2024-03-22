"""
策略模式：
定义一系列算法，把它们一一封装起来，并且使它们可以相互替换。本模式使得算法可以独立于使用它的客户而变化。---- <设计模式>

例子：
根据Order，应用最佳的打折方法
"""
from collections.abc import Sequence
from dataclasses import dataclass
from decimal import Decimal
from typing import Optional, Callable, NamedTuple

class Customer(NamedTuple):
    name: str
    fidelity: int

class LineItem(NamedTuple):
    product: str
    quantity: int
    price: Decimal

    def total(self):
        return self.price * self.quantity

@dataclass(frozen=True)
class Order:  # 上下文
    customer: Customer
    cart: Sequence[LineItem]
    promotion: Optional[Callable[['Order'], Decimal]] = None  

    def total(self) -> Decimal:
        totals = (item.total() for item in self.cart)
        return sum(totals, start=Decimal(0))

    def due(self) -> Decimal:
        if self.promotion is None:
            discount = Decimal(0)
        else:
            discount = self.promotion(self)  
        return self.total() - discount

    def __repr__(self):
        return f'<Order total: {self.total():.2f} due: {self.due():.2f}>'


Promotion = Callable[[Order], Decimal]

promos: list[Promotion] = []  
def promotion(promo: Promotion) -> Promotion: # 装饰器方法
    promos.append(promo) # 在模块加载的时候就运行
    return promo

def best_promo(order: Order) -> Decimal:
    """选择可用的最佳折扣"""
    return max(promo(order) for promo in promos)  

@promotion  
def fidelity(order: Order) -> Decimal:
    """为积分为1000或以上的顾客提供5%折扣"""
    if order.customer.fidelity >= 1000:
        return order.total() * Decimal('0.05')
    return Decimal(0)


@promotion
def bulk_item(order: Order) -> Decimal:
    """单个商品的数量为20个或以上时提供10%折扣"""
    discount = Decimal(0)
    for item in order.cart:
        if item.quantity >= 20:
            discount += item.total() * Decimal('0.1')
    return discount


@promotion
def large_order(order: Order) -> Decimal:
    """订单中不同商品的数量达到10个或以上时提供7%折扣"""
    distinct_items = {item.product for item in order.cart}
    if len(distinct_items) >= 10:
        return order.total() * Decimal('0.07')
    return Decimal(0)


if __name__ == "__main__":
    joe = Customer('John Doe', 0)
    ann = Customer('Ann Smith', 1100)
    cart = [LineItem('banana', 4, Decimal('.5')),
            LineItem('apple', 10, Decimal('1.5')),
            LineItem('watermelon', 5, Decimal(5))]
    print(Order(joe, cart, best_promo))
    print(Order(ann, cart, best_promo))
