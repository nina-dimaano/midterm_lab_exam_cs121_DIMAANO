# Dictionary to store game library with their quantities and rental costs
game_library = {
    1: {"name": "Donkey Kong", "quantity": 3, "cost": 2},
    2: {"name": "Super Mario Bros", "quantity": 5, "cost": 3},
    3: {"name": "Tetris", "quantity": 2, "cost": 1},
    # Add more games as needed
}

# Dictionary to store user accounts with their balances and points
user_accounts = {}

# Dictionary to store user inventory
user_inventory = {}

# Admin account details
admin_username = "admin"
admin_password = "adminpass"

# Function to display available games with their numbers and rental costs
def display_available_games():
    print("Available Games:")
    for num, details in game_library.items():
        print(f"{num}. {details['name']}: Quantity - {details['quantity']}, Cost - ${details['cost']}")

# Function to register a new user
def register_user():
    username = input("Enter a username: ")
    password = input("Enter a password: ")
    if username not in user_accounts:
        user_accounts[username] = {"password": password, "balance": 0, "points": 0, "inventory": []}
        print(f"User {username} registered successfully!")
        top_up_account(username, float(input("Enter an amount to top up your account: ")))
    else:
        print("Username already exists. Please log in.")

# Function to rent a game
def rent_game(username):
    display_available_games()
    game_choice = int(input("Enter the number of the game you want to rent: "))
    if game_choice in game_library:
        game_name = game_library[game_choice]["name"]
        if game_library[game_choice]["quantity"] > 0:
            if user_accounts[username]["balance"] >= game_library[game_choice]["cost"]:
                user_accounts[username]["balance"] -= game_library[game_choice]["cost"]
                game_library[game_choice]["quantity"] -= 1
                if username in user_inventory:
                    user_inventory[username].append(game_name)
                else:
                    user_inventory[username] = [game_name]
                print(f"Game {game_name} rented successfully!")
                update_points(username, game_library[game_choice]["cost"])
            else:
                print("Insufficient balance. Please top up your account.")
        else:
            print("Game out of stock. Please try again later.")
    else:
        print("Invalid game choice. Please try again.")

# Function to return a game
def return_game(username):
    display_inventory(username)
    if username in user_inventory and user_inventory[username]:
        print("Select the number of the game you want to return:")
        for idx, game in enumerate(user_inventory[username], start=1):
            print(f"{idx}. {game}")
        game_choice = int(input("Enter your choice: "))
        if 1 <= game_choice <= len(user_inventory[username]):
            game_name = user_inventory[username][game_choice - 1]
            for num, details in game_library.items():
                if details["name"] == game_name:
                    game_library[num]["quantity"] += 1
                    break
            user_inventory[username].remove(game_name)
            user_accounts[username]["points"] += 1
            print(f"Game {game_name} returned successfully!")
            redeem_free_game(username)
        else:
            print("Invalid choice. Please try again.")
    else:
        print("No games to return.")

# Function to top-up user account
def top_up_account(username, amount):
    user_accounts[username]["balance"] += amount
    print(f"Amount ${amount} added to your account.")

# Function to display user's inventory
def display_inventory(username):
    print(f"Inventory for {username}:")
    if username in user_inventory and user_inventory[username]:
        for game in user_inventory[username]:
            print(f"- {game}")
    else:
        print("No games rented.")

# Function for admin to update game details
def admin_update_game():
    display_available_games()
    game_choice = int(input("Enter the number of the game you want to update: "))
    if game_choice in game_library:
        game_library[game_choice]["quantity"] = int(input("Enter the new quantity: "))
        game_library[game_choice]["cost"] = float(input("Enter the new cost: "))
        print(f"Game {game_library[game_choice]['name']} details updated successfully!")
    else:
        print("Invalid game choice. Please try again.")

# Function to check user credentials
def check_credentials(username, password):
    if username in user_accounts and user_accounts[username]["password"] == password:
        return True
    else:
        return False

# Function for admin login
def admin_login():
    username = input("Enter admin username: ")
    password = input("Enter admin password: ")
    if username == admin_username and password == admin_password:
        return True
    else:
        return False

# Function to update user points
def update_points(username, cost):
    user_accounts[username]["points"] += int(cost / 2)
    if user_accounts[username]["points"] >= 3:
        print("Congratulations! You earned a free game!")
        user_accounts[username]["points"] -= 3
        redeem_free_game(username)

# Function to redeem a free game
def redeem_free_game(username):
    if user_accounts[username]["points"] >= 3:
        user_accounts[username]["points"] -= 3
        print("You redeemed a free game!")
        display_available_games()
        game_choice = int(input("Enter the number of the game you want to rent for free: "))
        if game_choice in game_library:
            game_name = game_library[game_choice]["name"]
            if game_library[game_choice]["quantity"] > 0:
                game_library[game_choice]["quantity"] -= 1
                if username in user_inventory:
                    user_inventory[username].append(game_name)
                else:
                    user_inventory[username] = [game_name]
                print(f"Game {game_name} rented successfully!")
            else:
                print("Game out of stock. Please try again later.")
        else:
            print("Invalid game choice. Please try again.")
    else:
        print("You don't have enough points to redeem a free game.")

# Main function
def main():
    print("Welcome to the Video Game Rental System!")
    while True:
        print("\nMenu:")
        print("1. Register as a new user")
        print("2. Log in as an existing user")
        print("3. Admin login")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            register_user()
        elif choice == "2":
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            if check_credentials(username, password):
                while True:
                    print("\nUser Menu:")
                    print("1. Display available games")
                    print("2. Rent a game")
                    print("3. Return a game")
                    print("4. Display inventory")
                    print("5. Log out")
                    user_choice = input("Enter your choice: ")
                    if user_choice == "1":
                        display_available_games()
                    elif user_choice == "2":
                        rent_game(username)
                    elif user_choice == "3":
                        return_game(username)
                    elif user_choice == "4":
                        display_inventory(username)
                    elif user_choice == "5":
                        break
                    else:
                        print("Invalid choice. Please try again.")
            else:
                print("Invalid username or password.")
        elif choice == "3":
            if admin_login():
                while True:
                    print("\nAdmin Menu:")
                    print("1. Update game details")
                    print("2. Exit")
                    admin_choice = input("Enter your choice: ")
                    if admin_choice == "1":
                        admin_update_game()
                    elif admin_choice == "2":
                        break
                    else:
                        print("Invalid choice. Please try again.")
            else:
                print("Invalid admin credentials.")
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please try again.")

# Call the main function to start the program
if __name__ == "__main__":
    main()
