from tkinter import ttk
from tkinter import scrolledtext
from tkinter import messagebox
import tkinter as tk
import threading
import time  # Simulate the delay from fetching data
import LetsHunt  # Assuming LetsHunt.py is in the same directory and has the necessary functions

# Function to fetch data
def fetch_data(progress, domain):
    try:
        # Get and display IP address
        ip_address = LetsHunt.get_ip_address(domain)
        root.after(0, update_text_widget, ip_text, ip_address + "\n")
        print(f"Address: {ip_address}")

        # Get and display DNS records
        dns_records = LetsHunt.get_dns_records(domain)
        for qtype, records in dns_records.items():
            root.after(0, update_text_widget, dns_text, f"{qtype}:\n")
            for record in records:
                root.after(0, update_text_widget, dns_text, record + "\n")
        print(f"DNS Records: {dns_records}")

        # Get and display server details
        server_details = LetsHunt.get_server_details(domain)
        root.after(0, update_text_widget, server_text, f"Web Server: {server_details.get('web_server')}\n")
        root.after(0, update_text_widget, server_text, f"Operating System: {server_details.get('operating_system')}\n")
        root.after(0, update_text_widget, server_text, "HTTP Headers:\n")
        for key, value in server_details.get("http_headers", {}).items():
            root.after(0, update_text_widget, server_text, f"{key}: {value}\n")
        print(f"Server Details: {server_details}")

        # Get and display WHOIS info
        whois_info = LetsHunt.get_whois_info(domain)
        for key, value in whois_info.items():
            if isinstance(value, list):
                for item in value:
                    root.after(0, update_text_widget, whois_text, f"{key}: {item}\n")
            else:
                root.after(0, update_text_widget, whois_text, f"{key}: {value}\n")
        print(f"WHOIS Info: {whois_info}")

        # Get and display subdomains
        subdomains = LetsHunt.enumerate_subdomains(domain)
        for subdomain, ip_address in subdomains:
            root.after(0, update_text_widget, subdomains_text, f"{subdomain}: {ip_address}\n")
        print(f"Subdomains: {subdomains}")

        # Get and display open ports
        open_ports = LetsHunt.port_scan(domain, ip_address)
        for port in open_ports:
            root.after(0, update_text_widget, ports_text, port + "\n")
        print(f"Open Ports: {open_ports}")

    except Exception as e:
        root.after(0, messagebox.showerror, "Error", f"An error occurred: {e}")
        print(f"Error: {e}")
    finally:
        # Stop and hide the progress bar
        root.after(0, progress.stop)
        root.after(0, progress.grid_remove)  # Hide the progress bar

# Function to update text widget
def update_text_widget(widget, text):
    widget.config(state='normal')
    widget.insert(tk.END, text)
    widget.config(state='disabled')

# Start the data fetching process and display the progress bar
def start_fetching():
    domain = domain_entry.get()
    if not domain:
        messagebox.showerror("Error", "Please enter a domain.")
        return

    # Clear previous results
    clear_results()

    # Set up and start the progress bar
    progress_bar.grid()  # Show the progress bar
    progress_bar.start(10)  # Start the progress bar animation

    # Start the data fetching in a new thread
    threading.Thread(target=fetch_data, args=(progress_bar, domain)).start()

# Function to clear results
def clear_results():
    ip_text.config(state='normal')
    ip_text.delete(1.0, tk.END)
    ip_text.config(state='disabled')

    dns_text.config(state='normal')
    dns_text.delete(1.0, tk.END)
    dns_text.config(state='disabled')

    server_text.config(state='normal')
    server_text.delete(1.0, tk.END)
    server_text.config(state='disabled')

    whois_text.config(state='normal')
    whois_text.delete(1.0, tk.END)
    whois_text.config(state='disabled')

    subdomains_text.config(state='normal')
    subdomains_text.delete(1.0, tk.END)
    subdomains_text.config(state='disabled')

    ports_text.config(state='normal')
    ports_text.delete(1.0, tk.END)
    ports_text.config(state='disabled')

# Set up the GUI
root = tk.Tk()
root.title("Lets Hunt")
root.configure(bg='black')

# Get screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Set the window size to a percentage of the screen resolution
window_width = int(screen_width * 0.8)  # 80% of screen width
window_height = int(screen_height * 0.8)  # 80% of screen height

# Center the window on the screen
root.geometry(f"{window_width}x{window_height}+{int(screen_width * 0.1)}+{int(screen_height * 0.1)}")

# Create a main frame
main_frame = ttk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=1)

# Create a canvas
canvas = tk.Canvas(main_frame, bg='black')
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

# Add a scrollbar to the canvas
scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Configure the canvas
canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

# Create another frame inside the canvas
second_frame = ttk.Frame(canvas, style='My.TFrame')

# Add that new frame to a window in the canvas
canvas.create_window((0, 0), window=second_frame, anchor="nw")

# Ensure that the domain_frame is centered and expanded
domain_frame = ttk.Frame(second_frame)
domain_frame.grid(column=0, row=0, padx=10, pady=5, columnspan=3, sticky="ew")

# Create domain_label and domain_entry and center them
domain_label = ttk.Label(domain_frame, text="Enter target domain:", font=("Arial", 12, "bold"), background='black', foreground='green')
domain_label.grid(row=0, column=0, padx=0, pady=0, sticky="w")

domain_entry = ttk.Entry(domain_frame, width=50)
domain_entry.grid(row=0, column=1, padx=0, pady=0, sticky="ew")

# Add a weight to columns so that domain_entry expands
domain_frame.grid_columnconfigure(0, weight=1)
domain_frame.grid_columnconfigure(1, weight=3)

# Create a progress bar
progress_bar = ttk.Progressbar(second_frame, orient="horizontal", length=190, mode="indeterminate", style='Horizontal.TProgressbar')
progress_bar.grid(column=3, row=1, padx=10, pady=5, columnspan=2, sticky="ew")

# Gather Info button
gather_button = tk.Button(second_frame, text="Start Hunt", command=start_fetching, activeforeground="white", bg='black', fg='red')
gather_button.grid(column=3, row=0, padx=20, pady=15, sticky='e')

# IP Address
ip_label = ttk.Label(second_frame, text="IP Address:", font=("Arial", 12, "bold"), background='black', foreground='green')
ip_label.grid(column=0, row=1, padx=10, pady=5)
ip_text = scrolledtext.ScrolledText(second_frame, width=50, height=1, wrap=tk.WORD, state='disabled', background='black', foreground='green')
ip_text.grid(column=1, row=1, padx=10, pady=5, columnspan=2)

# DNS Records
dns_label = ttk.Label(second_frame, text="DNS Records:", font=("Arial", 12, "bold"), background='black', foreground='green')
dns_label.grid(column=0, row=2, padx=10, pady=5)
dns_text = scrolledtext.ScrolledText(second_frame, width=50, height=6, wrap=tk.WORD, state='disabled', background='black', foreground='green')
dns_text.grid(column=1, row=2, padx=10, pady=5, columnspan=2)

# Server Details
server_label = ttk.Label(second_frame, text="Server Details:", font=("Arial", 12, "bold"), background='black', foreground='green')
server_label.grid(column=0, row=3, padx=10, pady=5)
server_text = scrolledtext.ScrolledText(second_frame, width=50, height=6, wrap=tk.WORD, state='disabled', background='black', foreground='green')
server_text.grid(column=1, row=3, padx=10, pady=5, columnspan=2)

# WHOIS Info
whois_label = ttk.Label(second_frame, text="WHOIS Info:", font=("Arial", 12, "bold"), background='black', foreground='green')
whois_label.grid(column=0, row=4, padx=10, pady=5)
whois_text = scrolledtext.ScrolledText(second_frame, width=50, height=6, wrap=tk.WORD, state='disabled', background='black', foreground='green')
whois_text.grid(column=1, row=4, padx=10, pady=5, columnspan=2)

# Subdomains
subdomains_label = ttk.Label(second_frame, text="Subdomains:", font=("Arial", 12, "bold"), background='black', foreground='green')
subdomains_label.grid(column=0, row=5, padx=10, pady=5)
subdomains_text = scrolledtext.ScrolledText(second_frame, width=50, height=6, wrap=tk.WORD, state='disabled', background='black', foreground='green')
subdomains_text.grid(column=1, row=5, padx=10, pady=5, columnspan=2)

# Open Ports
ports_label = ttk.Label(second_frame, text="Open Ports:", font=("Arial", 12, "bold"), background='black', foreground='green')
ports_label.grid(column=0, row=6, padx=10, pady=5)
ports_text = scrolledtext.ScrolledText(second_frame, width=50, height=6, wrap=tk.WORD, state='disabled', background='black', foreground='green')
ports_text.grid(column=1, row=6, padx=10, pady=5, columnspan=2)

# Style configuration
style = ttk.Style()
style.configure('My.TFrame', background='black')
style.configure('TLabel', background='black', foreground='green')
style.configure('TEntry', fieldbackground='black', foreground='green')
style.configure('TProgressbar', foreground='black', background='red')  # Configure all progress bars

# Hide progress bar initially
progress_bar.grid_remove()

# Run the application
root.mainloop()
