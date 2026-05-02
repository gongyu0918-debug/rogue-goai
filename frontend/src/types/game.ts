export type StoneColor = "black" | "white";

export interface BoardPoint {
  x: number;
  y: number;
}

export interface Stone extends BoardPoint {
  color: StoneColor;
}

export interface BoardClick extends BoardPoint {
  coord: string;
}

export interface PreviewState {
  boardSize: number;
  stones: Stone[];
  nextColor: StoneColor;
  lastClick: BoardClick | null;
  serverStatus: import("../contracts/status").ServerStatus | null;
  serverStatusError: string | null;
}

export type PreviewAction =
  | { type: "set-board-size"; size: number }
  | { type: "place-stone"; point: BoardClick }
  | { type: "clear-board" }
  | { type: "set-server-status"; status: import("../contracts/status").ServerStatus }
  | { type: "set-server-status-error"; error: string };
