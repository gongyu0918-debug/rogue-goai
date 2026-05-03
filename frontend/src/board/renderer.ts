import type { Stone } from "../types/game";
import type { BoardMetrics } from "./metrics";

export function drawBoard(ctx: CanvasRenderingContext2D, metrics: BoardMetrics, boardSize: number): void {
  const { size, pad, cell } = metrics;
  const boardGradient = ctx.createLinearGradient(0, 0, size, size);
  boardGradient.addColorStop(0, "#c99d56");
  boardGradient.addColorStop(0.52, "#e4bd73");
  boardGradient.addColorStop(1, "#9c6b35");
  ctx.fillStyle = boardGradient;
  ctx.fillRect(0, 0, size, size);

  ctx.fillStyle = "rgba(72, 38, 12, 0.16)";
  for (let i = 0; i < 26; i += 1) {
    const y = (i / 26) * size;
    ctx.fillRect(0, y, size, 1);
  }

  ctx.strokeStyle = "rgba(47, 24, 6, 0.82)";
  ctx.lineWidth = 1.2;
  for (let i = 0; i < boardSize; i += 1) {
    const p = pad + i * cell;
    ctx.beginPath();
    ctx.moveTo(p, pad);
    ctx.lineTo(p, size - pad);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(pad, p);
    ctx.lineTo(size - pad, p);
    ctx.stroke();
  }

  const hoshi = boardSize === 19 ? [3, 9, 15] : boardSize === 13 ? [3, 6, 9] : [2, 4, 6];
  ctx.fillStyle = "rgba(47, 24, 6, 0.9)";
  for (const x of hoshi) {
    for (const y of hoshi) {
      ctx.beginPath();
      ctx.arc(pad + x * cell, pad + y * cell, Math.max(2.5, cell * 0.08), 0, Math.PI * 2);
      ctx.fill();
    }
  }
}

export function drawStone(ctx: CanvasRenderingContext2D, metrics: BoardMetrics, stone: Stone): void {
  const { pad, cell } = metrics;
  const cx = pad + stone.x * cell;
  const cy = pad + stone.y * cell;
  const radius = cell * 0.43;
  const gradient = ctx.createRadialGradient(
    cx - radius * 0.35,
    cy - radius * 0.45,
    radius * 0.1,
    cx,
    cy,
    radius
  );

  if (stone.color === "black") {
    gradient.addColorStop(0, "#56504a");
    gradient.addColorStop(0.42, "#181612");
    gradient.addColorStop(1, "#050403");
  } else {
    gradient.addColorStop(0, "#ffffff");
    gradient.addColorStop(0.55, "#ded8cf");
    gradient.addColorStop(1, "#9f978d");
  }

  ctx.fillStyle = "rgba(0, 0, 0, 0.24)";
  ctx.beginPath();
  ctx.ellipse(cx + radius * 0.1, cy + radius * 0.14, radius * 0.96, radius * 0.84, 0, 0, Math.PI * 2);
  ctx.fill();

  ctx.fillStyle = gradient;
  ctx.beginPath();
  ctx.arc(cx, cy, radius, 0, Math.PI * 2);
  ctx.fill();
}
