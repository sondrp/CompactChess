import { ClickResult, GameInfo } from '../types';

const endpoint = 'http://localhost:8000';

export async function reset(): Promise<GameInfo> {
  const data = await fetch(`${endpoint}/reset`)
  return data.json()
}

export async function getGame(): Promise<GameInfo> {
  const data = await fetch(endpoint);
  return data.json()
}

export async function click({index, player}: {index: number, player: string}): Promise<ClickResult> {
  const turn = player === 'w' ? 'true' : 'false';
  const data = await fetch(`${endpoint}/click`, {
    headers: {
      index: index.toString(),
      white: turn,
    },
  });
  return data.json();
}
