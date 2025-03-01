# Smart Unit Converter

A beautiful and user-friendly unit converter built with Python and Streamlit. This application allows you to convert between various units across different categories including length, weight, temperature, volume, time, and speed.

## Features

-Multi-Language Support:
Supports English, Urdu, Spanish, French, and German.
Uses googletrans for dynamic translation.

-Unit Conversion:
Supports Length, Weight, Temperature, Time, and Volume.
Handles temperature conversions separately due to its unique formula.

-Conversion History:
Stores and displays the history of conversions in the session.

-Save as PDF:
Allows users to save the conversion result as a PDF using FPDF.

-Dark/Light Mode:
Users can toggle between dark and light themes.


## Installation

1. Clone this repository or download the files
2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

To run the unit converter, use the following command:
```bash
streamlit run app.py
```

The application will open in your default web browser.

## Usage

1. Select a conversion category from the sidebar
2. Enter the value you want to convert
3. Choose the source unit (convert from)
4. Choose the target unit (convert to)
5. Click the "Convert" button to see the result

## Dependencies

- Python 3.7+
- Streamlit
- Pint

## License

This project is open source and available under the MIT License. 