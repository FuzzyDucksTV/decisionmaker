import React, { useState } from 'react';
import CategorySelection from './components/CategorySelection';
import OptionCard from './components/common/OptionCard';
import DecisionButton from './components/DecisionButton';

const App = () => {
  const [selectedCategory, setSelectedCategory] = useState(null);
  const [selectedOptions, setSelectedOptions] = useState([]);

  const categories = ['Movies', 'Food', 'Travel'];

  const options = [
    { title: 'Option 1', description: 'Description for option 1' },
    { title: 'Option 2', description: 'Description for option 2' },
    // ... more options
  ];

  const handleCategorySelect = (category) => {
    setSelectedCategory(category);
  };

  const handleOptionSelect = (option) => {
    setSelectedOptions([...selectedOptions, option]);
  };

  const handleDecision = () => {
    // Logic to make a decision based on selected options
  };

  return (
    <div className="app">
      <CategorySelection
        categories={categories}
        onCategorySelect={handleCategorySelect}
      />

      {selectedCategory && (
        <div className="options">
          {options.map((option, index) => (
            <OptionCard key={index} option={option} onOptionSelect={handleOptionSelect} />
          ))}
        </div>
      )}

      {selectedOptions.length > 0 && <DecisionButton onClick={handleDecision} />}
    </div>
  );
};

export default App;
