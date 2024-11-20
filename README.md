# NetworkApp
A Python-based educational tool designed to help students practice and test their understanding of networking concepts. This program is part of a larger project that will eventually evolve into a web-based application.

# Current Features
The program currently implements two core functionalities:

Binary to Decimal Conversion Practice
- Displays bit position values representation
- Generates random binary numbers
- Tests user's ability to convert binary to decimal
- Provides visual feedback with byte representation
- Tracks user performance

Decimal to Binary Conversion Practice
- Generates random decimal numbers
- Tests user's ability to convert decimal to binary
- Provides immediate feedback
- Tracks user performance

# Requirements
- Python 3.x
- Pandas (for DataFrame operations)
- Random library (for number generation)
- Sqlite3

# Viewing csv files on VS Code / Github
install 'Edit csv' extension (extension to edit csv files with a table ui)

# Create a virtual environment (recommended)
python -m venv env
source env/bin/activate  

# Install required Python packages
pip install flask flask-cors pandas

# Run the Flask backend
python netQuizzer.py