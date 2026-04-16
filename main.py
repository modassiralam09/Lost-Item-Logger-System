import json
import os
import matplotlib.pyplot as plt

FILE_NAME = "items.json"


# -----------------------------
# Item Class
# -----------------------------

class Item:

    def __init__(self, name, description,
                 location, date,
                 contact, category, status):

        self.name = name
        self.description = description
        self.location = location
        self.date = date
        self.contact = contact
        self.category = category
        self.status = status

    def to_dict(self):

        return {
            "name": self.name,
            "description": self.description,
            "location": self.location,
            "date": self.date,
            "contact": self.contact,
            "category": self.category,
            "status": self.status
        }


# -----------------------------
# File Handling
# -----------------------------

def load_items():

    if os.path.exists(FILE_NAME):

        with open(FILE_NAME, "r") as f:
            return json.load(f)

    return []


def save_items(items):

    with open(FILE_NAME, "w") as f:
        json.dump(items, f, indent=4)


# -----------------------------
# Input Helper
# -----------------------------

def get_item_input(status):

    print(f"\nEnter {status} Item Details")

    name = input("Item Name: ")
    description = input("Description: ")
    location = input(f"Location {status}: ")
    date = input(f"Date {status}: ")
    contact = input("Contact Number: ")
    category = input("Category: ")

    return Item(
        name,
        description,
        location,
        date,
        contact,
        category,
        status
    )


# -----------------------------
# Add Lost Item
# -----------------------------

def add_lost_item():

    item = get_item_input("Lost")

    items = load_items()
    items.append(item.to_dict())

    save_items(items)

    print("✅ Lost item recorded successfully!")


# -----------------------------
# Add Found Item
# -----------------------------

def add_found_item():

    item = get_item_input("Found")

    items = load_items()
    items.append(item.to_dict())

    save_items(items)

    print("✅ Found item recorded successfully!")


# -----------------------------
# Display Items
# -----------------------------

def display_items():

    items = load_items()

    if not items:
        print("No records found.")
        return

    print("\n----- Item Records -----")

    for i, item in enumerate(items, 1):

        print(f"\nItem {i}")

        for key, value in item.items():
            print(f"{key}: {value}")


# -----------------------------
# Search Item
# -----------------------------

def search_item():

    keyword = input(
        "\nEnter item name to search: "
    ).lower()

    items = load_items()

    found = False

    for item in items:

        if keyword in item["name"].lower():

            print("\nItem Found:")

            for key, value in item.items():
                print(f"{key}: {value}")

            found = True

    if not found:
        print("No item found.")


# -----------------------------
# Match Lost & Found
# -----------------------------

def match_items():

    items = load_items()

    lost_items = [
        i for i in items
        if i["status"] == "Lost"
    ]

    found_items = [
        i for i in items
        if i["status"] == "Found"
    ]

    print("\nPossible Matches:")

    match_found = False

    for lost in lost_items:

        for found in found_items:

            if (
                lost["name"].lower()
                == found["name"].lower()
            ):

                print(
                    "\nLost Item:",
                    lost["name"],
                    "| Location:",
                    lost["location"]
                )

                print(
                    "Found Item:",
                    found["name"],
                    "| Location:",
                    found["location"]
                )

                match_found = True

    if not match_found:
        print("No matches found.")


# -----------------------------
# Reports
# -----------------------------

def show_reports():

    items = load_items()

    lost = sum(
        1 for i in items
        if i["status"] == "Lost"
    )

    found = sum(
        1 for i in items
        if i["status"] == "Found"
    )

    print("\n----- Report -----")

    print("Total Lost Items:", lost)
    print("Total Found Items:", found)
    print("Total Records:", len(items))


# -----------------------------
# Visualization
# -----------------------------

def show_charts():

    items = load_items()

    categories = {}

    for item in items:

        cat = item["category"]

        categories[cat] = (
            categories.get(cat, 0) + 1
        )

    if not categories:
        print("No data to display.")
        return

    names = list(categories.keys())
    values = list(categories.values())

    plt.bar(names, values)

    plt.title(
        "Lost/Found Items by Category"
    )

    plt.xlabel("Category")
    plt.ylabel("Number of Items")

    plt.show()


# -----------------------------
# Delete Item
# -----------------------------

def delete_item():

    items = load_items()

    if not items:
        print("No items to delete.")
        return

    display_items()

    try:

        index = int(
            input(
                "\nEnter item number to delete: "
            )
        ) - 1

        if 0 <= index < len(items):

            removed = items.pop(index)

            save_items(items)

            print(
                "✅ Item deleted:",
                removed["name"]
            )

        else:
            print("Invalid item number.")

    except ValueError:
        print("Invalid input.")


# -----------------------------
# Menu
# -----------------------------

def menu():

    options = {
        "1": add_lost_item,
        "2": add_found_item,
        "3": display_items,
        "4": search_item,
        "5": match_items,
        "6": show_reports,
        "7": show_charts,
        "8": delete_item
    }

    while True:

        print(
            "\n===== LOST ITEM LOGGER SYSTEM ====="
        )

        print("1. Add Lost Item")
        print("2. Add Found Item")
        print("3. Display All Items")
        print("4. Search Item")
        print("5. Match Lost & Found")
        print("6. Show Reports")
        print("7. Show Charts")
        print("8. Delete Item")
        print("9. Exit")

        choice = input("Enter your choice: ")

        if choice == "9":
            print("Exiting program...")
            break

        action = options.get(choice)

        if action:
            action()
        else:
            print("Invalid choice.")


# -----------------------------
# Run Program
# -----------------------------

if __name__ == "__main__":
    menu()