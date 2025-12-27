import sys
import csv
from reader.reader import ColumnarFileReader

def main():
    if len(sys.argv) != 3:
        print("Usage: python custom_to_csv.py <input_file> <output_csv>")
        return

    input_file = sys.argv[1]
    output_csv = sys.argv[2]

    reader = ColumnarFileReader(input_file)
    rows = reader.read_all()
    if not rows:
        print("No data found.")
        return

    with open(output_csv, "w", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print(f"CSV file '{output_csv}' written successfully.")

if __name__ == "__main__":
    main()
