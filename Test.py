from abc import ABC, abstractmethod
class User:
    def __init__(self, user_id, name, email, address):
        self.__user_id = user_id  # Encapsulated attribute
        self.name = name
        self.email = email
        self.address = address
        self.__password = None  # Should be set through setter

    def set_password(self, password):
        # Simple password storage for demonstration (in real apps, use hashing)
        self.__password = password

    def verify_password(self, password):
        return self.__password == password

    def get_user_id(self):
        return self.__user_id

    def update_address(self, new_address):
        self.address = new_address


class Customer(User):
    def __init__(self, user_id, name, email, address):
        super().__init__(user_id, name, email, address)
        self.__cart = []  # List of product objects
        self.__order_history = []
        self.__loyalty_points = 0

    def add_to_cart(self, product):
        if product.stock > 0:
            self.__cart.append(product)
            return True
        return False

    def remove_from_cart(self, product):
        if product in self.__cart:
            self.__cart.remove(product)
            return True
        return False

    def view_cart(self):
        total = 0
        print("\nYour Shopping Cart:")
        for idx, product in enumerate(self.__cart, 1):
            print(f"{idx}. {product.name} - ₹{product.price}")
            total += product.price
        print(f"Total: ₹{total}")
        return total

    def checkout(self):
        if not self.__cart:
            return None

        total = self.view_cart()
        order = Order(f"ORD-{self.get_user_id()}-{len(self.__order_history) + 1}",
                      self.__cart.copy(), total)
        self.__order_history.append(order)
        self.__cart.clear()
        self.__loyalty_points += int(total / 100)  # 1 point per ₹100
        return order


class Admin(User):
    def __init__(self, user_id, name, email, address):
        super().__init__(user_id, name, email, address)
        self.__access_level = "full"

    def add_product(self, inventory, product):
        inventory.add_product(product)
        return f"Added {product.name} to inventory"

    def update_product(self, inventory, product_id, new_price=None, new_stock=None):
        product = inventory.get_product(product_id)
        if product:
            if new_price:
                product.price = new_price
            if new_stock:
                product.stock = new_stock
            return f"Updated product {product_id}"
        return "Product not found"


class Product:
    def __init__(self, product_id, name, price, stock, category=None):
        self.__product_id = product_id
        self.name = name
        self.price = price
        self.stock = stock
        self.category = category

    def get_product_id(self):
        return self.__product_id

    def update_stock(self, quantity):
        self.stock += quantity

    def display_info(self):
        return (f"ID: {self.__product_id} | {self.name} | "
                f"Price: ₹{self.price} | Stock: {self.stock}")


class Inventory:
    def __init__(self):
        self.__products = {}

    def add_product(self, product):
        self.__products[product.get_product_id()] = product

    def get_product(self, product_id):
        return self.__products.get(product_id)

    def list_products(self):
        return "\n".join([p.display_info() for p in self.__products.values()])


class Order:
    def __init__(self, order_id, products, total_amount):
        self.__order_id = order_id
        self.products = products  # List of Product objects
        self.total_amount = total_amount
        self.__status = "Processing"
        self.__order_date = "Today"  # In real app, use datetime

    def get_order_id(self):
        return self.__order_id

    def update_status(self, new_status):
        self.__status = new_status

    def get_status(self):
        return self.__status

    def display_order(self):
        print(f"\nOrder ID: {self.__order_id}")
        print("Items:")
        for product in self.products:
            print(f"- {product.name}: ₹{product.price}")
        print(f"Total: ₹{self.total_amount}")
        print(f"Status: {self.__status}")


# Payment Classes using Abstraction
class Payment(ABC):
    @abstractmethod
    def process_payment(self, amount):
        pass


class CreditCardPayment(Payment):
    def process_payment(self, amount):
        print(f"Processing credit card payment of ₹{amount}")
        return True


class UPIPayment(Payment):
    def process_payment(self, amount):
        print(f"Processing UPI payment of ₹{amount}")
        return True


class CashOnDelivery(Payment):
    def process_payment(self, amount):
        print(f"Order placed with COD amount ₹{amount}")
        return True


# Main System Class
class ECommerceSystem:
    def __init__(self):
        self.inventory = Inventory()
        self.users = {}
        self.current_user = None

    def register_user(self, user_type, name, email, address, password):
        user_id = f"USER-{len(self.users) + 1}"
        if user_type.lower() == "customer":
            user = Customer(user_id, name, email, address)
        else:
            user = Admin(user_id, name, email, address)
        user.set_password(password)
        self.users[email] = user
        return user

    def login(self, email, password):
        user = self.users.get(email)
        if user and user.verify_password(password):
            self.current_user = user
            return user
        return None

    def run(self):
        # Sample initialization
        self.inventory.add_product(Product("P1001", "Laptop", 50000, 10, "Electronics"))
        self.inventory.add_product(Product("P1002", "Smartphone", 25000, 15, "Electronics"))

        while True:
            print("\n==== E-Commerce System ====")
            print("1. Register")
            print("2. Login")
            print("3. View Products")
            print("4. Exit")

            choice = input("Enter choice: ")

            if choice == "1":
                name = input("Name: ")
                email = input("Email: ")
                address = input("Address: ")
                password = input("Password: ")
                user_type = input("User Type (customer/admin): ")
                self.register_user(user_type, name, email, address, password)
                print("Registration successful!")

            elif choice == "2":
                email = input("Email: ")
                password = input("Password: ")
                user = self.login(email, password)
                if user:
                    print(f"Welcome, {user.name}!")
                    self.user_menu(user)
                else:
                    print("Invalid credentials")

            elif choice == "3":
                print("\nAvailable Products:")
                print(self.inventory.list_products())

            elif choice == "4":
                print("Goodbye!")
                break

            else:
                print("Invalid choice")

    def user_menu(self, user):
        while True:
            print("\n==== User Menu ====")
            print("1. View Products")
            print("2. Add to Cart")
            print("3. View Cart")
            print("4. Checkout")
            print("5. View Orders")
            print("6. Logout")

            choice = input("Enter choice: ")

            if choice == "1":
                print("\nAvailable Products:")
                print(self.inventory.list_products())

            elif choice == "2":
                product_id = input("Enter product ID: ")
                product = self.inventory.get_product(product_id)
                if product:
                    if isinstance(user, Customer):
                        if user.add_to_cart(product):
                            print(f"Added {product.name} to cart")
                        else:
                            print("Product out of stock")
                    else:
                        print("Only customers can add to cart")
                else:
                    print("Product not found")

            elif choice == "3":
                if isinstance(user, Customer):
                    user.view_cart()
                else:
                    print("Only customers have carts")

            elif choice == "4":
                if isinstance(user, Customer):
                    order = user.checkout()
                    if order:
                        print("\nOrder placed successfully!")
                        order.display_order()
                else:
                    print("Only customers can checkout")

            elif choice == "5":
                if isinstance(user, Customer):
                    print("\nYour Orders:")
                    for order in user._Customer__order_history:
                        order.display_order()
                else:
                    print("Only customers have order history")

            elif choice == "6":
                self.current_user = None
                print("Logged out successfully")
                break

            else:
                print("Invalid choice")


# Start the system
if __name__ == "__main__":
    system = ECommerceSystem()
    system.run()