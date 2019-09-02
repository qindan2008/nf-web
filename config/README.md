To deploy

1. Get an instance with Docker
2. add this to `/etc/docker/daemon.json`:
```angular2html
"insecure-registries" : [
    "why.docker.cgp-wr.sanger.ac.uk:5000",
    "genserv-ci.docker.cgp-wr.sanger.ac.uk:5000"
  ],
```
and restart with `sudo service docker restart`

3. `git clone https://github.com/cellgeni/nf-web.git`
4. export DOCKER_REGISTRY=why.docker.cgp-wr.sanger.ac.uk:5000
5. `cd nf-web/config && ./create-env.sh`