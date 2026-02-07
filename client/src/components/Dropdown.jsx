import React from "react";

const Dropdown = ({ label, options, value, onChange, required = true }) => {
  return (
    <div className="flex flex-col gap-1.5">
      {label && <label className="text-sm text-gray-600">{label}</label>}
      <select
        value={value}
        onChange={onChange}
        required={required}
        className="w-full px-3 py-2 bg-white border border-gray-200 rounded-md
                   text-sm text-gray-800
                   focus:outline-none focus:border-gray-400
                   cursor-pointer"
      >
        <option value="">Select...</option>
        {options.map((option, index) => (
          <option key={index} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>
    </div>
  );
};

export default Dropdown;
