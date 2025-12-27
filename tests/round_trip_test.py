import csv
from writer.writer import write_custom_file
from reader.reader import ColumnarFileReader

def read_csv_as_list(csv_path):
    with open(csv_path, newline='') as f:
        reader = csv.DictReader(f)
        return list(reader)

def compare_csv_to_custom(input_csv, custom_file):
    # Write custom file
    write_custom_file(input_csv, custom_file)

    # Read custom file back
    reader = ColumnarFileReader(custom_file)
    rows_from_custom = reader.read_all()

    # Read original CSV
    rows_from_csv = read_csv_as_list(input_csv)

    # Compare rows
    if rows_from_csv == rows_from_custom:
        print("✅ Round-trip test PASSED: CSV -> custom -> CSV matches exactly")
    else:
        print("❌ Round-trip test FAILED: Data mismatch")
        print("Original CSV:", rows_from_csv)
        print("From custom file:", rows_from_custom)

if __name__ == "__main__":
    input_csv = "sample_data/sample.csv"
    custom_file = "data.colf"
    compare_csv_to_custom(input_csv, custom_file)
