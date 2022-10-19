# OwU

OwU is yet another stack-based language, with features heavily borrowed from [K](https://wikiless.org/wiki/K_%28programming_language%29?lang=en).

# Basic programs

## Hello world!

```
{Hello world!}.
```

In OwU, every function is a string, and vice versa, so we can simply push a function with
the string up the stack, and print it out with `.`.

## Check odd or even

```
2W%0=
```

This program takes an input on the left, then return `0` for false, and `1` for true.

It takes the input like this:

```
10 2W%0=
```

With `10` being our input.

`W` is an operator for S**W**apping the last 2 elements of the stack, then modulo the first popped element with the second popped
element. Finally push 0 to stack and check if the result is equal to 0.

## Cat program

```
I.
```

`I` takes an integer input from the user, then push the input to the stack, and we output it with `.`.

## Print invisible text, K-to-OwU version

```
Sx:x^{ }W#1+#x^,
```

Note that in this program, `#` is used with 2 different functions in 2 different places.

Here, we take a string input from the user using `S`, then store it variable `x` using `:`.
Then, we push the value of `x` to the stack with `^`, then push a string with only a whitespace.
Next, we swap the order, pushing `x` to the top, then get the length of `x` with `#`.
We then `+ 1` to that length, and duplicate the whitespace string `len(x) + 1` times, again with `#`.
Finally, we push the string to top once again, and concat the two strings on the stack together.
