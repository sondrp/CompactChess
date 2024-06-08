import { useEffect, useState } from 'react';
import { GameInfo, LegalMove, ClickResult } from '../types';
import Square from './Square';
import { useParams } from 'react-router-dom';

export function processGame(game: string) {
  const match = /^\S+/.exec(game);
  if (!match) return '';
  let gamestring = match[0].replace(/\//g, '');
  gamestring = gamestring.replace(/\d/g, (m) => ' '.repeat(parseInt(m)));
  return gamestring;
}

function processLegalMoves(legalMoves: LegalMove[]): LegalMove[] {
  return legalMoves.map((m) => {
    const { result, square, id } = m;
    const row = ~~(square / 10);
    return {
      id,
      square: square - row * 2,
      result: processGame(result),
    };
  });
}

const extractTurn = (fen: string) => fen.split(' ')[1];

export default function Board({ gameInfo }: { gameInfo: GameInfo }) {
  const { id, username } = useParams();

  const [board, setBoard] = useState(processGame(gameInfo.board));
  const [legalMoves, setLegalMoves] = useState<LegalMove[]>([]);
  const [turn, setTurn] = useState(extractTurn(gameInfo.board));

  const [ws, setWs] = useState<WebSocket | null>(null);

  useEffect(() => {
    const socket = new WebSocket(`ws://localhost:8000/ws/${id}/${username}`);

    socket.addEventListener('open', () => {
      setWs(socket);
    });

    socket.addEventListener('message', (event) => {
      const clickResult: ClickResult = JSON.parse(event.data);
      setTurn(extractTurn(clickResult.game));
      setBoard(processGame(clickResult.game));
      setLegalMoves(processLegalMoves(clickResult.legal_moves));
    });

    return () => {
      socket.close();
    };
  }, [id, username]);

  const handleClick = (square: number) => {
    if (!ws) return;
    ws.send(square.toString());
  };

  const { white, black } = gameInfo;
  const pattern = RegExp(`w-${white}-[RNBQKP]|b-${black}-[rnbqkp]`);

  return (
    <div>
      <div className='grid grid-cols-8 w-fit border-2 shadow-2xl border-black'>
        {Array.from({ length: 64 }).map((_, i) => (
          <Square
            pattern={pattern}
            turn={turn}
            legalMove={legalMoves.find((m) => m.square === i)}
            handleClick={() => handleClick(i)}
            key={i}
            index={i}
            piece={board[i]}
          />
        ))}
      </div>
    </div>
  );
}
