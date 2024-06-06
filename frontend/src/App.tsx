import { useState } from 'react';
import BoardPreview from './components/BoardPreview';
import { useMutation } from '@tanstack/react-query';
import { createGame, getUser } from './network/requests';
import { cn } from './utils/cn';
import { GameInfo, User } from './types';
import SelectUser from './components/SelectUser';
import Board from './components/Board';

const EXAMPLE_GAMES = [
  '8/p6p/2P5/1pnPp1p1/b3p2P/5PrQ/1K6/4k3 w - - 0 1',
  'N7/6Pb/p2p4/1Rb3K1/2p1r1P1/2N2pP1/2R5/6k1 w - - 0 1',
  '8/1Q2Np1P/1K1nPB1P/2Pq3P/8/n2pk3/1P6/8 w - - 0 1',
  'b6B/1Rq1PpP1/4Bp2/p1k1pKp1/8/6N1/8/r7 w - - 0 1',
]; // TODO: these should come from database.

function App() {
  const [user, setUser] = useState<User | null>(null);

  const { mutate } = useMutation({
    mutationFn: getUser,
    onSuccess: setUser,
  });

  return (
    <div className='min-h-screen flex flex-col gap-20 pb-20 bg-orange-200'>
      <div className='h-20 flex items-center justify-center text-3xl font-extrabold bg-amber-900 text-orange-200'>
        Chess
      </div>
      <div className='flex items-end justify-center'>
        {!user ? (
          <SelectUser handleSelectUser={mutate} />
        ) : (
          <UserView user={user} />
        )}
      </div>

      <div className=''></div>
      <div className='flex gap-20 items-center justify-center'>
        {EXAMPLE_GAMES.map((game) => (
          <BoardPreview key={game} game={game} />
        ))}
      </div>
    </div>
  );
}

function UserView({ user }: { user: User }) {
  const [gameInfo, setGameInfo] = useState<GameInfo | null>(null);

  return <div className='flex items-center gap-2'>
    {!gameInfo ? <CreateGame user={user} setGameInfo={setGameInfo} /> : <Board gameInfo={gameInfo} />}
  </div>;
}

function CreateGame({
  user,
  setGameInfo,
}: {
  user: User;
  setGameInfo: (gameInfo: GameInfo) => void;
}) {
  const username = user.username;
  const [asWhite, setAsWhite] = useState(true);
  const [buttonText, setButtonText] = useState('Create new game');
  const { mutate } = useMutation({
    mutationFn: createGame,
    onMutate: () => setButtonText('Loading...'),
    onSuccess: setGameInfo,
  });
  return (
    <>
      <div className='mr-20'>Hello, {user.username}</div>
      <button
        onClick={() => mutate({ username, asWhite })}
        className='px-4 py-2 border rounded-md border-black'
      >
        {buttonText}
      </button>
      <div>as</div>
      <button
        onClick={() => setAsWhite(!asWhite)}
        className='px-4 py-2 border rounded-md border-black w-20'
      >
        {asWhite ? 'white' : 'black'}
      </button>
    </>
  );
}

export default App;
