menu = {
    "espresso": 7.0,
    "latte": 12.0,
    "cappuccino": 10.0
}
def Show_menu(Menu_dict):
    for item, price in Menu_dict.items():
        print(f"{item}: ${price}")
    if not Menu_dict:
        print("The menu is empty.")
Show_menu(menu)

def add_item(menu_dict):
    drink_name = input("enter the name of the drink you want to add: ").strip()
    if drink_name in menu_dict:
        print(f"{drink_name} is already on the menu.")
        return
    try:   
        drink_price = float(input("enter the price of the drink: ").strip())
    except ValueError:
        print("Invalid price. Please enter a number.")
        return
    menu_dict[drink_name] = drink_price
    print(f"{drink_name} has been added to the menu with a price of ${drink_price:.2f}.")
add_item(menu)

def update_price(menu_dict):
    drink_name = input("enter the name of the drink you want to update: ").strip()
    if drink_name not in menu_dict:
        print(f"{drink_name} is not on the menu.")
        return
    try:
        new_price = float(input("enter the new price of the drink: ").strip())
    except ValueError:
        print("Invalid price. Please enter a number.")
        return
    menu_dict[drink_name] = new_price
    print(f"The price of {drink_name} has been updated to ${new_price:.2f}.")
update_price(menu)

def delete_item(menu_dict):
    drink_name = input("enter the name of the drink you want to delete: ").strip()
    if drink_name not in menu_dict:
        print(f"{drink_name} is not on the menu.")
        return
    del menu_dict[drink_name]
    print(f"{drink_name} has been removed from the menu.")

delete_item(menu)

def show_options():
    print("What would you like to do?")
    print("1. Show menu")
    print("2. Add item")
    print("3. Update price")
    print("4. Delete item")
    print("5. Exit")

def run_coffe_shop():
    while True:
        show_options()
        choice = input("Enter your choice (1-5): ").strip()
        if choice == '1':
            Show_menu(menu)
        elif choice == '2':
            add_item(menu)
        elif choice == '3':
            update_price(menu)
        elif choice == '4':
            delete_item(menu)
        elif choice == '5':
            print("Thank you for using the coffee shop menu manager. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")
run_coffe_shop()
