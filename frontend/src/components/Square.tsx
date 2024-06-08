import { LegalMove } from '../types';
import { cn } from '../utils/cn';
import { getPieceImage } from '../utils/getPieceImage';
import { useParams } from 'react-router-dom';

type SquareProps = {
  pattern: RegExp;
  turn: string;
  legalMove?: LegalMove;
  handleClick: () => void;
  index: number;
  piece: string;
};

export default function Square(props: SquareProps) {
  const { id, username } = useParams();
  if (!username || !id) throw Error('bad params');

  const { pattern, turn, legalMove, handleClick, index, piece } = props;
  const column = index % 8;
  const row = Math.floor(index / 8);
  const isWhite = column % 2 === row % 2;

  const canClick = pattern.test(`${turn}-${username}-${piece}`) || !!legalMove;

  return (
    <button
      disabled={!canClick}
      onClick={handleClick}
      className={cn(
        'size-20 flex items-center justify-center relative',
        isWhite ? 'bg-orange-200' : 'bg-orange-800',
        canClick && 'cursor-pointer'
      )}
    >
      {piece != ' ' && (
        <img
          className={cn(canClick && 'hover:scale-110')}
          src={getPieceImage(piece)}
          alt='piece'
        />
      )}
      {!!legalMove && (
        <div className='absolute flex items-center justify-center size-5 rounded-full bg-green-800 opacity-70'></div>
      )}
    </button>
  );
}
