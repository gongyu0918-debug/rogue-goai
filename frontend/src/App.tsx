import { useCallback, useEffect, useReducer } from "react";
import { getStatus } from "./api/client";
import { BoardCanvas } from "./board/BoardCanvas";
import { initialPreviewState, previewReducer } from "./state/previewReducer";
import type { BoardClick } from "./types/game";

const BOARD_SIZES = [9, 13, 19] as const;

export function App() {
  const [state, dispatch] = useReducer(previewReducer, initialPreviewState);

  useEffect(() => {
    let cancelled = false;
    getStatus()
      .then((status) => {
        if (!cancelled) {
          dispatch({ type: "set-server-status", status });
        }
      })
      .catch((error: unknown) => {
        if (!cancelled) {
          dispatch({
            type: "set-server-status-error",
            error: error instanceof Error ? error.message : String(error)
          });
        }
      });
    return () => {
      cancelled = true;
    };
  }, []);

  const handlePointClick = useCallback((point: BoardClick) => {
    dispatch({ type: "place-stone", point });
  }, []);

  return (
    <main className="app">
      <section className="topbar">
        <div>
          <p className="eyebrow">React/TypeScript preview</p>
          <h1>rogue-go-arena</h1>
        </div>
        <div className="build-note" data-testid="preview-route">
          /react-preview
        </div>
      </section>

      <section className="workspace">
        <BoardCanvas
          boardSize={state.boardSize}
          onPointClick={handlePointClick}
          stones={state.stones}
        />
        <aside className="side-panel" aria-label="Preview controls">
          <div className="panel-section">
            <h2>Board</h2>
            <div className="segmented" aria-label="Board size">
              {BOARD_SIZES.map((size) => (
                <button
                  className={state.boardSize === size ? "active" : ""}
                  key={size}
                  onClick={() => dispatch({ type: "set-board-size", size })}
                  type="button"
                >
                  {size}x{size}
                </button>
              ))}
            </div>
          </div>

          <div className="panel-section">
            <h2>State Probe</h2>
            <dl className="probe-list">
              <div>
                <dt>Next</dt>
                <dd data-testid="next-color">{state.nextColor}</dd>
              </div>
              <div>
                <dt>Stones</dt>
                <dd data-testid="stone-count">{state.stones.length}</dd>
              </div>
              <div>
                <dt>Last</dt>
                <dd data-testid="last-click">{state.lastClick?.coord ?? "none"}</dd>
              </div>
            </dl>
          </div>

          <div className="panel-section">
            <h2>Server Contract</h2>
            <dl className="probe-list">
              <div>
                <dt>Revision</dt>
                <dd data-testid="server-revision">{state.serverStatus?.server_rev ?? "pending"}</dd>
              </div>
              <div>
                <dt>Engine</dt>
                <dd data-testid="engine-phase">{state.serverStatus?.engine_phase ?? "pending"}</dd>
              </div>
            </dl>
            {state.serverStatusError ? (
              <p className="error-text" data-testid="server-status-error">
                {state.serverStatusError}
              </p>
            ) : null}
          </div>

          <div className="panel-section">
            <h2>Migration Boundary</h2>
            <p>
              This preview validates the React canvas shell and reducer state while the legacy
              app remains the production root.
            </p>
            <button className="secondary" onClick={() => dispatch({ type: "clear-board" })} type="button">
              Clear stones
            </button>
          </div>
        </aside>
      </section>
    </main>
  );
}
