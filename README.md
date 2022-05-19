OpenShift Workshop
=========================

This project was developed as part of a workshop to deploy a statefull application in OpenShift / Kubernetes.


Docker build
============
``` build -t python-app . workshop-app```

Docker run App
============

```docker run -it -p 5000:5000 -e POSTGRES_DB_USER=postgres -e POSTGRES_DB_PSW=mysecretpassword -e SERVICE_POSTGRES_SERVICE_HOST=localhost  -e POSTGRES_DB_NAME=workshopdb -e HTML_Title=Demo-APP -e backgroudColorPage=green -d docker.io/library/smrcascao/workshop```

***More environment variables:***

| Environment Variable Name  | Type  | Description |
|---|---|---|
|STATIC_DIR_BASE_URL   |  STR | Static files (CSS, js)  |
|TEMPLATES_DIR_BASE_URL   |   STR|templates folder (Index.html, success.html) |
|BASE_URL   | STR | Base URL example:  "www.domain.com/service"  |
|backgroudColorPage | STR | Change background color (green, blue, red) |


Docker run postgres data base
============


```docker run --name some-postgres -e POSTGRES_PASSWORD=mysecretpassword -e POSTGRES_USER=postgres -e POSTGRES_DB=workshopdb -p 5432:5432 -d docker.io/library/postgres:10.15-alpine ```
