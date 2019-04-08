import subprocess
from collections import namedtuple

HostInfo = namedtuple('NetworkScanResult', ['ip', 'mac', 'info'])


def cli_exec(command, *args):
    """

    :param command:
    :param args:
    :return: tuple stdout, stderr
    """
    out = subprocess.Popen([command] + list(args),
                           stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT)
    return out.communicate()


def scan_network(interface):

    lines = cli_exec('ifconfig')[0].decode().splitlines()

    ip = None
    netmask = None

    while lines:
        if interface in lines.pop(0):
            break

    while lines:
        words = list(filter(None, map(str.strip, lines.pop(0).split(' '))))
        try:
            ip = words[words.index('inet') + 1]
        except ValueError:
            pass

        try:
            netmask = words[words.index('netmask') + 1]
        except ValueError:
            pass

    if not ip or not netmask:
        raise Exception('Failed to find network configuration for interface {}'.format(interface))

    bit_mask = {
        '255.255.255.0': 24,
        '255.255.0.0':   16,
        '255.0.0.0':      8,
    }[netmask]
    network = '.'.join(ip.split('.')[0:3] + ['0'])
    stdout, _ = cli_exec('sudo', 'arp-scan', '{}/{}'.format(network, bit_mask))
    stdout = stdout.decode().splitlines()[2:-3]
    return [HostInfo(*line.split('\t')) for line in stdout]