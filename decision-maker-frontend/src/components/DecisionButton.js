import React from 'react';

const DecisionButton = ({ onClick }) => {
  return (
    <button className="decision-button" onClick={onClick}>
      Make Decision
    </button>
  );
};

export default DecisionButton;
