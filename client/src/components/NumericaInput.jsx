import React from "react";

const NumericInput = ({
  label,
  value,
  onChange,
  placeholder,
  required = true,
}) => {
  return (
    <div className="flex flex-col gap-1.5">
      {label && <label className="text-sm text-gray-600">{label}</label>}
      <input
        type="number"
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        required={required}
        min="0"
        step="any"
        className="w-full px-3 py-2 bg-white border border-gray-200 rounded-md
                   text-sm text-gray-800
                   focus:outline-none focus:border-gray-400
                   placeholder:text-gray-300"
      />
    </div>
  );
};

export default NumericInput;
