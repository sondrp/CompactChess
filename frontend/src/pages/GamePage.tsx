import { useParams } from 'react-router-dom';
import { useState } from 'react';
import Square from '../components/Square';
import { GameInfo } from '../types';
import { useChessWebsocket } from '../hooks/useChessWebsocket';



// Time to figure out how to actually send data to the websocket. 
// I need to register players, and I need to post moves.
// I also have to send username along with the click, to confirm that they are allowed to make the move.
// Otherwise I will run into problems.

export default function GamePage() {
  const { id, username } = useParams();
  if (!username || !id) throw Error('something went wrong with the params');

  const { ws, board, white, black, turn, legalMoves } = useChessWebsocket(id, username);

  const [reversed, setReversed] = useState(username === black);

  const handleClick = (square: number) => {
    if (!ws) return;
    ws.send(JSON.stringify({
      "action": "click",
      username,
      square,
    }));
  };


  const pattern = RegExp(`w-${white}-[RNBQKP]|b-${black}-[rnbqkp]`);

  const topName = reversed ? white : black;
  const bottomName = reversed ? black : white;

  return (
    <div className='flex flex-col items-center justify-center relative'>
      <button
        className='absolute top-0 right-20 px-4 py-2 rounded-md border border-black'
        onClick={() => setReversed(!reversed)}
      >
        Flip Board
      </button>

      <div className='text-center py-2'>{topName}</div>
      <div className=''>
        <div className='grid grid-cols-8 w-fit border-2 shadow-2xl border-black'>
          {Array.from({ length: 64 }, (_, i) => (reversed ? 63 - i : i)).map(
            (i) => (
              <Square
                pattern={pattern}
                turn={turn}
                legalMove={legalMoves.find((m) => m.square === i)}
                handleClick={() => handleClick(i)}
                key={i}
                index={i}
                piece={board[i]}
              />
            )
          )}
        </div>
      </div>
      <div className='text-center py-2'>{bottomName}</div>
    </div>
  );
}
