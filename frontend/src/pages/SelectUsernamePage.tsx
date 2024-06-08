import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

export default function SelectUsernamePage() {
  const navigate = useNavigate();
  const [username, setUsername] = useState('');

  const handleEnter = (e: React.KeyboardEvent) => {
    if (e.key !== 'Enter') return;
    if (username.length < 3) return;

    navigate(`/${username}`);
  };

  return (
    <div className='flex-1 font-semibold text-xl flex flex-col gap-40 items-center justify-center'>
      <div className='gap-10 flex justify-center items-center w-fit relative -ml-24'>
        <div className=''>Play as</div>
        <input
          value={username}
          onKeyDown={handleEnter}
          onChange={(e) => setUsername(e.target.value)}
          placeholder='username'
          className='text-center bg-transparent outline-none px-4 py-2 border-b border-black'
        />
        {username.length > 0 && (
          <button
            onClick={() => navigate(`/${username}`)}
            disabled={username.length < 3}
            className='border border-black px-8 py-4 rounded-md disabled:opacity-50 absolute -right-40'
          >
            Enter
          </button>
        )}
      </div>
      <div className='text-sm'>
        <p>
          And before you say anything; no, I am not stopping you from using
          someone else's username.{' '}
        </p>
        <p>
          This project is not serious enough for me to implement proper
          authorization/access control.
        </p>
      </div>
    </div>
  );
}
