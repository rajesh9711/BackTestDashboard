import os
import pandas as pd
# Function to load data from a CSV file
def load_data(filename):
    file_path = os.path.join("uploaded_data", filename)
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    else:
        return None

def color_negative_red(value):
    s = str(value)  
    if not s.strip(): 
        return ""
    else:
        cleaned_value = ''.join(char for char in s if char.isdigit() or char == '-')
        cleaned_value = cleaned_value.strip("%")
        if cleaned_value:  
            value = float(cleaned_value) 
        else:
            value = 0 
        if value < 0:
            return "background-color: #e64940"  # Red color 
        # elif -1000 < value < -500:
        #     return "background-color: #f06c65"
        # elif -1500 < value < -1000:
        #     return "background-color: #a33833"
        # elif value < -1500:
        #     return "background-color: #61110d"
        # elif 0 < value < 10000:
        #     return "background-color: #bae8ba"
        # elif 10000 < value < 20000:
        #     return "background-color: #3ac23a"
        # elif 20000 < value < 30000:
        #     return "background-color: #1cb81c"
        # elif 30000 < value < 100000:
        #     return "background-color: #0c630c"
        elif value > 0:
            return "background-color: #77dd77"  # Green color 
        else:
            return "" 

def format_int_with_commas(value):
    if isinstance(value, str):
        value = value.strip("%")
        value = float(value)
        return f"{value:,}"
    else:
        return value
formats = [
        "%d/%m/%Y",
        "%Y-%m-%d %H:%M:%S",
        "%m/%d/%Y %H:%M",
        "%m/%d/%Y",
        "%d/%m/%Y",
        "%d/%m/%Y %H:%M",
        "%d-%m-%Y %H:%M",
        "%Y/%m/%d %H:%M",
        "%m/%d/%Y %H:%M",
        "%m/%d/%Y %H:%M:%S",
    ]

