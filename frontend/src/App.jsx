import React, { useEffect } from 'react';
import { useGame } from './hooks/useGame';
import Board from './components/Board';
import Sidebar from './components/Sidebar';
import { ShieldAlert } from 'lucide-react';
import './App.css';

function App() {
  const {
    gameState,
    legalMoves,
    loading,
    error,
    isAiThinking,
    startNewGame,
    makeMove,
    setError
  } = useGame();

  
  useEffect(() => {
    startNewGame();
  }, []);

  return (
    <>
      <header className="main-header">
        <div className="logo">
          <div className="logo-icon">O</div>
          <h1>OLI CHECKERS</h1>
        </div>
        {error && (
          <div className="error-toast" onClick={() => setError(null)}>
            <ShieldAlert size={18} />
            <span>{error}</span>
          </div>
        )}
      </header>

      <div className="app-container">
        <Sidebar 
          gameState={gameState} 
          onNewGame={startNewGame}
          isAiThinking={isAiThinking}
          loading={loading}
        />
        
        <main className="game-area">
          <Board 
            gameState={gameState}
            legalMoves={legalMoves}
            onMove={makeMove}
            isAiThinking={isAiThinking}
          />
        </main>
      </div>
    </>
  );
}

export default App;
