# WEB CRAWLER

This app crawls a website to get data, saves them to a database and exposes the data via an API.

## Environment Setup

Run docker-compose up --build in the directory to build the environment and run the app. Once the data has been crawled from the web, the APIs will be ready to be called.

```bash
docker-compose up --build
```

## Usage

Once the app is started, the web scraping commences; once that is concluded, the APIs will ready for use. The documentation can be viewed using the Swagger UI url:
 http://{HOST}:{PORT}/docs . For example:  http://0.0.0.0:8000/docs (as is the default for the app)

