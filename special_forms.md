## Special Forms
### f: lambda
Syntax: `(f [params] body*)`
Creates a lambda, where `params` is the list of parameters. Under certain circumstances, `params` can be omitted, in which case the lambda will have `x` as its only parameter. Specifically, `params` can be omitted if:
- The body only contains one item, or
- The first item in the body is not strictly a list of symbols.
### n: define/set
Syntax: `(n var1 val1 ... vark valk)`
Evaluates the `val`s, then sets the `var`s to the resulting values. Any variable names that do not already exist will be created. `valk` is also returned.
### u: for
Syntax: `(u iter-form body*)`
The first item in `iter-form` is the name of the iteration variable. What will happen depends on the other items:
- `(var n)`: loop from 0 (inclusive) to n (exclusive)
- `(var a b)`: loop from a (inclusive) to b (exclusive)
- `(var a b c)`: loop from a (inclusive) to b (exclusive) with step size c
- `(var list)`: iterate over the list
- `(var str)`: iterate over the characters of the string
### v: if/cond
Syntax: `(v test1 branch1 ... testk branchk [default])`
The first `test` that evaluates to true causes its corresponding `branch` to be evaluated. If the number of items is odd, the final item is `default`, which is evaluated if all tests are false. Otherwise, the default value is 0.
### w: while
Syntax: `(w test body*)`
Loops as long as `test` evaluates to true.