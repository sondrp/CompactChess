import { useEffect, useState } from "react";
import { GameInfo, LegalMove } from "../types";


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

            const message = JSON.parse(event.data)
            setBoard(processGame(message["board"]))
            setTurn(extractTurn(message["board"]))
            setLegalMoves(processLegalMoves(message["legal_moves"]))
            setWhite(message["white"])
            setBlack(message["black"])
        })
      
        return () => {
          socket.close();
        };
    }, [id, username])


    return { ws, board, white, black, turn, legalMoves }
}