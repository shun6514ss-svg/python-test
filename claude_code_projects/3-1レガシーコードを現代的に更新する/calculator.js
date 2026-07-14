// 合計金額を計算
function calculateTotalAmount(orders) {
  return orders.reduce((sum, order) => sum + order.amount, 0);
}

// 割引後の金額を計算
function applyDiscount(totalAmount, userType) {
  if (userType === "premium") {
    return totalAmount * 0.9;
  } else {
    return totalAmount;
  }
}

module.exports = {
  calculateTotalAmount,
  applyDiscount
};
