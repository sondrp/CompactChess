import { ClickResult, GameInfo } from '../types';

const endpoint = 'http://localhost:8000';

export async function getGame(id: string): Promise<GameInfo> {
  const data = await fetch(`${endpoint}/games/${id}`);
  return data.json();
}

export async function getGames(username: string): Promise<GameInfo[]> {
  const data = await fetch(`${endpoint}/games/user/${username}`)
  return data.json()
}

export async function createGame({white, black}: {white: string, black: string}): Promise<GameInfo> {
  const data = await fetch(`${endpoint}/create/${white}/${black}`);
  return data.json();
}

export async function join({id, username, color,}: { id: string, username: string, color: string}) {
  await fetch(`${endpoint}/games/join/${id}/${username}/${color}`);
}

export async function click({ id, username, square}: { id: string, username: string, square: number}): Promise<ClickResult> {
  const data = await fetch(`${endpoint}/games/${id}/${username}/${square}`)
  return data.json();
}
