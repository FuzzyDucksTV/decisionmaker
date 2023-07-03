// Context from Function c:\Users\water\source\repos\decision-maker-app\decision-maker-app\src\components\DecisionMakerContainer.js:DecisionMakerContainer.selectedOption
// const selectedOption = null;
import React from 'react';
import PropTypes from 'prop-types';
import './DecisionOptionsDisplay.css';

const DecisionOptionsDisplay = ({ options, onSelectOption }) => {
  if (!options || options.length === 0) {
    return <p className="no-options">No options available.</p>;
  }

  return (
    <div className="options-container">
      <h2>AI-Generated Options</h2>
      <ul className="options-list">
        {options.map((option, index) => (
          <li key={index} className="option-item">
            <button className="option-button" onClick={() => onSelectOption(option)}>
              {option.title}
            </button>
            <p className="option-description">{option.description}</p>
          </li>
        ))}
      </ul>
    </div>
  );
};

DecisionOptionsDisplay.propTypes = {
  options: PropTypes.arrayOf(
    PropTypes.shape({
      title: PropTypes.string.isRequired,
      description: PropTypes.string.isRequired,
    })
  ),
  onSelectOption: PropTypes.func.isRequired,
};

export default DecisionOptionsDisplay;
