from pathlib import Path
from typing import Dict, List

BASE_DIR = Path(__file__).resolve().parent
STOCK_FILE = BASE_DIR / "stock.txt"
INVOICE_DIR = BASE_DIR / "invoices"
INVOICE_DIR.mkdir(exist_ok=True)


def _sanitize_filename(value: str) -> str:
    allowed = (" ", "-", "_")
    sanitized = "".join(char if char.isalnum() or char in allowed else "_" for char in value.strip())
    return sanitized or "invoice"


def _write_stock_file(inventory: Dict[int, List]) -> None:
    with STOCK_FILE.open("w", encoding="utf-8") as file:
        for values in inventory.values():
            file.write(
                f"{values[0]},{values[1]},{values[2]},{values[3]},{values[4]},{values[5]}\n"
            )


def Update_Stock_Purchase(RF,Purchase_ID,Customer_Quantity):
    RF[Purchase_ID][3] = int(RF[Purchase_ID][3]) + int(Customer_Quantity)
    _write_stock_file(RF)


def Update_Stock_Sales(RF,Purchase_ID,Customer_Quantity):
    RF[Purchase_ID][3] = int(RF[Purchase_ID][3]) - int(Customer_Quantity)
    _write_stock_file(RF)


def Print_Sales_Bill(Name, Contact_Number, Date_Time, Laptop_Sold, Total, Shipping_Cost, Grand_Total,vat):
            print("\n")
            print("\t \t \t \t \t \t \t DESKTOP CARE")
            print("\t \t \t \t \t \t \t --------------" )
            print("\t \t \t \t \t Birgunj , Parsa | Phone no: +977 9803270700")
            print("\n")
            print("Customer's Name: "+ str(Name))
            print("Contact number: "+ str(Contact_Number))
            print("Purchase Date and Time: "+ str(Date_Time))
            print("\n")
            print("Product Name \t \t Total Quantity \t\t Price(per piece) \t\t\t Total")
            for i in Laptop_Sold:
                print(i[0], "\t\t\t" ,i[1], "\t\t\t " ,i[2], "\t\t\t " ,"$", i[3] )
                print("\n")
            print("Total Amount is: $"+str (Total))
            print("Shipping charge is: $", Shipping_Cost)
            print("Grand Total with 13% VAT: $"+ str(Grand_Total))
            print("\n")

def Generate_Sales_Bill(Name,D,Contact_Number,Date_Time,Laptop_Sold,Total,Shipping_Cost, Grand_Total,vat):
        filename = f"{_sanitize_filename(Name)}_{Date_Time.strftime('%Y%m%d_%H%M%S')}_sale.txt"
        file_path = INVOICE_DIR / filename
        with file_path.open("w", encoding="utf-8") as File:
            File.write("\n")
            File.write("\t \t \t \t \t \t \t DESKTOP CARE")
            File.write("\t \t \t \t \t \t \t --------------" )
            File.write("\t \t \t \t \t Birgunj, Parsa | Phone no: +977 9803270700")
            File.write("\n" )
            File.write("\nCustomer's Name: " + str(Name))
            File.write("\nContact Number: " + str(Contact_Number))
            File.write("\nPurchase Date and Time: " + str(Date_Time))
            File.write("\n" )
            File.write("\n************************************************************************************************************************\n" )
            File.write("Product Name \t  Total Quantity \t Price(per piece) \tTotal")
            File.write("\n************************************************************************************************************************ \n" )
            for i in Laptop_Sold:
                File.write(str(i[0])+" \t \t "+str(i[1])+" \t\t "+str(i[2])+" \t\t\t "+"$"+str(i[3]) +"\n")
                File.write("\n")
            File.write("\nTotal Amount is : $" + str(Total))
            File.write("\nShipping charge is : $ " +""+ str(Shipping_Cost) +"\n")
            File.write("Grand Total with 13% VAT: $"+ str(Grand_Total))
            File.write("\n")

def Print_Purchase_Bill(Name, Contact_Number, Date_Time, Laptop_Sold, Total, Shipping_Cost, Grand_Total):
        print("\n")
        print("\t \t \t \t \t \t \t DESKTOP CARE")
        print("\t \t \t \t \t \t \t --------------" )
        print("\t \t \t \t \t Birgunj , Parsa | Phone no: +977 9834678210")
        print("\n")
        print("Customer's Name: "+ str(Name))
        print("Contact number: "+ str(Contact_Number))
        print("Purchase Date and Time: "+ str(Date_Time))
        print("\n")
        print("Product Name \t \t Total Quantity \t\t Price(per piece) \t\t\t Total")

        for i in Laptop_Sold:
            print(i[0], " \t \t " ,i[1], "\t\t " ,i[2], " \t\t\t  " ,"$", i[3] )
            print("\n")
        print("Total Amount is: $"+str (Total))
        print("Shipping charge is: $", Shipping_Cost)
        print("Grand Total: $"+ str(Grand_Total))
        print("\n")

def Genarate_Purchase_Bill(Name,D, Contact_Number, Date_Time, Laptop_Sold, Total, Shipping_Cost, Grand_Total):
        filename = f"{_sanitize_filename(Name)}_{Date_Time.strftime('%Y%m%d_%H%M%S')}_purchase.txt"
        file_path = INVOICE_DIR / filename
        with file_path.open("w", encoding="utf-8") as File:
            File.write("\n")
            File.write("\t \t \t \t \t \t  DESKTOP CARE")
            File.write("\t \t \t \t \t \t --------------" )
            File.write("\t \t \t \t \t Birgunj, Parsa | Contact no: +977 9803273700")
            File.write("\n" )
            File.write("\nCustomer's Name: " + str(Name))
            File.write("\nContact number: " + str(Contact_Number))
            File.write("\nPurchase Date and Time: " + str(Date_Time))
            File.write("\n" )
            File.write("\n************************************************************************************************************************\n" )
            File.write("Product Name \t \t Total Quantity \t\t Price(per piece) \t\t\t Total")
            File.write("\n************************************************************************************************************************ \n" )

            for i in Laptop_Sold:
                File.write(str(i[0])+"\t \t "+str(i[1])+" \t\t "+str(i[2])+" \t\t\t "+"$"+str(i[3]) +"\n")
                File.write("\n")
            File.write("\nTotal Amount is: $" + str(Total))
            File.write("\nShipping charge is: $ " +""+ str(Shipping_Cost) +"\n")
            File.write("\nGrand Total: $" + str(Grand_Total))
