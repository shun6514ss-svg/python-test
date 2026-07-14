const fs = require('fs');
const { writeFile } = fs.promises;
const { fetchUser, fetchOrders } = require('./dataFetcher');
const { calculateTotalAmount, applyDiscount } = require('./calculator');

async function processUserData(userId) {
  const result = {};

  // 1. ユーザー情報と注文履歴を取得
  const user = await fetchUser(userId);
  result.user = user;

  const orders = await fetchOrders();
  result.orders = orders;

  // 2. 金額を計算
  const totalAmount = calculateTotalAmount(orders);
  result.totalAmount = totalAmount;

  // 3. 割引を適用
  result.discountedTotal = applyDiscount(totalAmount, user.type);

  // 4. 結果をファイルに保存
  const logText = `User: ${user.name}, Total: ${result.discountedTotal}`;
  try {
    await writeFile('user-log.txt', logText);
    console.log("File written successfully.");
  } catch (err) {
    console.log("Error writing file!");
    throw err;
  }

  return result;
}

// 実行部分
(async () => {
  console.log("Processing started...");
  const id = 2; // ユーザーIDを指定
  try {
    const data = await processUserData(id);
    console.log("Success! Final Data:", data);
  } catch (err) {
    console.error("Failed:", err);
  }
})();
