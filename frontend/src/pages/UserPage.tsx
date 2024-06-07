import { useMutation } from "@tanstack/react-query";
import { useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { createGame } from "../network/requests";


export default function UserPage() {


    return <div className="flex items-center justify-center">
        <CreateGame />
    </div>
}


function CreateGame() {
    const { username } = useParams()
    if (!username) throw Error("username not in params")

    const [asWhite, setAsWhite] = useState(true);
    const [buttonText, setButtonText] = useState('Create new game');
  
    const handleCreate = () => {
      const white = asWhite ? username : 'no opponent';
      const black = asWhite ? 'no opponent' : username;
      mutate({ white, black });
    };
  
    const navigate = useNavigate();
  
    const { mutate } = useMutation({
      mutationFn: createGame,
      onMutate: () => setButtonText('Loading...'),
      onSuccess: (gameInfo) => {
        navigate(`/${gameInfo.id}/${username}`);
      },
    });
    return (
      <div className='flex gap-2 items-center'>
        <button
          onClick={handleCreate}
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
  