# github-api-playground
 
# Project Title

Github API Playground

### Prerequisite

Install `pipenv`
```
https://github.com/pypa/pipenv
```


### Installing

```
pipenv sync
```

## Environment Variable

This project use `python-dotenv`, please create a `.env` file and provide following parameters.
| Name | Description | Value |
|------|----------|---------|
| `KEYWORD` | Searching keyword for Github, e.g. googleapis | String |


## Getting Started

```
pipenv shell
python main.py
```

## Optional Argument
```
python main.py --detail
```
For saving the full json data in local.
