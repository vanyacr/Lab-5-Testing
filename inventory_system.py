import json
from datetime import datetime
import sys  # Import sys for safe exiting


class InventorySystem:
    """Manages inventory operations, data loading, and saving."""

    def __init__(self, inventory_file="inventory.json"):
        """
        Initializes the inventory system.

        Args:
            inventory_file (str): The file to load/save inventory data.
        """
        self.inventory_file = inventory_file
        self.stock_data = {}  # No longer a global variable
        self.logs = []        # Logs are now part of the instance
        self.load_data()      # Load data on initialization

    def add_item(self, item, qty):
        """
        Adds a specified quantity of an item to the inventory.

        Args:
            item (str): The name of the item to add.
            qty (int): The quantity to add.
        """
        # Fix: Added type validation for item and quantity
        if not isinstance(item, str) or not item:
            print(f"Error: Item name '{item}' is not valid.")
            return

        if not isinstance(qty, int) or qty < 0:
            # Fix: E501 (line too long) - Broke long string
            print(f"Error: Quantity '{qty}' for item '{item}'"
                  " is not a valid non-negative number.")
            return

        self.stock_data[item] = self.stock_data.get(item, 0) + qty
        # Fix: Used f-string and logs are now part of the class
        log_message = f"{str(datetime.now())}: Added {qty} of {item}"
        self.logs.append(log_message)
        print(log_message)

    def remove_item(self, item, qty):
        """
        Removes a specified quantity of an item from inventory.

        If the quantity falls to 0 or below, the item is removed.

        Args:
            item (str): The name of the item to remove.
            qty (int): The quantity to remove.
        """
        # Fix: Added type validation for item and quantity
        if not isinstance(item, str) or not item:
            print(f"Error: Item name '{item}' is not valid.")
            return

        if not isinstance(qty, int) or qty < 0:
            # Fix: E501 (line too long) - Broke long string
            print(f"Error: Quantity '{qty}' for item '{item}'"
                  " is not a valid non-negative number.")
            return

        # Fix: Replaced 'bare-except' with specific checks
        if item not in self.stock_data:
            print(f"Info: Item '{item}' not in stock, cannot remove.")
            return

        if self.stock_data[item] < qty:
            # Fix: E501 (line too long) - Broke long f-string
            print(f"Warning: Not enough stock to remove {qty} of {item}. "
                  f"Only {self.stock_data[item]} available.")
            # Optionally, you could set to 0 or just not perform the action.
            # For this lab, we'll just remove what's left.
            qty = self.stock_data[item]  # Fix: E261 (two spaces before comment)

        self.stock_data[item] -= qty
        log_message = f"{str(datetime.now())}: Removed {qty} of {item}"

        if self.stock_data[item] <= 0:
            del self.stock_data[item]
            log_message += f". Item '{item}' removed from stock."

        self.logs.append(log_message)
        print(log_message)

    def get_qty(self, item):
        """
        Gets the current quantity of a specific item.

        Args:
            item (str): The name of the item.

        Returns:
            int: The quantity of the item, or 0 if not found.
        """
        # Use .get() for safe access (returns 0 if item doesn't exist)
        return self.stock_data.get(item, 0)

    def load_data(self):
        """
        Loads inventory data from the JSON file.
        Handles FileNotFoundError and JSONDecodeError.
        """
        # Fix: Use 'with' statement for safe file handling
        try:
            with open(self.inventory_file, "r", encoding="utf-8") as f:
                # Fix: No longer uses 'global'
                self.stock_data = json.loads(f.read())
                print(f"Data loaded from {self.inventory_file}")
        except FileNotFoundError:
            print(f"Warning: {self.inventory_file} not found. "
                  "Starting with empty inventory.")
            self.stock_data = {}
        except json.JSONDecodeError:
            print(f"Error: Could not decode {self.inventory_file}. "
                  "Starting with empty inventory.")
            self.stock_data = {}
        except Exception as e:
            # Fix: E501 (line too long) - Broke long string
            print("An unexpected error occurred loading data: "
                  f"{e}")
            sys.exit(1)  # Fix: E261 (two spaces before comment)

    def save_data(self):
        """Saves the current inventory data to the JSON file."""
        # Fix: Use 'with' statement for safe file handling
        try:
            with open(self.inventory_file, "w", encoding="utf-8") as f:
                # Use 'indent=4' for readable JSON
                f.write(json.dumps(self.stock_data, indent=4))
                print(f"Data saved to {self.inventory_file}")
        # Fix: Use modern 'OSError' instead of deprecated 'IOError'
        except OSError as e:
            # Fix: E501 (line too long) - Broke long f-string
            print(f"Error: Could not save data to {self.inventory_file}: "
                  f"{e}")

    def print_report(self):
        """Prints a report of all items and their quantities."""
        print("\n--- Items Report ---")
        if not self.stock_data:
            print("Inventory is empty.")
        else:
            # Use .items() to iterate key-value pairs
            for item, quantity in self.stock_data.items():
                print(f"{item} -> {quantity}")
        print("--------------------\n")

    def check_low_items(self, threshold=5):
        """
        Returns a list of items with stock below the threshold.

        Args:
            threshold (int): The stock level to check against.

        Returns:
            list: A list of item names below the threshold.
        """
        # Use a list comprehension for a clean, Pythonic way
        return [item for item, quantity in self.stock_data.items()
                if quantity < threshold]


def main():
    """Main function to run the inventory system logic."""

    # Instantiate the system
    inventory = InventorySystem()

    # Perform operations
    inventory.add_item("apple", 10)
    inventory.add_item("banana", 5)

    # Fix: This invalid call is now handled gracefully
    inventory.add_item(123, 10)  # Invalid item name
    inventory.add_item("grape", "ten")  # Fix: E261 (two spaces before comment)

    inventory.remove_item("apple", 3)

    # This call is now handled gracefully
    inventory.remove_item("orange", 1)

    print(f"\nApple stock: {inventory.get_qty('apple')}")
    print(f"Low items: {inventory.check_low_items()}")

    inventory.print_report()
    inventory.save_data()

    # Show logs
    print("\n--- Session Logs ---")
    for log in inventory.logs:
        print(log)

    # Fix: Removed dangerous 'eval' call
    print("\nSystem check complete.")


# Standard practice to run main() only when the script is executed directly
if __name__ == "__main__":
    main()