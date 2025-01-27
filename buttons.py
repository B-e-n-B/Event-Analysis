import tkinter as tk
from tkinter import ttk
from events import *
from Functions import *
import subprocess

# Create the main application window
root = tk.Tk()
root.title("Event Analysis")
root.geometry("400x300")
root.configure(bg="#f0f0f0")

# Add a title label
title_label = tk.Label(root, text="Pick an Event to Analyze", font=("Helvetica", 16, "bold"), bg="#f0f0f0", fg="#333")
title_label.pack(pady=20)

# Create a dropdown menu (combobox)
dropdown_label = tk.Label(root, text="Choose an option:", font=("Helvetica", 12), bg="#f0f0f0", fg="#333")
dropdown_label.pack(pady=10)

options = ["CPI YOY", "GDP Price Index", "PPI Ex Food Energy Yoy", "unemployement rate"]
dropdown_var = tk.StringVar(value=options[0])
dropdown_menu = ttk.Combobox(root, textvariable=dropdown_var, values=options, state="readonly", font=("Helvetica", 12))
dropdown_menu.pack(pady=10)

# Create a button
def on_button_click():
    selected_option = dropdown_var.get()
    if selected_option == options[0]:
        ChosenEvent = Cpi_Yoy
    if selected_option == options[1]:
        ChosenEvent = Gdp_Price_index
    if selected_option == options[2]:
        ChosenEvent = Ppi_Ex_Food_Energy_Yoy
    if selected_option == options[3]:
        ChosenEvent = Unemployement_Rate

    list_to_file(ChosenEvent, 'datelist.txt')
    subprocess.run(['python', 'Main.py'])


button = tk.Button(root, text="Run Analysis", font=("Helvetica", 12, "bold"), bg="#4CAF50", fg="white", padx=10, pady=5, command=on_button_click)
button.pack(pady=20)

# Run the application
root.mainloop()