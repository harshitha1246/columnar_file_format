# Simple Columnar File Format

## Overview
This project implements a simple custom columnar file format from scratch.
The format stores data column-by-column, enabling efficient analytical queries
through selective column reads.

## Features
- Columnar binary storage
- Support for int32, float64, and UTF-8 string data types
- Per-column compression using zlib
- Selective column reads using metadata offsets

## Project Structure
columnar_format/
├── SPEC.md
├── README.md
├── writer/
├── reader/
├── cli/
├── sample_data/
└── tests/


## Setup
This project uses only the Python standard library.
No external dependencies are required.

## Sample Data
A sample CSV file is provided in the `sample_data` directory.

## Usage
Command-line tools are provided to convert between CSV and the custom format.

