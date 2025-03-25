import tkinter as tk
from PIL import Image, ImageTk
from math import cos, sin, radians

import nt_interface

import os
import sys


root = tk.Tk()
root.title("Custom FRC Dashboard")
root.geometry("800x480")
root.configure(bg="#3e3e3e")

# Load and scale the image
# original_image = Image.open("img.png")


# # Scale factor (change these values for different sizes)
# scale_factor = 1.15  # Adjust this to make the image larger or smaller
# radius = 215  # Radius of the circle of buttons

# algaeOffColor = "#7a120b"

# new_width = int(original_image.width * scale_factor)
# new_height = int(original_image.height * scale_factor)

# # Resize the image
# resized_image = original_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
# photo = ImageTk.PhotoImage(resized_image)

# # Create label with resized image
# picture = tk.Label(root, image=photo, borderwidth=0)
# picture.place(relx=0.6, rely=0.6, anchor="center")

reefSideKey = [1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6]
algaePositions = [2, 5, 8, 11, 14, 17]

# def create_buttons_in_circle(center_x, center_y, radius, buttons=None):
#     """Function to create buttons in a circle around a center point, with 1 at the bottom"""
#     if buttons is None:
#         buttons = []  # Ensure buttons list is properly initialized

#     for i in range(18):
#         angle = (
#             -i * (360 / 18) + 90 + (360 / 18)
#         )  # Offset by 90 degrees to place 1 at the bottom
#         angle_rad = radians(angle)  # Convert to radians

#         # Correctly calculate button positions based on radius
#         x = center_x + (radius * cos(angle_rad))
#         y = center_y + (radius * sin(angle_rad))

#         if i < len(buttons):  # Update existing buttons
#             buttons[i].place(x=x, y=y, anchor="center")

#         else:  # Create new buttons
#             if determinePositionFromButtonNumber(i+1) == 0:
#                 text = "1"
#                 width = 2
#                 color = "red"
#             elif determinePositionFromButtonNumber(i+1) == 1:
#                 text = "A"
#                 width = 4
#                 color = algaeOffColor
#             else:
#                 text = "2"
#                 width = 2
#                 color = "red"
#             button = tk.Button(
#                 root,
#                 text=text,
#                 font=("Courier", 15),
#                 fg="black",
#                 width=width,
#                 height=2,
#                 bg=color,
#                 borderwidth=1,
#             )
#             button.place(x=x, y=y, anchor="center")
#             buttons.append(button)

#     return buttons


def create_level_buttons():
    buttons = []
    names = ["L3", "L2", "L1", "Home"]

    for i in range(3, -1, -1):  # 0 = Home, 1 = L1, 2 = L2, 3 = L3
        button = tk.Button(
            root,
            text=names[i],
            bg="red",
            fg="black",
            font=("Courier", 44),
            borderwidth=30,
        )
        button.grid(row=i, column=0, sticky="nswe")  # Adjusted row placement
        root.rowconfigure(i, weight=1)  # Make each row expand equally
        buttons.append(button)

    root.columnconfigure(0, weight=1)  # Ensure the column expands correctly
    return buttons


# def create_hp_buttons():
#     """Create Left and Right HP buttons"""
#     buttons = []
#     l = tk.Button(root, text="Left HP", bg="red", fg="black", font=("Courier", 44))
#     r = tk.Button(root, text="Right HP", bg="red", fg="black", font=("Courier", 44))

#     l.grid_configure(row=0, column=2, sticky="new")
#     r.grid_configure(row=0, column=5, sticky="new")
#     buttons.append(l)
#     buttons.append(r)
#     return buttons


def create_position_buttons():
    names = ["Left", "Algae", "Right"]
    buttons = []
    for i in range(3):
        button = tk.Button(
            root,
            text=names[i],
            bg="#9c0615",
            fg="black",
            font=("Courier", 30),
            borderwidth=10,
        )
        button.grid_configure(column=i + 2, row=3, sticky="nsew")
        root.columnconfigure(i + 2, weight=1)
        buttons.append(button)
    return buttons


def update_positions(event):
    """Function to update reef button positions when the window is resized"""
    # center_x = picture.winfo_x() + new_width // 2
    # center_y = picture.winfo_y() + new_height // 2

    # Update button positions
    # create_buttons_in_circle(center_x, center_y, radius, reefButtons)


def getReefSideFromButtonNumber(buttonNumber):
    return reefSideKey[buttonNumber - 1]


# def reef_side_selected(buttonNumber):
#     """Function called when a reef button is clicked."""

#     # Reset colors
#     for button in reefButtons:
#         if reefButtons.index(button) + 1 in algaePositions:

#             button.config(bg=algaeOffColor)
#         else:
#             button.config(bg="red")

#     # Change selected button to green
#     reefButtons[buttonNumber - 1].config(bg="green")

#     reefSide = getReefSideFromButtonNumber(buttonNumber)

#     if buttonNumber in algaePositions:
#         nt_interface.setNum("Position", 1)
#         nt_interface.setNum("Reef Side", reefSide)

#         level_selected(3 if reefSide % 2 == 1 else 2)  # Alternate L3, L2

#     else:
#         nt_interface.setNum("Position", determinePositionFromButtonNumber(buttonNumber))
#         print(buttonNumber)
#         print(reefSide)
#         nt_interface.setNum("Reef Side", reefSide)


def determinePositionFromButtonNumber(buttonNumber):
    match buttonNumber:
        case 1:
            return 0
        case 2:
            return 1
        case 3:
            return 2
        case 4:
            return 0
        case 5:
            return 1
        case 6:
            return 2
        case 7:
            return 0
        case 8:
            return 1
        case 9:
            return 2
        case 10:
            return 0
        case 11:
            return 1
        case 12:
            return 2
        case 13:
            return 0
        case 14:
            return 1
        case 15:
            return 2
        case 16:
            return 0
        case 17:
            return 1
        case 18:
            return 2


def level_selected(index):
    """Function called when a level button is clicked."""
    for i in range(3, -1, -1):
        levelButtons[i].config(bg="red")
    levelButtons[index].config(bg="green")

    nt_interface.setNum("Level", index)


def position_selected(index):
    """Function called when a position button is clicked."""
    for i in range(len(positionButtons)):
        positionButtons[i].config(bg="#9c0615")
    positionButtons[index].config(bg="green")

    nt_interface.setNum("Position", index)  # No +1 since it goes 0,1,2


#


# Create buttons initially and set commands
# hpButtons = create_hp_buttons()
# reefButtons = create_buttons_in_circle(450, 240, radius)
positionButtons = create_position_buttons()
levelButtons = create_level_buttons()


# for i in range(18):
#     reefButtons[i].config(command=lambda i=i: reef_side_selected(i + 1))

for i in range(1, 4):
    levelButtons[i].config(command=lambda i=i: level_selected(i))

for i in range(3):
    positionButtons[i].config(command=lambda i=i: position_selected(i))

# for i in range(2):
#     hpButtons[i].config(command=lambda i=i: hp_selected(i))

# Make the Home Elevator Button

levelButtons[0].config(
    command=lambda: nt_interface.setBoolean(
        "HomeSubsystems", (not nt_interface.getBoolean("HomeSubsystems"))
    )
)


# Bind the <Configure> event to dynamically update positions
root.bind("<Configure>", update_positions)

root.mainloop()
