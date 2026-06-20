import urllib.request
import csv
import io

url = "https://docs.google.com/spreadsheets/d/1MACuk1o089VAgMR43F46SXQkUwjQmEy6yZ4UDBJC8xk/export?format=csv&gid=185905705"

try:
    response = urllib.request.urlopen(url)
    csv_data = response.read().decode('utf-8')
    
    with open("sheet_structure.txt", "w", encoding="utf-8") as f:
        reader = csv.reader(io.StringIO(csv_data))
        for i, row in enumerate(reader):
            f.write(f"Row {i}: {row}\n")
    print("Success: Written to sheet_structure.txt")
except Exception as e:
    print("Error:", e)
