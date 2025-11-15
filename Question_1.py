import time

# Constants for better code readability
HASH_TABLE_SIZE = 10  # Number of buckets in hash table
INITIAL_PRODUCT_COUNT = 8  # Number of products to pre-load


# Entity Class for Baby Product
class BabyProduct:
    def __init__(self, product_id, name, category, price, stock_quantity, age_range):
        self.product_id = product_id
        self.name = name
        self.category = category
        self.price = price
        self.stock_quantity = stock_quantity
        self.age_range = age_range

    def __str__(self):
        return f"ID: {self.product_id}, Name: {self.name}, Category: {self.category}, Price: ${self.price:.2f}, Stock: {self.stock_quantity}, Age: {self.age_range}"


# Node class for linked list (used in separate chaining)
class Node:
    def __init__(self, product):
        self.product = product  # Store the product data
        self.next = None  # Pointer to next node in chain


# Hash Table with Separate Chaining
class HashTable:
    def __init__(self, size=HASH_TABLE_SIZE):
        self.size = size
        # Array of linked list heads - each index is a "bucket"
        self.table = [None] * size
        self.count = 0  # Track total number of products

    def hash_function(self, product_id):
        # Convert product ID to array index using Python's built-in hash
        # Modulo ensures index stays within array bounds (0 to size-1)
        return hash(product_id) % self.size

    def insert(self, product):
        # Step 1: Calculate which bucket to use
        index = self.hash_function(product.product_id)
        new_node = Node(product)

        # Step 2: Handle insertion
        if self.table[index] is None:
            # Bucket is empty - insert directly
            self.table[index] = new_node
        else:
            # Bucket occupied - traverse to end of linked list
            current = self.table[index]
            while current.next is not None:
                current = current.next
            # Append new node at the end
            current.next = new_node

        self.count += 1
        print(f"✓ Inserted: {product.name}")

    def search(self, product_id):
        # Step 1: Find the correct bucket
        index = self.hash_function(product_id)
        current = self.table[index]

        # Step 2: Search through the linked list in this bucket
        while current is not None:
            if current.product.product_id == product_id:
                return current.product  # Found it!
            current = current.next

        # Not found in this bucket
        return None

    def delete(self, product_id):
        # Step 1: Find the correct bucket
        index = self.hash_function(product_id)
        current = self.table[index]
        prev = None

        # Step 2: Search for the product in the linked list
        while current is not None:
            if current.product.product_id == product_id:
                # Found the product - now remove it
                if prev is None:
                    # Deleting first node in the chain
                    self.table[index] = current.next
                else:
                    # Deleting middle or end node
                    prev.next = current.next

                self.count -= 1
                print(f"✓ Deleted: {current.product.name}")
                return True

            # Move to next node
            prev = current
            current = current.next

        # Product not found
        print(f"✗ Product ID {product_id} not found")
        return False

    def display_all(self):
        print("\n" + "=" * 70)
        print("ALL PRODUCTS IN INVENTORY")
        print("=" * 70)

        # Go through each bucket
        for i in range(self.size):
            if self.table[i] is not None:
                print(f"\nBucket {i}:")
                current = self.table[i]
                # Traverse the linked list in this bucket
                while current is not None:
                    print(f"  → {current.product}")
                    current = current.next
        print("=" * 70)


# Array-based storage for performance comparison
class ArrayStorage:
    def __init__(self):
        self.products = []  # Simple Python list

    def insert(self, product):
        self.products.append(product)

    def search(self, product_id):
        # Linear search - check each product one by one
        for product in self.products:
            if product.product_id == product_id:
                return product
        return None


# Inventory System with Command-Line Interface
class InventorySystem:
    def __init__(self):
        self.hash_table = HashTable(size=HASH_TABLE_SIZE)
        self.load_initial_data()

    def load_initial_data(self):
        # Pre-defined products for testing
        products = [
            BabyProduct("P001", "Baby Bottle", "Feeding", 12.99, 50, "0-12 months"),
            BabyProduct("P002", "Diaper Pack", "Hygiene", 24.99, 100, "0-24 months"),
            BabyProduct("P003", "Baby Stroller", "Transport", 199.99, 15, "0-36 months"),
            BabyProduct("P004", "Pacifier Set", "Comfort", 8.99, 75, "0-6 months"),
            BabyProduct("P005", "Baby Monitor", "Safety", 89.99, 25, "0-36 months"),
            BabyProduct("P006", "Onesie 3-Pack", "Clothing", 19.99, 60, "0-12 months"),
            BabyProduct("P007", "Baby Wipes", "Hygiene", 6.99, 150, "0-36 months"),
            BabyProduct("P008", "Soft Toys", "Toys", 14.99, 40, "3-24 months"),
        ]

        print("\n" + "=" * 70)
        print("LOADING INITIAL INVENTORY...")
        print("=" * 70)

        for product in products:
            self.hash_table.insert(product)

        print(f"\n✓ Successfully loaded {len(products)} products into inventory!")

    def add_product(self):
        print("\n" + "=" * 70)
        print("ADD NEW PRODUCT")
        print("=" * 70)

        # Get product details from user
        product_id = input("Product ID: ")
        name = input("Product Name: ")
        category = input("Category: ")
        price = float(input("Price: $"))
        stock = int(input("Stock Quantity: "))
        age_range = input("Age Range: ")

        # Create product object and insert into hash table
        product = BabyProduct(product_id, name, category, price, stock, age_range)
        self.hash_table.insert(product)
        print("\n✓ Product added successfully!")

    def search_product(self):
        print("\n" + "=" * 70)
        print("SEARCH PRODUCT")
        print("=" * 70)

        product_id = input("Enter Product ID to search: ")

        # Measure search time
        start_time = time.time()
        product = self.hash_table.search(product_id)
        end_time = time.time()

        if product:
            print("\n✓ Product Found!")
            print("-" * 70)
            print(product)
            print("-" * 70)
            # Convert to microseconds for readability
            print(f"Search time: {(end_time - start_time) * 1000000:.2f} microseconds")
        else:
            print(f"\n✗ Product with ID '{product_id}' not found!")

    def run(self):
        # Main menu loop
        while True:
            print("\n" + "=" * 70)
            print("BABY PRODUCTS INVENTORY SYSTEM")
            print("=" * 70)
            print("1. Display All Products")
            print("2. Add New Product")
            print("3. Search Product by ID")
            print("4. Delete Product")
            print("5. Exit")
            print("=" * 70)

            choice = input("Enter your choice (1-5): ")

            if choice == "1":
                self.hash_table.display_all()
            elif choice == "2":
                self.add_product()
            elif choice == "3":
                self.search_product()
            elif choice == "4":
                product_id = input("\nEnter Product ID to delete: ")
                self.hash_table.delete(product_id)
            elif choice == "5":
                print("\n✓ Thank you for using the Inventory System!")
                break
            else:
                print("\n✗ Invalid choice! Please try again.")


# Performance Comparison: Hash Table vs Array
def performance_comparison():
    print("\n" + "=" * 70)
    print("PERFORMANCE COMPARISON: HASH TABLE vs ARRAY")
    print("=" * 70)

    # Create identical test data
    test_products = [
        BabyProduct("P001", "Baby Bottle", "Feeding", 12.99, 50, "0-12 months"),
        BabyProduct("P002", "Diaper Pack", "Hygiene", 24.99, 100, "0-24 months"),
        BabyProduct("P003", "Baby Stroller", "Transport", 199.99, 15, "0-36 months"),
        BabyProduct("P004", "Pacifier Set", "Comfort", 8.99, 75, "0-6 months"),
        BabyProduct("P005", "Baby Monitor", "Safety", 89.99, 25, "0-36 months"),
        BabyProduct("P006", "Onesie 3-Pack", "Clothing", 19.99, 60, "0-12 months"),
        BabyProduct("P007", "Baby Wipes", "Hygiene", 6.99, 150, "0-36 months"),
        BabyProduct("P008", "Soft Toys", "Toys", 14.99, 40, "3-24 months"),
    ]

    # Initialize both data structures
    hash_table = HashTable(size=HASH_TABLE_SIZE)
    array_storage = ArrayStorage()

    # Insert same data into both
    for product in test_products:
        hash_table.insert(product)
        array_storage.insert(product)

    # Products to search for in the test
    search_ids = ["P001", "P004", "P008"]

    # Hash table performance
    print("\n--- HASH TABLE SEARCH ---")
    hash_times = []

    for search_id in search_ids:
        # Use perf_counter for higher precision
        start = time.perf_counter()
        result = hash_table.search(search_id)
        end = time.perf_counter()

        # Calculate elapsed time in microseconds
        elapsed = (end - start) * 1000000
        hash_times.append(elapsed)
        print(f"Searching {search_id}: {elapsed:.4f} microseconds")

    avg_hash_time = sum(hash_times) / len(hash_times)
    print(f"Average Hash Table Search Time: {avg_hash_time:.4f} microseconds")

    # Array performance
    print("\n--- ARRAY SEARCH ---")
    array_times = []

    for search_id in search_ids:
        start = time.perf_counter()
        result = array_storage.search(search_id)
        end = time.perf_counter()

        elapsed = (end - start) * 1000000
        array_times.append(elapsed)
        print(f"Searching {search_id}: {elapsed:.4f} microseconds")

    avg_array_time = sum(array_times) / len(array_times)
    print(f"Average Array Search Time: {avg_array_time:.4f} microseconds")

    # Analysis
    print("\n" + "=" * 70)
    print("PERFORMANCE ANALYSIS")
    print("=" * 70)
    print(f"Hash Table Average: {avg_hash_time:.4f} microseconds")
    print(f"Array Average: {avg_array_time:.4f} microseconds")

    if avg_hash_time < avg_array_time:
        speedup = avg_array_time / avg_hash_time
        print(f"\n✓ Hash Table is {speedup:.2f}x FASTER than Array!")
        print("Reason: Hash tables provide O(1) average-case lookup time,")
        print("while arrays require O(n) linear search.")
    else:
        print("\n✓ Array performed better in this small dataset.")
        print("Reason: For small datasets, array's cache locality can be faster")
        print("than hash table's pointer chasing, despite worse complexity.")

    print("=" * 70)


# Main execution
if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("QUESTION 1: HASH TABLE IMPLEMENTATION")
    print("=" * 70)

    # Run performance comparison first
    performance_comparison()

    # Ask if user wants to run interactive system
    print("\n")
    run_interactive = input("Do you want to run the interactive inventory system? (y/n): ")

    if run_interactive.lower() == 'y':
        system = InventorySystem()
        system.run()
    else:
        print("\n✓ Program completed!")