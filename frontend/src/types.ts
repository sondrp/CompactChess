export type GameInfo = {
  id: number
  board: string;
  white: string, 
  black: string
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

