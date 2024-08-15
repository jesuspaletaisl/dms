# Application

This API is built using Python and  [Falcon Framework](https://falcon.readthedocs.io/en/stable/index.html).

### Installation

```
$ poetry install
```

### Local Development

```
$ poetry run uvicorn app:app --reload 
```

This command starts a local development server. Most changes are reflected live without having to restart the server.

### Testing

```
$ poetry run pytest --verbose tests
```

This command runs test cases locally.

