from . import analysis_class
import socket
import tldextract

print('read pcap file...')
fname = './mydump.pcap'
pa = analysis_class.PAnalyzer(fname=fname)

print('\n\ntop 10 src ip:')
print(pa.topSrcIP())

print('\n\ntop 10 dst ip:')
print(pa.topDstIP())

print('\n\nsave excel report...')
pa.excelReportIP()

print('\n\nsave word report...')
pa.wordReportIP()

print('\n\nsave traffic report...')
pa.trafficReport('sec', 'MB')

print('\n\ndns report...')
pa.dnsAnswerReport()

print('\n\ngraph...')
pa.toGraph()

print('\n\nare top 10 src ip domain\'s in top 1m alexa or top 1m cisco umbrella?')
for count, ip in pa.topSrcIP():
    try:
        name = socket.gethostbyaddr(ip)[0]
        domain = tldextract.extract(name)
        domain = '{}.{}'.format(domain.domain, domain.suffix)
        print('alexa:\t{}\t\t:\t{}'.format(domain, pa.domainInAlexa(domain)))
        print('cu   :\t{}\t\t:\t{}'.format(domain, pa.domainInAlexa(domain)))
    except Exception as e:
        print(e)

print('\n\nare top 10 src ip known to VT?')
for count, ip in pa.topSrcIP():
    try:
        pa.ipVt(ip, '70327e86bdfc4ec0551dc6d2c6107b45fa8642ad0ac423c9accb5a555b217c43')
    except Exception as e:
        print(e)

print('\n\npackets to json...')
for _ in pa.toJson(10):
    print(_)

