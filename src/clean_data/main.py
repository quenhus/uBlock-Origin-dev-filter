from collections import defaultdict
from pathlib import Path
from typing import Any, NamedTuple
from dns.resolver import Resolver, NoAnswer, NXDOMAIN, LifetimeTimeout, NoNameservers
from dns.rdatatype import RdataType
from time import sleep

import logging

NEW_LINE = "\n"
DNS_SERVER = ["1.1.1.1"]
DNS_SLEEP = 0.1

################################################
#
#                 DNS helpers
#
################################################

def domain_has_ip(resolver, domain):
    """ Return true if the domain has at least one IP (IPv4 or IPv6)"""
    len_dns_a = 0
    len_dns_aaaa = 0
    try:
        dns_response = resolver.resolve(domain, RdataType.A)
        len_dns_a = len(dns_response.rrset)
    except (NoAnswer, NXDOMAIN, LifetimeTimeout, NoNameservers) as e:
        # No response for this domain
        pass

    try:
        dns_response = resolver.resolve(domain, RdataType.AAAA)
        len_dns_aaaa = len(dns_response.rrset)
    except (NoAnswer, NXDOMAIN, LifetimeTimeout, NoNameservers) as e:
        # No response for this domain
        pass

    return len_dns_a + len_dns_aaaa > 0


################################################
#
#                       DEBUG
#
################################################

# For offline debugging
STUB_DNS = False

if STUB_DNS:
    def domain_has_ip(*args, **kwargs):
        from random import random
        return random() < 0.9

################################################
#
#               Markdown helpers
#p
################################################

def md_link(content: str, href: str):
    return f"[{content}]({href})"

def md_tr(*td: str):
    return "|".join(("", *td, "")) + NEW_LINE


################################################
#
#                     Main
#
################################################

class CleanResult(NamedTuple):
    url_filter: str
    domain: str
    has_ip: bool


def main():
    root_path = Path(__file__).parent.joinpath("../../").resolve()
    report_path = root_path.joinpath("src", "clean_data", "clean-report.md")

    resolver = Resolver(configure=False)
    resolver.nameservers = DNS_SERVER

    clean_result_per_file = defaultdict(list)

    for source_f in sorted(root_path.joinpath("data").glob("np*.txt")):
        with source_f.open("r") as source_fd:
            for line in source_fd:
                    if line.startswith("!") or not line.strip():
                        continue
                    url_filter = line.strip()
                    domain = url_filter.replace("*://", "").split("/", 1)[0]

                    url_list = []
                    if domain.startswith("*."):
                        url_list.append(domain.replace("*.", "www."))
                        domain = domain.replace("*.", "")
                    url_list.append(domain)

                    logging.info("Try resolve %s", domain)

                    this_domain_has_ip = any(domain_has_ip(resolver, u) for u in url_list)
                    clean_result_per_file[source_f.name].append(CleanResult(
                        url_filter,
                        domain,
                        this_domain_has_ip
                    ))

                    sleep(DNS_SLEEP)

    # Delete old report
    report_path.unlink(missing_ok=True)

    with report_path.open("w", encoding="utf8") as report_fd:
        report_fd.write(f"# Data cleaning report" + NEW_LINE + NEW_LINE)

        for file, clean_result_list in clean_result_per_file.items():
            report_fd.write(f"## Domains in `{file}`" + NEW_LINE*2)

            report_fd.write(md_tr("domain", "has_ip", "Google site:", "DDG site:"))
            report_fd.write(md_tr("---", ":---:", "---", "---"))

            clean_result: CleanResult
            for clean_result in clean_result_list:
                report_fd.write(md_tr(
                    md_link(clean_result.url_filter, f"//{clean_result.domain}"),
                    "" if clean_result.has_ip else "❌",
                    md_link("Search 🔎", f"https://www.google.com/search?q=site%3A{clean_result.domain}"),
                    md_link("Search 🔎", f"https://duckduckgo.com/?q=site%3A{clean_result.domain}")
                ))


if __name__ == "__main__":
    logging.basicConfig()
    logging.getLogger().setLevel(logging.INFO)

    main()