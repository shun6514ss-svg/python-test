// ヘルパー関数：遅延処理をPromiseでラップ
function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

// ユーザー情報を取得
async function fetchUser(userId) {
  await delay(500);
  const data = [
    { id: 1, name: "Taro", type: "standard" },
    { id: 2, name: "Hanako", type: "premium" },
    { id: 3, name: "Sachiko", type: "standard" },
  ];
  return data[userId];
}

// 注文履歴を取得
async function fetchOrders() {
  await delay(500);
  const orders = [
    { id: "o1", amount: 1000 },
    { id: "o2", amount: 2500 }
  ];
  return orders;
}

module.exports = {
  fetchUser,
  fetchOrders
};
