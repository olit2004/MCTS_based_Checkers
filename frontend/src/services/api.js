import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
});

export const gameService = {
  createGame: async () => {
    const response = await api.post('/game/new');
    return response.data;
  },

  getGameState: async (gameId) => {
    const response = await api.get(`/game/${gameId}/state`);
    return response.data;
  },

  getLegalMoves: async (gameId) => {
    const response = await api.get(`/game/${gameId}/legal-moves`);
    return response.data;
  },

  makeMove: async (gameId, moveData) => {
    const response = await api.post(`/game/${gameId}/move`, {
      from_pos: moveData.from,
      to_pos: moveData.to,
      captures: moveData.captures || [],
    });
    return response.data;
  },

  getAIByMove: async (gameId) => {
    const response = await api.post(`/game/${gameId}/ai-move`);
    return response.data;
  },

  getMoveHistory: async (gameId) => {
    const response = await api.get(`/game/${gameId}/history`);
    return response.data;
  },
};

export default api;
