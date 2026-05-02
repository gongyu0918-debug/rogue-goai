import { useCallback, useEffect, useRef, useState } from "react";
import type { BoardClick, Stone } from "../types/game";
import { toGoCoord } from "./coordinates";

interface BoardCanvasProps {
  boardSize: number;
  stones: Stone[];
  onPointClick: (point: BoardClick) => void;
}

interface BoardMetrics {
  size: number;
  pad: number;
  cell: number;
}

const MAX_CANVAS_CSS_SIZE = 680;
const MIN_CANVAS_CSS_SIZE = 280;

function getMetrics(cssSize: number, boardSize: number): BoardMetrics {
  const pad = Math.max(20, Math.round(cssSize * 0.07));
  return {
    size: cssSize,
    pad,
    cell: (cssSize - pad * 2) / (boardSize - 1)
  };
}

function nearestPoint(
  clientX: number,
  clientY: number,
  rect: DOMRect,
  boardSize: number
): BoardClick | null {
  const cssSize = Math.min(MAX_CANVAS_CSS_SIZE, Math.max(MIN_CANVAS_CSS_SIZE, rect.width));
  const metrics = getMetrics(cssSize, boardSize);
  const x = Math.round((clientX - rect.left - metrics.pad) / metrics.cell);
  const y = Math.round((clientY - rect.top - metrics.pad) / metrics.cell);
  if (x < 0 || y < 0 || x >= boardSize || y >= boardSize) {
    return null;
  }
  return { x, y, coord: toGoCoord(x, y, boardSize) };
}

function drawBoard(ctx: CanvasRenderingContext2D, metrics: BoardMetrics, boardSize: number): void {
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

function drawStone(ctx: CanvasRenderingContext2D, metrics: BoardMetrics, stone: Stone): void {
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

export function BoardCanvas({ boardSize, stones, onPointClick }: BoardCanvasProps) {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const wrapRef = useRef<HTMLDivElement | null>(null);
  const [hover, setHover] = useState<BoardClick | null>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    const wrap = wrapRef.current;
    if (!canvas || !wrap) {
      return;
    }

    const draw = () => {
      const rect = wrap.getBoundingClientRect();
      const cssSize = Math.min(MAX_CANVAS_CSS_SIZE, Math.max(MIN_CANVAS_CSS_SIZE, rect.width));
      const dpr = window.devicePixelRatio || 1;
      canvas.width = Math.round(cssSize * dpr);
      canvas.height = Math.round(cssSize * dpr);
      canvas.style.width = `${cssSize}px`;
      canvas.style.height = `${cssSize}px`;

      const ctx = canvas.getContext("2d");
      if (!ctx) {
        return;
      }
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      const metrics = getMetrics(cssSize, boardSize);
      drawBoard(ctx, metrics, boardSize);
      for (const stone of stones) {
        drawStone(ctx, metrics, stone);
      }

      if (hover) {
        ctx.strokeStyle = "rgba(18, 124, 130, 0.95)";
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.arc(metrics.pad + hover.x * metrics.cell, metrics.pad + hover.y * metrics.cell, metrics.cell * 0.5, 0, Math.PI * 2);
        ctx.stroke();
      }
    };

    draw();
    const observer = new ResizeObserver(draw);
    observer.observe(wrap);
    return () => observer.disconnect();
  }, [boardSize, hover, stones]);

  const handlePointerMove = useCallback(
    (event: React.PointerEvent<HTMLCanvasElement>) => {
      const rect = event.currentTarget.getBoundingClientRect();
      setHover(nearestPoint(event.clientX, event.clientY, rect, boardSize));
    },
    [boardSize]
  );

  const handlePointerLeave = useCallback(() => {
    setHover(null);
  }, []);

  const handlePointerDown = useCallback(
    (event: React.PointerEvent<HTMLCanvasElement>) => {
      const rect = event.currentTarget.getBoundingClientRect();
      const point = nearestPoint(event.clientX, event.clientY, rect, boardSize);
      if (point) {
        onPointClick(point);
      }
    },
    [boardSize, onPointClick]
  );

  return (
    <div className="board-shell" ref={wrapRef}>
      <canvas
        aria-label="Go board preview"
        className="board-canvas"
        data-testid="react-board-canvas"
        onPointerDown={handlePointerDown}
        onPointerLeave={handlePointerLeave}
        onPointerMove={handlePointerMove}
        ref={canvasRef}
      />
    </div>
  );
}
