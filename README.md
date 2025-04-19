# AMPA

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![PyQt5](https://img.shields.io/badge/PyQt5-%20v5.15.11-green.svg)](https://pypi.org/project/PyQt5/)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-%20v3.10.0-orange.svg)](https://matplotlib.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A PyQt5 application to calculate the parallactic angle and airmass based on various astronomical parameters.

## Features
- Calculate parallactic angle based on hour angles, declinations, and latitude.
- Calculate airmass based on hour angles, declinations, and latitude.
- Display results in a table format.
- Export table as a PNG or PDF.

## Requirements
- Python 3.8+
- PyQt5
- Matplotlib

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Icorebleidd/AMPA.git
   cd AMPA
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
Run the application with:
```bash
python AirMass.py
python ParallacticAngle.py
```

## Inputs
- **Hour Angles:** Comma-separated values in hours (e.g., `1.5 0 0, 3.0 0 0, 4.5 0 0`).
- **Declination:** Comma-separated values in degrees (e.g., `-30 0 0, 0 0 0, 30 0 0`).
- **Latitude:** Single value in degrees (e.g., `45 32 00`).

## Output
- A table displaying the computed parallactic angle or airmass values.
- Column headers: Computed values based on input hour angles or declinations.
- Row headers: Input values for declinations or hour angles.

## Exporting Data
You can save the table as a PNG or PDF file via the "Export Table" button.

## License
This project is licensed under the MIT License.

## Author
Leonardo Tozzo - [GitHub Profile](https://github.com/Icorebleidd)
