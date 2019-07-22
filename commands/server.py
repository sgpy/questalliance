import logging

import click

logging.basicConfig(filename='app.log', level=logging.DEBUG)


def resolve_hosted_url(port, local=False):
    if local:
        url = "127.0.0.1"
    else:
        url = "0.0.0.0"

    hosted_url = "{}:{}".format(url, port)
    return hosted_url, url


@click.command()
@click.option('--port', type=int, default=5000, help="server port to run on")
@click.option('--backend_host_name', type=str, default="http://localhost", help="Backend server url")
@click.option('--backend_host_port', type=int, default=1234, help="Backend server port")
@click.option('--local', type=bool, is_flag=False, help="Backend server port")
def deploy_relay_server(port, backend_host_name, backend_host_port, local):
    """Starts a relay server to communicate with dialogflow server

    Default: Runs on 5000 and connects to backend http://localhost:1234
    """
    logger = logging.getLogger(__name__)

    logger.info("Deploying relay server on port: {}...".format(port))
    hosted_url, url = resolve_hosted_url(port, local=local)
    logger.info("Deployed: {}".format(hosted_url))

    logger.info("Backend Host: {} Port: {}...".format(backend_host_name, backend_host_port))
    from assets.helloworld import app
    app.run(host=url, port=port)


@click.command()
@click.option('--port', type=int, default=1234, help="server port to run on")
@click.option('--local', type=bool, is_flag=False, help="Backend server port")
def deploy_backend_server(port, local):
    """Starts a mock backend server to serve relay server

    Default: Runs on 1234
    """
    logger = logging.getLogger(__name__)
    logger.info("Deploying mock backend server on port: {}...".format(port))
    hosted_url, url = resolve_hosted_url(port, local=local)
    from backend.server import validate
    try:
        validate()
    except ValueError as e:
        logger.error("Unable to launch backend server", exc_info=e)
        return -1
    from backend.server import app
    app.run(host=url, port=port)
    logger.info("Deployed: {}".format(hosted_url))
