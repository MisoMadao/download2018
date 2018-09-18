import dns.resolver
import argparse

# Nslookup like script, using dnspython
# Here we can choose which record to query
# run this script with a domain as argument and --query to choose the record
#
# This way is much easier than the previous one
#
# References about the dnspython module
# http://www.dnspython.org/


def nslookup(element, query):
    r = dns.resolver.query(element, query)
    for _ in r:
        print(_)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('name')
    parser.add_argument('--query', default='A', required=False)
    args = parser.parse_args()
    nslookup(args.name, args.query)
