import { useMutation } from "@tanstack/react-query";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import BoardPreview from "../components/BoardPreview";
import SelectUser from "../components/SelectUser";
import { getUser, createGame } from "../network/requests";
import { User } from "../types";

const EXAMPLE_GAMES = [
    '8/p6p/2P5/1pnPp1p1/b3p2P/5PrQ/1K6/4k3 w - - 0 1',
    'N7/6Pb/p2p4/1Rb3K1/2p1r1P1/2N2pP1/2R5/6k1 w - - 0 1',
    '8/1Q2Np1P/1K1nPB1P/2Pq3P/8/n2pk3/1P6/8 w - - 0 1',
    'b6B/1Rq1PpP1/4Bp2/p1k1pKp1/8/6N1/8/r7 w - - 0 1',
  ]; // TODO: these should come from database.
  

export default function HomePage() {
    const [user, setUser] = useState<User | null>(null);
  
    const { mutate } = useMutation({
      mutationFn: getUser,
      onSuccess: setUser,
    });
    return (
      <>
      <div className='flex items-end justify-center'>
        {!user ? (
          <SelectUser handleSelectUser={mutate} />
        ) : (
          <CreateGame user={user} />
        )}
      </div>
      <div className=''></div>
      <div className='flex gap-20 items-center justify-center'>
        {EXAMPLE_GAMES.map((game) => (
          <BoardPreview key={game} game={game} />
        ))}
      </div>
    </>
  );
}

function CreateGame({ user }: { user: User }) {
    const username = user.username;
    const [asWhite, setAsWhite] = useState(true);
    const [buttonText, setButtonText] = useState('Create new game');
  
    const navigate = useNavigate();
  
    const { mutate } = useMutation({
      mutationFn: createGame,
      onMutate: () => setButtonText('Loading...'),
      onSuccess: (gameInfo) => {
        navigate(`/games/${gameInfo.id}`, { state: { gameInfo: gameInfo } });
      },
    });
    return (
      <div className='flex gap-2 items-center'>
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
      </div>
    );
  }