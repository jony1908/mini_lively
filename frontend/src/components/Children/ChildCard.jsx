/**
 * ChildCard Component
 * 
 * Displays individual child information in a card format:
 * - Child's basic info (name, age)
 * - Interests and skills as tags
 * - Action buttons (edit, delete)
 */

import React from 'react';
import childAPI from '../../services/child';

const ChildCard = ({ child, onEdit, onDelete }) => {
  const handleEdit = () => {
    onEdit(child.id);
  };

  const handleDelete = () => {
    if (window.confirm(`Are you sure you want to remove ${childAPI.getChildFullName(child)}?`)) {
      onDelete(child.id);
    }
  };

  return (
    <div className="bg-[#f4f0e6] rounded-xl p-6 hover:shadow-md transition-shadow">
      {/* Header with avatar, name, age and actions */}
      <div className="flex items-start gap-4 mb-4">
        {/* Avatar */}
        <div className="flex-shrink-0">
          <div className="w-16 h-16 rounded-full overflow-hidden bg-[#e9e2ce] border-2 border-[#d1c9b3]">
            {child.avatar_url ? (
              <img 
                src={child.avatar_url} 
                alt={`${childAPI.getChildFullName(child)} avatar`} 
                className="w-full h-full object-cover"
              />
            ) : (
              <div className="w-full h-full flex items-center justify-center">
                <svg xmlns="http://www.w3.org/2000/svg" width="24px" height="24px" fill="#9e8747" viewBox="0 0 256 256">
                  <path d="M230.92,212c-15.23-26.33-38.7-45.21-66.09-54.16a72,72,0,1,0-73.66,0C63.78,166.78,40.31,185.66,25.08,212a8,8,0,1,0,13.85,8c18.84-32.56,52.14-52,89.07-52s70.23,19.44,89.07,52a8,8,0,1,0,13.85-8ZM72,96a56,56,0,1,1,56,56A56.06,56.06,0,0,1,72,96Z"></path>
                </svg>
              </div>
            )}
          </div>
        </div>

        {/* Name and info */}
        <div className="flex-1 min-w-0">
          <h3 className="text-[#1c180d] text-lg font-bold leading-tight">
            {childAPI.getChildFullName(child)}
          </h3>
          <p className="text-[#9e8747] text-sm">
            {child.age} years old
            {child.gender && (
              <span className="ml-2">• {child.gender}</span>
            )}
          </p>
        </div>
        
        {/* Action buttons */}
        <div className="flex gap-2 flex-shrink-0">
          <button
            onClick={handleEdit}
            className="p-2 text-[#9e8747] hover:text-[#1c180d] hover:bg-[#e9e2ce] rounded-lg transition-colors"
            title="Edit child"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 256 256">
              <path d="M227.31,73.37,182.63,28.69a16,16,0,0,0-22.63,0L36.69,152A15.86,15.86,0,0,0,32,163.31V208a16,16,0,0,0,16,16H92.69A15.86,15.86,0,0,0,104,219.31L227.31,96A16,16,0,0,0,227.31,73.37ZM92.69,208H48V163.31l88-88L180.69,120ZM192,108.69,147.31,64l24-24L216,84.69Z"></path>
            </svg>
          </button>
          <button
            onClick={handleDelete}
            className="p-2 text-[#9e8747] hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors"
            title="Remove child"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 256 256">
              <path d="M216,48H176V40a24,24,0,0,0-24-24H104A24,24,0,0,0,80,40v8H40a8,8,0,0,0,0,16h8V208a16,16,0,0,0,16,16H192a16,16,0,0,0,16-16V64h8a8,8,0,0,0,0-16ZM96,40a8,8,0,0,1,8-8h48a8,8,0,0,1,8,8v8H96Zm96,168H64V64H192ZM112,104v64a8,8,0,0,1-16,0V104a8,8,0,0,1,16,0Zm48,0v64a8,8,0,0,1-16,0V104a8,8,0,0,1,16,0Z"></path>
            </svg>
          </button>
        </div>
      </div>

      {/* Interests */}
      {child.interests && child.interests.length > 0 && (
        <div className="mb-3">
          <h4 className="text-[#1c180d] text-sm font-medium mb-2">Interests</h4>
          <div className="flex flex-wrap gap-1">
            {child.interests.slice(0, 4).map((interest, index) => (
              <span
                key={index}
                className="inline-block bg-[#fac638] text-[#1c180d] text-xs px-2 py-1 rounded-md"
              >
                {interest}
              </span>
            ))}
            {child.interests.length > 4 && (
              <span className="inline-block bg-[#e9e2ce] text-[#9e8747] text-xs px-2 py-1 rounded-md">
                +{child.interests.length - 4} more
              </span>
            )}
          </div>
        </div>
      )}

      {/* Skills */}
      {child.skills && child.skills.length > 0 && (
        <div>
          <h4 className="text-[#1c180d] text-sm font-medium mb-2">Skills</h4>
          <div className="flex flex-wrap gap-1">
            {child.skills.slice(0, 4).map((skill, index) => (
              <span
                key={index}
                className="inline-block bg-[#e9e2ce] text-[#1c180d] text-xs px-2 py-1 rounded-md"
              >
                {skill}
              </span>
            ))}
            {child.skills.length > 4 && (
              <span className="inline-block bg-[#d1c9b3] text-[#9e8747] text-xs px-2 py-1 rounded-md">
                +{child.skills.length - 4} more
              </span>
            )}
          </div>
        </div>
      )}

      {/* Empty state */}
      {(!child.interests || child.interests.length === 0) && (!child.skills || child.skills.length === 0) && (
        <p className="text-[#9e8747] text-sm italic">
          No interests or skills added yet
        </p>
      )}
    </div>
  );
};

export default ChildCard;