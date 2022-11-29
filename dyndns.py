#!/usr/bin/env python3
import CloudFlare
import argparse
import sys
import configparser
import urllib.request

if __name__ == "__main__":
    config = configparser.ConfigParser()
    CONFIG_PATH='/root/.secrets/cloudflare.ini'
    with open(CONFIG_PATH, 'r') as f:
      config_string = '[cloudflare]\n' + f.read()
    config = configparser.ConfigParser()
    config.read_string(config_string)
    external_ip = urllib.request.urlopen('https://ident.me').read().decode('utf8')
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--email", default=config['cloudflare']['dns_cloudflare_email'], required=False, help="The Cloudflare login email to use")
    parser.add_argument("-n", "--hostname", required=True, help="The hostname to update, e.g. mydyndns.mydomain.com")
    parser.add_argument("-k", "--api-key", default=config['cloudflare']['dns_cloudflare_api_key'],required=False, help="The Cloudflare global API key to use. NOTE: Domain-specific API tokens will NOT work!")
    parser.add_argument("-i", "--ip-address",default=external_ip, required=False, help="Which IP address to update the record to")
    parser.add_argument("-t", "--ttl", default=60, type=int, help="The TTL of the records in seconds (or 1 for auto)")
    args = parser.parse_args()
    # Initialize Cloudflare API client
    cf = CloudFlare.CloudFlare(
        email=args.email,
        token=args.api_key
    )
    # Get zone ID (for the domain). This is why we need the API key and the domain API token won't be sufficient
    zone = ".".join(args.hostname.split(".")[-2:]) # domain = test.mydomain.com => zone = mydomain.com
    zones = cf.zones.get(params={"name": zone})
    if len(zones) == 0:
        print(f"Could not find CloudFlare zone {zone}, please check domain {args.hostname}")
        sys.exit(2)
    zone_id = zones[0]["id"]
    # Fetch existing A record
    a_record = cf.zones.dns_records.get(zone_id, params={"name": args.hostname, "type": "A"})[0]
    # Update record & save to cloudflare
    a_record["ttl"] = args.ttl # 1 == auto
    a_record["content"] = args.ip_address
    cf.zones.dns_records.put(zone_id, a_record["id"], data=a_record)
