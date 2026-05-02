import type { BoardClick } from "../types/game";
import { toGoCoord } from "./coordinates";
import { getBoardCssSize, getMetrics } from "./metrics";

export function nearestPoint(
  clientX: number,
  clientY: number,
  rect: DOMRect,
  boardSize: number
): BoardClick | null {
  const cssSize = getBoardCssSize(rect.width);
  const metrics = getMetrics(cssSize, boardSize);
  const x = Math.round((clientX - rect.left - metrics.pad) / metrics.cell);
  const y = Math.round((clientY - rect.top - metrics.pad) / metrics.cell);
  if (x < 0 || y < 0 || x >= boardSize || y >= boardSize) {
    return null;
  }
  return { x, y, coord: toGoCoord(x, y, boardSize) };
}
