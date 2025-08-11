from match3_generator import generate_new_grid_html,load_grid_from_json,generate_grid_html_from_existing


def main():
    choice = input("Type 'new' to generate new grid or 'load' to load from JSON: ").strip().lower()

    if choice == "new":
        try:
            user_input = int(input("Enter number of normal tiles (1-81): "))
            if 1 <= user_input <= 81:
                generate_new_grid_html(normal_tile_count=user_input)
            else:
                print("❌ Please enter a number between 1 and 81.")
        except ValueError:
            print("❌ Invalid input. Please enter a number.")
    elif choice == "load":
        try:
            grid = load_grid_from_json()
            generate_grid_html_from_existing(grid)
        except FileNotFoundError:
            print("❌ grid_layout.json not found. Please generate a grid first.")
    else:
        print("❌ Invalid input. Type 'new' or 'load'.")

if __name__ == "__main__":
    main()

