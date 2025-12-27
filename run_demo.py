# run_demo.py
import os

print("Converting CSV -> Custom columnar format...")
os.system("python cli/csv_to_custom.py sample_data/sample.csv data.colf")

print("\nConverting Custom format -> CSV...")
os.system("python cli/custom_to_csv.py data.colf output.csv")

print("\nRunning round-trip test...")
os.system("python -m tests.round_trip_test")
