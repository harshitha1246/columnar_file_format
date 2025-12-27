import csv
import struct
import zlib

# Constants
MAGIC = b"COLF"      # 4-byte magic number
VERSION = 1           # format version

# Data types
TYPE_INT = 1
TYPE_FLOAT = 2
TYPE_STRING = 3


def infer_type(value):
    """
    Infer the data type of a column from the first value.
    Returns TYPE_INT, TYPE_FLOAT, or TYPE_STRING
    """
    try:
        int(value)
        return TYPE_INT
    except:
        try:
            float(value)
            return TYPE_FLOAT
        except:
            return TYPE_STRING


def write_custom_file(csv_path, output_path):
    """
    Convert a CSV file into custom columnar format.
    """
    # 1. Read CSV
    with open(csv_path, newline='') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    column_names = reader.fieldnames
    num_rows = len(rows)
    num_columns = len(column_names)

    # 2. Extract columns
    columns = {name: [] for name in column_names}
    for row in rows:
        for name in column_names:
            columns[name].append(row[name])

    # 3. Infer column types
    column_types = {}
    for name in column_names:
        column_types[name] = infer_type(columns[name][0])

    # 4. Encode and compress columns
    column_blocks = []
    for name in column_names:
        raw = b""

        if column_types[name] == TYPE_INT:
            for v in columns[name]:
                raw += struct.pack("<i", int(v))

        elif column_types[name] == TYPE_FLOAT:
            for v in columns[name]:
                raw += struct.pack("<d", float(v))

        else:  # STRING
            offsets = []
            data = b""
            pos = 0
            for v in columns[name]:
                offsets.append(pos)
                encoded = v.encode("utf-8")
                data += encoded
                pos += len(encoded)

            # Store offsets first
            for off in offsets:
                raw += struct.pack("<i", off)
            # Then concatenated string data
            raw += data

        # Compress column
        compressed = zlib.compress(raw)

        column_blocks.append({
            "name": name,
            "type": column_types[name],
            "compressed": compressed,
            "compressed_size": len(compressed),
            "uncompressed_size": len(raw),
        })

    # 5. Write file
    with open(output_path, "wb") as f:
        # Header: Magic, Version, #columns, #rows
        f.write(MAGIC)
        f.write(struct.pack("<B", VERSION))
        f.write(struct.pack("<i", num_columns))
        f.write(struct.pack("<i", num_rows))

        # Schema
        for block in column_blocks:
            name_bytes = block["name"].encode("utf-8")
            f.write(struct.pack("<B", len(name_bytes)))
            f.write(name_bytes)
            f.write(struct.pack("<B", block["type"]))

        # Placeholder for metadata (offset, compressed size, uncompressed size)
        metadata_pos = f.tell()
        for _ in column_blocks:
            f.write(struct.pack("<qii", 0, 0, 0))

        # Write column data and record offsets
        offsets = []
        for block in column_blocks:
            offset = f.tell()
            f.write(block["compressed"])
            offsets.append(offset)

        # Go back and write metadata
        f.seek(metadata_pos)
        for i, block in enumerate(column_blocks):
            f.write(struct.pack(
                "<qii",
                offsets[i],
                block["compressed_size"],
                block["uncompressed_size"]
            ))


# Example usage (for testing)
if __name__ == "__main__":
    write_custom_file("sample_data/sample.csv", "data.colf")
    print("Custom columnar file 'data.colf' written successfully.")
