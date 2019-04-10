from matka.luci_api import LoginInfo, mk_section, get_all, delete_all
import time

from matka.network_utils import scan_network, HostInfo

login_info = LoginInfo('http://192.168.1.1', 'root', 'root')


def mk_name():
    return "managed{:d}".format(int(time.time()))


def set_hostname(login_info: LoginInfo, ip: str, mac: str, hostname: str) -> None:
    mk_section(login_info, 'dhcp', 'host', mk_name(), {
        'dns': '1',
        'ip': ip,
        'mac': mac,
        'name': hostname,
        'leasetime': 'infinite',
    })


def remove_hostname(login_info, hostname):
    dhcp_config = get_all(login_info, 'dhcp')
    host_section_name = match_section(dhcp_config, name=hostname)['.name']
    delete_all(login_info, 'dhcp', host_section_name)


def get_hostnames(login_info):
    return list(match_all_sections(get_all(login_info, 'dhcp'), **{'.type': 'host'}))


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
      'matka': 'wan'
    })


def match_all_sections(config, **values):
    values = values.items()
    for section in config.values():
        if values <= getattr(section, 'items', lambda: [])():
            yield section


def match_section(config, **values):
    return next(match_all_sections(config, **values))


def remove_port_forwarding(login_info, ip, src_port, dst_port):
    firewall_config = get_all(login_info, 'firewall')
    port_forwarding_section = match_section(
        firewall_config, dest_ip=str(ip), dest_port=str(dst_port), src_dport=str(src_port))
    port_forwarding_section_name = port_forwarding_section['.name']
    x=delete_all(login_info, 'firewall', port_forwarding_section_name)
    return x


def get_forwarded_ports(login_info):
    firewall_config = get_all(login_info, 'firewall')
    return list(match_all_sections(firewall_config, **{'.type': 'redirect'}))


login_info = LoginInfo('http://192.168.1.1', 'xxxxx', 'xxxxxx')
set_hostname(login_info, "192.168.1.247", "b8:27:eb:b4:f7:b2", 'dupa.lab.hs3.pl')
remove_hostname(login_info, 'dupa.lab.hs3.pl')
forward_port(login_info, '192.168.1.69', 3922, 3922)
#remove_port_forwarding(login_info, '192.168.1.69', 3922, 3922)
print(get_forwarded_ports(login_info))
print(get_hostnames(login_info))