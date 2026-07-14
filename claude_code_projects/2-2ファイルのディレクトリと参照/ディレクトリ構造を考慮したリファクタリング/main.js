const { distance2D, average } = require('./src/math/math');
const { capitalize, truncate } = require('./src/utils/string');

function main() {
  console.log('=== Dummy App ===');

  // 数学関数の利用例
  const d = distance2D(0, 0, 3, 4);
  console.log(`distance2D((0,0)->(3,4)) = ${d}`); // 5

  const avg = average([10, 20, 30, 40]);
  console.log(`average([10,20,30,40]) = ${avg}`);

  // 文字列関数の利用例
  const title = capitalize('hello claude code');
  console.log(`capitalize(...) = ${title}`);

  const short = truncate('This is a long message for testing utilities.', 18);
  console.log(`truncate(..., 18) = ${short}`);

  // ちょっとだけ「それっぽい」統合例
  const report = `${capitalize('report')}: distance=${d.toFixed(2)}, avg=${avg.toFixed(1)}`;
  console.log(truncate(report, 40));
}

main();