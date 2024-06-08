import { Link, Outlet, useParams } from 'react-router-dom';

function App() {
  const { username } = useParams()

  return (
    <div className='min-h-screen flex flex-col gap-20 pb-20 bg-orange-200'>
      <Link to={`/${username ?? ""}`} className='h-20 flex items-center justify-center text-3xl font-extrabold bg-amber-900 text-orange-200'>
        Chess
      </Link>
      <Outlet />
    </div>
  );
}

export default App;
