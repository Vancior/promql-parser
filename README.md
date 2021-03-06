# PromQL(subset) parser

It can only parse a very small subset of PromQL, and add a new label selector to every metric.

checkout 5 test cases in yacc_test.py:

```shell
python3 yacc_test.py
```

dependencies:
+ [PLY](https://www.dabeaz.com/ply/)