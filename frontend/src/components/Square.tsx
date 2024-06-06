import { useMutation } from '@tanstack/react-query';
import { click } from '../network/requests';
import { LegalMove, ClickResult } from '../types';
import { cn } from '../utils/cn';
import { getPieceImage } from '../utils/getPieceImage';

const PLAYER_COLOR = 'w'; // TODO : make dynamic

type SquareProps = {
  legalMove?: LegalMove;
  handleClick: (clickResult: ClickResult) => void;
  index: number;
  piece: string;
};
/* On click -> a request should be sent to the api. */
export default function Square(props: SquareProps) {
  const { legalMove, handleClick, index, piece } = props;
  const column = index % 8;
  const row = Math.floor(index / 8);
  const isWhite = column % 2 === row % 2;
  const isPlayerPiece = /w[RNBQKP]|b[rnbqkp]/.test(PLAYER_COLOR + piece);

  const { mutate } = useMutation({
    mutationFn: click,
    onSuccess: handleClick,
  });

  return (
    <div
      onClick={() => mutate({ index: index + 2 * row, player: PLAYER_COLOR })}
      className={cn(
        'size-20 flex items-center justify-center relative',
        isWhite ? 'bg-orange-200' : 'bg-orange-800',
        isPlayerPiece && 'cursor-pointer'
      )}
    >
      {piece != ' ' && (
        <img
          className={cn(isPlayerPiece && 'hover:scale-110')}
          src={getPieceImage(piece)}
          alt='piece'
        />
      )}
      {!!legalMove && (
        <div className='absolute flex items-center justify-center size-5 rounded-full bg-green-800 opacity-70'></div>
      )}
    </div>
  );
}
