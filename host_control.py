from luci_api import LoginInfo, get_all, mk_section
import time

from network_utils import scan_network

login_info = LoginInfo('http://192.168.1.1', 'root', 'root')


def mk_name():
    return "managed{:d}".format(int(time.time()))


MAC = 'b8:27:eb:b4:f7:b2'

the_host = next(filter(lambda host: host.mac.lower() == MAC.lower(), scan_network('wlp3s0')))

mk_section(login_info, 'dhcp', 'host', mk_name(), {
    'dns': '1',
    'ip': the_host.ip,
    'mac': the_host.mac,
    'name': 'mroz.lab.hs3.pl',
    'leasetime': 'infinite',
})
