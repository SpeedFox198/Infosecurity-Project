try {
    cd ./server
    hypercorn app:sio_app --certfile ../cert.pem --keyfile ../key.pem -c config.toml --reload
}
finally {
    cd ..
}
