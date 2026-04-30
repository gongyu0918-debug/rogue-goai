// Card-specific board overlay drawing.

function drawRogueMarks() {
  ctx.save();
  if (rogueSeals.length) {
    const isBlackhole = activeRogueCard === "blackhole";
    const isGolden = activeRogueCard === "golden_corner";
    const isFog = activeRogueCard === "fog";
    rogueSeals.forEach(([sx, sy]) => {
      const px = PAD + sx * CELL;
      const py = PAD + sy * CELL;
      if (isBlackhole) {
        ctx.fillStyle = "rgba(80, 0, 120, 0.22)";
        ctx.fillRect(px - CELL/2, py - CELL/2, CELL, CELL);
        ctx.fillStyle = "rgba(80, 0, 120, 0.45)";
        ctx.font = `${CELL * 0.32}px sans-serif`;
        ctx.textAlign = "center"; ctx.textBaseline = "middle";
        ctx.fillText("?", px, py);
      } else if (isGolden) {
        ctx.fillStyle = "rgba(212, 175, 55, 0.18)";
        ctx.fillRect(px - CELL/2, py - CELL/2, CELL, CELL);
        ctx.fillStyle = "rgba(212, 175, 55, 0.5)";
        ctx.font = `${CELL * 0.32}px sans-serif`;
        ctx.textAlign = "center"; ctx.textBaseline = "middle";
        ctx.fillText("?", px, py);
      } else if (isFog) {
        ctx.fillStyle = "rgba(70, 150, 210, 0.22)";
        ctx.fillRect(px - CELL/2, py - CELL/2, CELL, CELL);
        ctx.strokeStyle = "rgba(70, 150, 210, 0.45)";
        ctx.lineWidth = 1.5;
        ctx.strokeRect(px - CELL/2, py - CELL/2, CELL, CELL);
      } else {
        const r = CELL * 0.32;
        ctx.strokeStyle = "rgba(220, 40, 40, 0.85)";
        ctx.lineWidth = 2.5;
        ctx.beginPath();
        ctx.moveTo(px - r, py - r); ctx.lineTo(px + r, py + r);
        ctx.moveTo(px + r, py - r); ctx.lineTo(px - r, py + r);
        ctx.stroke();
      }
    });
  }

  if (gameState && gameState.ko_point && !reviewMode) {
    const [kx, ky] = gameState.ko_point;
    if (gameState.board[ky][kx] === 0) {
      const px = PAD + kx * CELL;
      const py = PAD + ky * CELL;
      const r = CELL * 0.18;
      ctx.fillStyle = "rgba(220, 40, 40, 0.55)";
      ctx.fillRect(px - r, py - r, r * 2, r * 2);
    }
  }

  if (activeRogueCard === "joseki_ocd" && gameState
      && gameState.rogue_joseki_targets && !gameState.rogue_joseki_done) {
    const board = getCurrentBoard();
    gameState.rogue_joseki_targets.forEach(([tx, ty]) => {
      if (board && board[ty] && board[ty][tx] !== 0) return;
      const px = PAD + tx * CELL;
      const py = PAD + ty * CELL;
      ctx.strokeStyle = "rgba(0, 200, 80, 0.7)";
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.arc(px, py, CELL * 0.38, 0, Math.PI * 2);
      ctx.stroke();
      ctx.fillStyle = "rgba(0, 200, 80, 0.15)";
      ctx.fill();
    });
  }

  if (activeRogueCard === "puppet" && gameState?.rogue_puppet_target) {
    const [tx, ty] = gameState.rogue_puppet_target;
    const board = getCurrentBoard();
    if (board && board[ty] && board[ty][tx] === 0) {
      const px = PAD + tx * CELL;
      const py = PAD + ty * CELL;
      ctx.strokeStyle = "rgba(188, 120, 255, 0.9)";
      ctx.lineWidth = 2.5;
      ctx.beginPath();
      ctx.arc(px, py, CELL * 0.34, 0, Math.PI * 2);
      ctx.stroke();
      ctx.fillStyle = "rgba(188, 120, 255, 0.18)";
      ctx.beginPath();
      ctx.arc(px, py, CELL * 0.24, 0, Math.PI * 2);
      ctx.fill();
    }
  }

  if (ultimatePlayerCard === "joseki_burst" && gameState
      && gameState.ultimate_joseki_targets && !gameState.ultimate_joseki_done) {
    const board = getCurrentBoard();
    gameState.ultimate_joseki_targets.forEach(([tx, ty]) => {
      if (board && board[ty] && board[ty][tx] === (myColor === "B" ? 1 : 2)) return;
      const px = PAD + tx * CELL;
      const py = PAD + ty * CELL;
      ctx.strokeStyle = "rgba(255, 120, 20, 0.85)";
      ctx.lineWidth = 2.5;
      ctx.beginPath();
      ctx.arc(px, py, CELL * 0.26, 0, Math.PI * 2);
      ctx.stroke();
      ctx.fillStyle = "rgba(255, 120, 20, 0.18)";
      ctx.beginPath();
      ctx.arc(px, py, CELL * 0.2, 0, Math.PI * 2);
      ctx.fill();
    });
  }

  if (aiRogueSeals.length) {
    const isAiBlackhole = activeAiRogueCard === "blackhole";
    const isAiGolden = activeAiRogueCard === "golden_corner";
    const isAiFog = activeAiRogueCard === "fog";
    aiRogueSeals.forEach(([sx, sy]) => {
      const px = PAD + sx * CELL;
      const py = PAD + sy * CELL;
      if (isAiBlackhole) {
        ctx.fillStyle = "rgba(180, 40, 60, 0.20)";
        ctx.fillRect(px - CELL/2, py - CELL/2, CELL, CELL);
      } else if (isAiGolden) {
        ctx.fillStyle = "rgba(220, 80, 80, 0.18)";
        ctx.fillRect(px - CELL/2, py - CELL/2, CELL, CELL);
      } else if (isAiFog) {
        ctx.fillStyle = "rgba(180, 90, 120, 0.22)";
        ctx.fillRect(px - CELL/2, py - CELL/2, CELL, CELL);
      }
      ctx.fillStyle = "rgba(255, 190, 190, 0.92)";
      ctx.font = `${CELL * 0.28}px sans-serif`;
      ctx.textAlign = "center";
      ctx.textBaseline = "middle";
      ctx.fillText("!", px, py);
    });
  }
  ctx.restore();
}
