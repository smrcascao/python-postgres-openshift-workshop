OpenShift Workshop
=========================

This project was developed as part of a workshop to deploy a statefull application in OpenShift / Kubernetes.


Docker build
============
``` build -t python-app . workshop-app```

Docker run
============

```docker run -it -p 5000:5000 -e POSTGRES_DB_USER=postgres -e POSTGRES_DB_PSW=mysecretpassword -e SERVICE_POSTGRES_SERVICE_HOST=localhost  -e POSTGRES_DB_NAME=workshopdb -d ```


