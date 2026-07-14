# レガシーコード → モダンコード リファクタリングガイド

## 📊 改善点の比較

| 項目 | レガシー | モダン | 効果 |
|------|---------|--------|------|
| **変数宣言** | `var` | `const`/`let` | スコープ安全性向上、バグ削減 |
| **非同期処理** | コールバック地獄 | async/await | 可読性向上、エラーハンドリング簡潔化 |
| **文字列連結** | `+` で結合 | テンプレートリテラル | 可読性向上 |
| **ループ処理** | 古い for文 | `reduce()` | 関数型プログラミング、簡潔性 |
| **並行処理** | 順序実行 | `Promise.all()` | パフォーマンス向上 |
| **関数設計** | 1関数で複数責任 | 単一責任の原則 | テスト容易性、再利用性 |
| **エラー処理** | 各レベルで異なる | 統一的な try-catch | 保守性向上 |
| **定数管理** | ハードコード | 定数で定義 | 変更管理が容易 |

---

## 🔄 具体的な改善例

### 1️⃣ var → const/let への変更

**レガシー:**
```javascript
var result = {};
var user = data[userId];
var orders = [...];
var totalAmount = 0;
```

**モダン:**
```javascript
const user = await fetchUser(userId);
const orders = await fetchOrders();
const totalAmount = calculateTotalAmount(orders);
```

✨ **メリット:**
- ブロックスコープで予期しない上書きを防止
- `const` で意図を明確に（変更しない値）
- var のホイスティング問題を回避

---

### 2️⃣ コールバック地獄 → async/await

**レガシー:**
```javascript
setTimeout(function() {
  // ユーザー取得
  setTimeout(function() {
    // 注文取得
    fs.writeFile('...', logText, function(err) {
      // ファイル保存
      callback(null, result);
    });
  }, 500);
}, 500);
```

**モダン:**
```javascript
async function processUserData(userId) {
  const [user, orders] = await Promise.all([
    fetchUser(userId),
    fetchOrders(),
  ]);
  await saveLog(user, discountedTotal);
  return result;
}
```

✨ **メリット:**
- コードが線形で読みやすい
- ネストが減って理解しやすい
- try-catch で一元的にエラー処理

---

### 3️⃣ 文字列連結 → テンプレートリテラル

**レガシー:**
```javascript
var logText = "User: " + user.name + ", Total: " + result.discountedTotal;
```

**モダン:**
```javascript
const logText = `User: ${user.name}, Total: ${discountedTotal}`;
```

✨ **メリット:**
- 変数の挿入が視覚的に明確
- 複雑な計算も `${}` 内に直接記述可能
- 複数行文字列も簡単

---

### 4️⃣ for文 → reduce()

**レガシー:**
```javascript
var totalAmount = 0;
for (var i = 0; i < orders.length; i++) {
  totalAmount = totalAmount + orders[i].amount;
}
```

**モダン:**
```javascript
const totalAmount = orders.reduce((total, order) => total + order.amount, 0);
```

✨ **メリット:**
- 関数型プログラミング的でモダン
- 意図が明確（合計を計算している）
- ループ変数の管理が不要

---

### 5️⃣ 順序実行 → 並行実行（Promise.all）

**レガシー:**
```javascript
// 500ms + 500ms = 1000ms かかる（順序実行）
setTimeout(function() {
  // ユーザー取得（500ms後）
  setTimeout(function() {
    // 注文取得（さらに500ms後）
  }, 500);
}, 500);
```

**モダン:**
```javascript
// 500ms で完了（並行実行）
const [user, orders] = await Promise.all([
  fetchUser(userId),      // 500ms
  fetchOrders(),          // 500ms
]);
```

✨ **メリット:**
- パフォーマンス向上（500ms → 500ms）
- 複雑な依存関係の管理が簡単

---

### 6️⃣ 単一責任の原則

**レガシー:**
```javascript
// 1つの関数が多くの責任を持つ
function processUserData(userId, callback) {
  // 責任1: ユーザー取得
  // 責任2: 注文取得
  // 責任3: 計算
  // 責任4: ファイル保存
  // 責任5: エラーハンドリング
}
```

**モダン:**
```javascript
// 各関数が1つの責任のみ
async function fetchUser(userId) { ... }        // ユーザー取得
async function fetchOrders() { ... }            // 注文取得
function calculateTotalAmount(orders) { ... }  // 計算
async function saveLog(...) { ... }            // ファイル保存
async function processUserData(userId) { ... } // 統合処理
```

✨ **メリット:**
- テストが容易（各関数を独立してテスト）
- 再利用性が高い
- 変更時の影響範囲が限定される

---

### 7️⃣ マジックナンバーの定数化

**レガシー:**
```javascript
setTimeout(function() { ... }, 500);  // 500は何の意味？
fs.writeFile('user-log.txt', ...);    // ファイル名が固定
totalAmount * 0.9;                    // 0.9は何の意味？
```

**モダン:**
```javascript
const TIMEOUT_MS = 500;
const DEFAULT_LOG_FILE = 'user-log.txt';
const PREMIUM_DISCOUNT_RATE = 0.9;

await sleep(TIMEOUT_MS);
await saveLog(user, discountedTotal, DEFAULT_LOG_FILE);
applyDiscount(totalAmount, user.type);
```

✨ **メリット:**
- 意図が明確
- 変更時に一箇所だけ修正すれば OK
- 他の開発者が理解しやすい

---

### 8️⃣ 統一的なエラーハンドリング

**レガシー:**
```javascript
fs.writeFile('user-log.txt', logText, function(err) {
  if (err) {
    console.log("Error writing file!");  // 情報が不足
    callback(err, null);
  } else {
    callback(null, result);
  }
});
```

**モダン:**
```javascript
async function processUserData(userId, logFile) {
  try {
    // ... 処理
    await saveLog(user, discountedTotal, logFile);
    return result;
  } catch (error) {
    console.error(`✗ 処理失敗: ${error.message}`);
    throw error; // 呼び出し側で処理可能に
  }
}

processUserData(userId)
  .then((data) => console.log('✓ 成功！', data))
  .catch((error) => console.error('✗ エラー:', error.message));
```

✨ **メリット:**
- 全ての非同期処理を一元的に管理
- エラーメッセージが具体的
- スタックトレースが保持される

---

## 📋 モダン版の利点のまとめ

| 観点 | 改善 |
|------|------|
| **可読性** | コールバック地獄が解消され、流れが直線的に |
| **保守性** | 関数が単一責任を持ち、変更が容易 |
| **テスト性** | 各関数が独立しており、ユニットテスト可能 |
| **パフォーマンス** | 並行実行により、実行時間が短縮 |
| **エラーハンドリング** | 一元管理で予測可能 |
| **再利用性** | 小さな関数に分割されており、他の処理で再利用可能 |

---

## 🚀 さらに改善できる点

1. **TypeScript への移行** - 型安全性の向上
2. **依存性注入（DI）** - fs モジュールをモック化可能
3. **ログライブラリ** - console.log ではなく winston や pino を使用
4. **バリデーション** - zod や yup で入力値検証
5. **テストの追加** - Jest などでユニットテスト・統合テスト
6. **設定管理** - dotenv で環境変数管理

