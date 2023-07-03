// src/components/HomePage.js 
// 
import React, { useCallback } from 'react';
import CustomButton from './common/CustomButton';

const HomePage = ({ categories, onSelectCategory }) => {
  const handleSelectCategory = useCallback(
    (category) => {
      onSelectCategory(category);
    },
    [onSelectCategory]
  );

  return (
    <div className="home-page">
      <h1>Select a Category</h1>
      <div className="categories">
        {categories.map((category) => (
          <CustomButton
            key={category}
            text={category}
            onClick={() => handleSelectCategory(category)}
          />
        ))}
      </div>
    </div>
  );
};

export default HomePage;