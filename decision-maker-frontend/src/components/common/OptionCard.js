import React, { useState, useEffect } from 'react';

const OptionCard = ({ category, onOptionSelect }) => {
  const [options, setOptions] = useState([]);

  useEffect(() => {
    // Fetch options from the backend
    fetch(`/api/recommendations?category=${category}`)
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => setOptions(data))
      .catch(error => console.error('Error fetching options:', error));
  }, [category]);
  return (
    <div className="option-card">
      <h3>Options for {category}</h3>
      <ul>
        {options.map((option, index) => (
          <li key={index} onClick={() => onOptionSelect(option)}>
            {option.title}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default OptionCard;