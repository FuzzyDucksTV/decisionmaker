// src/components/common/CustomButton.js
import React from 'react';

const CustomButton = ({ text, onClick, className }) => {
  return (
    <button className={`custom-button ${className}`} onClick={onClick}>
      {text}
    </button>
  );
};

export default CustomButton;