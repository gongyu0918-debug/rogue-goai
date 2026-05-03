import { useCallback, useEffect, useRef, useState } from "react";
import type { BoardClick, Stone } from "../types/game";
import { nearestPoint } from "./input";
import { getBoardCssSize, getMetrics } from "./metrics";
import { drawBoard, drawStone } from "./renderer";

interface BoardCanvasProps {
  boardSize: number;
  stones: Stone[];
  onPointClick: (point: BoardClick) => void;
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
      const cssSize = getBoardCssSize(rect.width);
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
