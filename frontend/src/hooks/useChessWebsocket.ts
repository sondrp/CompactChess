import { useEffect, useState } from "react";
import { ClickResult, GameInfo, LegalMove } from "../types";

// I promise I will move these processing steps to the api.
// they should not happen here
export function processGame(game: string) {
    const match = /^\S+/.exec(game);
    if (!match) return '';
    let gamestring = match[0].replace(/\//g, '');
    gamestring = gamestring.replace(/\d/g, (m) => ' '.repeat(parseInt(m)));
    return gamestring;
  }
  
  export function processLegalMoves(legalMoves: LegalMove[]): LegalMove[] {
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
  
  export const extractTurn = (fen: string) => fen.split(' ')[1];
  


  // TODO add white and black to the socket too, since that will cause changes
export function useChessWebsocket(id: string, username: string) {
    const [ws, setWs] = useState<WebSocket | null>(null)
    const [board, setBoard] = useState(" ".repeat(64))
    const [turn, setTurn] = useState("")
    const [legalMoves, setLegalMoves] = useState<LegalMove[]>([])
    const [white, setWhite] = useState("")
    const [black, setBlack] = useState("")

    useEffect(() => {
        const socket = new WebSocket(`ws://localhost:8000/ws/join/${id}/${username}`)

        socket.addEventListener('open', () => {
            setWs(socket)

        })

        // TODO : change these to check for property, not if they have the type
        socket.addEventListener('message', event => {
            const websocketMessage: Record<string, string> = JSON.parse(event.data)
  
            if (websocketMessage["type"] === "game_info") {
                const gameInfo: GameInfo = JSON.parse(websocketMessage["game_info"])
                setBoard(processGame(gameInfo.board))
                setTurn(extractTurn(gameInfo.board))
                setWhite(gameInfo.white)
                setBlack(gameInfo.black) 
              }

            if (websocketMessage["type"] === "click_result") {
              const fen: string = websocketMessage["game"]
              const legal_moves = JSON.parse(websocketMessage["legal_moves"]) 
              setTurn(extractTurn(fen))
              setBoard(processGame(fen))
              setLegalMoves(processLegalMoves(legal_moves))
            }
        })
      
        return () => {
          socket.close();
        };
    }, [id, username])


    return { ws, board, white, black, turn, legalMoves }
}