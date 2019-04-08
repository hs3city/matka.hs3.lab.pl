from luci_api import LoginInfo, mk_section, get_all
import time

from network_utils import scan_network, HostInfo

login_info = LoginInfo('http://192.168.1.1', 'root', 'root')


def mk_name():
    return "managed{:d}".format(int(time.time()))


def set_hostname(login_info: LoginInfo, host_info: HostInfo, hostname: str) -> None:
    mk_section(login_info, 'dhcp', 'host', mk_name(), {
        'dns': '1',
        'ip': host_info.ip,
        'mac': host_info.mac,
        'name': hostname,
        'leasetime': 'infinite',
    })


def forward_port(login_info, ip, src_port, dst_port):
    name = mk_name()
    return mk_section(login_info, 'firewall', 'redirect', name, {
      'src_dport': src_port,
      'dest_ip': ip,
      'dest_port': dst_port,
      'name': name,
      'target': 'DNAT',
      'proto': 'tcp udp',
      'dest': 'lan',
      'src': 'wan'
    })

