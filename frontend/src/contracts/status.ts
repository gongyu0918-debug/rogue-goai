export interface AccessUrls {
  local: string[];
  lan: string[];
}

export interface ServerStatus {
  server_rev: string;
  host: string;
  port: number;
  access_urls: AccessUrls;
  katago_ready: boolean;
  katago_exe: boolean;
  katago_model: boolean;
  katago_model_name: string | null;
  katago_model_loaded: boolean;
  no_katago: boolean;
  cpu_mode: boolean;
  static_ready: boolean;
  card_config: string;
  card_config_errors: string[];
  engine_phase: string;
  engine_message: string;
  engine_backend: string | null;
  engine_backend_exe: string | null;
  engine_model: string | null;
  engine_last_error: string | null;
  engine_attempts: unknown[];
  engine_candidates: unknown[];
  engine_initializing: boolean;
  engine_log_tail: string[];
  nvidia_detected: boolean;
}
