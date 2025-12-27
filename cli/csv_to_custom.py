import sys
from writer.writer import write_custom_file

def main():
    if len(sys.argv) != 3:
        print("Usage: python csv_to_custom.py <input_csv> <output_file>")
        return

    input_csv = sys.argv[1]
    output_file = sys.argv[2]

    write_custom_file(input_csv, output_file)
    print(f"Custom columnar file '{output_file}' written successfully.")

if __name__ == "__main__":
    main()
