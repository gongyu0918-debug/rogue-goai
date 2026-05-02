import type { CardConfigPayload } from "../contracts/cardConfig";
import type { ServerStatus } from "../contracts/status";
import type { WsAction } from "../contracts/ws";

async function fetchJson<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(path, {
    headers: { Accept: "application/json", ...init?.headers },
    ...init
  });
  if (!response.ok) {
    throw new Error(`${response.status} ${response.statusText}`);
  }
  return (await response.json()) as T;
}

export function getStatus(): Promise<ServerStatus> {
  return fetchJson<ServerStatus>("/status");
}

export function getCardConfig(): Promise<CardConfigPayload> {
  return fetchJson<CardConfigPayload>("/api/card-config");
}

export function createWsUrl(gameId: string): string {
  const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
  return `${protocol}//${window.location.host}/ws/${encodeURIComponent(gameId)}`;
}

export function sendWs(socket: WebSocket, action: WsAction): void {
  if (socket.readyState === WebSocket.OPEN) {
    socket.send(JSON.stringify(action));
  }
}
