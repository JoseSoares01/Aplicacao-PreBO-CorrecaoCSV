# PreBO CSV Correction Tool

This is a simple Python desktop application built using PySimpleGUI. It allows users to import a CSV file (pipe-delimited), extract specific columns, adjust some fields (like "referencia"), and export the result in CSV or XLS format.

## Features
- Selects predefined columns by Excel-like letter references
- Reformats "referencia" column (removes leading zeros and re-adds one)
- Outputs a new file with a timestamped filename
- GUI with clear instructions and user feedback

## How to Use
1. Select the input CSV file.
2. Choose the output folder.
3. Choose the desired export format.
4. Click "Corrigir" to process the file.

## Dependencies
See `requirements.txt`.

## License
MIT
