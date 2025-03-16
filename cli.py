#!/home/k/.pyenv/shims/python

import click
from db import session
from app import Menu, Customer, Order


@click.group(invoke_without_command=True)
@click.pass_context

def cli(ctx):
    pass
    if ctx.invoked_subcommand is None:
        interactive_menu(ctx)


def interactive_menu(ctx):
    while True:
        click.echo("\n---  Welcome to K Restaurant ---")
        click.echo("1. Add Customer")
        click.echo("2. View Customers")
        click.echo("3. Search Customer by ID")
        click.echo("4. View Menu")
        click.echo("5. Add Menu Item")
        click.echo("6. Delete Menu Item")
        click.echo("7. Create Order")
        click.echo("8. View Orders by Table")
        click.echo("9. Delete Order")
        click.echo("10. View Order Total")
        click.echo("0. Exit")

        choice = click.prompt("Select an option", type=int)

        if choice == 1:
            ctx = click.Context(add_customer)
            ctx.invoke(add_customer)
        elif choice == 2:
            ctx = click.Context(view_customers)
            ctx.invoke(view_customers)
        elif choice == 3:
            ctx = click.Context(search_customer_by_id)
            ctx.invoke(search_customer_by_id)
        elif choice == 4:
            ctx = click.Context(view_menu)
            ctx.invoke(view_menu)
        elif choice == 5:
            ctx = click.Context(add_menu_item)
            ctx.invoke(add_menu_item)
        elif choice == 6:
            ctx = click.Context(delete_menu_item)
            ctx.invoke(delete_menu_item)
        elif choice == 7:
            ctx = click.Context(create_order)
            ctx.invoke(create_order)
        elif choice ==8:
            ctx = click.Context(view_orders_by_table)
            ctx.invoke(view_orders_by_table)
        elif choice == 9:
            ctx = click.Context(delete_order)
            ctx.invoke(delete_order)
        elif choice == 10:
            ctx = click.Context(view_order_total)
            ctx.invoke(view_order_total)
        elif choice == 0:
            customer_name = None

            last_served_order = session.query(Order).filter_by(status="served").order_by(Order.id.desc()).first()

            if last_served_order:
                customer = session.query(Customer). filter_by(id=last_served_order.customer_id).first()
                if customer:
                    customer_name = customer.name

            if customer_name:
                click.echo(f"🫂 Goodbye {customer_name}, Thank you for being our customer!🙂")
            else:
                click.echo("Exiting...")

            break

@click.command()
@click.option('--name', prompt="Customer Name")
@click.option('--phone', prompt="Phone Number")
def add_customer(name, phone):
    name = click.prompt("Enter Customer Name", type=str)
    phone = click.prompt("Enter Phone Number", type=str)

    if not name.strip():
        click.echo("❌ Error: Name canot be empty.")
        return
    if not phone.strip():
        click.echo("❌ Error: Phone number cannot be empty.")
        return
    
    customer = Customer(name=name, phone=phone)
    session.add(customer)
    session.commit()
    click.echo(f"✅ Customer '{name}' added successfully!")


@click.command()
def view_customers():
    customers = session.query(Customer).all()
    for customer in customers:
        click.echo(customer)

@click.command()
def search_customer_by_id():
    customer_id = click.prompt("Enter Customer ID to search", type=int)
    customer = session.query(Customer).filter_by(id=customer_id).first()

    if customer:
        click.echo("✅ Customer Found:")
        click.echo(f"ID: {customer.id}")
        click.echo(f"Name: {customer.name}")
        click.echo(f"Phone: {customer.phone}")
    else:
        click.echo("❌ No customer found with that ID.")

@click.command()
def view_menu():
    menu_items= session.query(Menu).all()
    if menu_items:
        click.echo("Menu:")
        for item in menu_items:
            click.echo(f"{item.id} | {item.name} - KES {item.price} ({item.category})")
    else:
        click.echo("❌ No menu item, please add item")

@click.command()
@click.option('--name', prompt="Menu Name")
@click.option('--price', prompt="Price", type=float)
@click.option('--category', prompt="Category")
def add_menu_item(name, price, category):
    name = click.prompt("Enter menu item name", type=str)
    price = click.prompt("Enter price (KES)", type=float)
    category = click.prompt("Enter category (e.g., Drink, Main Course)", type=str)

    if not name.strip():
        click.echo("❌ Error: Name cannot be empty.")
        return
    if price <= 0:
        click.echo("❌ Error: Price must be greater than zero.")
        return
    if not category.strip():
        click.echo("❌ Error: Category cannot be empty.")
        return
    
    menu_item = Menu(name=name, price=price, category=category.strip())
    session.add(menu_item)
    session.commit()
    click.echo(f"✅ Menu item '{name}' added successfully!")

@click.command()
@click.option('--menu_id', prompt="Menu Item ID", type=int)
def delete_menu_item(menu_id):
    #item_id = click.prompt("Enter the ID of the menu item to delete", type=int)
    item = session.query(Menu).filter_by(id ==menu_id).first()
    if item:    
        session.delete(item)
        session.commit()
        click.echo(f"✅ Menu item '{item.name}' deleted successfully!") 
    else:
        click.echo("❌ Menu item not found.")

@click.command()
@click.option('--customer_id', prompt="Customer ID", type=int)
@click.option('--table_number', prompt="Table Number", type=int)
@click.option('--menu_items', prompt="Menu Item Names (comma-separated)")

def create_order(customer_id, table_number, menu_items):
    customer_id = click.prompt("Enter Customer ID", type=int)
    click.echo(f"🔍 Checking for Customer ID: {customer_id}")

    customer = session.query(Customer).filter_by(id=customer_id).first()
    if not customer:
        click.echo("❌ Error: Customer ID not found.")
        return
    
    table_number = click.prompt("Enter Table Number", type=int)

    click.echo(f"👋 Hello, {customer.name}! Ur Table Number is {table_number}")

    menu_items = click.prompt("Enter Menu Item Names (comma-separated)", type=str)
    menu_names = [name.strip() for name in menu_items.split(",")]
    menu_items = session.query(Menu).filter(Menu.name.in_(menu_names)).all()
    
    if not menu_items:
        click.echo("❌ Order cannot be created! Add menu item.")
        return
    
    if len(menu_items) == 0:
        click.echo("⚠️ Order cannot be empty! Please add at least one menu item.")
        return
    
    order = Order(customer_id=customer_id, table_number=table_number, status="pending")
    order.menu_items.extend(menu_items)
    session.add(order)
    session.commit()


    total_amount = sum(item.price for item in menu_items)
    menu_list = ','.join([item.name for item in menu_items])
    click.echo(f"✅ Welcome, {customer.name} Your Order for {menu_list} has been created - Total: KES {total_amount}")

@click.command()
@click.option('--table_number', prompt="Enter Table Number", type=int)
def view_orders_by_table(table_number):
    table_number = click.prompt ("Enter Table Number", type=int)
    orders = session.query(Order).filter_by(table_number=table_number).all()

    if not orders:
        click.echo(f"❌ No orders found for Table {table_number}.")
        return

    click.echo(f"\n📜 Orders for Table {table_number}:")
    for order in orders:
        menu_list = ', '.join([item.name for item in order.menu_items])
        total_amount = sum(item.price for item in order.menu_items)
        click.echo(f"Order {order.id} - {order.customer.name}: {menu_list} for Table {table_number} is Total: KES {total_amount}")

@click.command()
@click.option('--order_id', prompt="Order ID", type=int)
def delete_order(order_id):
    order_id = click.prompt("Enter Order ID", type=int)
    order = session.query(Order).filter_by(id=order_id).first()

    if not order:
        click.echo("❌ Order not found!")
        return
    
    order.menu_items.clear()
    session.delete(order)
    session.commit()
    click.echo(f"✅ Your Order ID {order_id} deleted successfully!")


@click.command()
@click.option('--order_id', prompt="Order ID", type=int)
def view_order_total(order_id):
    order_id = click.prompt("Enter Order ID", type=int)
    click.echo(f"🔍 Checking order ID {order_id}")
    order = session.query(Order).filter_by(id=order_id).first()
    if not order:
        click.echo("❌ Order not found!")
        return
    
    customer = session.query(Customer).filter_by(id=order.customer_id).first()
    if not customer:
        click.echo("❌ Customer not found!")
        return
    
    menu_items = order.menu_items
    if not menu_items:
        click.echo("❌ No items found in this order!")
        return
    
    menu_list = ','.join([item.name for item in order.menu_items])
    order_status = "Served" if order.status == "served" else "Waiting"
    total_amount = sum(item.price for item in order.menu_items)

    click.echo("\n--- Order Summary ---")
    click.echo(f"Customer: {customer.name}")
    click.echo(f"Food Items: {menu_list}")
    click.echo(f"Status: {order_status}")
    click.echo(f"Total: KES {total_amount}")
    click.echo(f"✅ Your Total Order for {menu_list} is KES: {total_amount}") 

cli.add_command(add_customer)
cli.add_command(view_customers)
cli.add_command(search_customer_by_id)
cli.add_command(view_menu)
cli.add_command(add_menu_item)
cli.add_command(delete_menu_item)
cli.add_command(create_order)
cli.add_command(view_orders_by_table)
cli.add_command(delete_order)
cli.add_command(view_order_total)

if __name__== '__main__':
    cli()

