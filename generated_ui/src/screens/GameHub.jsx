import React from 'react';
import GameItem from '../components/GameItem';
// Assuming Game data is fetched from an API or stored in a file
const gameData = [ /* Fetched or imported game data */ ];

const GameHub = () => {
  return (
    <div className="container mx-auto px-4 py-6">
      <h1 className="text-2xl font-bold mb-4">Game Hub</h1 >
      <ul className="grid grid-cols-3 gap-4">
        {gameData.map((game) => (
          <li key={game.id}>
            <GameItem game={game} />
          </li>
        ))}
      </ul>
    </div>
  );
};

export default GameHub;