"""
Prerequisites:
- Python 3.x
- Flask (pip install flask flask-cors pandas)

"""
from flask import Flask, request, jsonify
from flask_cors import CORS  # Allows cross-origin requests between frontend and backend
import random
import pandas as pd

# Create Flask application instance
app = Flask(__name__)
# Enable Cross-Origin Resource Sharing (CORS)
CORS(app)

def bin_to_dec_logic():
    """
    Generate a random binary to decimal conversion problem
    
    Process:
    1. Generate a random integer between 0-255
    2. Convert the integer to an 8-bit binary string
    
    Returns:
    - Dictionary with binary and decimal representations
    """
    # Generate random number between 0 and 255
    random_decimal = random.randint(0, 255)
    # Convert to 8-bit binary string (e.g., '01010010')
    random_binary = format(random_decimal, '08b')

    return {
        "random_binary": random_binary,
        "random_decimal": random_decimal
    }

@app.route('/bin-to-dec', methods=['GET'])
def generate_problem():
    """
    API Endpoint to generate a new binary conversion problem
    
    When frontend makes a GET request to this route:
    1. Generate a new problem
    2. Return problem details as JSON
    """
    problem = bin_to_dec_logic()
    return jsonify(problem)

@app.route('/check-answer', methods=['POST'])
def check_answer():
    """
    API Endpoint to validate user's answer
    
    Process:
    1. Receive user's guess and correct answer from frontend
    2. Compare user's guess with correct decimal
    3. Determine if answer is correct
    4. Save result to CSV for tracking
    5. Return result to frontend
    """
    # Get data sent from frontend
    data = request.json
    user_guess = data.get('userGuess')
    correct_decimal = data.get('correctDecimal')
    
    # Check if user's guess matches correct decimal
    result = "Correct" if int(user_guess) == correct_decimal else "Wrong"
    
    # Create a DataFrame to log the attempt
    guess_df = pd.DataFrame({
        "Random Binary": [data.get('randomBinary')],
        "Random Decimal": [correct_decimal],
        "User Guess": [user_guess],
        "Result": [result]
    })
    
    # Append result to CSV file (optional tracking)
    guess_df.to_csv("decimal_guess.csv", 
                    mode='a',  # Append mode 
                    header=not pd.io.common.file_exists("decimal_guess.csv"),  # Add header only if file doesn't exist
                    index=False)  
    
    # Send back result to frontend
    return jsonify({
        "result": result,
        "correctDecimal": correct_decimal
    })

if __name__ == '__main__':
    app.run(debug=True)  # Enables helpful error messages and auto-reload