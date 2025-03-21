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

## 基础运算符，数学运算
### 数学运算
 - +
 - -
 - *
 - /
 - %
 - **

### 用+连接字符串
 - 从左到右计算
 - 如果两个操作数都是数字，则执行数值加法。
 - 如果其中一个操作数是字符串，则执行字符串拼接。
```
alert( '1' + 2 ); // "12"
alert(2 + 2 + '1' ); // "41"，不是 "221"
alert('1' + 2 + 2); // "122"，不是 "14"
```

### 数字转化
 - 如果运算元不是数字，加号 + 则会将其转化为数字。
```
// 对数字无效
let x = 1;
alert( +x ); // 1

let y = -2;
alert( +y ); // -2

// 转化非数字
alert( +true ); // 1
alert( +"" );   // 0
```

### 赋值运算符
#### 赋值 = 返回一个值
```
let a = 1;
let b = 2;

let c = 3 - (a = b + 1); // a = b + 1 返回3

alert( a ); // 3
alert( c ); // 0
```

#### 链式赋值
```
let a, b, c;

a = b = c = 2 + 2;

alert( a ); // 4
alert( b ); // 4
alert( c ); // 4
```

### 自增/自减
 - ++
 - \--

### 位运算符
 - &
 - |
 - ^
 - ~
 - <<
 - \>>
 - \>>>
  
### 逗号运算符
```
let a = (1 + 2, 3 + 4);

alert( a ); // 7（3 + 4 的结果）
```
逗号运算符能让我们处理多个表达式，使用 , 将它们分开。每个表达式都运行了，但是只有最后一个的结果会被返回。


## 值的比较
 - 所有比较运算符均返回布尔值
 - 字符串比较根据字典序
 - 当对不同类型的值进行比较时，JavaScript 会首先将其转化为数字（number）再判定大小。
 - 关系运算符（如 >=、<=、<、>）的工作方式与 == 不同。它们会触发操作数的“抽象关系比较”（Abstract Relational Comparison），并尝试将操作数转换为原始值（primitive values），通常是数字。
 - 严格相等运算符 === 在进行比较时不会做任何的类型转换。


### 对 null 和 undefined 进行比较
```
alert( null === undefined ); // false
alert( null == undefined ); // true
```

## 条件分支：if 和 '?'
### “if” 语句
```
if (year == 2025) alert( 'You are right!' );
```
### 布尔转换
if (…) 语句会计算圆括号内的表达式，并将计算结果转换为布尔型。

### “else” 语句
```
let year = prompt('In which year was ECMAScript-2015 specification published?', '');

if (year == 2015) {
  alert( 'You guessed it right!' );
} else {
  alert( 'How can you be so wrong?' ); // 2015 以外的任何值
}
```
### 多个条件：“else if”
```
let year = prompt('In which year was ECMAScript-2015 specification published?', '');

if (year < 2015) {
  alert( 'Too early...' );
} else if (year > 2015) {
  alert( 'Too late' );
} else {
  alert( 'Exactly!' );
}
```

### 条件运算符 ‘?’
```
let result = condition ? value1 : value2;
```
if condition is true, then value1 else value2


## 逻辑运算符
 - ||（或）
 - &&（与）
 - !（非）
 - 空值合并运算符（nullish coalescing operator） '??'

a ?? b 等价于下面的语句： 当a既不是null 也不是 undefined时，返回a，否则返回b。
```
result = (a !== null && a !== undefined) ? a : b;
```

## 循环：while 和 for
 - while
```
while (condition) {
  // 代码
  // 所谓的“循环体”
}


let i = 3;
while (i) { // 当 i 变成 0 时，条件为假，循环终止
  alert( i );
  i--;
}
```
 - do..while
```
do {
  // 循环体
} while (condition);


let i = 0;
do {
  alert( i );
  i++;
} while (i < 3);
```

 - “for” 循环
```
for (begin; condition; step) {
  // ……循环体……
}

for (let i = 0; i < 3; i++) { // 结果为 0、1、2
  alert(i);
}
```


## break/continue
 - break: 跳出循环
 - conitinue：跳到下次迭代
### break/continue 标签
有时候我们需要一次从多层嵌套的循环中跳出来。
标签 是在循环之前带有冒号的标识符：
```
labelName: for (...) {
  ...
}
```
break <labelName> 语句跳出循环至标签处：
```
outer: for (let i = 0; i < 3; i++) {

  for (let j = 0; j < 3; j++) {

    let input = prompt(`Value at coords (${i},${j})`, '');

    // 如果是空字符串或被取消，则中断并跳出这两个循环。
    if (!input) break outer; // (*)

    // 用得到的值做些事……
  }
}

alert('Done!');
```

## "switch" 语句
switch 语句可以替代多个 if 判断。
```
switch(x) {
  case 'value1':  // if (x === 'value1')
    ...
    [break]

  case 'value2':  // if (x === 'value2')
    ...
    [break]

  default:
    ...
    [break]
}


let a = 2 + 2;

switch (a) {
  case 3:
    alert( 'Too small' );
    break;
  case 4:
    alert( 'Exactly!' );
    break;
  case 5:
    alert( 'Too big' );
    break;
  default:
    alert( "I don't know such values" );
}
```


## 函数
### 函数声明
```
function name(parameter1, parameter2, ... parameterN) {
  ...body...
}

function showMessage() {
  alert( 'Hello everyone!' );
}
```
### 局部变量
```
function showMessage() {
  let message = "Hello, I'm JavaScript!"; // 局部变量

  alert( message );
}

showMessage(); // Hello, I'm JavaScript!

alert( message ); // <-- 错误！变量是函数的局部变量
```
### 外部变量
```
let userName = 'John';

function showMessage() {
  let message = 'Hello, ' + userName;
  alert(message);
}

showMessage(); // Hello, John
```

### 默认值
```
function showMessage(from, text = "no text given") {
  alert( from + ": " + text );
}

showMessage("Ann"); // Ann: no text given
```

### 返回值
```
function sum(a, b) {
  return a + b;
}

let result = sum(1, 2);
alert( result ); // 3
```

### 函数命名
 - 用动词前缀, get, calc, create, check ...
  

## 函数表达式
 - 函数声明：
```
function sayHi() {
  alert( "Hello" );
}
```
 - 函数表达式
```
let sayHi = function() {
  alert( "Hello" );
};
```
上面的两个代码示例的含义是一样的：“创建一个函数并将其放入变量 sayHi 中”。

### 函数是一个值
```
function sayHi() {   // (1) 创建
  alert( "Hello" );
}

let func = sayHi;    // (2) 复制

func(); // Hello     // (3) 运行复制的值（正常运行）！
sayHi(); // Hello    //     这里也能运行（为什么不行呢）
```

### 回调函数
ask 的两个参数值 yes 和 no 可以被称为 回调函数 或简称 回调。
```
function ask(question, yes, no) {
  if (confirm(question)) yes()
  else no();
}

ask(
  "Do you agree?",
  function() { alert("You agreed."); },
  function() { alert("You canceled the execution."); }
);
```
### 函数表达式 vs 函数声明
当 JavaScript 准备 运行脚本时，首先会在脚本中寻找全局函数声明，并创建这些函数。我们可以将其视为“初始化阶段”。
 - 函数表达式是在代码执行到达时被创建，并且仅从那一刻起可用。
 - 在函数声明被定义之前，它就可以被调用。

## 箭头函数
从 => 的左侧获取参数，计算并返回右侧表达式的计算结果。
```
let func = (arg1, arg2, ..., argN) => expression;

let sum = (a, b) => a + b;
/* 这个箭头函数是下面这个函数的更短的版本：

let sum = function(a, b) {
  return a + b;
};
*/

let double = n => n * 2; //如果我们只有一个参数，还可以省略掉参数外的圆括号，使代码更短

let sayHi = () => alert("Hello!"); //如果没有参数，括号则是空的（但括号必须保留）
```

箭头函数可以像函数表达式一样使用:

```
let age = prompt("What is your age?", 18);

let welcome = (age < 18) ?
  () => alert('Hello!') :
  () => alert("Greetings!");

welcome();
```
### 多行的箭头函数
带有多行的表达式或语句, 可以使用花括号将它们括起来, 需要包含 return 才能返回值（就像常规函数一样）。
```
let sum = (a, b) => {  // 花括号表示开始一个多行函数
  let result = a + b;
  return result; // 如果我们使用了花括号，那么我们需要一个显式的 “return”
};

alert( sum(1, 2) ); // 3
```