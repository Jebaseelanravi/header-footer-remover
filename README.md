# Remove headers and footers


 ## Goal

* As input, your code should expect to receive a semi-formatted text file as in the few examples provided in the [`input/`](input/) directory.  
* As output, your code should print the same semi-formatted text but without header and footer lines - as far as you're able to exclude them. 

## Solution

## Functionalites implemented

1. Functionalities to remove headers and footer from the text file
2. Functionalities to remove page number both formats (Page 2 of 10 or 10)

## How to setup in your Machine

```shell

git clone git-repo

cd header-footer-remover

pip install -r requirements.txt

python main.py


```


## How to run the testcase

```shell

pytest test_main.py

```

## How to get the code coverage

```shell
coverage run -m pytest

coverage html
```

## code coverage results

[alt text](https://github.com/Jebaseelanravi/header-footer-remover/blob/main/code-coverage.png?raw=true)

