from fastapi import APIRouter
import pkg_resources

version_router = APIRouter()

@version_router.get('/')
def get_version():
    return pkg_resources.get_distribution('zettabgp').version
