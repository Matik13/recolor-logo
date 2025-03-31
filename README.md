# Recolor Logo

A Python script that creates color variations of an logo by swapping RGB channels of chosen dominant color.

![python_r_all.png](https://github.com/Matik13/recolor-logo/blob/main/python_r_all.png)

## Features

- Swap RGB channels based on dominance in a selected color component
- Generate all possible color variations with repetitions (3³=27 variations)
- Support for images with and without alpha channel (transparency)
- Output each variation as a separate file
- Create a composite grid view of all generated variations

## Requirements

- **Python 3.x**
- [Pillow](https://pypi.org/project/pillow/) – for image processing
- Python Standard Libraries:
  - `os`
  - `itertools`

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/Matik13/recolor-logo.git
   cd recolor-logo
   ```

2. Install the required packages:
   ```bash
   pip install Pillow
   ```

## Usage

1. Place your image in the same directory as the script
2. Run the script:
   ```bash
   python color_swapper.py
   ```
3. Follow the prompts:
   - Enter the image filename (with extension)
   - Choose which color channel to replace ('r', 'g', or 'b')

## How It Works

1. The script loads the input image and converts it to the appropriate mode (RGB or RGBA)
2. For each pixel, it checks if the specified color component is dominant
3. If dominant, it swaps the RGB channels according to the current permutation
4. Each variation is saved in an output directory
5. A composite grid of all variations is generated

## Output

The program creates a new directory named `[original_filename]_output` containing:

- Individual images with naming pattern: `[original_name]_[replaced_channel]_[new_channel_order].[extension]`
- A composite grid image of all variations: `[original_name]_[replaced_channel]_all.[extension]` (including original image)

## Example

![python.png](https://github.com/Matik13/recolor-logo/blob/main/python.png)

For an input image `python.png` with 'b' as the color to replace:

- Output folder: `python_output/`
- Individual files like: `python_b_rrg.png`, `python_b_grb.png`, etc.
- Grid composite: `python_b_all.png`

![python_b_all.png](https://github.com/Matik13/recolor-logo/blob/main/python_b_all.png)

## License

This project is open-source and available under the [MIT License](LICENSE).
