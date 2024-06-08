import { Link, useParams } from 'react-router-dom';
import { GameInfo } from '../types';
import { cn } from '../utils/cn';
import { getPieceImage } from '../utils/getPieceImage';
import { processGame } from '../hooks/useChessWebsocket';

export default function BoardPreview({ game }: { game: GameInfo }) {
  const { username } = useParams()
  if (!username) throw Error("bad params")
  const { id, white, black } = game;

  const board = processGame(game.board);

  return (
    <Link to={`/${id}/${username}`} className='flex flex-col items-center'>
      <div>{black}</div>
      <div className='grid grid-cols-8 w-80 border-black border-8'>
        {Array.from({ length: 64 }).map((_, i) => (
          <Square index={i} piece={board[i]} key={i} />
        ))}
      </div>
      <div>{white}</div>
    </Link>
  );
}

function Square({ index, piece }: { index: number; piece: string }) {
  const col = ~~(index / 8);
  const row = index % 8;
  const isWhite = col % 2 === row % 2;

  return (
    <div className={cn('size-10', isWhite ? 'bg-slate-200' : 'bg-amber-700')}>
      {piece !== ' ' && <img src={getPieceImage(piece)} alt='piece' />}
    </div>
  );
}
