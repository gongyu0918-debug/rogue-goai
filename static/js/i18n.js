// Language selection, locale packs, and small localization helpers.

function normalizeLang(lang) {
  const raw = String(lang || "").trim().toLowerCase();
  if (raw.startsWith("ja")) return "ja";
  if (raw.startsWith("ko") || raw.startsWith("kr")) return "ko";
  if (raw.startsWith("en")) return "en";
  return "zh";
}

const urlLang = new URLSearchParams(window.location.search).get("lang");
let currentLang = normalizeLang(urlLang || localStorage.getItem("rogue_go_arena_lang") || navigator.language || "zh");
const LOCALE_FILES = {
  zh: "zh-CN.json",
  en: "en-US.json",
  ja: "ja-JP.json",
  ko: "ko-KR.json",
};
const localeCache = {};

function activeLocalePack() {
  return localeCache[currentLang] || localeCache.zh || null;
}

function fallbackLocalePack() {
  return localeCache.zh || activeLocalePack();
}

function escapeHtml(value) {
  return String(value ?? "").replace(/[&<>"']/g, char => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#039;",
  })[char]);
}

async function loadLocalePack(lang) {
  const normalized = normalizeLang(lang);
  if (localeCache[normalized]) return localeCache[normalized];
  const file = LOCALE_FILES[normalized] || LOCALE_FILES.zh;
  const response = await fetch("/static/locales/" + file + "?v=20260428b", { cache: "no-cache" });
  if (!response.ok) throw new Error("Failed to load locale " + file + ": " + response.status);
  const pack = await response.json();
  localeCache[normalized] = pack;
  return pack;
}

async function ensureLocale(lang = currentLang) {
  try {
    await loadLocalePack("zh");
    const normalized = normalizeLang(lang);
    if (normalized !== "zh") await loadLocalePack(normalized);
  } catch (err) {
    console.warn("[i18n] locale loading failed", err);
  }
}

function localizedValue(zh, en, ja, ko) {
  const packValue = activeLocalePack()?.phrases?.[zh];
  if (packValue !== undefined) return packValue;
  if (currentLang === "en") return en ?? zh;
  if (currentLang === "ja") return ja ?? zh;
  if (currentLang === "ko") return ko ?? zh;
  return fallbackLocalePack()?.phrases?.[zh] ?? zh;
}

function ui(zh, en, ja, ko) {
  return localizedValue(zh, en, ja, ko);
}

function langObjectValue(value) {
  if (!value || typeof value !== "object") return value || "";
  return value[currentLang] ?? value.zh ?? value.en ?? "";
}

function rankLabel(rankId) {
  if (!rankId) return "";
  const kyuMatch = String(rankId).match(/^(\d+)k$/);
  if (kyuMatch) {
    const n = kyuMatch[1];
    if (currentLang === "en") return `${n} kyu`;
    if (currentLang === "ja") return `${n}級`;
    if (currentLang === "ko") return `${n}급`;
    return `${n}级`;
  }
  const amaMatch = String(rankId).match(/^a(\d+)d$/);
  if (amaMatch) {
    const n = amaMatch[1];
    if (currentLang === "en") return `Amateur ${n} dan`;
    if (currentLang === "ja") return `アマ${n}段`;
    if (currentLang === "ko") return `아마 ${n}단`;
    return `业余${n}段`;
  }
  const proMatch = String(rankId).match(/^p(\d+)d$/);
  if (proMatch) {
    const n = proMatch[1];
    if (currentLang === "en") return `Pro ${n} dan`;
    if (currentLang === "ja") return `プロ${n}段`;
    if (currentLang === "ko") return `프로 ${n}단`;
    return ["职业一段","职业二段","职业三段","职业四段","职业五段","职业六段","职业七段","职业八段","职业九段"][Number(n) - 1] || rankId;
  }
  return RANK_LABELS[rankId] || rankId;
}

function rankGroupLabel(label) {
  const groups = activeLocalePack()?.rankGroups || fallbackLocalePack()?.rankGroups || {};
  if (label.includes("级位")) return groups.kyu || label;
  if (label.includes("业余")) return groups.amateur || label;
  if (label.includes("职业")) return groups.pro || label;
  return label;
}

async function setLanguage(lang) {
  closeWoodSelectMenu();
  currentLang = normalizeLang(lang);
  localStorage.setItem("rogue_go_arena_lang", currentLang);
  await ensureLocale(currentLang);
  applyLanguage();
}
