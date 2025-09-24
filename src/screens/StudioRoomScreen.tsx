import React, { useState, useEffect } from 'react';
import './StudioRoomScreen.css';

interface StudioRoomScreenProps {
  playerName: string;
  studioName: string;
}

const StudioRoomScreen: React.FC<StudioRoomScreenProps> = ({ playerName, studioName }) => {
  const [playerPosition, setPlayerPosition] = useState({ x: 400, y: 300 });
  const [keysPressed, setKeysPressed] = useState<Set<string>>(new Set());

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      setKeysPressed(prev => new Set(prev).add(e.key.toLowerCase()));
    };

    const handleKeyUp = (e: KeyboardEvent) => {
      setKeysPressed(prev => {
        const newKeys = new Set(prev);
        newKeys.delete(e.key.toLowerCase());
        return newKeys;
      });
    };

    window.addEventListener('keydown', handleKeyDown);
    window.addEventListener('keyup', handleKeyUp);

    return () => {
      window.removeEventListener('keydown', handleKeyDown);
      window.removeEventListener('keyup', handleKeyUp);
    };
  }, []);

  useEffect(() => {
    const moveSpeed = 5;
    const interval = setInterval(() => {
      setPlayerPosition(prev => {
        let newX = prev.x;
        let newY = prev.y;

        if (keysPressed.has('w') || keysPressed.has('arrowup')) {
          newY = Math.max(20, prev.y - moveSpeed);
        }
        if (keysPressed.has('s') || keysPressed.has('arrowdown')) {
          newY = Math.min(580, prev.y + moveSpeed);
        }
        if (keysPressed.has('a') || keysPressed.has('arrowleft')) {
          newX = Math.max(20, prev.x - moveSpeed);
        }
        if (keysPressed.has('d') || keysPressed.has('arrowright')) {
          newX = Math.min(780, prev.x + moveSpeed);
        }

        return { x: newX, y: newY };
      });
    }, 16);

    return () => clearInterval(interval);
  }, [keysPressed]);

  return (
    <div className="studio-room-container">
      <div className="studio-info">
        <h2>{studioName}</h2>
        <p>Player: {playerName}</p>
      </div>

      <div className="room">
        {/* Bed */}
        <div className="furniture bed">
          <div className="bed-pillow"></div>
          <div className="bed-mattress"></div>
        </div>

        {/* Desk */}
        <div className="furniture desk">
          <div className="desk-monitor"></div>
          <div className="desk-surface"></div>
        </div>

        {/* Shower */}
        <div className="furniture shower">
          <div className="shower-head"></div>
          <div className="shower-door"></div>
        </div>

        {/* Fridge */}
        <div className="furniture fridge">
          <div className="fridge-door"></div>
          <div className="fridge-handle"></div>
        </div>

        {/* Microwave */}
        <div className="furniture microwave">
          <div className="microwave-door"></div>
        </div>

        {/* Player */}
        <div
          className="player"
          style={{
            left: `${playerPosition.x}px`,
            top: `${playerPosition.y}px`
          }}
        ></div>
      </div>

      <div className="controls-hint">
        Use WASD or Arrow Keys to move
      </div>
    </div>
  );
};

export default StudioRoomScreen;