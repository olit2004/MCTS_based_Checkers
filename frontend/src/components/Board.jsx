import React, { useState, useEffect, useRef } from 'react';
import Piece from './Piece';
import './Board.css';

const ANIMATION_DURATION = 380; // ms

const Board = ({ gameState, legalMoves, onMove, isAiThinking }) => {
  const [selectedPos, setSelectedPos] = useState(null);
  const [availableTargets, setAvailableTargets] = useState([]);

 
  const [animatingMove, setAnimatingMove] = useState(null);

  const boardRef = useRef(null);

  
  const prevBoardRef = useRef(null);
  const prevPlayerRef = useRef(null);

  useEffect(() => {
    if (!gameState) return;

    const prev = prevBoardRef.current;
    const prevPlayer = prevPlayerRef.current;

    // Detect AI move: previous turn was AI's (player === -1) and board changed
    if (prev && prevPlayer === -1 && gameState.current_player === 1) {
      const diff = detectMoveDiff(prev, gameState.board);
      if (diff) {
        triggerAnimation(diff.from, diff.to, diff.pieceType);
      }
    }

    prevBoardRef.current = gameState.board;
    prevPlayerRef.current = gameState.current_player;
  }, [gameState]);

  if (!gameState) return null;

  const { board, current_player } = gameState;

  

  function detectMoveDiff(oldBoard, newBoard) {
    let appeared = null;  // square that gained a piece
    let disappeared = null; // square that lost a piece
    let movedPiece = null;

    for (let r = 0; r < 8; r++) {
      for (let c = 0; c < 8; c++) {
        const was = oldBoard[r][c];
        const now = newBoard[r][c];
        if (was !== 'empty' && now === 'empty') {
          disappeared = [r, c];
          movedPiece = was;
        } else if (was === 'empty' && now !== 'empty') {
          appeared = [r, c];
        }
      }
    }
    if (appeared && disappeared) {
      return { from: disappeared, to: appeared, pieceType: movedPiece };
    }
    return null;
  }

  function triggerAnimation(from, to, pieceType) {
    setAnimatingMove({ from, to, pieceType });
    setTimeout(() => setAnimatingMove(null), ANIMATION_DURATION);
  }

  // Compute translate offset between two squares based on board grid
  function getAnimationStyle(from, to) {
    if (!boardRef.current) return {};

    const squares = boardRef.current.querySelectorAll('.square');
    const idx = (r, c) => r * 8 + c;

    const fromEl = squares[idx(from[0], from[1])];
    const toEl = squares[idx(to[0], to[1])];

    if (!fromEl || !toEl) return {};

    const fRect = fromEl.getBoundingClientRect();
    const tRect = toEl.getBoundingClientRect();

    const dx = tRect.left - fRect.left;
    const dy = tRect.top - fRect.top;
    const size = fRect.width;

    return {
      '--anim-dx': `${dx}px`,
      '--anim-dy': `${dy}px`,
      '--anim-size': `${size}px`,
      '--anim-duration': `${ANIMATION_DURATION}ms`,
    };
  }



  const handleSquareClick = (row, col) => {
    if (isAiThinking || gameState.current_player === -1) return;

    const piece = board[row][col];

    const move = availableTargets.find(m => m.to[0] === row && m.to[1] === col);
    if (move) {
      
      const movingPiece = board[move.from[0]][move.from[1]];
      triggerAnimation(move.from, move.to, movingPiece);
      
      setTimeout(() => onMove(move), 50);
      setSelectedPos(null);
      setAvailableTargets([]);
      return;
    }

    const isOwnPiece = (
      (current_player === 1 && piece.startsWith('white_')) ||
      (current_player === -1 && piece.startsWith('black_'))
    );

    if (piece !== 'empty' && isOwnPiece) {
      setSelectedPos([row, col]);
      const moves = legalMoves.filter(m => m.from[0] === row && m.from[1] === col);
      setAvailableTargets(moves);
    } else {
      setSelectedPos(null);
      setAvailableTargets([]);
    }
  };

  const isTarget = (row, col) => availableTargets.some(m => m.to[0] === row && m.to[1] === col);


  const isAnimatingFrom = (r, c) =>
    animatingMove && animatingMove.from[0] === r && animatingMove.from[1] === c;

  const isAnimatingTo = (r, c) =>
    animatingMove && animatingMove.to[0] === r && animatingMove.to[1] === c;

  const animStyle = animatingMove
    ? getAnimationStyle(animatingMove.from, animatingMove.to)
    : {};

  return (
    <div className={`board-container ${isAiThinking ? 'thinking' : ''}`}>
      <div className="board" ref={boardRef}>
        {board.map((rowArr, rIdx) => (
          <div key={rIdx} className="board-row">
            {rowArr.map((cell, cIdx) => {
              const isDark = (rIdx + cIdx) % 2 === 1;
              const isSelected = selectedPos && selectedPos[0] === rIdx && selectedPos[1] === cIdx;
              const isMoveTarget = isTarget(rIdx, cIdx);

             
              const isFrom = isAnimatingFrom(rIdx, cIdx);
              const isTo   = isAnimatingTo(rIdx, cIdx);
              const hideStaticPiece = isFrom || isTo;

              return (
                <div
                  key={`${rIdx}-${cIdx}`}
                  className={`square ${isDark ? 'dark' : 'light'} ${isMoveTarget ? 'target' : ''}`}
                  onClick={() => handleSquareClick(rIdx, cIdx)}
                >
                
                  {cell !== 'empty' && !hideStaticPiece && (
                    <Piece
                      type={cell}
                      isSelected={isSelected}
                    />
                  )}

                 
                  {animatingMove && isFrom && (
                    <div className="piece-animator" style={animStyle}>
                      <Piece type={animatingMove.pieceType} isSelected={false} />
                    </div>
                  )}

                  {isMoveTarget && <div className="target-dot" />}
                </div>
              );
            })}
          </div>
        ))}
      </div>
    </div>
  );
};

export default Board;
