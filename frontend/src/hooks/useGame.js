import { useState, useEffect, useCallback } from 'react';
import { gameService } from '../services/api';

export const useGame = () => {
  const [gameId, setGameId] = useState(null);
  const [gameState, setGameState] = useState(null);
  const [legalMoves, setLegalMoves] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [isAiThinking, setIsAiThinking] = useState(false);

  const startNewGame = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await gameService.createGame();
      setGameId(data.game_id);
      setGameState(data.state);
      const movesData = await gameService.getLegalMoves(data.game_id);
      setLegalMoves(movesData.moves);
    } catch (err) {
      setError('Failed to start new game');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const refreshGameState = useCallback(async (id) => {
    try {
      const state = await gameService.getGameState(id);
      setGameState(state);
      const movesData = await gameService.getLegalMoves(id);
      setLegalMoves(movesData.moves);
    } catch (err) {
      console.error('Failed to refresh game state', err);
    }
  }, []);

  const makeMove = async (move) => {
    if (!gameId || loading || isAiThinking) return;

    setLoading(true);
    try {
      const result = await gameService.makeMove(gameId, move);
      if (result.success) {
        setGameState(result.state);
        const movesData = await gameService.getLegalMoves(gameId);
        setLegalMoves(movesData.moves);
      }
    } catch (err) {
      setError(err.response?.data?.detail || 'Illegal move');
    } finally {
      setLoading(false);
    }
  };

  const triggerAiMove = async () => {
    if (!gameId || loading || isAiThinking || (gameState && gameState.game_over)) return;

    setIsAiThinking(true);
    try {
      const result = await gameService.getAIByMove(gameId);
      if (result.success) {
        setGameState(result.state);
        const movesData = await gameService.getLegalMoves(gameId);
        setLegalMoves(movesData.moves);
      }
    } catch (err) {
      setError('AI failed to make a move');
      console.error(err);
    } finally {
      setIsAiThinking(false);
    }
  };

  // Auto-trigger AI if it's black's turn (AI plays black)
  useEffect(() => {
    console.log('Game State Check:', {
      current_player: gameState?.current_player,
      game_over: gameState?.game_over,
      isAiThinking,
      loading
    });

    if (gameState && gameState.current_player === -1 && !gameState.game_over && !isAiThinking) {
      console.log('Triggering AI Move...');
      triggerAiMove();
    }
  }, [gameState, isAiThinking, gameId, loading]); // Added loading to dependencies

  return {
    gameId,
    gameState,
    legalMoves,
    loading,
    error,
    isAiThinking,
    startNewGame,
    makeMove,
    setError,
  };
};
