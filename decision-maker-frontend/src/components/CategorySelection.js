import React from 'react';

const CategorySelection = ({ categories, onCategorySelect }) => {
  return (
    <div>
      <h2>Select a Category:</h2>
      <ul>
        {categories.map((category, index) => (
          <li key={index} onClick={() => onCategorySelect(category)}>
            {category}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default CategorySelection;
