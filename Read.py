from pathlib import Path
from typing import Dict, List

BASE_DIR = Path(__file__).resolve().parent
STOCK_FILE = BASE_DIR / "stock.txt"


def File_Read() -> Dict[int, List]:
    laptop_dictionary: Dict[int, List] = {}
    with STOCK_FILE.open("r", encoding="utf-8") as stock_file:
        for index, line in enumerate(stock_file, start=1):
            cleaned_line = line.strip()
            if not cleaned_line:
                continue

            parts = [part.strip() for part in cleaned_line.split(",")]
            if len(parts) != 6:
                print(f"Skipping malformed line in stock file: {cleaned_line}")
                continue

            try:
                parts[3] = int(parts[3])
            except ValueError:
                print(f"Invalid quantity detected in stock file: {cleaned_line}")
                continue

            laptop_dictionary[index] = parts

    return laptop_dictionary


def Generate_Table() -> None:
    with STOCK_FILE.open("r", encoding="utf-8") as stock_file:
        print("ID  Product Name        Brand           Price    Quantity    Processor       Graphics Card")
        print("-------------------------------------------------------------------------------------------------")
        for index, line in enumerate(stock_file, start=1):
            parts = [part.strip() for part in line.strip().split(",")]
            if len(parts) != 6:
                continue
            name, brand, price, quantity, processor, graphics = parts
            print(f"{index:<3} {name:<18} {brand:<15} {price:<8} {quantity:<10} {processor:<15} {graphics}")