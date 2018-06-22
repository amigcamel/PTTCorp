# PTTCorp

## Deploy
    MONGODB_HOST=<mongodb host> MONGODB_PORT=<mongodb port> uwsgi --master --http 0.0.0.0:8002 --module PTTCorp.wsgi --static-map /static_pttcorp=static_pttcorp --process 4 --manage-script-name --mount=/pttcorp=PTTCorp/wsgi.py
