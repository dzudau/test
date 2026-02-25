class Product:
    def __init__(self, product_id, name, price):
        self.product_id = product_id
        self.name = name
        self.price = price

    def __str__(self):
        return f"[{self.product_id}] {self.name} - {self.price} тенге"


class Cart:
    def __init__(self):
        self.items = []

    def add_product(self, product):
        self.items.append(product)

    def remove_product(self, product):
        if product in self.items:
            self.items.remove(product)
            print(f"Удалено: {product.name}")
        else:
            print("Товар не найден в корзине")

    def get_total(self):
        total = 0
        for product in self.items:
            total += product.price
        return total

    def show_cart(self):
        if not self.items:
            print("Корзина пуста")
            return
        print("\nКорзина:")
        for product in self.items:
            print(f"{product.name} = {product.price} тенге")
        print(f"Итого: {self.get_total()} тенге\n")


class Shop:
    def __init__(self):
        self.products = []

    def add_product(self, product):
        self.products.append(product)

    def show_products(self):
        print("\nСписок товаров:")
        for product in self.products:
            print(product)

    def get_product_by_id(self, product_id):
        for product in self.products:
            if product.product_id == product_id:
                return product
        return None


class User:
    def __init__(self, username):
        self.username = username
        self.cart = Cart()

    def __str__(self):
        return f"Пользователь: {self.username}"


class StoreApp:
    def __init__(self):
        self.shop = Shop()
        self.user = None
        self.seed_products()

    def seed_products(self):
        self.shop.add_product(Product(1, "яблоко", 50))
        self.shop.add_product(Product(2, "банан", 30))
        self.shop.add_product(Product(3, "хлеб", 40))
        self.shop.add_product(Product(4, "молоко", 60))

    def run(self):
        print("Добро пожаловать в магазин!")
        username = input("Введите имя пользователя: ")
        self.user = User(username)

        while True:
            print("\n1 - Показать товары")
            print("2 - Добавить в корзину")
            print("3 - Показать корзину")
            print("4 - Удалить из корзины")
            print("5 - Оформить заказ")
            print("0 - Выход")

            choice = input("Выберите действие: ")

            if choice == "1":
                self.shop.show_products()

            elif choice == "2":
                try:
                    product_id = int(input("Введите ID товара: "))
                except ValueError:
                    print("Введите число!")
                    continue

                product = self.shop.get_product_by_id(product_id)
                if product:
                    self.user.cart.add_product(product)
                else:
                    print("Товар не найден")

            elif choice == "3":
                self.user.cart.show_cart()

            elif choice == "4":
                try:
                    product_id = int(input("Введите ID товара для удаления: "))
                except ValueError:
                    print("Введите число!")
                    continue

                product = self.shop.get_product_by_id(product_id)
                if product:
                    self.user.cart.remove_product(product)
                else:
                    print("Товар не найден")

            elif choice == "5":
                total = self.user.cart.get_total()
                if total > 0:
                    print(f"Заказ оформлен! Сумма к оплате: {total} тенге")
                    self.user.cart = Cart()
                else:
                    print("Корзина пуста")

            elif choice == "0":
                print("До свидания!")
                break

            else:
                print("Неверный ввод")


if __name__ == "__main__":
    app = StoreApp()
    app.run()