import { useQuery } from '@tanstack/react-query';
import { getGame } from './network/requests';
import Board from './components/Board';

function App() {
  const { data, isSuccess } = useQuery({
    queryKey: ['board'],
    queryFn: getGame,
  });

  return (
    <div className='flex gap-10 h-screen items-center justify-center'>
      {isSuccess && <Board data={data} />}
    </div>
  );
}

export default App;
