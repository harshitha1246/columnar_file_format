import struct
import zlib

# Constants (must match writer.py)
TYPE_INT = 1
TYPE_FLOAT = 2
TYPE_STRING = 3
MAGIC = b"COLF"
VERSION = 1


class ColumnarFileReader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.num_rows = 0
        self.num_columns = 0
        self.schema = []  # list of (name, type)
        self.metadata = []  # list of (offset, compressed_size, uncompressed_size)
        self._parse_header()

    def _parse_header(self):
        with open(self.file_path, "rb") as f:
            magic = f.read(4)
            if magic != MAGIC:
                raise ValueError("Not a valid custom columnar file")

            version = struct.unpack("<B", f.read(1))[0]
            if version != VERSION:
                raise ValueError("Unsupported file version")

            self.num_columns = struct.unpack("<i", f.read(4))[0]
            self.num_rows = struct.unpack("<i", f.read(4))[0]

            # Read schema
            self.schema = []
            for _ in range(self.num_columns):
                name_len = struct.unpack("<B", f.read(1))[0]
                name = f.read(name_len).decode("utf-8")
                dtype = struct.unpack("<B", f.read(1))[0]
                self.schema.append((name, dtype))

            # Read metadata
            self.metadata = []
            for _ in range(self.num_columns):
                offset, csize, usize = struct.unpack("<qii", f.read(16))
                self.metadata.append((offset, csize, usize))

    def read_all(self):
        """Read entire file and return as list of dicts (rows)"""
        data = {name: self._read_column(i) for i, (name, _) in enumerate(self.schema)}
        rows = []
        for i in range(self.num_rows):
            row = {name: data[name][i] for name in data}
            rows.append(row)
        return rows

    def read_columns(self, column_names):
        """Read only specified columns"""
        indices = [i for i, (name, _) in enumerate(self.schema) if name in column_names]
        data = {}
        for i in indices:
            name, _ = self.schema[i]
            data[name] = self._read_column(i)
        rows = []
        for i in range(self.num_rows):
            row = {name: data[name][i] for name in data}
            rows.append(row)
        return rows

    def _read_column(self, index):
        name, dtype = self.schema[index]
        offset, csize, usize = self.metadata[index]
        with open(self.file_path, "rb") as f:
            f.seek(offset)
            compressed = f.read(csize)
            raw = zlib.decompress(compressed)

            result = []
            if dtype == TYPE_INT:
                for i in range(0, usize, 4):
                    result.append(struct.unpack("<i", raw[i:i+4])[0])
            elif dtype == TYPE_FLOAT:
                for i in range(0, usize, 8):
                    result.append(struct.unpack("<d", raw[i:i+8])[0])
            else:  # string
                # First part is offsets array
                offsets = []
                for i in range(0, 4*self.num_rows, 4):
                    offsets.append(struct.unpack("<i", raw[i:i+4])[0])
                strings_data = raw[4*self.num_rows:]
                for i in range(self.num_rows):
                    start = offsets[i]
                    end = offsets[i+1] if i+1 < self.num_rows else len(strings_data)
                    s = strings_data[start:end].decode("utf-8")
                    result.append(s)
            return result


# Example usage
if __name__ == "__main__":
    reader = ColumnarFileReader("data.colf")
    all_rows = reader.read_all()
    print("All rows:", all_rows)

    selected_rows = reader.read_columns(["name", "score"])
    print("Selected columns:", selected_rows)
