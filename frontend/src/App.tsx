import { useMutation, useQuery } from '@tanstack/react-query';
import { click, getGame } from './network/requests';
import { ClickResult, GameInfo } from './types';
import { cn } from './utils/cn';
import { getPieceImage } from './utils/getPieceImage';

function processGame(game: string) {
  const match = /^\S+/.exec(game);
  if (!match) return '';
  let gamestring = match[0].replace(/\//g, '');
  gamestring = gamestring.replace(/\d/g, (m) => ' '.repeat(parseInt(m)));
  return gamestring;
}


const PLAYER_COLOR = "w"  // TODO : make dynamic

function App() {
  const { data, isSuccess } = useQuery({
    queryKey: ['board'],
    queryFn: getGame,
  });

  return (
    <div className='flex h-screen items-center justify-center'>
      {isSuccess && <Board data={data} />}
    </div>
  );
}

// Board needs to get something back when a square is clicked on. So we pass it a click result right?

function Board({ data }: { data: GameInfo }) {
  const game = processGame(data.game);

  const handleClick = (clickResult: ClickResult) => {
    console.log(clickResult)
    console.log("we got some data here!")
    console.log(clickResult.legal_moves)
  }

  return (
    <div className='grid grid-cols-8 w-fit'>
      {Array.from({ length: 64 }).map((_, i) => (
        <Square handleClick={handleClick} key={i} index={i} piece={game[i]} />
      ))}
    </div>
  );
}

type SquareProps = {
  handleClick: (clickResult: ClickResult) => void
  index: number
  piece: string
}
/* On click -> a request should be sent to the api. */
function Square(props: SquareProps) {
  const { handleClick, index, piece} = props
  const column = index % 8;
  const row = Math.floor(index / 8);
  const isWhite = column % 2 === row % 2;
  const isPlayerPiece = /w[RNBQKP]|b[rnbqkp]/.test(PLAYER_COLOR + piece)

  const { mutate } = useMutation({
    mutationFn: click,
    onSuccess: handleClick
  })

  return (
    <div
    onClick={() => mutate({index: index + 2 * row, player: PLAYER_COLOR})}
      className={cn(
        'size-20 flex items-center justify-center',
        isWhite ? 'bg-orange-200' : 'bg-orange-800',
        isPlayerPiece && "cursor-pointer"
      )}
    >
      {piece != " " && <img className={cn(isPlayerPiece && "hover:scale-110")} src={getPieceImage(piece)} alt='piece' />}
    </div>
  );
}

export default App;
