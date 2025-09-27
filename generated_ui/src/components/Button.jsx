import React from 'react';
// Assuming Button component is implemented
const Button = ({ children, onClick }) => {
  return (
    <button className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500" OnClick={OnClick}>
      {children}
    </button>
  );
};

export default Button;