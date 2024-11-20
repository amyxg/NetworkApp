import React, { useState } from 'react';
import BinaryToDecimal from './BinaryToDecimal';

function App() {
  const [selectedOption, setSelectedOption] = useState(null);

  const networkOptions = [
    { id: 1, name: 'Binary to Decimal' },
    // Add other options from menu here
  ];

  const renderSelectedComponent = () => {
    switch(selectedOption) {
      case 1:
        return <BinaryToDecimal />;
      default:
        return (
          <div>
            <h2>Network Conversion Tools</h2>
            {networkOptions.map(option => (
              <button 
                key={option.id} 
                onClick={() => setSelectedOption(option.id)}
                style={{margin: '10px', padding: '10px'}}
              >
                {option.name}
              </button>
            ))}
          </div>
        );
    }
  };

  return (
    <div className="App">
      {renderSelectedComponent()}
      {selectedOption !== null && (
        <button 
          onClick={() => setSelectedOption(null)}
          style={{margin: '10px', padding: '10px'}}
        >
          Back to Main Menu
        </button>
      )}
    </div>
  );
}

export default App;