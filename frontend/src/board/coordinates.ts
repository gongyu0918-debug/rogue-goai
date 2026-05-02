const LETTERS = "ABCDEFGHJKLMNOPQRST";

export function toGoCoord(x: number, y: number, boardSize: number): string {
  const col = LETTERS[x] ?? "?";
  return `${col}${boardSize - y}`;
}
