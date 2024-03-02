## Input

### Rule

Using `i*2+1` or `i*2` to represent the item i has been selected or not.
For example

```
@0: a = false @1: a = true
@2: b = false @3: b = true
@4: c = false @5: c = true
```

With the raw input:

```
a b c
0 1 0
0 0 1
```

You can use the command `cd input/ && python convert.py` to parse the input. Then it will be parsed to:

```
a b c
0 3 4
1 2 5
```

### Dataset

Sample dataset:

- https://dtai.cs.kuleuven.be/CP4IM/datasets/
- http://fimi.uantwerpen.be/data/

## Run

### Build Kissat

Clone the kissat repository from
https://github.com/arminbiere/kissat

And build kissat by using command (only for the first time):

```
cd kissat
./configure && make test
```

### Run the code

For run an input with selected solution, you can using `main.py`. Show the help message:

```
python main.py -h
```

### Benchmark

```
python benchmark.py
```
