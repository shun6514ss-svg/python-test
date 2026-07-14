/**
 * 数学: 2点間の距離（ユークリッド距離）
 * @param {number} x1
 * @param {number} y1
 * @param {number} x2
 * @param {number} y2
 * @returns {number}
 */
function distance2D(x1, y1, x2, y2) {
  const dx = x2 - x1;
  const dy = y2 - y1;
  return Math.sqrt(dx * dx + dy * dy);
}

/**
 * 数学: 配列の平均値
 * @param {number[]} nums
 * @returns {number}
 */
function average(nums) {
  if (!Array.isArray(nums) || nums.length === 0) return 0;
  const sum = nums.reduce((acc, n) => acc + n, 0);
  return sum / nums.length;
}

module.exports = {
  distance2D,
  average,
};
