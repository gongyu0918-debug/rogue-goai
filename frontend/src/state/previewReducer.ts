import type { PreviewAction, PreviewState, Stone } from "../types/game";

export const initialPreviewState: PreviewState = {
  boardSize: 19,
  stones: [
    { x: 3, y: 3, color: "black" },
    { x: 15, y: 15, color: "white" },
    { x: 3, y: 15, color: "black" },
    { x: 15, y: 3, color: "white" }
  ],
  nextColor: "black",
  lastClick: null,
  serverStatus: null,
  serverStatusError: null
};

export function previewReducer(state: PreviewState, action: PreviewAction): PreviewState {
  switch (action.type) {
    case "set-board-size":
      return {
        ...state,
        boardSize: action.size,
        stones: initialPreviewState.stones.filter((stone) => stone.x < action.size && stone.y < action.size),
        nextColor: "black",
        lastClick: null
      };
    case "place-stone": {
      const existing = state.stones.find(
        (stone) => stone.x === action.point.x && stone.y === action.point.y
      );
      const stones = existing
        ? state.stones.map((stone): Stone =>
            stone.x === action.point.x && stone.y === action.point.y
              ? { ...stone, color: state.nextColor }
              : stone
          )
        : [...state.stones, { ...action.point, color: state.nextColor }];
      return {
        ...state,
        stones,
        lastClick: action.point,
        nextColor: state.nextColor === "black" ? "white" : "black"
      };
    }
    case "clear-board":
      return {
        ...state,
        stones: [],
        nextColor: "black",
        lastClick: null
      };
    case "set-server-status":
      return {
        ...state,
        serverStatus: action.status,
        serverStatusError: null
      };
    case "set-server-status-error":
      return {
        ...state,
        serverStatus: null,
        serverStatusError: action.error
      };
    default:
      return state;
  }
}
