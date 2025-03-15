#!/home/k/.pyenv/shims/python

import click
from db import session
from app import Menu, Customer, Order


@click.group(invoke_without_command=True)
@click.pass_context

def cli(ctx):
    if ctx.invoked_subcommand is None:
        interactive_menu(ctx)


def interactive_menu(ctx):
    while True:
        click.echo("\n---  Welcome to K Restaurant ---")
        click.echo("1. Add Menu Item")
        click.echo("2. View Menu")
        click.echo("3. Delete Menu Item")
        click.echo("4. Add Customer")
        click.echo("5. View Customers")
        click.echo("6. Search Customer by ID")
        click.echo("7. Create Order")
        click.echo("8. View Order Total")
        click.echo("9. Delete Order")
        click.echo("0. Exit")

        choice = click.prompt("Select an option", type=int)

        if choice == 1:
            ctx = click.Context(add_menu_item)
            ctx.invoke(add_menu_item)
        elif choice == 2:
            ctx = click.Context(view_menu)
            ctx.invoke(view_menu)
        elif choice == 3:
            ctx = click.Context(delete_menu_item)
            ctx.invoke(delete_menu_item)
        elif choice == 4:
            ctx = click.Context(add_customer)
            ctx.invoke(add_customer)
        elif choice == 5:
            ctx = click.Context(view_customers)
            ctx.invoke(view_customers)
        elif choice == 6:
            ctx = click.Context(search_customer_by_id)
            ctx.invoke(search_customer_by_id)
        elif choice == 7:
            ctx = click.Context(create_order)
            ctx.invoke(create_order)
        elif choice == 8:
            ctx = click.Context(view_order_total)
            ctx.invoke(view_order_total)
        elif choice == 9:
            ctx = click.Context(delete_order)
            ctx.invoke(delete_order)
        elif choice == 0:
            click.echo("Exiting...")
            break
        else:
            click.echo("Invalid option, please try again.")


@click.command()
@click.option('--name', prompt="Menu Name")
@click.option('--price', prompt="Price", type=float)
@click.option('--category', prompt="Category")

def add_menu_item(name, price, category):
    name = click.prompt("Enter menu item name", type=str)
    price = click.prompt("Enter price (KES)", type=float)
    category = click.prompt("Enter category (e.g., Drink, Main Course)", type=str)

    if not name.strip():
        click.echo("Erro: Name cannot be empty.")
        return
    if price <= 0:
        click.echo("Error: Price must be greater than zero.")
        return
    if not category.strip():
        click.echo("Error: Category cannot be empty.")
        return
    
    menu_item = Menu(name=name, price=price, category=category.strip())
    session.add(menu_item)
    session.commit()
    click.echo(f"Menu item '{name}' added successfully!")

@click.command()

def view_menu():
    menu = session.query(Menu).all()
    for item in menu:
        click.echo(item)

@click.command()
@click.option('--menu_id', prompt="Menu Item ID", type=int)

def delete_menu_item():
    item_id = click.prompt("Enter the ID of the menu item to delete", type=int)
    item_to_delete = session.query(Menu).filter(Menu.id == item_id).first()
    if not item_to_delete:
        click.echo("❌ Error: Menu item not found!")
        return
        
    session.delete(item_to_delete)
    session.commit()
    click.echo(f"✅ Menu item with ID {item_id} deleted successfully!") 


#customer management
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
        click.echo(f"📞 Phone: {customer.phone}")
    else:
        click.echo("❌ No customer found with that ID.")

#order management
@click.command()
@click.option('--customer_id', prompt="Customer ID", type=int)
@click.option('--menu_ids', prompt="Menu Item IDs (comma-separated)")

def create_order(customer_id, menu_ids):
    
    menu_ids = [int(id.strip()) for id in menu_ids.split(",")]
    menu_items = session.query(Menu).filter(Menu.id.in_(menu_ids)).all()
    
    if not menu_items:
        click.echo("No valid menu items found!")
        return
    
    order = Order(customer_id=customer_id)
    order.menu_items.extend(menu_items)
    session.add(order)
    session.commit()
    click.echo(f"Order {order.id} created with {len(menu_items)} items - Total: KES {order.total_amount}")
    
@click.command()
@click.option('--order_id', prompt="Order ID", type=int)

def view_order_total(order_id):
    order = session.query(Order).filter_by(id=order_id).first()
    if order:
        click.echo(f"Order {order.id} Total: KES {order.total_amount}")
    else:
        click.echo("Order not found!")
        
@click.command()
@click.option('--order_id', prompt="Order ID", type=int)

def delete_order(order_id):
    order = session.query(Order).filter_by(id=order_id).first()
    if order:
        order.menu_items = []
        session.delete(order)
        session.commit()
        click.echo("Order deleted.")
    else:
        click.echo("Order not found!")



cli.add_command(add_menu_item)
cli.add_command(view_menu)
cli.add_command(delete_menu_item)
cli.add_command(add_customer)
cli.add_command(view_customers)
cli.add_command(search_customer_by_id)
cli.add_command(create_order)
cli.add_command(view_order_total)
cli.add_command(delete_order)


if __name__== '__main__':
    cli()

