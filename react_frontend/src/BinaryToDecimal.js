import React, { useState, useEffect } from 'react';
import axios from 'axios';  // Library for making HTTP requests

function BinaryToDecimal() {
  // React State Hooks to manage component's dynamic data
  // State variables track:
  // 1. Current conversion problem
  // 2. User's input guess
  // 3. Feedback message after answer submission
  const [problem, setProblem] = useState(null);
  const [userGuess, setUserGuess] = useState('');
  const [feedback, setFeedback] = useState('');

  // useEffect Hook: Run when component first loads
  // Generates first problem automatically
  useEffect(() => {
    generateProblem();
  }, []); // Empty dependency array means "run only once on initial render"

  // Async function to fetch a new conversion problem from backend
  const generateProblem = async () => {
    try {
      // Make GET request to Flask backend
      const response = await axios.get('http://localhost:5000/bin-to-dec');
      
      // Update component's state with new problem
      setProblem(response.data);
      
      // Reset user input and feedback for new problem
      setUserGuess('');
      setFeedback('');
    } catch (error) {
      console.error('Error generating problem', error);
    }
  };

  // Handle user's answer submission
  const handleSubmit = async (e) => {
    e.preventDefault();  // Prevent default form submission behavior
    
    try {
      // Send POST request to check answer
      const response = await axios.post('http://localhost:5000/check-answer', {
        userGuess,
        correctDecimal: problem.random_decimal,
        randomBinary: problem.random_binary
      });

      // Set feedback based on correctness of answer
      setFeedback(response.data.result === 'Correct' 
        ? 'Correct! Well done!' 
        : `Incorrect. The correct decimal is ${response.data.correctDecimal}`
      );
    } catch (error) {
      console.error('Error checking answer', error);
    }
  };

  // Display bit representation of binary number
  const displayBitRepresentation = () => {
    // Decimal values for each binary place (2^7 to 2^0)
    const bitValues = [128, 64, 32, 16, 8, 4, 2, 1];
    
    return (
      <table>
        <thead>
          <tr>
            {/* Display place values */}
            <th>Power of 2</th>
            {bitValues.map(val => <th key={val}>{val}</th>)}
          </tr>
          <tr>
            {/* Display binary digits */}
            <td>Binary</td>
            {problem.random_binary.split('').map((bit, index) => (
              <td key={index}>{bit}</td>
            ))}
          </tr>
        </thead>
      </table>
    );
  };

  // Render the component's UI
  return (
    <div>
      <h2>Binary to Decimal Conversion</h2>
      {problem && (  // Only render if problem is loaded
        <>
          <p>Binary Number: {problem.random_binary}</p>
          {displayBitRepresentation()}
          
          {/* Form for user to input guess */}
          <form onSubmit={handleSubmit}>
            <input 
              type="number" 
              value={userGuess}
              onChange={(e) => setUserGuess(e.target.value)}
              placeholder="Enter decimal value"
              min="0"
              max="255"
              required
            />
            <button type="submit">Check Answer</button>
          </form>
          
          {/* Display feedback after submission */}
          {feedback && <p>{feedback}</p>}
          
          {/* Button to generate new problem */}
          <button onClick={generateProblem}>Generate New Problem</button>
        </>
      )}
    </div>
  );
}

export default BinaryToDecimal;