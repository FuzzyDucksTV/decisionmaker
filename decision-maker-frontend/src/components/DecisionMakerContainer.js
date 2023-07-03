
import React, { useState, useEffect } from 'react';
import DecisionOptionsDisplay from './DecisionOptionsDisplay';
import './DecisionMakerContainer.css';

const DecisionMakerContainer = () => {
  const [options, setOptions] = useState([]);
  const [selectedOption, setSelectedOption] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchOptions = async () => {
      // Simulating an API call
      setTimeout(() => {
        const aiGeneratedOptions = [
          { title: 'Option 1', description: 'Description for option 1' },
          { title: 'Option 2', description: 'Description for option 2' },
        ];
        setOptions(aiGeneratedOptions);
        setLoading(false);
      }, 1000);
    };
    fetchOptions();
  }, []);

  const handleSelectOption = (option) => {
    setSelectedOption(option);
  };

  return (
    <div className="decision-maker-container">
      {loading ? (
        <div className="loading">Loading...</div>
      ) : (
        <>
          <DecisionOptionsDisplay options={options} onSelectOption={handleSelectOption} />
          {selectedOption && (
            <div className="selected-option">
              <h2>Selected Option</h2>
              <p>{selectedOption.title}</p>
              <p>{selectedOption.description}</p>
            </div>
          )}
        </>
      )}
    </div>
  );
};

export default DecisionMakerContainer;
