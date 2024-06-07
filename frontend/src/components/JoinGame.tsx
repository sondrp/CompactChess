// To be able to a game, we need a couple of things.
// id of the game (params)
// name of the user that wants to join
// that is it really...

import { useMutation, useQueryClient } from "@tanstack/react-query";
import { join } from "../network/requests";
import { useParams } from "react-router-dom";

export default function Opponent({ name }: { name: string }) {
  const { id } = useParams()
  if (typeof id !== "string") throw Error("id is not a string somehow")

  const noOpponent = name === 'no opponent';

  const queryClient = useQueryClient()
  const { mutate } = useMutation({
      mutationFn: () => join({id, color: "black", username: "username"}),
      onSuccess: () => queryClient.invalidateQueries({
          queryKey: ['games', id],
        })
  })

  return (
    <div className='flex justify-center items-center py-2 relative'>
      {name}
      {noOpponent && (
        <div className='absolute right-20 gap-2 flex items-center'>
          <button onClick={() => mutate()} className='border-b border-black px-4'>
            join
          </button>
          <div>as user</div>
        </div>
      )}
    </div>
  );
}
