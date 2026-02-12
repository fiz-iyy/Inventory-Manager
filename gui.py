import os
import sys
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
from typing import Callable, Dict, List

from Read import File_Read
from Write import (
    Update_Stock_Purchase,
    Update_Stock_Sales,
    Print_Sales_Bill,
    Generate_Sales_Bill,
    Print_Purchase_Bill,
    Genarate_Purchase_Bill,
    INVOICE_DIR,
)


def _parse_price_to_int(price: str) -> int:
    return int(price.replace("$", "").replace(" ", ""))


class SellWindow(tk.Toplevel):
    def __init__(self, master: tk.Tk, on_complete: Callable[[], None]) -> None:
        super().__init__(master)
        self.title("Sell Laptops")
        self.geometry("620x520")
        self.resizable(False, False)

        self.on_complete = on_complete
        self.inventory = File_Read()
        self.cart: List[Dict] = []

        self.customer_name_var = tk.StringVar()
        self.customer_contact_var = tk.StringVar()
        self.product_id_var = tk.StringVar()
        self.quantity_var = tk.StringVar()

        self._build_ui()

    def _build_ui(self) -> None:
        form_frame = ttk.LabelFrame(self, text="Customer Details")
        form_frame.pack(fill="x", padx=10, pady=10)

        ttk.Label(form_frame, text="Name").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(form_frame, textvariable=self.customer_name_var).grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(form_frame, text="Contact Number").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(form_frame, textvariable=self.customer_contact_var).grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        form_frame.columnconfigure(1, weight=1)

        selection_frame = ttk.LabelFrame(self, text="Add Products")
        selection_frame.pack(fill="x", padx=10, pady=10)

        ttk.Label(selection_frame, text="Product ID").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(selection_frame, textvariable=self.product_id_var, width=10).grid(row=0, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(selection_frame, text="Quantity").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        ttk.Entry(selection_frame, textvariable=self.quantity_var, width=10).grid(row=0, column=3, padx=5, pady=5, sticky="w")

        ttk.Button(selection_frame, text="Add to Cart", command=self._add_to_cart).grid(row=0, column=4, padx=5, pady=5)

        selection_frame.columnconfigure(4, weight=1)

        self.cart_tree = ttk.Treeview(
            self,
            columns=("id", "name", "quantity", "unit_price", "total"),
            show="headings",
            height=8,
        )
        self.cart_tree.heading("id", text="ID")
        self.cart_tree.heading("name", text="Product Name")
        self.cart_tree.heading("quantity", text="Quantity")
        self.cart_tree.heading("unit_price", text="Unit Price")
        self.cart_tree.heading("total", text="Total ($)")

        self.cart_tree.column("id", width=50, anchor="center")
        self.cart_tree.column("name", width=180)
        self.cart_tree.column("quantity", width=80, anchor="center")
        self.cart_tree.column("unit_price", width=100, anchor="center")
        self.cart_tree.column("total", width=100, anchor="center")

        self.cart_tree.pack(fill="both", expand=True, padx=10, pady=10)

        action_frame = ttk.Frame(self)
        action_frame.pack(fill="x", padx=10, pady=10)

        ttk.Button(action_frame, text="Remove Selected", command=self._remove_selected).pack(side="left")
        ttk.Button(action_frame, text="Complete Sale", command=self._complete_sale).pack(side="right")

    def _add_to_cart(self) -> None:
        try:
            product_id = int(self.product_id_var.get())
            quantity = int(self.quantity_var.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Product ID and Quantity must be numeric.")
            return

        if product_id not in self.inventory:
            messagebox.showerror("Invalid Product", "Selected product ID does not exist.")
            return

        if quantity <= 0:
            messagebox.showerror("Invalid Quantity", "Quantity must be greater than zero.")
            return

        available_quantity = int(self.inventory[product_id][3])
        already_selected = sum(item["quantity"] for item in self.cart if item["id"] == product_id)

        if quantity + already_selected > available_quantity:
            messagebox.showerror(
                "Insufficient Stock",
                f"Only {available_quantity - already_selected} units available for this product.",
            )
            return

        price_str = self.inventory[product_id][2]
        unit_price = _parse_price_to_int(price_str)
        total_price = unit_price * quantity

        existing_item = next((item for item in self.cart if item["id"] == product_id), None)
        if existing_item:
            existing_item["quantity"] += quantity
            existing_item["total_price"] += total_price
        else:
            self.cart.append(
                {
                    "id": product_id,
                    "name": self.inventory[product_id][0],
                    "unit_price_str": price_str,
                    "unit_price": unit_price,
                    "quantity": quantity,
                    "total_price": total_price,
                    "graphics": self.inventory[product_id][5],
                }
            )

        self._refresh_cart_view()
        self.product_id_var.set("")
        self.quantity_var.set("")

    def _remove_selected(self) -> None:
        selected_item = self.cart_tree.selection()
        if not selected_item:
            return

        cart_index = int(selected_item[0])
        if 0 <= cart_index < len(self.cart):
            del self.cart[cart_index]
            self._refresh_cart_view()

    def _refresh_cart_view(self) -> None:
        for item in self.cart_tree.get_children():
            self.cart_tree.delete(item)

        for index, cart_item in enumerate(self.cart):
            self.cart_tree.insert(
                "",
                "end",
                iid=str(index),
                values=(
                    cart_item["id"],
                    cart_item["name"],
                    cart_item["quantity"],
                    cart_item["unit_price_str"],
                    cart_item["total_price"],
                ),
            )

    def _complete_sale(self) -> None:
        if not self.cart:
            messagebox.showwarning("Empty Cart", "Please add at least one product before completing the sale.")
            return

        name = self.customer_name_var.get().strip()
        contact = self.customer_contact_var.get().strip()

        if not name or not contact:
            messagebox.showerror("Missing Information", "Customer name and contact number are required.")
            return

        stock_data = File_Read()
        for cart_item in self.cart:
            Update_Stock_Sales(stock_data, cart_item["id"], cart_item["quantity"])

        laptop_sold = [
            [
                cart_item["name"],
                cart_item["quantity"],
                cart_item["unit_price_str"],
                cart_item["total_price"],
                cart_item["graphics"],
            ]
            for cart_item in self.cart
        ]

        total = sum(item["total_price"] for item in self.cart)
        vat = round(total * 0.13, 2)
        shipping_cost = 12
        grand_total = total + vat + shipping_cost
        date_time = datetime.now()
        date_parts = str(date_time).split(" ")

        Print_Sales_Bill(name, contact, date_time, laptop_sold, total, shipping_cost, grand_total, vat)
        Generate_Sales_Bill(name, date_parts, contact, date_time, laptop_sold, total, shipping_cost, grand_total, vat)

        messagebox.showinfo("Sale Completed", f"Sale recorded successfully. Grand Total: ${grand_total:.2f}")
        self.on_complete()
        self.destroy()


class PurchaseWindow(tk.Toplevel):
    def __init__(self, master: tk.Tk, on_complete: Callable[[], None]) -> None:
        super().__init__(master)
        self.title("Purchase Laptops")
        self.geometry("600x480")
        self.resizable(False, False)

        self.on_complete = on_complete
        self.inventory = File_Read()
        self.cart: List[Dict] = []

        self.vendor_name_var = tk.StringVar(value="DESKTOP CARE")
        self.vendor_contact_var = tk.StringVar(value="+977 9803270700")
        self.product_id_var = tk.StringVar()
        self.quantity_var = tk.StringVar()

        self._build_ui()

    def _build_ui(self) -> None:
        form_frame = ttk.LabelFrame(self, text="Vendor Details")
        form_frame.pack(fill="x", padx=10, pady=10)

        ttk.Label(form_frame, text="Vendor Name").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(form_frame, textvariable=self.vendor_name_var).grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(form_frame, text="Contact Number").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(form_frame, textvariable=self.vendor_contact_var).grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        form_frame.columnconfigure(1, weight=1)

        selection_frame = ttk.LabelFrame(self, text="Add Products")
        selection_frame.pack(fill="x", padx=10, pady=10)

        ttk.Label(selection_frame, text="Product ID").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(selection_frame, textvariable=self.product_id_var, width=10).grid(row=0, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(selection_frame, text="Quantity").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        ttk.Entry(selection_frame, textvariable=self.quantity_var, width=10).grid(row=0, column=3, padx=5, pady=5, sticky="w")

        ttk.Button(selection_frame, text="Add to Cart", command=self._add_to_cart).grid(row=0, column=4, padx=5, pady=5)

        selection_frame.columnconfigure(4, weight=1)

        self.cart_tree = ttk.Treeview(
            self,
            columns=("id", "name", "quantity", "unit_price", "total"),
            show="headings",
            height=8,
        )
        self.cart_tree.heading("id", text="ID")
        self.cart_tree.heading("name", text="Product Name")
        self.cart_tree.heading("quantity", text="Quantity")
        self.cart_tree.heading("unit_price", text="Unit Price")
        self.cart_tree.heading("total", text="Total ($)")

        self.cart_tree.column("id", width=50, anchor="center")
        self.cart_tree.column("name", width=180)
        self.cart_tree.column("quantity", width=80, anchor="center")
        self.cart_tree.column("unit_price", width=100, anchor="center")
        self.cart_tree.column("total", width=100, anchor="center")

        self.cart_tree.pack(fill="both", expand=True, padx=10, pady=10)

        action_frame = ttk.Frame(self)
        action_frame.pack(fill="x", padx=10, pady=10)

        ttk.Button(action_frame, text="Remove Selected", command=self._remove_selected).pack(side="left")
        ttk.Button(action_frame, text="Complete Purchase", command=self._complete_purchase).pack(side="right")

    def _add_to_cart(self) -> None:
        try:
            product_id = int(self.product_id_var.get())
            quantity = int(self.quantity_var.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Product ID and Quantity must be numeric.")
            return

        if product_id not in self.inventory:
            messagebox.showerror("Invalid Product", "Selected product ID does not exist.")
            return

        if quantity <= 0:
            messagebox.showerror("Invalid Quantity", "Quantity must be greater than zero.")
            return

        price_str = self.inventory[product_id][2]
        unit_price = _parse_price_to_int(price_str)
        total_price = unit_price * quantity

        existing_item = next((item for item in self.cart if item["id"] == product_id), None)
        if existing_item:
            existing_item["quantity"] += quantity
            existing_item["total_price"] += total_price
        else:
            self.cart.append(
                {
                    "id": product_id,
                    "name": self.inventory[product_id][0],
                    "unit_price_str": price_str,
                    "unit_price": unit_price,
                    "quantity": quantity,
                    "total_price": total_price,
                    "graphics": self.inventory[product_id][5],
                }
            )

        self._refresh_cart_view()
        self.product_id_var.set("")
        self.quantity_var.set("")

    def _remove_selected(self) -> None:
        selected_item = self.cart_tree.selection()
        if not selected_item:
            return

        cart_index = int(selected_item[0])
        if 0 <= cart_index < len(self.cart):
            del self.cart[cart_index]
            self._refresh_cart_view()

    def _refresh_cart_view(self) -> None:
        for item in self.cart_tree.get_children():
            self.cart_tree.delete(item)

        for index, cart_item in enumerate(self.cart):
            self.cart_tree.insert(
                "",
                "end",
                iid=str(index),
                values=(
                    cart_item["id"],
                    cart_item["name"],
                    cart_item["quantity"],
                    cart_item["unit_price_str"],
                    cart_item["total_price"],
                ),
            )

    def _complete_purchase(self) -> None:
        if not self.cart:
            messagebox.showwarning("Empty Cart", "Please add at least one product before completing the purchase.")
            return

        vendor_name = self.vendor_name_var.get().strip()
        vendor_contact = self.vendor_contact_var.get().strip()

        if not vendor_name or not vendor_contact:
            messagebox.showerror("Missing Information", "Vendor name and contact number are required.")
            return

        stock_data = File_Read()
        for cart_item in self.cart:
            Update_Stock_Purchase(stock_data, cart_item["id"], cart_item["quantity"])

        laptop_purchased = [
            [
                cart_item["name"],
                cart_item["quantity"],
                cart_item["unit_price_str"],
                cart_item["total_price"],
                cart_item["graphics"],
            ]
            for cart_item in self.cart
        ]

        total = sum(item["total_price"] for item in self.cart)
        shipping_cost = 12
        grand_total = total + shipping_cost
        date_time = datetime.now()
        date_parts = str(date_time).split(" ")

        Print_Purchase_Bill(vendor_name, vendor_contact, date_time, laptop_purchased, total, shipping_cost, grand_total)
        Genarate_Purchase_Bill(
            vendor_name,
            date_parts,
            vendor_contact,
            date_time,
            laptop_purchased,
            total,
            shipping_cost,
            grand_total,
        )

        messagebox.showinfo("Purchase Completed", f"Purchase recorded successfully. Grand Total: ${grand_total:.2f}")
        self.on_complete()
        self.destroy()


class InventoryApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Desktop Care Inventory Manager")
        self.geometry("880x480")
        self.resizable(False, False)

        self.stock_tree = ttk.Treeview(
            self,
            columns=("name", "brand", "price", "quantity", "processor", "graphics"),
            show="headings",
        )

        self.stock_tree.heading("name", text="Product Name")
        self.stock_tree.heading("brand", text="Brand")
        self.stock_tree.heading("price", text="Price")
        self.stock_tree.heading("quantity", text="Quantity")
        self.stock_tree.heading("processor", text="Processor")
        self.stock_tree.heading("graphics", text="Graphics Card")

        self.stock_tree.column("name", width=150)
        self.stock_tree.column("brand", width=120)
        self.stock_tree.column("price", width=80, anchor="center")
        self.stock_tree.column("quantity", width=80, anchor="center")
        self.stock_tree.column("processor", width=150)
        self.stock_tree.column("graphics", width=150)

        self.stock_tree.pack(fill="both", expand=True, padx=10, pady=10)

        button_frame = ttk.Frame(self)
        button_frame.pack(fill="x", padx=10, pady=10)

        ttk.Button(button_frame, text="Sell Products", command=self.open_sell_window).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Purchase Products", command=self.open_purchase_window).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Refresh Stock", command=self.refresh_stock_view).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Open Invoices Folder", command=self.open_invoices_folder).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Exit", command=self.destroy).pack(side="right", padx=5)

        self.refresh_stock_view()

    def refresh_stock_view(self) -> None:
        for item in self.stock_tree.get_children():
            self.stock_tree.delete(item)

        stock_data = File_Read()
        for product_id, details in stock_data.items():
            name, brand, price, quantity, processor, graphics = details
            self.stock_tree.insert(
                "",
                "end",
                iid=str(product_id),
                values=(name, brand, price, quantity, processor, graphics),
            )

    def open_sell_window(self) -> None:
        SellWindow(self, self.refresh_stock_view)

    def open_purchase_window(self) -> None:
        PurchaseWindow(self, self.refresh_stock_view)

    def open_invoices_folder(self) -> None:
        invoice_path = INVOICE_DIR
        if not invoice_path.exists() or not any(invoice_path.iterdir()):
            messagebox.showinfo("Invoices Folder", "No invoices have been generated yet.")
            return

        try:
            if sys.platform.startswith("win"):
                os.startfile(invoice_path)  # type: ignore[attr-defined]
            elif sys.platform == "darwin":
                os.spawnlp(os.P_NOWAIT, "open", "open", str(invoice_path))
            else:
                os.spawnlp(os.P_NOWAIT, "xdg-open", "xdg-open", str(invoice_path))
        except Exception as exc:
            messagebox.showerror("Error", f"Unable to open folder: {exc}")

    def run(self) -> None:
        self.mainloop()

