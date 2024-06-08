import { cn } from '../utils/cn';
import { getPieceImage } from '../utils/getPieceImage';
import { processGame } from './Board';

export default function BoardPreview({ game }: { game: string }) {
  const board = processGame(game);

  return (
    <div className='grid grid-cols-8 w-fit border-black border-8'>
      {Array.from({ length: 64 }).map((_, i) => (
        <Square index={i} piece={board[i]} key={i} />
      ))}
    </div>
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
