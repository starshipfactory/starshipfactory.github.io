# Edit mode

## Development

`jekyll build --watch --incremental` can be run inside docker with docker-compose by running `docker-compose up`. It handles rebuilds automatically with the flages provided inside `docker-compose.yml`.

## Webserver

Run a webserver inside `_site/`: `cd _site/ && python3 -m http.server`.
