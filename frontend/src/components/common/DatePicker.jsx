/**
 * DatePicker Component
 * 
 * A custom date picker with:
 * - Beautiful dropdown interface matching design system
 * - Month/Year selectors with navigation
 * - Cream/beige theme consistency
 * - Mobile-friendly design
 */

import React, { useState, useRef, useEffect } from 'react';

const DatePicker = ({ 
  value, 
  onChange, 
  placeholder = "Select date...",
  label,
  error,
  maxDate,
  minDate,
  className = ''
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const [currentMonth, setCurrentMonth] = useState(new Date().getMonth());
  const [currentYear, setCurrentYear] = useState(new Date().getFullYear());
  const dropdownRef = useRef(null);

  // Initialize current month/year based on value or current date
  useEffect(() => {
    if (value) {
      const date = new Date(value);
      setCurrentMonth(date.getMonth());
      setCurrentYear(date.getFullYear());
    }
  }, [value]);

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setIsOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  // Month names
  const months = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
  ];

  // Get days in month
  const getDaysInMonth = (month, year) => {
    return new Date(year, month + 1, 0).getDate();
  };

  // Get first day of month (0 = Sunday, 1 = Monday, etc.)
  const getFirstDayOfMonth = (month, year) => {
    return new Date(year, month, 1).getDay();
  };

  // Format date for display
  const formatDisplayDate = (dateString) => {
    if (!dateString) return '';
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  // Handle date selection
  const handleDateSelect = (day) => {
    const selectedDate = new Date(currentYear, currentMonth, day);
    const dateString = selectedDate.toISOString().split('T')[0]; // YYYY-MM-DD format
    
    // Check if date is within allowed range
    if (maxDate && selectedDate > new Date(maxDate)) return;
    if (minDate && selectedDate < new Date(minDate)) return;
    
    onChange(dateString);
    setIsOpen(false);
  };

  // Navigate months
  const navigateMonth = (direction) => {
    if (direction === 'prev') {
      if (currentMonth === 0) {
        setCurrentMonth(11);
        setCurrentYear(currentYear - 1);
      } else {
        setCurrentMonth(currentMonth - 1);
      }
    } else {
      if (currentMonth === 11) {
        setCurrentMonth(0);
        setCurrentYear(currentYear + 1);
      } else {
        setCurrentMonth(currentMonth + 1);
      }
    }
  };

  // Generate calendar days
  const generateCalendarDays = () => {
    const daysInMonth = getDaysInMonth(currentMonth, currentYear);
    const firstDay = getFirstDayOfMonth(currentMonth, currentYear);
    const today = new Date();
    const selectedDate = value ? new Date(value) : null;
    const maxDateObj = maxDate ? new Date(maxDate) : null;
    const minDateObj = minDate ? new Date(minDate) : null;

    const days = [];

    // Empty cells for days before first day of month
    for (let i = 0; i < firstDay; i++) {
      days.push(<div key={`empty-${i}`} className="w-10 h-10"></div>);
    }

    // Days of the month
    for (let day = 1; day <= daysInMonth; day++) {
      const dayDate = new Date(currentYear, currentMonth, day);
      const isToday = dayDate.toDateString() === today.toDateString();
      const isSelected = selectedDate && dayDate.toDateString() === selectedDate.toDateString();
      const isDisabled = 
        (maxDateObj && dayDate > maxDateObj) || 
        (minDateObj && dayDate < minDateObj);

      days.push(
        <button
          key={day}
          type="button"
          onClick={() => !isDisabled && handleDateSelect(day)}
          disabled={isDisabled}
          className={`w-10 h-10 rounded-lg text-sm font-medium transition-colors ${
            isSelected
              ? 'bg-[#fac638] text-[#1c180d]'
              : isToday
              ? 'bg-[#f4f0e6] text-[#1c180d] border border-[#fac638]'
              : isDisabled
              ? 'text-[#d1c9b3] cursor-not-allowed'
              : 'text-[#1c180d] hover:bg-[#f4f0e6]'
          }`}
          style={{
            backgroundColor: isSelected 
              ? '#fac638' 
              : isToday 
              ? '#f4f0e6' 
              : 'transparent',
            color: isSelected || isToday 
              ? '#1c180d' 
              : isDisabled 
              ? '#d1c9b3' 
              : '#1c180d'
          }}
        >
          {day}
        </button>
      );
    }

    return days;
  };

  // Generate year options (current year ± 50)
  const generateYearOptions = () => {
    const currentYearValue = new Date().getFullYear();
    const years = [];
    for (let year = currentYearValue - 50; year <= currentYearValue + 10; year++) {
      years.push(year);
    }
    return years;
  };

  return (
    <div className={`relative ${className}`} ref={dropdownRef}>
      {label && (
        <label className="block text-[#1c180d] text-base font-medium leading-normal pb-2">
          {label}
        </label>
      )}
      
      {/* Input field */}
      <div 
        className={`relative w-full h-14 bg-[#f4f0e6] rounded-xl border-2 cursor-pointer transition-colors ${
          isOpen ? 'border-[#fac638]' : 'border-transparent'
        } ${error ? 'border-red-300' : ''}`}
        onClick={() => setIsOpen(true)}
      >
        <div className="flex items-center justify-between p-4 h-full">
          <span className={`text-base ${value ? 'text-[#1c180d]' : 'text-[#9e8747]'}`}>
            {value ? formatDisplayDate(value) : placeholder}
          </span>
          <svg 
            className={`w-5 h-5 text-[#9e8747] transition-transform ${isOpen ? 'rotate-180' : ''}`}
            fill="none" 
            stroke="currentColor" 
            viewBox="0 0 24 24"
          >
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
          </svg>
        </div>

        {/* Calendar dropdown */}
        {isOpen && (
          <div className="absolute top-full left-0 right-0 mt-1 bg-white border border-[#e9e2ce] rounded-xl shadow-lg z-50" style={{backgroundColor: '#ffffff'}}>
            {/* Month/Year navigation */}
            <div className="flex items-center justify-between p-4 border-b border-[#e9e2ce]">
              <button
                type="button"
                onClick={() => navigateMonth('prev')}
                className="p-2 hover:bg-[#f4f0e6] rounded-lg transition-colors"
                style={{backgroundColor: 'transparent', color: '#9e8747'}}
              >
                <svg className="w-4 h-4 text-[#9e8747]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                </svg>
              </button>

              <div className="flex items-center gap-2">
                <select
                  value={currentMonth}
                  onChange={(e) => setCurrentMonth(parseInt(e.target.value))}
                  className="bg-white text-[#1c180d] font-medium focus:outline-none border border-[#e9e2ce] rounded px-2 py-1"
                  style={{backgroundColor: '#ffffff', color: '#1c180d'}}
                >
                  {months.map((month, index) => (
                    <option key={index} value={index} className="bg-white text-[#1c180d]" style={{backgroundColor: '#ffffff', color: '#1c180d'}}>{month}</option>
                  ))}
                </select>
                
                <select
                  value={currentYear}
                  onChange={(e) => setCurrentYear(parseInt(e.target.value))}
                  className="bg-white text-[#1c180d] font-medium focus:outline-none border border-[#e9e2ce] rounded px-2 py-1"
                  style={{backgroundColor: '#ffffff', color: '#1c180d'}}
                >
                  {generateYearOptions().map(year => (
                    <option key={year} value={year} className="bg-white text-[#1c180d]" style={{backgroundColor: '#ffffff', color: '#1c180d'}}>{year}</option>
                  ))}
                </select>
              </div>

              <button
                type="button"
                onClick={() => navigateMonth('next')}
                className="p-2 hover:bg-[#f4f0e6] rounded-lg transition-colors"
                style={{backgroundColor: 'transparent', color: '#9e8747'}}
              >
                <svg className="w-4 h-4 text-[#9e8747]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                </svg>
              </button>
            </div>

            {/* Calendar grid */}
            <div className="p-4">
              {/* Day labels */}
              <div className="grid grid-cols-7 gap-1 mb-2">
                {['Su', 'Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa'].map(day => (
                  <div key={day} className="text-center text-xs font-medium text-[#9e8747] py-2">
                    {day}
                  </div>
                ))}
              </div>

              {/* Calendar days */}
              <div className="grid grid-cols-7 gap-1">
                {generateCalendarDays()}
              </div>
            </div>

            {/* Quick actions */}
            <div className="border-t border-[#e9e2ce] p-3 flex justify-between">
              <button
                type="button"
                onClick={() => {
                  const today = new Date().toISOString().split('T')[0];
                  onChange(today);
                  setIsOpen(false);
                }}
                className="text-sm text-[#fac638] hover:underline"
                style={{backgroundColor: 'transparent', color: '#fac638'}}
              >
                Today
              </button>
              <button
                type="button"
                onClick={() => {
                  onChange('');
                  setIsOpen(false);
                }}
                className="text-sm text-[#9e8747] hover:underline"
                style={{backgroundColor: 'transparent', color: '#9e8747'}}
              >
                Clear
              </button>
            </div>
          </div>
        )}
      </div>

      {/* Error message */}
      {error && (
        <p className="mt-1 text-sm text-red-600">{error}</p>
      )}
    </div>
  );
};

export default DatePicker;