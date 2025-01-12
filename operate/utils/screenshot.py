import os
import platform
import subprocess

import pyautogui
import Xlib.display
import Xlib.X
import Xlib.Xutil  # not sure if Xutil is necessary
from PIL import Image, ImageDraw, ImageGrab


def capture_screen_with_cursor(file_path):
    user_platform = platform.system()

    if user_platform == "Windows":
        screenshot = pyautogui.screenshot()
        screenshot.save(file_path)
    elif user_platform == "Linux":
        # Use xlib to prevent scrot dependency for Linux
        screen = Xlib.display.Display().screen()
        size = screen.width_in_pixels, screen.height_in_pixels
        screenshot = ImageGrab.grab(bbox=(0, 0, size[0], size[1]))
        screenshot.save(file_path)
    elif user_platform == "Darwin":  # (Mac OS)
        # Use the screencapture utility to capture the screen with the cursor
        subprocess.run(["screencapture", "-C", file_path])
        # Add graph lines to the screenshot
        add_graph_lines(file_path, grid_spacing=50)
    else:
        print(
            f"The platform you're using ({user_platform}) is not currently supported"
        )


def add_graph_lines(file_path, grid_spacing=50):
    """Add horizontal and vertical grid lines to the screenshot with labels.

    Args:
        file_path (str): Path to the screenshot file
        grid_spacing (int): Spacing between grid lines in pixels
    """
    # Open the screenshot
    img = Image.open(file_path)
    width, height = img.size

    # Create a larger canvas to accommodate labels
    padding = 30  # Space for labels
    new_img = Image.new(
        "RGBA", (width + padding, height + padding), (0, 0, 0, 0)
    )
    new_img.paste(img, (padding, padding))
    draw = ImageDraw.Draw(new_img)

    # Font settings for labels
    font_color = "rgba(255, 255, 255, 255)"  # White text for better visibility
    line_color = "rgba(255, 255, 255, 64)"  # Very light white (25% opacity)

    # Draw vertical lines with labels
    for x in range(0, width, grid_spacing):
        x_pos = x + padding
        draw.line(
            [(x_pos, padding), (x_pos, height + padding)],
            fill=line_color,
            width=1,
        )
        # Add x-axis label above the image
        draw.text((x_pos - 10, 5), str(x), fill=font_color, font_size=8)

    # Draw horizontal lines with labels
    for y in range(0, height, grid_spacing):
        y_pos = y + padding
        draw.line(
            [(padding, y_pos), (width + padding, y_pos)],
            fill=line_color,
            width=1,
        )
        # Add y-axis label to the left of the image
        draw.text((5, y_pos - 10), str(y), fill=font_color, font_size=8)

    # Save the modified image
    new_img.save(file_path)
