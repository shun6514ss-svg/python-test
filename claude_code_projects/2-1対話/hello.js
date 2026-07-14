const fs = require("fs");

// config.jsonから設定を読み込む
const config = JSON.parse(fs.readFileSync("config.json", "utf8"));
const language = config.language;

const now = new Date();
const hour = now.getHours();

// 時間帯に応じた挨拶を取得
let timeOfDay;
const timeRanges = config.timeRanges;
if (hour >= timeRanges.night.start && hour < timeRanges.night.end) {
  timeOfDay = "night";
} else if (hour >= timeRanges.morning.start && hour < timeRanges.morning.end) {
  timeOfDay = "morning";
} else if (hour >= timeRanges.afternoon.start && hour < timeRanges.afternoon.end) {
  timeOfDay = "afternoon";
} else {
  timeOfDay = "evening";
}

const greeting = config.greetings[language][timeOfDay];

// ロケールを言語設定に応じて決定
const locale = language === "ja" ? "ja-JP" : "en-US";
const dateStr = now.toLocaleDateString(locale, {
  year: "numeric",
  month: "long",
  day: "numeric",
  weekday: "long",
});
const timeStr = now.toLocaleTimeString(locale);

console.log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");
console.log(`📅 今日の日付: ${dateStr}`);
console.log(`🕐 現在時刻: ${timeStr}`);
console.log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");
console.log(`\n${greeting}\n`);
