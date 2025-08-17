/**
 * MultiSelect Component
 * 
 * A reusable multi-selection component with:
 * - Dropdown interface with search functionality
 * - Tag-based display of selected items
 * - Custom option addition capability
 * - Mobile-friendly design
 */

import React, { useState, useRef, useEffect } from 'react';

const MultiSelect = ({ 
  options = [], 
  selectedItems = [], 
  onChange,
  placeholder = "Select items...",
  label,
  allowCustom = true,
  maxItems,
  className = '',
  error
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [customInput, setCustomInput] = useState('');
  const [showCustomInput, setShowCustomInput] = useState(false);
  const dropdownRef = useRef(null);
  const inputRef = useRef(null);

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setIsOpen(false);
        setShowCustomInput(false);
        setSearchTerm('');
        setCustomInput('');
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  // Filter options based on search term
  const filteredOptions = options.filter(option =>
    option.toLowerCase().includes(searchTerm.toLowerCase()) &&
    !selectedItems.includes(option)
  );

  // Handle option selection
  const handleOptionSelect = (option) => {
    if (maxItems && selectedItems.length >= maxItems) {
      return;
    }

    const newSelected = [...selectedItems, option];
    onChange(newSelected);
    setSearchTerm('');
  };

  // Handle removing selected item
  const handleRemoveItem = (itemToRemove) => {
    const newSelected = selectedItems.filter(item => item !== itemToRemove);
    onChange(newSelected);
  };

  // Handle adding custom option
  const handleAddCustom = () => {
    if (!customInput.trim()) return;

    const newOption = customInput.trim();
    if (!selectedItems.includes(newOption)) {
      handleOptionSelect(newOption);
    }
    setCustomInput('');
    setShowCustomInput(false);
  };

  // Handle search input change
  const handleSearchChange = (e) => {
    setSearchTerm(e.target.value);
    setShowCustomInput(false);
  };

  // Handle key events
  const handleKeyDown = (e) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      if (showCustomInput) {
        handleAddCustom();
      } else if (filteredOptions.length > 0) {
        handleOptionSelect(filteredOptions[0]);
      }
    } else if (e.key === 'Escape') {
      setIsOpen(false);
      setShowCustomInput(false);
      setSearchTerm('');
      setCustomInput('');
    }
  };

  return (
    <div className={`relative ${className}`} ref={dropdownRef}>
      {label && (
        <label className="block text-[#1c180d] text-base font-medium leading-normal pb-2">
          {label}
        </label>
      )}
      
      {/* Selected items display */}
      {selectedItems.length > 0 && (
        <div className="flex flex-wrap gap-2 mb-2">
          {selectedItems.map((item, index) => (
            <span
              key={index}
              className="inline-flex items-center gap-1 bg-[#fac638] text-[#1c180d] text-sm px-2 py-1 rounded-lg"
            >
              {item}
              <button
                type="button"
                onClick={() => handleRemoveItem(item)}
                className="ml-1 text-[#1c180d] hover:text-red-600 focus:outline-none bg-transparent"
              >
                ×
              </button>
            </span>
          ))}
        </div>
      )}

      {/* Main input area */}
      <div 
        className={`relative w-full min-h-[56px] bg-[#f4f0e6] rounded-xl border-2 cursor-pointer transition-colors ${
          isOpen ? 'border-[#fac638]' : 'border-transparent'
        } ${error ? 'border-red-300' : ''}`}
        onClick={() => setIsOpen(true)}
      >
        <div className="flex items-center p-4">
          <input
            ref={inputRef}
            type="text"
            value={searchTerm}
            onChange={handleSearchChange}
            onKeyDown={handleKeyDown}
            placeholder={selectedItems.length > 0 ? "Search or add more..." : placeholder}
            className="flex-1 bg-transparent text-[#1c180d] placeholder:text-[#9e8747] focus:outline-none text-base"
            onFocus={() => setIsOpen(true)}
          />
          <svg 
            className={`w-5 h-5 text-[#9e8747] transition-transform ${isOpen ? 'rotate-180' : ''}`}
            fill="none" 
            stroke="currentColor" 
            viewBox="0 0 24 24"
          >
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
          </svg>
        </div>

        {/* Dropdown menu */}
        {isOpen && (
          <div className="absolute top-full left-0 right-0 mt-1 bg-white border border-[#e9e2ce] rounded-xl shadow-lg z-50 max-h-64 overflow-y-auto" style={{backgroundColor: '#ffffff'}}>
            {/* Search results */}
            {filteredOptions.length > 0 && (
              <div className="p-2">
                <div className="text-xs text-[#9e8747] px-2 py-1 uppercase tracking-wider">
                  Suggestions
                </div>
                {filteredOptions.map((option, index) => (
                  <button
                    key={index}
                    type="button"
                    onClick={() => handleOptionSelect(option)}
                    className="w-full text-left px-3 py-2 hover:bg-[#f4f0e6] rounded-lg text-[#1c180d] transition-colors"
                    style={{backgroundColor: 'transparent', color: '#1c180d'}}
                    disabled={maxItems && selectedItems.length >= maxItems}
                  >
                    {option}
                  </button>
                ))}
              </div>
            )}

            {/* Custom input section */}
            {allowCustom && (
              <div className="border-t border-[#e9e2ce] p-2">
                {!showCustomInput ? (
                  <button
                    type="button"
                    onClick={() => setShowCustomInput(true)}
                    className="w-full text-left px-3 py-2 text-[#fac638] hover:bg-[#f4f0e6] rounded-lg transition-colors"
                    style={{backgroundColor: 'transparent', color: '#fac638'}}
                    disabled={maxItems && selectedItems.length >= maxItems}
                  >
                    + Add custom option
                  </button>
                ) : (
                  <div className="flex gap-2">
                    <input
                      type="text"
                      value={customInput}
                      onChange={(e) => setCustomInput(e.target.value)}
                      onKeyDown={(e) => {
                        if (e.key === 'Enter') {
                          e.preventDefault();
                          handleAddCustom();
                        }
                      }}
                      placeholder="Enter custom option..."
                      className="flex-1 px-3 py-2 bg-white border border-[#e9e2ce] rounded-lg focus:outline-none focus:border-[#fac638] text-sm text-[#1c180d] placeholder:text-[#9e8747]"
                      style={{backgroundColor: '#ffffff', color: '#1c180d'}}
                      autoFocus
                    />
                    <button
                      type="button"
                      onClick={handleAddCustom}
                      className="px-3 py-2 bg-[#fac638] text-[#1c180d] rounded-lg hover:bg-[#e9b429] transition-colors text-sm font-medium"
                    >
                      Add
                    </button>
                  </div>
                )}
              </div>
            )}

            {/* No options message */}
            {filteredOptions.length === 0 && searchTerm && !showCustomInput && (
              <div className="p-4 text-center text-[#9e8747] text-sm">
                No matching options found
                {allowCustom && (
                  <div className="mt-2">
                    <button
                      type="button"
                      onClick={() => setShowCustomInput(true)}
                      className="text-[#fac638] hover:underline"
                    >
                      Add "{searchTerm}" as custom option
                    </button>
                  </div>
                )}
              </div>
            )}

            {/* Max items warning */}
            {maxItems && selectedItems.length >= maxItems && (
              <div className="p-3 bg-yellow-50 border-t border-[#e9e2ce] text-xs text-yellow-800">
                Maximum {maxItems} items selected
              </div>
            )}
          </div>
        )}
      </div>

      {/* Error message */}
      {error && (
        <p className="mt-1 text-sm text-red-600">{error}</p>
      )}

      {/* Help text */}
      {maxItems && (
        <p className="mt-1 text-xs text-[#9e8747]">
          {selectedItems.length}/{maxItems} items selected
        </p>
      )}
    </div>
  );
};

export default MultiSelect;