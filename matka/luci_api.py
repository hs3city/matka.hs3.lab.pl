from matka.luci_rpc_client import connect, disconnect, request, apply, ApiConnection
from typing import Sequence, Mapping, Generic, TypeVar
from collections import namedtuple


JsonRpcResponse = Generic[TypeVar(Sequence), TypeVar(Mapping)]


LoginInfo = namedtuple('LoginInfo', ['uri', 'username', 'password'])


def connected(method):
    def wrapper(login_info: LoginInfo, *args, **kwargs):
        connection = connect(*login_info)
        try:
            return method(connection, *args, **kwargs)
        finally:
            disconnect(connection)
    return wrapper


def auto_apply(method):
    def _apply(connection, *args, **kwargs):
        rsp = method(connection, *args, **kwargs)
        apply(connection)
        return rsp
    return _apply


@connected
def get_all(connection: ApiConnection, config: str, section: str = None) -> dict:
    """Get all sections of a config or all values of a section.
    :param connection:
    :param config:UCI config name
    :param section:[optional] UCI section name
    :return: JSON RPC response result
    """
    return request(connection, 'uci', 'get_all', config, section)


@connected
@auto_apply
def delete_all(connection, config, section):
    return request(connection, 'uci', 'delete', config, section)


@connected
@auto_apply
def mk_section(connection, section, section_type, name, values):
    return request(connection, 'uci', 'section', section, section_type, name, values)
