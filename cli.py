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

    
