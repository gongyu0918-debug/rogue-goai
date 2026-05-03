export interface BoardMetrics {
  size: number;
  pad: number;
  cell: number;
}

export const MAX_CANVAS_CSS_SIZE = 680;
export const MIN_CANVAS_CSS_SIZE = 280;

export function getBoardCssSize(width: number): number {
  return Math.min(MAX_CANVAS_CSS_SIZE, Math.max(MIN_CANVAS_CSS_SIZE, width));
}

export function getMetrics(cssSize: number, boardSize: number): BoardMetrics {
  const pad = Math.max(20, Math.round(cssSize * 0.07));
  return {
    size: cssSize,
    pad,
    cell: (cssSize - pad * 2) / (boardSize - 1)
  };
}
