#!/home/k/.pyenv/shims/python

import click
from app import session, Menu, Customer, Order

@click.group()

def cli():
    pass

#menu management
@click.command()

def interactive_menu():
    while True:
        click.echo("\n---  Welcome to K Restaurant ---")
        click.echo("1. Add Menu Item")
        click.echo("2. View Menu")
        click.echo("3. Delete Menu Item")
        click.echo("4. Add Customer")
        click.echo("5. View Customers")
        click.echo("6. Search Customer")
        click.echo("7. Create Order")
        click.echo("8. View Order Total")
        click.echo("9. Delete Order")
        click.echo("0. Exit")

        choice = click.prompt("Select an option", type=int)

        if choice == 1:
            name = click.prompt("Menu Name")
            price = click.prompt("Price", type=float)
            category = click.prompt("Category")
            add_menu_item(name, price, category)
        elif choice == 2:
            view_menu()
        elif choice == 3:
            menu_id = click.prompt("Menu Item ID", type=int)
            delete_menu_item(menu_id)
        elif choice == 4:
            name = click.prompt("Customer Name")
            phone = click.prompt("Phone Number")
            add_customer(name, phone)
        elif choice == 5:
            view_customers()
        elif choice == 6:
            name = click.prompt("Customer Name")
            search_customer(name)
        elif choice == 7:
            customer_id = click.prompt("Customer ID", type=int)
            menu_ids = click.prompt("Menu Item IDs (comma-separated)")
            create_order(customer_id, menu_ids)
        elif choice == 8:
            order_id = click.prompt("Order ID", type=int)
            view_order_total(order_id)
        elif choice == 9:
            order_id = click.prompt("Order ID, type=int")
            delete_order(order_id)
        elif choice == 0:
            click.echo("Exiting...")
            break
        else:
            click.echo("Invalid option, please try again.")


@click.command()
@click.argument('name')
@click.argument('price', type=float)
@click.argument('category')

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
@click.argument('menu_id', type=int)

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
@click.argument('name')
@click.argument('phone')

def add_customer(name, phone):
    customer = Customer(name=name, phone=phone)
    session.add(customer)
    session.commit()
    click.echo(f"Added {customer}")

@click.command()

def view_customers():
    customers = session.query(Customer).all()
    for customer in customers:
        click.echo(customer)

@click.command()
@click.argument('name')

def search_customer(name):
    customers = session.query(Customer).filter(Customer.name.ilike(f"%{name}%")).all()
    for customer in customers:
        click.echo(customer)


#order management
@click.command()
@click.argument('customer_id', type=int)
@click.argument('menu_ids')

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
@click.argument('order_id', type=int)

def view_order_total(order_id):
    order = session.query(Order).filter_by(id=order_id).first()
    if order:
        click.echo(f"Order {order.id} Total: KES {order.total_amount}")
    else:
        click.echo("Order not found!")
        
@click.command()
@click.argument('order_id', type=int)

def delete_order(order_id):
    order = session.query(Order).filter_by(id=order_id).first()
    if order:
        session.delete(order)
        session.commit()
        click.echo("Order deleted.")
    else:
        click.echo("Order not found!")


cli.add_command(interactive_menu)
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

