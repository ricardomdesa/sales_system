import os
import sys
from datetime import datetime

from prettytable import PrettyTable

from model import Seller, Sale, init_db


def validate_fields(sale_costumer, sale_date, sale_name, sale_value):
    if any(char.isdigit() for char in sale_costumer):
        raise ValueError('Sale costumer must not contain numbers')

    try:
        datetime.strptime(sale_date, "%d/%m/%Y").strftime("%d/%m/%Y")
    except ValueError:
        raise
    if sale_value <= 0.0:
        raise ValueError('Sale Value must be greater then 0')


def print_sellers():
    seller_list = Seller.query.all()

    seller_table = PrettyTable(['Seller id', 'Seller Name'])
    for seller in seller_list:
        seller_table.add_row([seller.id, seller.seller_name])

    print(seller_table)


def add_sale():
    print_sellers()

    try:
        seller_id = int(input('Select the Seller id: '))
    except ValueError:
        return 'Sale not added. Seller id must be a integer number'

    costumer = input('Customer name: ')
    sale_date = input('Date of Sale: (dd/mm/YYYY) ')
    sale_name = input('Sale Item Name: ')
    try:
        sale_value = float(input('Sale value: R$ '))
    except ValueError:
        return 'Sale not added. Value must only contain 0-9 and . Ex: 10.99'

    try:
        validate_fields(sale_costumer=costumer, sale_date=sale_date, sale_name=sale_name, sale_value=sale_value)
    except ValueError as E:
        print(E.args)
        return 'Sale not added, invalid arguments'

    seller_db = Seller.query.filter_by(id=seller_id).first()

    if seller_db:
        seller_db.amount_sales += sale_value
        seller_db.save()
        sale = Sale(seller_id=seller_db.id, customer_name=costumer, sale_date=sale_date, sale_name=sale_name,
                    sale_value=sale_value)
        sale.save()
        resp = 'Sale added'
        print_sales()
    else:
        resp = 'Sale not added, invalid arguments'

    return resp


def print_sales():
    os.system('cls' if os.name == 'nt' else 'clear')
    sales_list = Sale.query.join(Seller).order_by(Seller.amount_sales.desc()).all()

    sale_table = PrettyTable(['Sale id', 'Seller name', 'Customer name', 'Sale Item Name', 'Date of sale',
                              'sale value'])

    for sale in sales_list:
        sale_table.add_row([sale.id, sale.seller.seller_name, sale.customer_name, sale.sale_name, sale.sale_date,
                            sale.sale_value])

    print(sale_table)
    return ''


def edit_sale():
    print_sales()
    sale_id = int(input('Select the Sale id to edit: '))

    sale_to_edit = Sale.query.filter_by(id=sale_id).first()

    if sale_to_edit:
        previous_value = sale_to_edit.sale_value
        print_sellers()

        try:
            seller_id = int(input('Select the Seller id: '))
        except ValueError:
            return 'Sale not added. Seller id must be a integer number'

        costumer = input('Customer name: ')
        sale_date = input('Date of Sale: (dd/mm/YYYY)')
        sale_name = input('Sale Item Name: ')
        try:
            sale_value = float(input('Sale value: R$ '))
        except ValueError:
            return 'Sale not added. Value must only contain 0-9 and . Ex: 10.99'

        try:
            validate_fields(sale_costumer=costumer, sale_date=sale_date, sale_name=sale_name, sale_value=sale_value)
        except ValueError as E:
            print(E.args)
            return 'Sale not edited, invalid seller id'

        seller_db = Seller.query.filter_by(id=seller_id).first()

        if seller_db:
            # update amount sales if value was changed
            if previous_value != sale_value:
                seller_db.amount_sales += sale_value
                seller_db.save()

            sale = Sale(seller_id=seller_db.id, customer_name=costumer, sale_date=sale_date, sale_name=sale_name,
                        sale_value=sale_value)
            sale.save()
            print_sales()
            resp = 'Sale edited'
        else:
            resp = 'Sale not edited, invalid seller id'
    else:
        resp = f'Sale with id {sale_id} not found'

    return resp


def delete_sale():
    print_sales()
    sale_id = int(input('Select the Sale id to delete: '))
    sale_to_del = Sale.query.filter_by(id=sale_id).first()
    if sale_to_del:
        sale_table = PrettyTable(['Sale id', 'Seller name', 'Customer name', 'Sale Item Name', 'Date of sale',
                                  'sale value'])
        sale_table.add_row([sale_to_del.id, sale_to_del.seller.seller_name, sale_to_del.customer_name,
                            sale_to_del.sale_name, sale_to_del.sale_date, sale_to_del.sale_value])
        print(sale_table)
        if input('\nConfirm delete the Sale above? (y, n)') == 'y':
            # update the amount sales of seller
            seller = Seller.query.filter_by(id=sale_to_del.seller_id).first()
            seller.amount_sales -= sale_to_del.sale_value
            seller.save()

            # delete sale
            sale_to_del.delete()
            print_sales()
            resp = f'Sale with id {sale_id} deleted'
        else:
            resp = 'Sale not deleted'
    else:
        resp = f'Sale with id {sale_id} not found'
    return resp


def options():
    options = 'Options:\n' \
              '   n\t\tNew sale\n' \
              '   p\t\tPrint sales\n' \
              '   e\t\tEdit sale\n' \
              '   d\t\tDelete sale\n' \
              '   q\t\tQuit\n' \
              ' Ctrl+c\t\treturn to main menu\n'

    print(f'\n==== Sales System ====\n')
    print(options)

    return input('Select an option: ')


def quit():
    sys.exit()
    return ''


if __name__ == '__main__':
    init_db()
    print_sales()

    op = {
        'n': add_sale,
        'p': print_sales,
        'e': edit_sale,
        'd': delete_sale,
        'q': quit
    }

    while True:
        try:
            option = options()
            func = op.get(option, lambda: 'invalid choice')()
            print(func)
        except KeyboardInterrupt:
            print_sales()
