export type GameInfo = {
  game: string;
};

export type LegalMove = {
  square: number,
  result: string,
  id: string
}

export type ClickResult = {
  game: string,
  legal_moves: LegalMove[]
}