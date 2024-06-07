import { useMutation } from '@tanstack/react-query';
import { click } from '../network/requests';
import { LegalMove, ClickResult } from '../types';
import { cn } from '../utils/cn';
import { getPieceImage } from '../utils/getPieceImage';
import { useParams } from 'react-router-dom';

type SquareProps = {
  pattern: RegExp
  turn: string
  legalMove?: LegalMove;
  handleClick: (clickResult: ClickResult) => void;
  index: number;
  piece: string;
};


// so what are we doing here? Make sure that active user is clicking the board. Also make sure is is their turn? We make these checks on the
// server, but does not hurt do do here either I guess. For that we need players, and turn. which we get from the gamestring.
// not provided here. could pass in a test? Can check against the pieces maybe? 
export default function Square(props: SquareProps) {
  const { id, username} = useParams()
  if (!username || !id) throw Error("bad params")

  const { pattern, turn, legalMove, handleClick, index, piece } = props;
  const column = index % 8;
  const row = Math.floor(index / 8);
  const isWhite = column % 2 === row % 2;
  
  const canClick = pattern.test(`${turn}-${username}-${piece}`) || !!legalMove

  const { mutate } = useMutation({
    mutationFn: click,
    onSuccess: handleClick,
  });


  return (
    <button
    disabled={!canClick}
      onClick={() => mutate({id, username, square: index + 2 * row})}
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
