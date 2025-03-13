#!/home/k/.pyenv/shims/python

import click
from app import session, Menu, Customer, Order

@click.group()

def cli():
    pass

#menu management
@click.command()
@click.option('--name', prompt="Menu Name")
@click.option('--price', prompt="Price", type=float)
@click.option('--category', prompt="Category")

def add_menu_item(name, price, category):
    menu_item = Menu(name=name, price=price, category=category)
    session.add(menu_item)
    session.commit()
    click.echo(f"Added {menu_item}")

@click.command()

def view_menu():
    menu = session.query(Menu).all()
    for item in menu:
        click.echo(item)

@click.command()
@click.option('--menu_id', prompt="Menu Item ID", type=int)

def delete_menu_item(menu_id):

    menu_item = session.query(Menu).filter_by(id=menu_id).first()
    if menu_item:
        session.delete(menu_item)
        session.commit()
        click.echo("Menu item deleted.")
    else:
        click.echo("Menu item not found!")

#customer management
@click.command()
@click.option('--name', prompt="Customer Name")
@click.option('--phone', prompt="Phone Number")

def add_customer(name, phone):
    customer = Customer(name=name, phone=phone)      #adding a new customer
    session.add(customer)
    session.commit()
    click.echo(f"Added {customer}")

@click.command()

def view_customers():
    customers = session.query(Customer).all()
    for customer in customers:
        click.echo(customer)

@click.command()
@click.option('--name', prompt="Customer Name")

def search_customer(name):
    customers = session.query(Customer).filter(Customer.name.ilike(f"%{name}%")).all()
    for customer in customers:
        click.echo(customer)


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
    
    order = Order(customer_id=customer_id, menu_items=menu_items)
    session.add(order)
    session.commit()
    click.echo(f"Order {order.id} created with {len(menu_items)} items - Total: KES {order.tatal_amount}")
    
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
cli.add_command(search_customer)
cli.add_command(create_order)
cli.add_command(view_order_total)
cli.add_command(delete_order)


if __name__== '__main__':
    cli()

