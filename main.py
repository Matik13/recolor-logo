import os
from PIL import Image
from itertools import product

image_filename = input("Enter the image filename (with extension): ")

color_to_replace = input("Enter the color to replace (r, g, b): ").lower()
if color_to_replace not in ['r', 'g', 'b']:
    raise ValueError("Invalid. Please enter 'r', 'g', or 'b'.")

script_dir = os.path.dirname(os.path.realpath(__file__))
image_path = os.path.join(script_dir, image_filename)

output_dir = os.path.join(script_dir, f"{os.path.splitext(image_filename)[0]}_output")
os.makedirs(output_dir, exist_ok=True)

image = Image.open(image_path)

has_alpha = image.mode in ("RGBA", "LA")
image = image.convert("RGBA") if has_alpha else image.convert("RGB")

data = image.getdata()

letters = ['r', 'g', 'b']
combinations = [combo for combo in product(letters, repeat=3) if combo not in [('r', 'g', 'b')]]

original_name = os.path.splitext(image_filename)[0]

color_index = {'r': 0, 'g': 1, 'b': 2}
replace_idx = color_index[color_to_replace]

modified_images = [image]

for combo in combinations:
    new_data = []

    for item in data:
        r, g, b = item[:3]
        a = item[3] if has_alpha else 255

        color_values = [r, g, b]
        if color_values[replace_idx] > max(color_values[:replace_idx] + color_values[replace_idx + 1:]):
            new_r = r if combo[0] == 'r' else g if combo[0] == 'g' else b
            new_g = r if combo[1] == 'r' else g if combo[1] == 'g' else b
            new_b = r if combo[2] == 'r' else g if combo[2] == 'g' else b
            new_data.append((new_r, new_g, new_b, a) if has_alpha else (new_r, new_g, new_b))
        else:
            new_data.append(item)

    new_image = image.copy()
    new_image.putdata(new_data)
    modified_images.append(new_image)

    filename_suffix = "".join(combo)
    file_extension = os.path.splitext(image_filename)[1]
    modified_image_path = os.path.join(output_dir,
                                       f'{original_name}_{color_to_replace}_{filename_suffix}{file_extension}')
    new_image.save(modified_image_path)

grid_width = 9
grid_height = 3
image_width, image_height = image.size
grid_image = Image.new("RGBA" if has_alpha else "RGB", (grid_width * image_width, grid_height * image_height))

for index, img in enumerate(modified_images):
    x_offset = (index % grid_width) * image_width
    y_offset = (index // grid_width) * image_height
    grid_image.paste(img, (x_offset, y_offset))

grid_image_path = os.path.join(output_dir, f"{original_name}_{color_to_replace}_all{file_extension}")
grid_image.save(grid_image_path)
