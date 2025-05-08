import requests
import customtkinter as ctk
import ctypes
from tkinter import messagebox
import webbrowser  # to open Discord invite in the browser
import logging

# Hide console window (Windows only)
ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

# Configure logging
logging.basicConfig(filename="webhook_tool_log.txt", level=logging.INFO, 
                    format="%(asctime)s - %(message)s")

# Function to send messages
def send_messages():
    webhook_url = webhook_entry.get().strip()
    message = message_entry.get("1.0", "end").strip()
    times = times_entry.get().strip()

    # Input validation
    if not webhook_url or not message or not times.isdigit():
        messagebox.showerror("Error", "Please fill all fields correctly!")
        return

    times = int(times)

    # Disable button to prevent multiple clicks
    send_button.configure(state="disabled", text="Sending...")

    # Log the action
    logging.info(f"Sending {times} messages to {webhook_url} with message: {message}")

    for _ in range(times):
        response = requests.post(webhook_url, json={"content": message})
        if response.status_code != 204:
            messagebox.showerror("Error", f"Failed to send message: {response.text}")
            send_button.configure(state="normal", text="Send Messages")
            return

    messagebox.showinfo("Success", f"Sent {times} messages successfully!")
    send_button.configure(state="normal", text="Send Messages")

# Function to delete webhook
def delete_webhook():
    webhook_url = webhook_entry.get().strip()
    if not webhook_url:
        messagebox.showerror("Error", "Please enter a webhook URL!")
        return

    response = requests.delete(webhook_url)
    if response.status_code in [200, 204]:
        messagebox.showinfo("Success", "Webhook deleted successfully!")
    else:
        messagebox.showerror("Error", f"Failed to delete webhook: {response.text}")
    logging.info(f"Attempted to delete webhook: {webhook_url}")

# Function to open Discord invite link
def open_discord():
    webbrowser.open("https://discord.gg/FPWnA3bRtf")

# GUI setup
ctk.set_appearance_mode("dark")  # Dark mode
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("TWS' Webhook Tool")
root.geometry("500x500")  # Adjusted size for better layout
root.resizable(False, False)

# UI Components
header_label = ctk.CTkLabel(root, text="Webhook Tool", font=("Arial", 18, "bold"))
header_label.pack(pady=10)

discord_button = ctk.CTkButton(root, text="Join My Discord Server", command=open_discord, fg_color="#7289DA", font=("Arial", 14, "bold"))
discord_button.pack(pady=10)

# Webhook URL Section
ctk.CTkLabel(root, text="Enter Webhook URL:", font=("Arial", 14)).pack(pady=5)
webhook_entry = ctk.CTkEntry(root, width=400)
webhook_entry.pack(pady=5)

# Message Section
ctk.CTkLabel(root, text="Enter Message:", font=("Arial", 14)).pack(pady=5)
message_entry = ctk.CTkTextbox(root, height=100, width=400)
message_entry.pack(pady=5)

# Times to send Section
ctk.CTkLabel(root, text="How many times to send:", font=("Arial", 14)).pack(pady=5)
times_entry = ctk.CTkEntry(root, width=100)
times_entry.pack(pady=5)

# Buttons
send_button = ctk.CTkButton(root, text="Send Messages", command=send_messages, fg_color="#4CAF50", font=("Arial", 14))
send_button.pack(pady=10)

# Delete Webhook Button (Red)
delete_button = ctk.CTkButton(root, text="Delete Webhook", command=delete_webhook, fg_color="#D32F2F", font=("Arial", 14))
delete_button.pack(side="bottom", pady=15)

# Run the GUI
root.mainloop()
