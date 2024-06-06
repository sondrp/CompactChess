import { useState } from "react";
import { cn } from "../utils/cn";

type SelectUserProps = {
  handleSelectUser: (username: string) => void;
};

export default function SelectUser(props: SelectUserProps) {
  const { handleSelectUser } = props;
  const [input, setInput] = useState('');

  const handleEnter = (e: React.KeyboardEvent) => {
    if (e.key !== 'Enter') return;
    if (input.length < 3) return;
    handleSelectUser(input);
  };

  return (
    <div className='flex gap-10 items-center relative'>
      <input
        value={input}
        onKeyDown={handleEnter}
        onChange={(e) => setInput(e.target.value)}
        className='px-4 py-2 outline-none w-48 bg-transparent placeholder:text-black border-b border-black'
        placeholder='Search or create user'
      />
      <button
        disabled={input.length < 3}
        className={cn(
          'px-4 py-2 border rounded-md border-black shadow-inner disabled:opacity-50 absolute -right-20',
          input.length === 0 && 'hidden'
        )}
      >
        Enter
      </button>
    </div>
  );
}
