# Simple Columnar File Format Specification

## 1. Overview
This document describes a simple custom columnar file format designed for analytical workloads.
The format stores data column-by-column instead of row-by-row, enabling efficient selective
column reads.

## 2. File Layout
The file is divided into two main sections:

1. Header
2. Column Data Blocks

All column data blocks are stored as contiguous compressed binary blocks.

## 3. Endianness
All multi-byte numeric values are stored in Little Endian format.

## 4. Header Structure
The header contains metadata required to read the file and locate each column.

Header fields:
- Magic Number (4 bytes): ASCII string "COLF"
- Version (1 byte): File format version
- Number of Columns (4 bytes): int32
- Number of Rows (4 bytes): int32

## 5. Supported Data Types
The format supports the following data types:
- int32
- float64
- UTF-8 encoded string

## 6. Compression
Each column is compressed independently using the zlib compression algorithm.

## 7. Schema Encoding
The schema defines the structure of the table and is stored in the header.
For each column, the following information is stored sequentially:

- Column Name Length (1 byte)
- Column Name (N bytes, UTF-8 encoded)
- Data Type (1 byte)

Data Type values:
- 1 = int32
- 2 = float64
- 3 = string

## 8. Column Metadata
After the schema, metadata for each column is stored.
This metadata enables efficient selective column reads.

For each column, the following fields are stored:

- Column Offset (8 bytes): Byte position in the file where the compressed column block starts
- Compressed Size (4 bytes): Size of the compressed column data in bytes
- Uncompressed Size (4 bytes): Size of the column data before compression

The reader uses the column offset to seek directly to the required column
without scanning the entire file.

## 9. Column Data Encoding

### 9.1 int32
Values are stored as a contiguous sequence of 4-byte signed integers.

### 9.2 float64
Values are stored as a contiguous sequence of 8-byte floating-point numbers.

### 9.3 string
String columns are stored using two components:
1. An array of int32 offsets indicating the start position of each string
2. A contiguous UTF-8 encoded string data buffer

This approach avoids scanning and allows efficient access to variable-length data.

## 10. Selective Column Reads
The reader first parses the header to obtain schema and column metadata.
To read specific columns, the reader seeks directly to the corresponding
column offsets and decompresses only the required column blocks.
