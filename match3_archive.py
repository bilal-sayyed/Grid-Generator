# This is a starting old code in main.py, shiifted here

# from match3_generator import generate_grid_html
#
# def main():
#     try:
#         user_input = int(input("Enter number of normal tiles (1-81): "))
#         if 1 <= user_input <= 81:
#             generate_grid_html(normal_tile_count=user_input)
#         else:
#             print("Please enter a number between 1 and 81.")
#     except ValueError:
#         print("Invalid input. Please enter a number.")
#
# if __name__ == "__main__":
#     main()
# ------------------------------------------------------------------------------------------------------------------

# # From here it is image trigger
# class DottedGridTwoColorCheckerGenerator:
#     def __init__(self, size=9, board_size=720):
#         self.size = size
#         self.board_size = board_size
#         self.cell_size = board_size // size  # 80px per cell for 9x9
#
#         # No gaps - tiles fill entire cells
#         self.tile_size = self.cell_size  # Full cell size, no gaps
#
#         # Colors with updated opacity levels
#         self.green_tile = (76, 175, 80, 127)  # Green with 50% opacity (unchanged)
#         self.tan_tile = (210, 180, 140, 179)  # Tan with 70% opacity (alpha=179)
#         self.void_grey = (160, 160, 160, 127)  # Grey with 50% opacity (alpha=127)
#         self.dot_color = (100, 100, 100)  # Dark grey for dotted lines
#
#         # Total possible tiles (9x9 = 81)
#         self.total_tiles = self.size * self.size
#
#     def generate_selective_layout(self, num_filled):
#         """Generate layout with exactly num_filled tiles randomly placed"""
#         if num_filled < 0 or num_filled > self.total_tiles:
#             raise ValueError(f"Number of filled tiles must be between 0 and {self.total_tiles}")
#
#         # Start with all positions as void (False)
#         layout = [[False for _ in range(self.size)] for _ in range(self.size)]
#
#         # Get all possible tile positions
#         all_positions = []
#         for row in range(self.size):
#             for col in range(self.size):
#                 all_positions.append((row, col))
#
#         # Randomly select exactly num_filled positions to be filled
#         selected_positions = random.sample(all_positions, num_filled)
#
#         # Mark selected positions as filled (True)
#         for row, col in selected_positions:
#             layout[row][col] = True
#
#         print(f"🎯 Selected {num_filled} random positions out of {self.total_tiles} total tiles")
#         return layout
#
#     def get_checker_color(self, row, col):
#         """Determine if this position should be green or tan based on checker pattern"""
#         # Checker pattern: alternating colors
#         if (row + col) % 2 == 0:
#             return self.green_tile  # Green for even positions
#         else:
#             return self.tan_tile  # Tan for odd positions
#
#     def draw_colored_tile_with_opacity(self, base_img, x, y, color_rgba):
#         """Draw colored tile with opacity covering full cell"""
#         # Create a temporary image with alpha channel for transparency
#         overlay = Image.new('RGBA', (self.tile_size, self.tile_size), color_rgba)
#
#         # Convert base image to RGBA if it isn't already
#         if base_img.mode != 'RGBA':
#             base_rgba = base_img.convert('RGBA')
#         else:
#             base_rgba = base_img
#
#         # Paste the colored overlay with transparency
#         base_rgba.paste(overlay, (x, y), overlay)
#         return base_rgba
#
#     def draw_void_tile_with_opacity(self, base_img, x, y):
#         """Draw void tile with 50% opacity covering full cell"""
#         # Create a temporary image with alpha channel for transparency
#         overlay = Image.new('RGBA', (self.tile_size, self.tile_size), self.void_grey)
#
#         # Convert base image to RGBA if it isn't already
#         if base_img.mode != 'RGBA':
#             base_rgba = base_img.convert('RGBA')
#         else:
#             base_rgba = base_img
#
#         # Paste the grey overlay with 50% transparency
#         base_rgba.paste(overlay, (x, y), overlay)
#         return base_rgba
#
#     def draw_dotted_grid_lines(self, draw):
#         """Draw dotted grid lines over the entire board"""
#         dot_spacing = 6  # Space between dots
#         dot_size = 2  # Size of each dot
#
#         # Draw dotted vertical lines
#         for i in range(self.size + 1):
#             x = i * self.cell_size
#             for y in range(0, self.board_size, dot_spacing):
#                 if y + dot_size <= self.board_size:
#                     draw.rectangle([x - 1, y, x + 1, y + dot_size],
#                                    fill=self.dot_color)
#
#         # Draw dotted horizontal lines
#         for i in range(self.size + 1):
#             y = i * self.cell_size
#             for x in range(0, self.board_size, dot_spacing):
#                 if x + dot_size <= self.board_size:
#                     draw.rectangle([x, y - 1, x + dot_size, y + 1],
#                                    fill=self.dot_color)
#
#     def render_updated_opacity_grid(self, num_filled, show_image=True):
#         """Render grid with updated opacity: green 50%, tan 70%, grey 50%"""
#         timestamp = int(time.time())
#
#         # Start with RGBA image for transparency support
#         img = Image.new('RGBA', (self.board_size, self.board_size), (255, 255, 255, 255))
#         draw = ImageDraw.Draw(img)
#
#         # Generate layout with exactly num_filled tiles
#         layout = self.generate_selective_layout(num_filled)
#
#         filled_count = 0
#         void_count = 0
#         green_count = 0
#         tan_count = 0
#
#         # Step 1: Draw all void tiles with 50% opacity
#         for row in range(self.size):
#             for col in range(self.size):
#                 if not layout[row][col]:
#                     cell_x = col * self.cell_size
#                     cell_y = row * self.cell_size
#                     img = self.draw_void_tile_with_opacity(img, cell_x, cell_y)
#                     void_count += 1
#
#         # Step 2: Draw colored tiles with checker pattern
#         for row in range(self.size):
#             for col in range(self.size):
#                 if layout[row][col]:
#                     cell_x = col * self.cell_size
#                     cell_y = row * self.cell_size
#
#                     # Determine color based on checker pattern
#                     tile_color = self.get_checker_color(row, col)
#
#                     # Draw the colored tile with opacity
#                     img = self.draw_colored_tile_with_opacity(img, cell_x, cell_y, tile_color)
#
#                     filled_count += 1
#                     if tile_color == self.green_tile:
#                         green_count += 1
#                     else:
#                         tan_count += 1
#
#         # Step 3: Draw dotted grid lines over everything
#         draw = ImageDraw.Draw(img)  # Refresh draw object after transparency operations
#         self.draw_dotted_grid_lines(draw)
#
#         # Convert back to RGB for saving (removes alpha channel)
#         final_img = Image.new('RGB', img.size, (255, 255, 255))
#         final_img.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
#
#         # Verify counts with updated opacity levels
#         print(f"🟢 Green tiles (50% opacity): {green_count}")
#         print(f"🟤 Tan tiles (70% opacity): {tan_count}")
#         print(f"📊 Total filled tiles: {filled_count} (requested: {num_filled})")
#         print(f"🟫 Grey void tiles (50% opacity): {void_count}")
#         print(f"🎨 Checker pattern: Green and tan alternating")
#         print(f"⚫ Dotted grid lines: Applied over entire grid")
#
#         # Save with descriptive filename
#         filename = f"green50_tan70_grey50_opacity_{num_filled}_of_{self.total_tiles}_{timestamp}.png"
#         final_img.save(filename)
#         print(f"✅ Grid saved as '{filename}'")
#
#         # Display immediately
#         if show_image:
#             try:
#                 final_img.show()
#                 print("🖼️ Updated opacity grid displayed!")
#             except Exception as e:
#                 print(f"Display error: {e}")
#                 print(f"📁 Please open '{filename}' manually")
#
#         return final_img, filename
#
#     def print_generation_info(self, num_filled):
#         """Print information about the grid with updated opacity levels"""
#         print("🟢🟤🟫 UPDATED OPACITY LEVELS GRID 🟫🟤🟢")
#         print("=" * 50)
#         print(f"Grid size: {self.size}x{self.size} = {self.total_tiles} total tiles")
#         print(f"Canvas: {self.board_size}x{self.board_size} pixels")
#         print(f"Cell size: {self.cell_size}x{self.cell_size} pixels (no gaps)")
#         print(f"Tiles to fill: {num_filled} out of {self.total_tiles}")
#         print(f"Void tiles: {self.total_tiles - num_filled}")
#         print("\nUpdated Opacity Settings:")
#         print("🟢 GREEN TILES:")
#         print(f"  - Color: RGB{self.green_tile[:3]} with 50% opacity")
#         print("  - Checker pattern even positions")
#         print("  - Semi-transparent, balanced visibility")
#         print("🟤 TAN TILES:")
#         print(f"  - Color: RGB{self.tan_tile[:3]} with 70% opacity")
#         print("  - Checker pattern odd positions")
#         print("  - More opaque, stronger presence")
#         print("🟫 GREY VOID TILES:")
#         print(f"  - Color: RGB{self.void_grey[:3]} with 50% opacity")
#         print("  - Medium transparency")
#         print("  - Balanced with green tiles")
#         print("🎨 VISUAL HIERARCHY:")
#         print("  - Tan tiles: Most visible (70% opacity)")
#         print("  - Green & Grey: Medium visibility (50% opacity)")
#         print("  - Creates layered visual depth")
#         print("⚫ DOTTED GRID:")
#         print("  - All grid lines dotted")
#         print("  - No gaps between tiles")
#
#
# # Interactive function to get user input
# def get_user_tile_count():
#     """Get tile count from user with validation"""
#     while True:
#         try:
#             user_input = input("Enter number of tiles to fill (1-81): ").strip()
#             if user_input == "":
#                 return 40  # Default value
#
#             num_tiles = int(user_input)
#
#             if 1 <= num_tiles <= 81:
#                 return num_tiles
#             else:
#                 print("❌ Please enter a number between 1 and 81")
#
#         except ValueError:
#             print("❌ Please enter a valid number")
#
#
# # Main execution
# def main():
#     print("🟢🟤🟫 UPDATED OPACITY LEVELS GRID 🟫🟤🟢")
#     print("=" * 60)
#     print("Updated opacity settings as requested:")
#     print("🟢 Green tiles: 50% opacity (unchanged)")
#     print("🟤 Tan tiles: 70% opacity (increased from 50%)")
#     print("🟫 Grey void tiles: 50% opacity (increased from 30%)")
#     print("⚫ All grid lines dotted, no gaps between tiles")
#     print()
#
#     print("Choose option:")
#     print("1. Enter custom number of tiles to fill")
#     print("2. Quick examples (10, 25, 50, 75 tiles)")
#     print("3. Use default (40 tiles)")
#
#     choice = input("Enter choice (1-3): ").strip()
#
#     generator = DottedGridTwoColorCheckerGenerator(size=9, board_size=720)
#
#     if choice == "1":
#         # Custom tile count
#         num_filled = get_user_tile_count()
#     elif choice == "2":
#         print("Choose example:")
#         print("a) 10 tiles  b) 25 tiles  c) 50 tiles  d) 75 tiles")
#         example_choice = input("Enter choice (a-d): ").strip().lower()
#
#         examples = {"a": 10, "b": 25, "c": 50, "d": 75}
#         num_filled = examples.get(example_choice, 40)
#     else:
#         # Default
#         num_filled = 40
#
#     generator.print_generation_info(num_filled)
#     print(f"\n🎨 Generating grid with updated opacity levels ({num_filled} filled tiles)...")
#     generator.render_updated_opacity_grid(num_filled)
#
#     print(f"\n✨ Updated opacity grid generated successfully!")
#     print("✅ New opacity levels applied:")
#     print("  🟢 Green tiles: 50% opacity (unchanged)")
#     print("  🟤 Tan tiles: 70% opacity (MORE VISIBLE)")
#     print("  🟫 Grey void tiles: 50% opacity (MORE VISIBLE)")
#     print("  🎯 Tan tiles now have strongest presence")
#     print("  ⚫ Dotted grid maintained")
#
#
# if __name__ == "__main__":
#     main()
