# fastapi_test

## run
* start the postgres database:
```docker run -e POSTGRES_PASSWORD=password -v HOST/PATH/TO/DB:/var/lib/postgresql/data -p 5432:5432 -d postgres```
<br>or, for no volume, just: <br>
```docker run -e POSTGRES_PASSWORD=password -p 5432:5432 -d postgres```
* start fastapi:<br>
```fastapi run```
