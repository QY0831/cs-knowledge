# 基础知识
## 变量
 - 驼峰命名
 - var定义变量
 - const定义常量
'''
let num = 5;
let myName = "Joe";
const AGE = 18;
'''

## 数据类型
### Number
 - 代表整数和浮点数。
 - 特殊数值: Infinity, -Infinity, NaN

### BigInt
 - 比number类型存储更大范围的整数 (大于2\*\*53-1的 或 小于 -(2\*\*53-1))
  
### String
 - "",'',``都可以
 - ``支持嵌入变量或表达式（与python fstring一样）
```
let name = "John";

// 嵌入一个变量
alert( `Hello, ${name}!` ); // Hello, John!

// 嵌入一个表达式
alert( `the result is ${1 + 2}` ); // the result is 3
```

### Boolean
 - true or false

### null
 - 表示一个未知的值

### undefined
 - 如果一个变量已被声明，但未被赋值，那么它的值就是 undefined
```
let age;

alert(age); // 弹出 "undefined"
```

### Object, Symbol
 - object 用于储存数据集合和更复杂的实体 (对象)
 - symbol 类型用于创建对象的唯一标识符

### typeof 运算符
```
typeof undefined // "undefined"

typeof 0 // "number"

typeof 10n // "bigint"

typeof true // "boolean"

typeof "foo" // "string"

typeof Symbol("id") // "symbol"

typeof Math // "object"  (1)

typeof null // "object"  (2)

typeof alert // "function"  (3)
```

## 交互
### alert
弹出一条消息，等待用户确认。
```
alert("Hello");
```
### prompt
```
result = prompt(title, [default]);
```
浏览器会显示一个带有文本消息的模态窗口，还有 input 框和确定/取消按钮。
 - title: 显示给用户的文本
 - default: input框的初始值

```
let age = prompt('How old are you?', 100);

alert(`You are ${age} years old!`); // You are 100 years old!
```

### confirm
```
result = confirm(question);
```
confirm 函数显示一个带有 question 以及确定和取消两个按钮的模态窗口。  
点击确定返回 true，点击取消返回 false。

```
let isBoss = confirm("Are you the boss?");

alert( isBoss ); // 如果“确定”按钮被按下，则显示 true
```

## 类型转换
### 字符串转换
```
let value = 123; // 123
value = String(value); // "123"
```
### 数字型转换
在算术函数和表达式中，会自动进行 number 类型转换。
```
alert( "6" / "2" ); // 3, string 类型的值被自动转换成 number 类型后进行计算
```
也可以使用 Number(value) 显式地将这个 value 转换为 number 类型。
```
let str = "123";
alert(typeof str); // string

let num = Number(str); // 变成 number 类型 123

alert(typeof num); // number
```
转换失败时，转换结果会是NaN
```
let age = Number("xxxx")
```

### 布尔型转换
 - 直观上为“空”的值（如 0、空字符串、null、undefined 和 NaN）将变为 false
 - 其他值变成 true。
```
alert( Boolean(1) ); // true
alert( Boolean(0) ); // false

alert( Boolean("hello") ); // true
alert( Boolean("") ); // false
```
