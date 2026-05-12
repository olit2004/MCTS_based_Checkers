import React from 'react';
import { RotateCcw, Play, History, Trophy, Bot, User } from 'lucide-react';
import './Sidebar.css';

const Sidebar = ({ gameState, onNewGame, isAiThinking, loading }) => {
  if (!gameState) {
    return (
      <div className="sidebar">
        <button className="btn-primary" onClick={onNewGame} disabled={loading}>
          <Play size={18} />
          Start Game
        </button>
      </div>
    );
  }

  const { current_player, move_history, game_over, winner } = gameState;
  const isWhiteTurn = current_player === 1;

  return (
    <div className="sidebar">

      {/* Turn Status Card */}
      <div className="status-card">
        {game_over ? (
          <div className="winner-announcement">
            <Trophy size={28} className="trophy-icon" />
            <h3>{winner === 1 ? 'White Wins!' : winner === -1 ? 'Black Wins!' : "It's a Draw!"}</h3>
          </div>
        ) : isAiThinking ? (
          <div className="ai-thinking-card">
            <div className="thinking-header">
              <Bot size={18} />
              <span> MCTS is Searching ..</span>
            </div>
            <div className="thinking-dots">
              <span /><span /><span />
            </div>
          </div>
        ) : (
          <div className="turn-indicator">
            <div className={`turn-piece-icon ${isWhiteTurn ? 'white' : 'black'}`} />
            <div className="turn-text">
              {isWhiteTurn ? (
                <>
                  <div className="turn-label">Your Turn</div>
                  <div className="turn-sub">Playing as White</div>
                </>
              ) : (
                <>
                  <div className="turn-label">AI's Turn</div>
                  <div className="turn-sub">Playing as Black</div>
                </>
              )}
            </div>
          </div>
        )}
      </div>

      {/* Controls */}
      <div className="controls">
        <button className="btn-secondary" onClick={onNewGame} disabled={loading || isAiThinking}>
          <RotateCcw size={18} />
          New Game
        </button>
      </div>

      {/* Move History */}
      <div className="history-section">
        <div className="section-header">
          <History size={16} />
          <span>Move History</span>
          {move_history.length > 0 && (
            <span className="move-count">{move_history.length}</span>
          )}
        </div>
        <div className="history-list">
          {move_history.length === 0 ? (
            <div className="empty-history">No moves yet</div>
          ) : (
            [...move_history].reverse().map((move, idx) => {
              const moveNum = move_history.length - idx;
              const isWhiteMove = moveNum % 2 === 1;
              return (
                <div key={idx} className={`history-item ${idx === 0 ? 'latest' : ''}`}>
                  <span className="move-number">{moveNum}.</span>
                  <div className={`move-piece-dot ${isWhiteMove ? 'white' : 'black'}`} />
                  <span className="move-coords">
                    ({move.from[0]},{move.from[1]}) → ({move.to[0]},{move.to[1]})
                  </span>
                  {move.captures.length > 0 && <span className="capture-tag">×{move.captures.length}</span>}
                </div>
              );
            })
          )}
        </div>
      </div>
    </div>
  );
};

export default Sidebar;
