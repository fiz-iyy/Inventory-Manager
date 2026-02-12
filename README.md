# Inventory-Manager
Inventory Manager is a Tkinter‑based desktop app for managing a laptop shop’s stock, sales, and purchases, with invoice generation and file‑based persistence.

Inventory Manager is a Python desktop application for managing inventory in a laptop shop. It provides a simple GUI built with Tkinter on top of a file‑based backend (using stock.txt), keeping the original business logic intact while improving usability.

Tech stack - 
Language: Python 3

GUI: Tkinter (tkinter, ttk, messagebox)

Persistence: Plain text files (stock.txt for inventory, .txt invoices)

Structure:
 * Main.py / DesktopCare.pyw – entry points
 * gui.py – Tkinter GUI (inventory table, dialogs, actions)
 * Read.py – stock loading and console table helper
 * Write.py – stock updates and invoice file generation
 * Operations.py – original CLI operations (kept for reference/compatibility)
 * stock.txt – initial laptop data
 * invoices/ – generated bills
