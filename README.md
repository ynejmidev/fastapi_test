# fastapi_test

## run
* start the postgres database:
```sh
docker run -e POSTGRES_PASSWORD=password -v HOST/PATH/TO/DB:/var/lib/postgresql/data -p 5432:5432 -d postgres
```
<br>or, for no volume, just: <br>
```sh
docker run -e POSTGRES_PASSWORD=password -p 5432:5432 -d postgres
```
* start fastapi:<br>
```sh
fastapi run
```
* test:<br>
```sh
pytest
```
