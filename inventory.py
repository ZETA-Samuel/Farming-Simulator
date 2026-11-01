class Inventory:

    def __init__(self):
        self.coins = 1000

        self.items = {}

    def add_item(self,item,quantity = 1):
        if not isinstance(quantity, int) or isinstance(quantity, bool) or quantity < 1:
            raise ValueError("quantity must be a positive integer")

        if item not in self.items:
            self.items[item] = 0

        self.items[item] += quantity

    def remove_item(self,item,quantity = 1):
        if not self.has_items(item, quantity):
            return False

        self.items[item] -= quantity
        if self.items[item] == 0:
            del self.items[item]
        return True

    def has_coins(self, amount):
        return isinstance(amount, int) and not isinstance(amount, bool) and amount >= 0 and self.coins >= amount

    def buy(self,item,price):
        if not isinstance(price, int) or isinstance(price, bool) or price < 0:
            return False
        if not self.has_coins(price):
            return False

        self.coins -= price
        self.add_item(item)
        return True

    def has_items(self, item, quantity=1):
        return (
            isinstance(quantity, int)
            and not isinstance(quantity, bool)
            and quantity > 0
            and self.items.get(item, 0) >= quantity
        )

    def sell(self, item, price, quantity=1):
        if not isinstance(price, int) or isinstance(price, bool) or price < 0:
            return False
        if not self.has_items(item, quantity):
            return False

        self.remove_item(item, quantity)
        self.coins += price * quantity
        return True