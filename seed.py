#!/home/k/.pyenv/shims/python

from db import session
from app.menu import Menu
from app.customer import Customer
from app.order import Order

def seed_data():
    
    print("Seeding database...")

    session.query(Order).delete()
    session.query(Customer).delete()
    session.query(Menu).delete()


    menu_items = [
        Menu(name="Cheeseburger", price=300),
        Menu(name="Pizza", price=1100),
        Menu(name="Pasta", price=250)
    ]
    session.add_all(menu_items)


    customers = [
        Customer(name="Alice", phone="1234567890"),
        Customer(name="Bob", phone="0987654321")
    ]
    session.add_all(customers)


    order1 = Order(customer=customers[0], menu_items=[menu_items[0], menu_items[1]])  # Cheeseburger + Pizza
    order2 = Order(customer=customers[1], menu_items=[menu_items[2]])  # Pasta

    session.add_all([order1, order2])


    session.commit()
    print("Database seeded successfully!")

if __name__ == "__main__":
    seed_data()
