const fs = require('fs');
const path = require('path');

// inventory.jsonを読み込む
const inventoryPath = path.join(__dirname, 'inventory.json');
const inventory = JSON.parse(fs.readFileSync(inventoryPath, 'utf8'));

console.log('📦 インベントリ分析\n');
console.log('='.repeat(50));

let totalValue = 0;

inventory.forEach(item => {
  const itemTotal = item.price * item.stock;
  totalValue += itemTotal;

  console.log(`商品: ${item.name}`);
  console.log(`  価格: ¥${item.price.toLocaleString()}`);
  console.log(`  在庫: ${item.stock}個`);
  console.log(`  小計: ¥${itemTotal.toLocaleString()}`);
  console.log('');
});

console.log('='.repeat(50));
console.log(`\n📊 在庫の合計金額: ¥${totalValue.toLocaleString()}`);
console.log(`合計商品数: ${inventory.length}種類`);
