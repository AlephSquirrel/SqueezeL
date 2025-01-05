
## Codepage
|     |0|1|2|3|4|5|6|7|8|9|
|-----|-|-|-|-|-|-|-|-|-|-|
|**0**| |"|(|)|0|1|2|3|4|5|
|**1**|6|7|8|9|a|b|c|d|e|f|
|**2**|g|h|i|j|k|l|m|n|o|p|
|**3**|q|r|s|t|u|v|w|x|y|z|
## Literals
Numeric literals are simply strings of digits: `123`
If you need to put numbers next to each other, you can separate them with spaces: `1 2 3`
There is no special syntax for making lists, but you can create them with the `l` function. For example, `(l1 2 3)` returns the list `[1, 2, 3]`. 
String literals are contained between `"` characters. Since the codepage of SqueezeL is rather limited, there are a few types of escape sequence to help you out:
- Parentheses are escaped by doubling them: `((` is `(` and `))` is `)`.
- A quote character is escaped with `)"`.
- An uppercase letter is represented with `)a`, where `a` is the corresponding lowercase letter.
- Any character in the range [0...359] can be represented with a right parenthesis followed by 2 base-36 digits, like this: `)0x` -> `!`
- Any character in Unicode can be represented with a left parenthesis followed by 4 base-36 digits, like this: `(2qtb` -> `🐿`
## Symbols
A symbol can be:
- Any letter from `a` to `y`
- A digraph: `z` followed by any alphanumeric character besides `m`, `o`, or `s`
- A trigraph: `zm`, `zo`, or `zs`, followed by any alphanumeric character. These generally contain `m`ath operations, `o`ther operations, and `s`tring operations, respectively.
## EOF
Any parentheses or string literals left open at EOF are automatically closed.