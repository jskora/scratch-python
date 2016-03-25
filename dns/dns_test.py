#!/env/bin python

# ------------------------------------------------------------
# dns_test.py
# Exercise DNS requests using IPv4 and IPv6 transport
# and evaluate capture response and remdiation of SCAPY
# DNS packet bug.
# ------------------------------------------------------------
# references
# http://stackoverflow.com/questions/26433826/no-dns-layer-using-scapy-from-python-2-6
# https://bitbucket.org/secdev/scapy/issues/913/dns-responses-are-malformed-after
# https://bitbucket.org/secdev/scapy/pull-requests/18/implemented-phils-idea-to-solve-issue-913/diff
# https://en.wikipedia.org/wiki/IPv6_address
# ------------------------------------------------------------

from multiprocessing import Process
from scapy.all import sniff
from scapy.layers.inet import UDP, IP
from scapy.layers.dns import DNS
from scapy.utils import rdpcap, wrpcap
import time
import sys
import subprocess


def msg(txt):
    sys.stderr.write(txt + "\n")
    sys.stderr.flush()


def dig(four6):
    msg("dig sleeping")
    time.sleep(2)
    if four6 == "4":
        subprocess.call("dig -4 +time=1 +tries=1 @192.168.2.1 cnn.com".split(" "))
    else:
        subprocess.call("dig -6 +time=1 +tries=1 @192.168.2.1 cnn.com".split(" "))
    time.sleep(2)
    msg("dig done")


def parent(ip_version):
    msg("============================================================")
    msg("starting dig process USING IPv{}".format(ip_version))
    p = Process(target=dig, args=(ip_version, ))
    p.start()
    msg("starting sniff")
    pkts = sniff("eth0", lfilter=lambda x: (UDP in x and DNS in x), timeout=6)
    msg("sniff done, joining dig")
    p.join()

    msg("\noriginal\n----------------------------------------")
    pkts.nsummary()

    msg("\nsave and reload 1\n----------------------------------------")
    pktfile = "pkts2.pcap"
    wrpcap(pktfile, pkts)
    pkts2 = rdpcap(pktfile)
    pkts2.nsummary()

    msg("\nsave and reload 2\n----------------------------------------")
    for p in pkts:
        if IP in p:
            del(p[IP].len)
        if UDP in p:
            del(p[UDP].len)
            del(p[UDP].chksum)
    pktfile = "pkts3.pcap"
    wrpcap(pktfile, pkts)
    pkts3 = rdpcap(pktfile)
    pkts3.nsummary()
    msg("----------------------------------------\n")

if __name__ == "__main__":
    parent(4)
    parent(6)
