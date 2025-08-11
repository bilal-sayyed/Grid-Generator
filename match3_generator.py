import os
import json
import csv
import random
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_timestamped_filename(base_name, extension):
    layouts_dir = os.path.join(BASE_DIR, "layouts")
    os.makedirs(layouts_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
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

def generate_new_grid_html(normal_tile_count=40, style="auto", save_files=False):
    grid_size = 9
    symmetry = style
    grid = generate_symmetric_grid(grid_size, normal_tile_count, symmetry)

    if save_files:
        save_layout_to_json(grid)
        save_layout_to_csv(grid)
        # Optionally: save to DB here if you want

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

    return html

def generate_grid_html_from_existing(grid, save_file=False):
    if save_file:
        html_filename = get_timestamped_filename("grid_from_json", "html")
    else:
        html_filename = None

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

    if save_file and html_filename:
        with open(html_filename, "w") as f:
            f.write(html)
        print("✅ HTML (existing grid) saved to:", os.path.abspath(html_filename))

    return html