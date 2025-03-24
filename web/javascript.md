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

# 对象
我们可以在创建对象的时候，立即将一些属性以键值对的形式放到 {...} 中。
```
let user = {     // 一个对象
  name: "John",  // 键 "name"，值 "John"
  age: 30,        // 键 "age"，值 30
  "likes birds": true,  // 多词属性名必须加引号
};

// 读取文件的属性：
alert( user.name ); // John
alert( user.age ); // 30


// 我们可以随时添加、删除和读取文件。
user.isAdmin = true;
delete user.age;

```

## 方括号
```
let user = {};

// 设置
user["likes birds"] = true;

// 读取
alert(user["likes birds"]); // true

// 删除
delete user["likes birds"];
```

## 计算属性
属性名从变量中提取
```
let fruit = prompt("Which fruit to buy?", "apple");

let bag = {
  [fruit]: 5, // 属性名是从 fruit 变量中得到的
};

alert( bag.apple ); // 5 如果 fruit="apple"


let fruit = 'apple';
let bag = {
  [fruit + 'Computers']: 5 // bag.appleComputers = 5
};
```
## 属性值简写
```
function makeUser(name, age) {
  return {
    name: name,
    age: age,
    // ……其他的属性
  };
}

let user = makeUser("John", 30);
alert(user.name); // John
```
在上面的例子中属性名跟变量名一样。这种通过变量生成属性的应用场景很常见，在这有一种特殊的 属性值缩写 方法，使属性名变得更短。

```
function makeUser(name, age) {
  return {
    name, // 与 name: name 相同
    age,  // 与 age: age 相同
    // ...
  };
}
```

## “in” 操作符
读取不存在的属性只会得到 undefined
```
let user = {};

alert( user.noSuchProperty === undefined ); // true 意思是没有这个属性
```
检查属性是否存在的操作符 "in"
```
let user = { name: "John", age: 30 };

alert( "age" in user ); // true，user.age 存在
alert( "blabla" in user ); // false，user.blabla 不存在。
```

## "for..in" 循环

```
for (key in object) {
  // 对此对象属性中的每个键执行的代码
}


let user = {
  name: "John",
  age: 30,
  isAdmin: true
};

for (let key in user) {
  // keys
  alert( key );  // name, age, isAdmin
  // 属性键的值
  alert( user[key] ); // John, 30, true
}
```

## 对象引用和复制
```
let user = { name: "John" };

let admin = user; // 复制引用

admin.name = 'Pete'; // 通过 "admin" 引用来修改

alert(user.name); // 'Pete'，修改能通过 "user" 引用看到
```
### 通过引用来比较
仅当两个对象为同一对象时，两者才相等。
```
let a = {};
let b = a; // 复制引用

alert( a == b ); // true，都引用同一对象
alert( a === b ); // true
```
### 克隆与合并，Object.assign
Object.assign可以克隆、合并对象
```
Object.assign(dest, [src1, src2, src3...])
```
 - 第一个参数 dest 是指目标对象。
 - 更后面的参数 src1, ..., srcN（可按需传递多个参数）是源对象。
 - 该方法将所有源对象的属性拷贝到目标对象 dest 中。换句话说，从第二个开始的所有参数的属性都被拷贝到第一个参数的对象中。
 - 调用结果返回 dest。

```
let user = { name: "John" };

let permissions1 = { canView: true };
let permissions2 = { canEdit: true };

// 将 permissions1 和 permissions2 中的所有属性都拷贝到 user 中
Object.assign(user, permissions1, permissions2);

// 现在 user = { name: "John", canView: true, canEdit: true }
```

简单克隆
```
let user = {
  name: "John",
  age: 30
};

let clone = Object.assign({}, user);
```

### 深层克隆
当属性是对其他对象的引用时，会以引用形式被拷贝，我们应该使用一个拷贝循环来检查 user[key] 的每个值，如果它是一个对象，那么也复制它的结构。这就是所谓的“深拷贝”。
```
let user = {
  name: "John",
  sizes: {
    height: 182,
    width: 50
  }
};

let clone = Object.assign({}, user);

alert( user.sizes === clone.sizes ); // true，同一个对象

// user 和 clone 分享同一个 sizes
user.sizes.width++;       // 通过其中一个改变属性值
alert(clone.sizes.width); // 51，能从另外一个获取到变更后的结果
```

## 垃圾回收

对于开发者来说，JavaScript 的内存管理是自动的、无形的。我们创建的原始值、对象、函数……这一切都会占用内存。

### 可达性（Reachability）
 - 当对象是可达状态时，它一定是存在于内存中的。
 - JavaScript 引擎监控着所有对象的状态，并删除掉那些已经不可达的。

## 对象方法，"this"
声明对象，并添加方法
```
let user = {
  name: "John",
  age: 30
};

user.sayHi = function() {
  alert("Hello!");
};

user.sayHi(); // Hello!
```

### 方法简写
```
user = {
  sayHi: function() {
    alert("Hello");
  }
};

// 方法简写看起来更好，对吧？
let user = {
  sayHi() { // 与 "sayHi: function(){...}" 一样
    alert("Hello");
  }
};
```

### 方法中的 “this”
```
let user = {
  name: "John",
  age: 30,

  sayHi() {
    // "this" 指的是“当前的对象”
    alert(this.name);
  }

};

user.sayHi(); // John
```

### “this” 不受限制

JavaScript 中的 this 可以用于任何函数，即使它不是对象的方法。

```
let user = { name: "John" };
let admin = { name: "Admin" };

function sayHi() {
  alert( this.name );
}

// 在两个对象中使用相同的函数
user.f = sayHi;
admin.f = sayHi;

// 这两个调用有不同的 this 值
// 函数内部的 "this" 是“点符号前面”的那个对象
user.f(); // John（this == user）
admin.f(); // Admin（this == admin）

admin['f'](); // Admin（使用点符号或方括号语法来访问这个方法，都没有关系。）
```

## 构造器和操作符 "new"

### 构造函数
 - 它们的命名以大写字母开头。
 - 它们只能由 "new" 操作符来执行
```
function User(name) {
  this.name = name;
  this.isAdmin = false;
}

let user = new User("Jack");

alert(user.name); // Jack
alert(user.isAdmin); // false
```
```
  function Calculator(){
    this.read = function(){
      this.a = +prompt('number A', 0);
      this.b = +prompt('number B', 0);
    }

    this.sum = function(){
      return this.a + this.b;
    }

    this.mul = function(){
      return this.a * this.b;
    }

  }
```


## 可选链 "?."
```
let user = {}; // user 没有 address 属性

alert(user.address ? user.address.street ? user.address.street.name : null : null);
```
使用可选链优雅地检查嵌套属性
```
let user = {}; // user 没有 address 属性

alert( user?.address?.street ); // undefined（不报错）
```

### 其它变体：?.()，?.[]
?.() 用于调用一个可能不存在的函数。
```
let userAdmin = {
  admin() {
    alert("I am admin");
  }
};

let userGuest = {};

userAdmin.admin?.(); // I am admin

userGuest.admin?.(); // 啥都没发生（没有这样的方法）
```

?.[] 从一个可能不存在的对象上安全地读取属性。

```
let key = "firstName";

let user1 = {
  firstName: "John"
};

let user2 = null;

alert( user1?.[key] ); // John
alert( user2?.[key] ); // undefined
```

## symbol 类型
“symbol” 值表示唯一的标识符。
```
let id1 = Symbol("id");
let id2 = Symbol("id");

alert(id1 == id2); // false
```
### “隐藏”属性
symbol 允许我们创建对象的“隐藏”属性，代码的任何其他部分都不能意外访问或重写这些属性。

```
let user = { // 属于另一个代码
  name: "John"
};

let id = Symbol("id");

user[id] = 1;

alert( user[id] ); // 我们可以使用 symbol 作为键来访问数据
```
### 全局 symbol
Symbol.for(key)会检查全局注册表，如果有一个描述为 key 的 symbol，则返回该 symbol，否则将创建一个新 symbol（Symbol(key)），并通过给定的 key 将其存储在注册表中。

```
// 从全局注册表中读取
let id = Symbol.for("id"); // 如果该 symbol 不存在，则创建它

// 再次读取（可能是在代码中的另一个位置）
let idAgain = Symbol.for("id");

// 相同的 symbol
alert( id === idAgain ); // true
```

### Symbol.keyFor
```
// 通过 name 获取 symbol
let sym = Symbol.for("name");
let sym2 = Symbol.for("id");

// 通过 symbol 获取 name
alert( Symbol.keyFor(sym) ); // name
alert( Symbol.keyFor(sym2) ); // id
```

### 系统 symbol
JavaScript 内部有很多“系统” symbol，我们可以使用它们来微调对象的各个方面。
https://tc39.github.io/ecma262/#sec-well-known-symbols
