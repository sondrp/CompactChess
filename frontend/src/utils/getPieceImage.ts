
export function getPieceImage(name: string) {
    let piece = name
    if (/[rnbqkp]/g.test(name)) {
        piece = 'b' + piece
    }
    if (/[RNBQKP]/g.test(name)) {
        piece = 'w' + piece.toLowerCase()
    }

    return new URL(`../assets/${piece}.png`, import.meta.url).href;
  }