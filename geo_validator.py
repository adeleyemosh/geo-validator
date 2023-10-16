import pandas as pd
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
from geopy.geocoders import Nominatim
import tkinter as tk
from tkinter import filedialog
from datetime import datetime
import os

def batch_geocode(coordinates):
    geolocator = Nominatim(user_agent="geo_validator")
    locations = []
    for coord in coordinates:
        lat, lon = coord
        try:
            location = geolocator.reverse((lat, lon), exactly_one=True)
            locations.append('Valid' if location else 'Invalid')
        except (GeocoderTimedOut, GeocoderServiceError):
            locations.append('Invalid')
    return locations

def validate_coordinates(df):
    coordinates = list(zip(df['Latitude'].astype(float), df['Longitude'].astype(float)))
    df['Validation Status'] = batch_geocode(coordinates)
    return df

def main():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(filetypes=[("Data Files", "*.csv;*.xls;*.xlsx")])

    if file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
    elif file_path.endswith('.xlsx'):
        df = pd.read_excel(file_path)
    else:
        print("Unsupported file format. Please provide a CSV or XLSX file.")
        exit()

    # Validate the coordinates and add a validation status column
    df = validate_coordinates(df)

    # Define the output folder and generate a timestamp
    output_folder = 'output'
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    
    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    # Generate the output file path with the timestamp
    output_file_path = f'{output_folder}/validated_coordinates_{timestamp}.csv'
    
    # Save the updated DataFrame to the new CSV file
    df.to_csv(output_file_path, index=False)

    print(f"Validation completed. Results saved to {output_file_path}")

if __name__ == "__main__":
    main()
