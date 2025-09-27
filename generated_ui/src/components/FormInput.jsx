import React from 'react';
// Assuming FormInput component is implemented
const FormInput = ({ type, name, placeholder }) => {
  return (
    <input type={type} name={name} placeholder={placeholder} className="w-full px-4 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500" />
  );
};

export default FormInput;