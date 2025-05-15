import tkinter as tk
from PIL import Image, ImageTk

from dashboard import nt_interface

root = tk.Tk()
root.title("Custom FRC Dashboard")
root.geometry("800x480")
root.configure(bg="#3e3e3e")


def create_level_buttons():
    buttons = []
    names = ["L3", "L2", "L1", "Home"]

    for i in range(3, -1, -1):
        button_color = "blue" if i == 3 else "red"

        button = tk.Button(
            root,
            text=names[i],
            bg=button_color,
            fg="black",
            font=("Courier", 44),
            borderwidth=30,
        )
        button.grid(row=i, column=0, sticky="nswe")
        root.rowconfigure(i, weight=1)
        buttons.append(button)

    root.columnconfigure(0, weight=1)
    return buttons


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
        button.grid(column=i + 2, row=3, sticky="nsew")
        root.columnconfigure(i + 2, weight=1)
        buttons.append(button)

    return buttons


def create_intake_outtake_buttons():
    buttons = []

    button_intake = tk.Button(
        root,
        text="Intake",
        bg="blue",
        fg="black",
        font=("Courier", 30),
        borderwidth=5,
    )
    button_intake.grid(column=4, row=0, sticky="nsew")

    button_outtake = tk.Button(
        root,
        text="Outtake",
        bg="blue",
        fg="black",
        font=("Courier", 30),
        borderwidth=5,
    )
    button_outtake.grid(column=4, row=1, sticky="nsew")

    # **Force Windows to treat touch like a regular click**
    button_intake.bind(
        "<ButtonPress-1>", lambda event: nt_interface.setBoolean("IntakeOn", True)
    )
    button_intake.bind(
        "<ButtonRelease-1>", lambda event: nt_interface.setBoolean("IntakeOn", False)
    )

    button_outtake.bind(
        "<ButtonPress-1>", lambda event: nt_interface.setBoolean("OuttakeOn", True)
    )
    button_outtake.bind(
        "<ButtonRelease-1>", lambda event: nt_interface.setBoolean("OuttakeOn", False)
    )

    buttons.append(button_intake)
    buttons.append(button_outtake)

    return buttons


def level_selected(index):
    """Function called when a level button is clicked."""
    for i in range(3, -1, -1):
        levelButtons[i].config(bg="blue" if i == 0 else "red")

    levelButtons[index].config(bg="green")
    nt_interface.setNum("Level", index)


def position_selected(index):
    """Function called when a position button is clicked."""
    for button in positionButtons:
        button.config(bg="#9c0615")

    positionButtons[index].config(bg="green")
    nt_interface.setNum("Position", index)


positionButtons = create_position_buttons()
levelButtons = create_level_buttons()
# intakeOuttakeButtons = create_intake_outtake_buttons()

for i in range(1, 4):
    levelButtons[i].config(command=lambda i=i: level_selected(i))

for i in range(3):
    positionButtons[i].config(command=lambda i=i: position_selected(i))

# Make the Home Elevator Button toggle the HomeSubsystems boolean
levelButtons[0].config(
    command=lambda: nt_interface.setBoolean(
        "HomeSubsystems", not nt_interface.getBoolean("HomeSubsystems")
    )
)

root.mainloop()
