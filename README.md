# _fastapi-mongo-boilerplate_

[comment]: <> ([![N|Solid]&#40;https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png&#41;]&#40;https://fastapi.tiangolo.com/&#41;)

[comment]: <> ([![N|Solid]&#40;https://webimages.mongodb.com/_com_assets/cms/kuyjf3vea2hg34taa-horizontal_default_slate_blue.svg?auto=format%252Ccompress&#41;]&#40;https://www.mongodb.com/&#41;)
## About Project
This project have been created to provide ready-to-implement solution between 
[FastAPI][src-1] and [MongoDB][src-2], regardless of area of usage.

It was meant to resolve CRUD requests to given Mongo container, that contains any possible databases.

## Build
### Docker 
To build project with docker all you need to do is run command:
```shell
docker-compose up -d 
```
You can add `--build` in case to apply your changes.

### IDE Run
In order to run with project with your IDE there are 3 steps to make this project run. But first let's get into project dir:
```shell
cd fastapi-mongo-boilerplate
```

**Step 1**: Setup MongoDB database (i.e., with docker)
```shell
docker-compose up -d app-db
```

**Step 2**: Set environment variable `API_ENV` on `development`
```shell
# Ubuntu
export API_ENV=development

# MacOS/Ubuntu
export API_ENV=development
```

**Step 3**: Run api 
```shell
# with Python
python src/app.py

# with Uvicorn
uvicorn src.app:app --host 0.0.0.0 --port 5052 --reload 
```

That's it! Now you can develop your awesome project! 

## Usage

Request usually goes in provided below schema:

    /api/{databaseName}/{collectionName}

So database as well as collections within it will be easily callable and can be defined by developer.



[src-1]: https://fastapi.tiangolo.com/
[src-2]: https://www.mongodb.com/