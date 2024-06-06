import { useMutation } from "@tanstack/react-query";
import { useState } from "react";
import { reset } from "../network/requests";
import { GameInfo, LegalMove, ClickResult } from "../types";
import Square from "./Square";

export function processGame(game: string) {
    const match = /^\S+/.exec(game);
    if (!match) return '';
    let gamestring = match[0].replace(/\//g, '');
    gamestring = gamestring.replace(/\d/g, (m) => ' '.repeat(parseInt(m)));
    return gamestring;
  }
  
  // Remove padding from the squares. The padding is
  // used on the backend, but not needed here.
  // This should probably be a job for the api, but oh well.
  function processLegalMoves(legalMoves: LegalMove[]): LegalMove[] {
    return legalMoves.map((m) => {
      const { result, square, id } = m;
      const row = ~~(square / 10);
      return {
        id,
        square: square - row * 2,
        result: processGame(result),
      };
    });
  }

export default function Board({ gameInfo }: { gameInfo: GameInfo }) {
    const [board, setBoard] = useState(processGame(gameInfo.board));
    const [legalMoves, setLegalMoves] = useState<LegalMove[]>([]);
  
    const { mutate } = useMutation({
      mutationFn: reset,
      onSuccess: (gameInfo) => setBoard(processGame(gameInfo.board)),
    });
  
    const handleClick = (clickResult: ClickResult) => {
      setBoard(processGame(clickResult.game));
      setLegalMoves(processLegalMoves(clickResult.legal_moves));
    };
  
    return (
      <>
        <div className='grid grid-cols-8 w-fit'>
          {Array.from({ length: 64 }).map((_, i) => (
            <Square
              legalMove={legalMoves.find((m) => m.square === i)}
              handleClick={handleClick}
              key={i}
              index={i}
              piece={board[i]}
            />
          ))}
        </div>
        <button
          onClick={() => mutate()}
          className='px-4 py-2 rounded-md bg-blue-600 text-white'
        >
          Reset
        </button>
      </>
    );
  }