class Product:

    def __init__(self, name, categoria, price, quantity):
        self.name = name
        self.categoria = categoria
        self.price = float(price)
        self.quantity = int(quantity)

    def update_price(self, new_price):
        if new_price >= 0:
            self.price = new_price
        else:
            raise ValueError("not correct price")

    def update_quantity(self, new_quantity):
        if new_quantity >= 0:
            self.quantity = new_quantity
        else:
            raise ValueError("not correct quantity")

class Customer:

    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.orders = []

    def add_new_order(self, order):
        self.orders.append(order)

    def __str__(self):
        return f"{self.name}, {self.email}"

class Order:

    def __init__(self):
        self.total_price = 0
        self.product_list = []

    def add_product(self, product):
        self.product_list.append(product)


    def get_total_price(self):
        self.total_price = 0
        for product in self.product_list:
            self.total_price += product.price * product.quantity

        return self.total_price

customer = Customer("Mark", "mark@gmail.com")
order = Order()

with open('products.txt', 'r') as file:
    for product_line in file:
        print(product_line)
        name, categoria, price, quantity = product_line.strip().split(",")

        product = Product(name, categoria, price, quantity)
        order.add_product(product)

customer.add_new_order(order)


print(customer)
print(f"Total_price: {order.get_total_price()}")
