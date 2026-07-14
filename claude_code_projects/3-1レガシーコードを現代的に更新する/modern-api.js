import fs from 'fs/promises';

// 定数の定義
const TIMEOUT_MS = 500;
const PREMIUM_DISCOUNT_RATE = 0.9;
const DEFAULT_LOG_FILE = 'user-log.txt';

// ダミーデータ（実際にはデータベースから取得）
const USER_DATA = [
  { id: 1, name: 'Taro', type: 'standard' },
  { id: 2, name: 'Hanako', type: 'premium' },
  { id: 3, name: 'Sachiko', type: 'standard' },
];

const ORDER_DATA = [
  { id: 'o1', amount: 1000 },
  { id: 'o2', amount: 2500 },
];

// ユーティリティ関数
const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

// 関数の分割：単一責任の原則に従う

/**
 * ユーザー情報を取得
 * @param {number} userId
 * @returns {Promise<Object>}
 */
async function fetchUser(userId) {
  await sleep(TIMEOUT_MS);
  const user = USER_DATA[userId];
  if (!user) {
    throw new Error(`ユーザーID ${userId} が見つかりません`);
  }
  return user;
}

/**
 * 注文履歴を取得
 * @returns {Promise<Array>}
 */
async function fetchOrders() {
  await sleep(TIMEOUT_MS);
  return ORDER_DATA;
}

/**
 * 注文の合計金額を計算
 * @param {Array} orders
 * @returns {number}
 */
function calculateTotalAmount(orders) {
  return orders.reduce((total, order) => total + order.amount, 0);
}

/**
 * 割引後の金額を計算
 * @param {number} totalAmount
 * @param {string} userType
 * @returns {number}
 */
function applyDiscount(totalAmount, userType) {
  return userType === 'premium' ? totalAmount * PREMIUM_DISCOUNT_RATE : totalAmount;
}

/**
 * ログをファイルに保存
 * @param {Object} user
 * @param {number} discountedTotal
 * @param {string} logFile
 * @returns {Promise<void>}
 */
async function saveLog(user, discountedTotal, logFile = DEFAULT_LOG_FILE) {
  const logText = `User: ${user.name}, Total: ${discountedTotal}`;
  try {
    await fs.writeFile(logFile, logText, 'utf8');
    console.log('✓ ファイルに正常に書き込まれました。');
  } catch (error) {
    throw new Error(`ファイル書き込みエラー (${logFile}): ${error.message}`);
  }
}

/**
 * メイン処理：ユーザーデータを処理
 * @param {number} userId
 * @param {string} logFile
 * @returns {Promise<Object>}
 */
async function processUserData(userId, logFile = DEFAULT_LOG_FILE) {
  try {
    console.log('処理開始...');

    // 複数の非同期処理を並行実行（Promise.all）
    const [user, orders] = await Promise.all([
      fetchUser(userId),
      fetchOrders(),
    ]);

    // 計算処理
    const totalAmount = calculateTotalAmount(orders);
    const discountedTotal = applyDiscount(totalAmount, user.type);

    // ログ保存
    await saveLog(user, discountedTotal, logFile);

    // 結果をまとめる
    const result = {
      user,
      orders,
      totalAmount,
      discountedTotal,
    };

    console.log('✓ 処理完了');
    return result;
  } catch (error) {
    console.error(`✗ 処理失敗: ${error.message}`);
    throw error; // 呼び出し側でハンドリング可能にする
  }
}

// 実行
const userId = 2;
processUserData(userId)
  .then((data) => {
    console.log('✓ 成功！最終データ:', data);
  })
  .catch((error) => {
    console.error('✗ エラーが発生しました:', error.message);
    process.exit(1);
  });
