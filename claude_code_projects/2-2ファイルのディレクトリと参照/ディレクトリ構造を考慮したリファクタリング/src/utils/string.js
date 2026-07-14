/**
 * 文字列: 先頭を大文字にする（簡易）
 * @param {string} s
 * @returns {string}
 */
function capitalize(s) {
  if (typeof s !== 'string' || s.length === 0) return '';
  return s[0].toUpperCase() + s.slice(1);
}

/**
 * 文字列: 指定文字数で省略（末尾に "..."）
 * @param {string} s
 * @param {number} maxLen
 * @returns {string}
 */
function truncate(s, maxLen) {
  if (typeof s !== 'string') return '';
  if (typeof maxLen !== 'number' || maxLen <= 0) return '';
  if (s.length <= maxLen) return s;
  if (maxLen <= 3) return '.'.repeat(maxLen); // 例外的に短すぎる場合
  return s.slice(0, maxLen - 3) + '...';
}

module.exports = {
  capitalize,
  truncate,
};
