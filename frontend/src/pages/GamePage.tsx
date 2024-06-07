import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { useParams } from 'react-router-dom';
import { getGame, join } from '../network/requests';
import Board from '../components/Board';

export default function GamePage() {
  const { username, id } = useParams();
  if (!username || !id) throw Error('something went wrong with the params');

  const { data, isSuccess } = useQuery({
    queryKey: ['games', id],
    queryFn: () => getGame(id),
  });

  if (!isSuccess) return <div>Loading...</div>;

  const { white, black } = data
  const hasBlack = black !== "no opponent"
  const hasWhite = white !== "no opponent"

  return (
    <div className='flex flex-col items-center justify-center relative'>
      {!hasWhite && <Join color='white' />}
      {!hasBlack && <Join color='black' />}

      {hasBlack && <div className='text-center py-2'>{black}</div>}
      <Board gameInfo={data} />
      {hasWhite && <div className='text-center py-2'>{white}</div>}
    </div>
  );
}

function Join({color}: {color: string}) {
  const { username, id } = useParams();
  if (!username || !id) throw Error('something went wrong with the params');

  const queryClient = useQueryClient()
  const { mutate } = useMutation({
    mutationFn: join,
    onSuccess: () => queryClient.invalidateQueries({
        queryKey: ['games', id]
    })
  })

  return <button onClick={() => mutate({id, username, color})} className='absolute top-0 left-20 px-4 py-2 rounded-md border border-black'>Join {color} as {username}</button>;
}
