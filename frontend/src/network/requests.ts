import { ClickResult, GameInfo, User } from '../types';

const endpoint = 'http://localhost:8000';

export async function reset(): Promise<GameInfo> {
  const data = await fetch(`${endpoint}/reset`);
  return data.json();
}

export async function getUser(username: string): Promise<User> {
  const data = await fetch(`${endpoint}/users`, {
    headers: {
      username: username,
    },
  });
  return data.json();
}

export async function getGame(id: string): Promise<GameInfo> {
  const data = await fetch(`${endpoint}/games/${id}`);
  return data.json();
}

export async function createGame({
  username,
  asWhite,
}: {
  username: string;
  asWhite: boolean;
}): Promise<GameInfo> {
  const white = asWhite ? username : 'no opponent';
  const black = asWhite ? 'no opponent' : username;
  const data = await fetch(`${endpoint}/create`, {
    headers: { white, black },
  });
  return data.json();
}

export async function join({
  id,
  color,
  username,
}: {
  id: string,
  color: string,
  username: string
}) {
  console.log(`joining ${id} as ${username}`)
  await fetch(`${endpoint}/games/join/${id}`, {
    headers: {
      color,
      username,
    }
  })
}

export async function click({
  id,
  index,
  player,
}: {
  id: string;
  index: number;
  player: string;
}): Promise<ClickResult> {
  const turn = player === 'w' ? 'true' : 'false';
  const data = await fetch(`${endpoint}/click`, {
    headers: {
      id,
      index: index.toString(),
      white: turn,
    },
  });
  return data.json();
}
