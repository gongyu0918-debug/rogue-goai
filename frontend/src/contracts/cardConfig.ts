export interface LocalizedText {
  zh?: string;
  en?: string;
  ja?: string;
  ko?: string;
  [locale: string]: string | undefined;
}

export interface CardPresentation {
  name?: LocalizedText | string;
  desc?: LocalizedText | string;
  description?: LocalizedText | string;
  meta?: LocalizedText | string;
  icon?: string;
  [key: string]: unknown;
}

export interface CardDefinition {
  id: string;
  enabled?: boolean;
  weight?: number;
  tier?: string;
  effect?: string;
  presentation?: CardPresentation;
  config?: Record<string, unknown>;
  [key: string]: unknown;
}

export interface CardConfigPayload {
  source: string;
  cards: {
    rogue?: CardDefinition[];
    ultimate?: CardDefinition[];
    [group: string]: CardDefinition[] | undefined;
  };
  schema?: Record<string, unknown>;
  errors: string[];
}
