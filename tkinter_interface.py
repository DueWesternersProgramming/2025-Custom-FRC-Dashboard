import tkinter as tk
from PIL import Image, ImageTk
from math import cos, sin, radians

import nt_interface

import os
import sys


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


root = tk.Tk()
root.title("Custom FRC Dashboard")
root.geometry("800x480")
root.configure(bg="#3e3e3e")

# Load and scale the image
original_image = Image.open(resource_path("img.png"))


# Scale factor (change these values for different sizes)
scale_factor = 1.15  # Adjust this to make the image larger or smaller
radius = 215  # Radius of the circle of buttons

algaeOffColor = "#7a120b"

new_width = int(original_image.width * scale_factor)
new_height = int(original_image.height * scale_factor)

# Resize the image
resized_image = original_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
photo = ImageTk.PhotoImage(resized_image)

# Create label with resized image
picture = tk.Label(root, image=photo, borderwidth=0)
picture.place(relx=0.6, rely=0.6, anchor="center")

leftPositions = [x for x in range(1, 18, 3)]
algaePositions = [x for x in range(2, 18, 3)]
rightPositions = [x for x in range(3, 18, 3)]


def create_buttons_in_circle(center_x, center_y, radius, buttons=None):
    """Function to create buttons in a circle around a center point, with 1 at the bottom"""
    if buttons is None:
        buttons = []  # Ensure buttons list is properly initialized

    for i in range(18):
        angle = (
            -i * (360 / 18) + 90 + (360 / 18)
        )  # Offset by 90 degrees to place 1 at the bottom
        angle_rad = radians(angle)  # Convert to radians

        # Correctly calculate button positions based on radius
        x = center_x + (radius * cos(angle_rad))
        y = center_y + (radius * sin(angle_rad))

        if i < len(buttons):  # Update existing buttons
            buttons[i].place(x=x, y=y, anchor="center")
        else:  # Create new buttons
            if i + 1 in leftPositions:
                text = "1"
                width = 2
                color = "red"
            elif i + 1 in algaePositions:
                text = "A"
                width = 4
                color = algaeOffColor
            else:
                text = "2"
                width = 2
                color = "red"
            button = tk.Button(
                root,
                text=text,
                font=("Courier", 15),
                fg="black",
                width=width,
                height=2,
                bg=color,
                borderwidth=1,
            )
            button.place(x=x, y=y, anchor="center")
            buttons.append(button)

    return buttons


def create_level_buttons():
    buttons = []
    names = ["L3", "L2", "L1", "Home"]

    for i in range(3, -1, -1):  # 0 = Home, 1 = L1, 2 = L2, 3 = L3
        button = tk.Button(
            root, text=names[i], bg="red", fg="black", font=("Courier", 44)
        )
        button.grid(row=i, column=0, sticky="nsw")  # Adjusted row placement
        root.rowconfigure(i, weight=1)  # Make each row expand equally
        buttons.append(button)

    root.columnconfigure(0, weight=1)  # Ensure the column expands correctly
    return buttons


def create_hp_buttons():
    """Create Left and Right HP buttons"""
    buttons = []
    l = tk.Button(root, text="Left HP", bg="red", fg="black", font=("Courier", 44))
    r = tk.Button(root, text="Right HP", bg="red", fg="black", font=("Courier", 44))

    l.grid_configure(row=0, column=2, sticky="new")
    r.grid_configure(row=0, column=5, sticky="new")
    buttons.append(l)
    buttons.append(r)
    return buttons


# def create_position_buttons():
#     names = ["Left", "Algae", "Right"]
#     buttons = []
#     for i in range(3):
#         button = tk.Button(
#             root, text=names[i], bg="red", fg="black", font=("Courier", 30)
#         )
#         button.grid_configure(column=i + 3, row=3, sticky="nsew")
#         root.columnconfigure(i + 3, weight=1)
#         buttons.append(button)
#     return buttons


def update_positions(event):
    """Function to update reef button positions when the window is resized"""
    center_x = picture.winfo_x() + new_width // 2
    center_y = picture.winfo_y() + new_height // 2

    # Update button positions
    create_buttons_in_circle(center_x, center_y, radius, reefButtons)


def reef_side_selected(index):
    """Function called when a reef button is clicked."""
    selection = index + 1  # Convert 0-based index to 1-based position

    # Reset colors except selected one
    for i, button in enumerate(reefButtons):
        if i == index:
            continue  # Skip the selected one
        if (i + 1) in algaePositions:
            button.config(bg=algaeOffColor)
        else:
            button.config(bg="red")
    # Change selected button to green
    reefButtons[index].config(bg="green")

    if selection in algaePositions:
        nt_interface.setNum("Position", 1)
        algae_index = algaePositions.index(selection) + 1  # Get Algae index 1-6
        nt_interface.setNum("Reef Side", algae_index)
        level_selected(2 if algae_index % 2 == 1 else 1)  # Alternate L3, L2
    else:
        if selection in leftPositions:
            nt_interface.setNum("Position", 0)
        elif selection in rightPositions:
            nt_interface.setNum("Position", 2)


def level_selected(index):
    """Function called when a level button is clicked."""
    for i in range(3, -1, -1):
        levelButtons[i].config(bg="red")
    levelButtons[index].config(bg="green")

    nt_interface.setNum("Level", index)


# def position_selected(index):
#     """Function called when a position button is clicked."""
#     for i in range(len(positionButtons)):
#         positionButtons[i].config(bg="red")
#     positionButtons[index].config(bg="green")

#     nt_interface.setNum("Position", index)  # No +1 since it goes 0,1,2


def hp_selected(index):
    """Function called when a HP button is clicked."""
    for i in range(len(hpButtons)):
        hpButtons[i].config(bg="red")
    hpButtons[index].config(bg="green")

    nt_interface.setNum("HumanPlayer", index)


# Create buttons initially and set commands
hpButtons = create_hp_buttons()
reefButtons = create_buttons_in_circle(450, 240, radius)
# positionButtons = create_position_buttons()
levelButtons = create_level_buttons()


for i in range(18):
    reefButtons[i].config(command=lambda i=i: reef_side_selected(i))

for i in range(1, 4):
    levelButtons[i].config(command=lambda i=i: level_selected(i))

# for i in range(3):
#     positionButtons[i].config(command=lambda i=i: position_selected(i))

for i in range(2):
    hpButtons[i].config(command=lambda i=i: hp_selected(i))

# Make the Home Elevator Button

levelButtons[0].config(
    command=lambda: nt_interface.setBoolean(
        "HomeSubsystems", (not nt_interface.getBoolean("HomeSubsystems"))
    )
)


# Bind the <Configure> event to dynamically update positions
root.bind("<Configure>", update_positions)

root.mainloop()
