# OO-2019-BUAA

本仓库**不包含**OO作业代码。

根据相关规定，OO作业代码**不允许**公布。

BUAA Object Oriented homework tools

## LICENSE

MIT License

## Tools

### Checkstyle

Python frontend for Checkstyle that checks all Java projects in the specified directory

#### Usage

```shell
usage: checkstyle.py [-h] [--jar JAR] [--config CONFIG] directory

positional arguments:
  directory        root directory that contains the projects

optional arguments:
  -h, --help       show this help message and exit
  --jar JAR        Checkstyle JAR file
  --config CONFIG  specifies the location of the file that defines the
                   configuration modules.
```

#### Example

Path:

oo_2019_homework/homework_1/src/A.java

oo_2019_homework/homework_2/src/B.java

How to run:

```bash
python checkstyle.py --jar checkstyle-8.12-all.jar --config config.xml oo_2019_homework
```

## Data generator

### Homework 10

#### Requirements

numpy

#### Usage

```bash
python gen_10.py > in.txt
```
