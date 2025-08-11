import os
import json
import csv
import random
import webbrowser
import subprocess
import platform
from datetime import datetime
from grid_db import save_grid_to_db

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def open_db_browser():
    db_path = os.path.join(BASE_DIR, "grids.db")
    if platform.system() == "Windows":
        browser_path = r"C:\Program Files\DB Browser for SQLite\DB Browser for SQLite.exe"
        subprocess.Popen([browser_path, db_path])
    else:
        print("🚫 DB browser opening is only supported on Windows.")


def get_timestamped_filename(base_name, extension):
    layouts_dir = os.path.join(BASE_DIR, "layouts")
    os.makedirs(layouts_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    return os.path.join(layouts_dir, f"{base_name}_{timestamp}.{extension}")


def save_layout_to_json(grid, folder="layouts"):
    layouts_path = os.path.join(BASE_DIR, folder)
    os.makedirs(layouts_path, exist_ok=True)
    filename = os.path.join(layouts_path, f"grid_layout_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    with open(filename, "w") as f:
        json.dump(grid, f, indent=2)
    print(f"✅ Grid layout saved to {filename}")


def save_layout_to_csv(grid, folder="layouts"):
    layouts_path = os.path.join(BASE_DIR, folder)
    os.makedirs(layouts_path, exist_ok=True)
    filename = os.path.join(layouts_path, f"grid_layout_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
    with open(filename, "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerows(grid)
    print(f"✅ Grid layout saved to {filename}")


def load_grid_from_json(folder="layouts"):
    layouts_path = os.path.join(BASE_DIR, folder)
    if not os.path.exists(layouts_path):
        print(f"❌ Folder not found: {layouts_path}")
        return []
    json_files = [f for f in os.listdir(layouts_path) if f.endswith(".json")]
    if not json_files:
        print("❌ No JSON files found in layouts folder.")
        return []
    latest_file = max(json_files, key=lambda f: os.path.getmtime(os.path.join(layouts_path, f)))
    full_path = os.path.join(layouts_path, latest_file)
    with open(full_path, "r") as f:
        grid = json.load(f)
    print(f"✅ Loaded grid from {full_path}")
    return grid


def generate_symmetric_grid(grid_size, normal_tile_count, symmetry):
    total_tiles = grid_size * grid_size
    base_half = ['normal'] * (normal_tile_count // 2) + ['void'] * (grid_size**2 // 2 - normal_tile_count // 2)
    random.shuffle(base_half)

    def mirror_row(row):
        return row + row[::-1] if grid_size % 2 == 0 else row + row[-2::-1]

    grid = []
    if symmetry == "vertical":
        for i in range(grid_size):
            row = base_half[i * (grid_size // 2):(i + 1) * (grid_size // 2)]
            grid.append(mirror_row(row))

    elif symmetry == "horizontal":
        top_half = [base_half[i * grid_size:(i + 1) * grid_size] for i in range(grid_size // 2)]
        grid = top_half + top_half[::-1]

    elif symmetry == "diagonal":
        grid = [['void'] * grid_size for _ in range(grid_size)]
        filled = 0
        for i in range(grid_size):
            for j in range(grid_size):
                if i <= j and filled < normal_tile_count:
                    grid[i][j] = 'normal'
                    grid[j][i] = 'normal'
                    filled += 2 if i != j else 1

    else:  # default: auto
        tiles = ['normal'] * normal_tile_count + ['void'] * (total_tiles - normal_tile_count)
        random.shuffle(tiles)
        grid = [tiles[i:i + grid_size] for i in range(0, total_tiles, grid_size)]

    return grid


def generate_new_grid_html(normal_tile_count=40):
    grid_size = 9
    print("Choose grid style:")
    print("1 - Auto (Random)")
    print("2 - Vertical Symmetric")
    print("3 - Horizontal Symmetric")
    print("4 - Diagonal Symmetric")
    style_choice = input("🔢 Your choice (1-4): ").strip()

    symmetry_map = {
        "1": "auto",
        "2": "vertical",
        "3": "horizontal",
        "4": "diagonal"
    }

    symmetry = symmetry_map.get(style_choice, "auto")
    grid = generate_symmetric_grid(grid_size, normal_tile_count, symmetry)

    # Ask save mode
    print("\nHow would you like to save the grid?")
    print("1 - All (JSON, CSV, HTML, DB)")
    print("2 - Only JSON")
    print("3 - Only HTML")
    print("4 - Only SQLite DB")
    save_mode = input("💾 Your choice (1-4): ").strip()

    filename_only = f"grid_layout_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    if save_mode == "1":
        save_layout_to_json(grid)
        save_layout_to_csv(grid)
        save_html = True
        save_grid_to_db(filename_only, grid)

    elif save_mode == "2":
        save_layout_to_json(grid)
        save_html = False

    elif save_mode == "3":
        save_html = True

    elif save_mode == "4":
        save_grid_to_db(filename_only, grid)
        save_html = False

    else:
        print("❌ Invalid save choice.")
        save_html = False

    # Always generate HTML
    html = """
    <html>
    <head>
        <style>
            body {
                background-color: #222;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }
            .grid {
                display: grid;
                grid-template-columns: repeat(9, 40px);
                grid-template-rows: repeat(9, 40px);
                gap: 2px;
            }
            .tile {
                width: 40px;
                height: 40px;
                opacity: 0.5;
            }
            .normal {
                background-color: #7dd185;
            }
            .void {
                background-color: lightgrey;
            }
        </style>
    </head>
    <body>
        <div class="grid">
    """

    for row in grid:
        for tile in row:
            html += f'<div class="tile {tile}"></div>\n'

    html += "</div></body></html>"

    html_filename = os.path.join(BASE_DIR, get_timestamped_filename("grid_layout", "html") if save_html else "temp_grid.html")
    with open(html_filename, "w") as f:
        f.write(html)

    print(f"✅ HTML {'saved to' if save_html else 'temporarily created'}: {html_filename}")
    webbrowser.open('file://' + os.path.realpath(html_filename))


def generate_grid_html_from_existing(grid):
    html_filename = get_timestamped_filename("grid_from_json", "html")

    html = """
    <html>
    <head>
        <style>
            body {
                background-color: #222;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }
            .grid {
                display: grid;
                grid-template-columns: repeat(9, 40px);
                grid-template-rows: repeat(9, 40px);
                gap: 2px;
            }
            .tile {
                width: 40px;
                height: 40px;
                opacity: 0.5;
            }
            .normal {
                background-color: #7dd185;
            }
            .void {
                background-color: lightgrey;
            }
        </style>
    </head>
    <body>
        <div class="grid">
    """

    for row in grid:
        for tile in row:
            html += f'<div class="tile {tile}"></div>\n'

    html += "</div></body></html>"

    with open(html_filename, "w") as f:
        f.write(html)

    print("✅ HTML (existing grid) saved to:", os.path.abspath(html_filename))
    webbrowser.open('file://' + os.path.realpath(html_filename))