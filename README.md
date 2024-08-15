# Website

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

### Build

```
$ poetry build
```

This command generates static content into the `build` directory and can be served using any static contents hosting service.

