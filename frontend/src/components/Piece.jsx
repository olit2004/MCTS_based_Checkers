import React from 'react';

const Piece = ({ type, isSelected, isCapturable }) => {
  const isWhite = type === 'white_piece' || type === 'white_king';
  const isKing = type === 'white_king' || type === 'black_king';

  return (
    <div className={`piece ${isWhite ? 'white' : 'black'} ${isKing ? 'king' : ''} ${isSelected ? 'selected' : ''} ${isCapturable ? 'capturable' : ''}`}>
      <svg viewBox="0 0 100 100" className="piece-svg">
        <circle cx="50" cy="50" r="45" className="outer-circle" />
        <circle cx="50" cy="50" r="35" className="inner-circle" />
        {isKing && (
          <path
            d="M50 30 L60 50 L80 50 L65 65 L70 85 L50 75 L30 85 L35 65 L20 50 L40 50 Z"
            fill="currentColor"
            className="crown-icon"
          />
        )}
      </svg>
    </div>
  );
};

export default Piece;
