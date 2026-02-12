from datetime import datetime
from Read import *
from Write import *



def Welcome_Message():
     print ("\n")
     print ("\n")
     print ("\n")
     print("***********************************************************************************************************************")
     print(" ----------------- Welcome to DESKTOP CARE -----------------")
     print("***********************************************************************************************************************")
     print ("\n")

def Sell_Products(RF):
        
        Condition = True
        Laptop_Sold = []
        More_Products = True
        print("To generate bill, please provide the details: ")
        print("\n")
        Name = input("Enter your Name: ")
        Contact_Number = input("Enter your phone number: ")
        print("\n")

        while More_Products== True:
            print("**************************************************************************************************************************************************************")
            print("S.N      Product Name             Brand             Price             Quantity             Processor             Graphics Card")
            print("**************************************************************************************************************************************************************")
            Generate_Table()
            print("**************************************************************************************************************************************************************" )
            print("\n")

            while Condition == True:
                try:
                    Purchase_ID = int(input("Enter the laptop ID: "))
                    
                # Valid ID
                    while Purchase_ID <= 0 or Purchase_ID > len(RF):
                        print("Please Enter The valid Laptop ID !")
                        print("\n")
                        Purchase_ID = int(input("Enter the laptop ID: "))
                    
                
                    Customer_Quantity = int(input("Enter the quantity of laptop: "))
                    print("\n")

                    # Valid Quantity
                    Quantity_Desired = RF[Purchase_ID][3]
                    if Customer_Quantity <= 0 or Customer_Quantity > int(Quantity_Desired):
                        print("Dear user, we are currently out of stock, Please choose another laptop")
                        print("\n")
                        continue
                    else:

                        print("\n")
                        Update_Stock_Sales(RF,Purchase_ID,Customer_Quantity) 
                        Condition= False
                except:
                     print("Please Do Not enter String Values")  

            #
            Product_Name = RF[Purchase_ID][0]
            Graphics_card = RF[Purchase_ID][5]
            Unit_Price = RF[Purchase_ID][2]
            Quantity_Selected = Customer_Quantity
            Price_Selected_Quantity = RF[Purchase_ID][2].replace("$", '')
            Total_Price = int(Price_Selected_Quantity) * int(Quantity_Selected)
            Laptop_Sold.append([Product_Name, Quantity_Selected, Unit_Price, Total_Price, Graphics_card])
            customer_request = input("Do you wish to continue (Y/N)?").upper()
            print("\n")
        
            if customer_request == "Y":
                More_Products = True
                Condition = True
            else:
                
                More_Products =False
                Shipping_Cost = 12
                
                Total = 0 
                
                for i in Laptop_Sold:
                    Total += int(i[3])
                vat=(Total*0.13)    
                Grand_Total = Total + Shipping_Cost +vat
                Date_Time = datetime.now()
                D = str(Date_Time).split(" ")
                X = "_".join(D)
                Z = X.replace(":","_")
                Print_Sales_Bill(Name, Contact_Number, Date_Time, Laptop_Sold, Total, Shipping_Cost, Grand_Total,vat)
                Generate_Sales_Bill(Name,D,Contact_Number,Date_Time,Laptop_Sold,Total,Shipping_Cost, Grand_Total,vat)

def Purchase_Products(RF):
        Laptop_Sold = []
        More_Products = True
        while More_Products== True:
            print("**************************************************************************************************************************************************************")
            print("S.N      Product Name             Brand             Price             Quantity             Processor             Graphics Card")
            print("**************************************************************************************************************************************************************")
            Generate_Table()
            print("**************************************************************************************************************************************************************" )
            print("\n")

            Purchase_ID = int(input("Enter the ID of laptop: "))

            # Valid ID
            while Purchase_ID <= 0 or Purchase_ID > len(RF):
                        print("Please Enter The valid Laptop ID !")
                        print("\n")
                        Purchase_ID = int(input("Enter the laptop ID: "))

            Name = "DESKTOP CARE"
            Contact_Number = "+977 9803270700"
            Customer_Quantity = int(input("Enter the quantity of laptop: "))
            print("\n")
            
            # Valid Quantity
            Quantity_Desired = RF[Purchase_ID][3]
            Update_Stock_Purchase(RF,Purchase_ID,Customer_Quantity)

            # 
            Product_Name = RF[Purchase_ID][0]
            Graphics_card = RF[Purchase_ID][5]
            Unit_Price = RF[Purchase_ID][2]
            Quantity_Selected = Customer_Quantity
            Price_Selected_Quantity = RF[Purchase_ID][2].replace("$", '')
            Total_Price = int(Price_Selected_Quantity) * int(Quantity_Selected)
            Laptop_Sold.append([Product_Name, Quantity_Selected, Unit_Price, Total_Price, Graphics_card])
            customer_request = input("Do you wish to Continue(Y/N)?").upper()
            
            print("\n")
        
            if customer_request == "Y":
                More_Products = True
            else:
                More_Products = False
                Shipping_Cost = 12
                Total = 0
                
                for i in Laptop_Sold:
                    Total += int(i[3])
                Grand_Total = Total + Shipping_Cost
                Date_Time = datetime.now()
                D = str(Date_Time).split(" ")
                X = "_".join(D)
                Z = X.replace(":","_")
                Print_Purchase_Bill(Name, Contact_Number, Date_Time, Laptop_Sold, Total, Shipping_Cost, Grand_Total)
                Genarate_Purchase_Bill(Name,D, Contact_Number, Date_Time, Laptop_Sold, Total, Shipping_Cost, Grand_Total)
