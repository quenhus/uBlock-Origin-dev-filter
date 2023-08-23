from pathlib import Path
from contextlib import ExitStack
from functools import lru_cache


LINE_SEP = "\n"
COMMA_SEP = ","

SOURCE_DATA_PATH = Path("./data")
DEST_DATA_PATH = Path("./dist")
OTHER_FORMAT_DATA_PATH = DEST_DATA_PATH.joinpath("./other_format/")


def left_replace(input_str, old, new, count=1):
    return new.join(input_str.split(old, count))
def right_replace(input_str, old, new, count=1):
    return new.join(input_str.rsplit(old, count))

@lru_cache(128)
def regex_to_domain(url):
    url = left_replace(url, "*://", "", 1)
    url = left_replace(url, "*.", "", 1)
    url = right_replace(url, "/*", "", 1)
    return url

def to_domain_attr(url):
    return url \
        .replace("*://", "") \
        .replace("*.", ".") \
        .replace("/*", "") \
        .lstrip(".")

def to_domain_ublock(url):
    formated_url = regex_to_domain(url)
    if "/" in formated_url:
        return f"||{formated_url}$all"
    else:
        # We can use this syntax which is more optimized
        return f"||{formated_url}^$all"

def to_domain_ublacklist(url):
    formated_url = regex_to_domain(url)
    return f"*://*.{formated_url}/*"

def to_domain_hosts_filter(url):
    formated_url = regex_to_domain(url)
    return f"0.0.0.0 {formated_url}"

def to_google(url):
    return f'google.*###rso .TzHB6b a[href*="{regex_to_domain(url)}"]:upward(.TzHB6b)'

def to_duckduckgo(url):
    return f'duckduckgo.com##.react-results--main > li:has(a[href*="{regex_to_domain(url)}"])'

def to_brave(url):
    return f'search.brave.com###results > div:has(a[href*="{regex_to_domain(url)}"])'

def to_startpage(url):
    return f'startpage.com##.w-gl__result:has(a[href*="{regex_to_domain(url)}"])'

def to_ecosia(url):
    return f'ecosia.org###main .result:has(a[href*="{regex_to_domain(url)}"])'

def to_userscript(url):
    return f'[data-domain*="{to_domain_attr(url)}"]'

def append_in_se(fd_by_filter, filter_name, source_is_for_dev, value):
    fd_by_filter[filter_name]["current"].write(value)
    fd_by_filter[filter_name]["global"].write(value)

    if source_is_for_dev:
        # Add in the "all" filter
        # The dev filter was formerly called "all". Dont rename it for compatibility
        fd_by_filter[filter_name]["all"].write(value)

UBLACKLIST_FILTER_TITLE = "uBlacklist"
HOSTS_FILTER_TITLE = "DNS hosts blocklist"
DOMAINS_FILTER_TITLE = "Domains blocklist"

def get_userscript_start(name):
    return f"""// ==UserScript==
// @name        uBlock-Origin-dev-filter – {name}
// @description Filter copycat-websites from DuckDuckGo and Google
// @match       https://*.duckduckgo.com/*
// @include     https://*.google.*/*
// ==/UserScript==
(function() {{
    const css = `
"""

def get_userscript_end():
    return """#__non-existent__{display: none}`;
    if (document.location.hostname.includes('google')) {
        const domains = css
            .split('\\n')
            .map(
                (s) => s.slice(15).replace('"],', '').trim(),
            )
            .filter(Boolean);
        // Remove {display:none}
        domains.splice(domains.length - 1, 1);
        for (const domain of domains) {
            try {
                const p = document
                    .querySelector(`#search a[href*="${domain}"]`)
                    .parentNode.parentNode.parentNode.parentNode;
                if (p) {
                    p.parentNode.removeChild(p);
                }
            } catch (e) {
                // Ignore
            }
        }
    } else {
        const style = document.createElement('style');
        style.textContent = css;
        document.head.insertAdjacentElement('beforeend', style);
    }
})();"""

def get_ublock_filters_header(name):
    return f"""! Title: uBlock-Origin-dev-filter – {name}
! Expires: 1 day
! Description: Filters to block and remove copycat-websites from search engines. Specific to dev websites like StackOverflow or GitHub.
! Homepage: https://github.com/quenhus/uBlock-Origin-dev-filter
! Licence: https://github.com/quenhus/uBlock-Origin-dev-filter/blob/main/LICENSE
!
! GitHub issues: https://github.com/quenhus/uBlock-Origin-dev-filter/issues
! GitHub pull requests: https://github.com/quenhus/uBlock-Origin-dev-filter/pulls
"""

def get_common_filters_header(name):
    return f"""# Title: uBlock-Origin-dev-filter – {name}
# Expires: 1 day
# Description: Filters to block and remove copycat-websites from search engines. Specific to dev websites like StackOverflow or GitHub.
# Homepage: https://github.com/quenhus/uBlock-Origin-dev-filter
# Licence: https://github.com/quenhus/uBlock-Origin-dev-filter/blob/main/LICENSE
#
# GitHub issues: https://github.com/quenhus/uBlock-Origin-dev-filter/issues
# GitHub pull requests: https://github.com/quenhus/uBlock-Origin-dev-filter/pulls
"""

dev_sources_list = (
    "github",
    "stackoverflow",
    "npm",
)

ubo_search_engines = {
    "google": {
        "name": "Google",
        "formater": lambda url: to_google(url) + LINE_SEP
    },
    "duckduckgo": {
        "name": "DuckDuckGo",
        "formater": lambda url: to_duckduckgo(url) + LINE_SEP
    },
    "google_duckduckgo": {
        "name": "Google+DuckDuckGo",
        "formater": lambda url: to_google(url) + LINE_SEP + to_duckduckgo(url) + LINE_SEP
    },
    "brave": {
        "name": "Brave",
        "formater": lambda url: to_brave(url) + LINE_SEP
    },
    "startpage": {
        "name": "Startpage",
        "formater": lambda url: to_startpage(url) + LINE_SEP
    },
    "ecosia": {
        "name": "Ecosia",
        "formater": lambda url: to_ecosia(url) + LINE_SEP
    },
    "all_search_engines": {
        "name": "All Search Engines",
        "formater": lambda url: to_google(url) + LINE_SEP + to_duckduckgo(url) + LINE_SEP + to_brave(url) + LINE_SEP + to_startpage(url) + LINE_SEP + to_ecosia(url) + LINE_SEP
    }
}

def main():
    root_path = Path(__file__).parent.joinpath("../")
    dist_path = root_path.joinpath(DEST_DATA_PATH)
    other_format_dist_path = root_path.joinpath(OTHER_FORMAT_DATA_PATH)

    tmp_txt = dist_path.joinpath("tmp.txt")

    # For uBlock
    # File used by all source (stackoverflow_copycats, github_copycats, ...)
    path_by_filter = {
        se: {
            "dist": dist_path.joinpath(se),
            "global": dist_path.joinpath(se, "global.txt"),
            "all": dist_path.joinpath(se, "all.txt"),
        }
        for se in ubo_search_engines.keys()
    }

    # For Userscript filters
    path_by_filter["userscript_gd"] = {
        "dist": dist_path.joinpath("userscript", "google_duckduckgo"),
        "global": dist_path.joinpath("userscript", "google_duckduckgo", "global.txt"),
        "all": dist_path.joinpath("userscript", "google_duckduckgo", "all.txt"),
    }

    # For uBlacklist filters
    path_by_filter["uBlacklist"] = {
        "dist": other_format_dist_path.joinpath("uBlacklist"),
        "global": other_format_dist_path.joinpath("uBlacklist", "global.txt"),
        "all": other_format_dist_path.joinpath("uBlacklist", "all.txt"),
    }

    # For hosts filters
    path_by_filter["hosts"] = {
        "dist": other_format_dist_path.joinpath("hosts"),
        "global": other_format_dist_path.joinpath("hosts", "global.txt"),
        "all": other_format_dist_path.joinpath("hosts", "all.txt"),
    }

    # For domains filters
    path_by_filter["domains"] = {
        "dist": other_format_dist_path.joinpath("domains"),
        "global": other_format_dist_path.joinpath("domains", "global.txt"),
        "all": other_format_dist_path.joinpath("domains", "all.txt"),
    }

    # Create folders for each SE in ./dist/
    for se_files in path_by_filter.values():
        se_files["dist"].mkdir(parents=True, exist_ok=True)

    with ExitStack() as global_stack:
        # Open all files (one "all.txt" and one "global.txt" for each search engine)
        fd_by_filter = {
            se: {
                "global": global_stack.enter_context(se_files["global"].open("w", encoding="utf8")),
                "all": global_stack.enter_context(se_files["all"].open("w", encoding="utf8")),
            }
            for se, se_files in path_by_filter.items()
        }

        # Add header in each general uBlock filter
        for filter_name, filter_meta in ubo_search_engines.items():
            se_name = filter_meta['name']
            fd_by_filter[filter_name]["global"].write(get_ublock_filters_header(f"{se_name} – Global"))
            # The dev filter was formerly called "all". Dont rename it for compatibility
            fd_by_filter[filter_name]["all"].write(get_ublock_filters_header(f"{se_name} – Dev"))

        # Add header in each userscript filter
        fd_by_filter["userscript_gd"]["global"].write(get_userscript_start("Google+DuckDuckGo - Global"))
        fd_by_filter["userscript_gd"]["all"].write(get_userscript_start("Google+DuckDuckGo - Dev"))

        # Add header in each other filters
        fd_by_filter["uBlacklist"]["global"].write(get_common_filters_header(f"{UBLACKLIST_FILTER_TITLE} - Global"))
        fd_by_filter["uBlacklist"]["all"].write(get_common_filters_header(f"{UBLACKLIST_FILTER_TITLE} - Dev"))
        fd_by_filter["hosts"]["global"].write(get_common_filters_header(f"{HOSTS_FILTER_TITLE} - Global"))
        fd_by_filter["hosts"]["all"].write(get_common_filters_header(f"{HOSTS_FILTER_TITLE} - Dev"))
        fd_by_filter["domains"]["global"].write(get_common_filters_header(f"{DOMAINS_FILTER_TITLE} - Global"))
        fd_by_filter["domains"]["all"].write(get_common_filters_header(f"{DOMAINS_FILTER_TITLE} - Dev"))

        for source_f in sorted(root_path.joinpath(SOURCE_DATA_PATH).glob("*.txt")):
            source_stem = source_f.stem

            # Sort and find duplicates
            with source_f.open("r") as source_fd, tmp_txt.open("w") as tmp:
                already_in = set()
                for line in source_fd:
                    if line.startswith("!") or not line.strip():
                        tmp.write(line)
                        continue
                    url = line.strip()
                    if url in already_in:
                        print(f"Find duplicate: {url}. Skip!")
                        continue
                    else:
                        already_in.add(url)
                        tmp.write(line)
            tmp_txt.replace(source_f)

            with ExitStack() as source_stack, source_f.open("r") as source_fd:
                # Create one file per SE, to add specific filter
                for filter_name in fd_by_filter:
                    dist = path_by_filter[filter_name]["dist"]
                    f = dist.joinpath(f"{source_stem}.txt")
                    fd_by_filter[filter_name]["current"] = source_stack.enter_context(f.open("w", encoding="utf8"))

                source_name = source_f.stem.replace("_copycats", "")
                source_is_for_dev = source_name in dev_sources_list

                # Add header in each source-specific uBlock filter
                for filter_name, filter_meta in ubo_search_engines.items():
                    se_name = filter_meta['name']
                    fd_by_filter[filter_name]["current"].write(get_ublock_filters_header(f"{se_name} – {source_name}"))

                # Add header in each userscript filter
                fd_by_filter["userscript_gd"]["current"].write(get_userscript_start(f"Google+DuckDuckGo - {source_name}"))

                # Add header in each other filters
                fd_by_filter["uBlacklist"]["current"].write(get_common_filters_header(f"{UBLACKLIST_FILTER_TITLE} - {source_name}"))
                fd_by_filter["hosts"]["current"].write(get_common_filters_header(f"{HOSTS_FILTER_TITLE} - {source_name}"))
                fd_by_filter["domains"]["current"].write(get_common_filters_header(f"{DOMAINS_FILTER_TITLE} - {source_name}"))

                for line in source_fd:
                    if line.startswith("!") or not line.strip():
                        continue
                    url = line.strip()

                    # Block the domain
                    for filter_name, filter_meta in ubo_search_engines.items():
                        append_in_se(fd_by_filter, filter_name, source_is_for_dev, to_domain_ublock(url) + LINE_SEP)

                        append_in_se(fd_by_filter, filter_name, source_is_for_dev, filter_meta["formater"](url))

                    append_in_se(fd_by_filter, "userscript_gd", source_is_for_dev, to_userscript(url) + COMMA_SEP + LINE_SEP)
                    append_in_se(fd_by_filter, "uBlacklist", source_is_for_dev, to_domain_ublacklist(url) + LINE_SEP)
                    append_in_se(fd_by_filter, "hosts", source_is_for_dev, to_domain_hosts_filter(url) + LINE_SEP)
                    append_in_se(fd_by_filter, "domains", source_is_for_dev, regex_to_domain(url) + LINE_SEP)


                # Add footer in each userscript filter
                fd_by_filter["userscript_gd"]["current"].write(get_userscript_end())

        # Add footer in each userscript filter
        for source_type in ("global", "all"):
            fd_by_filter["userscript_gd"][source_type].write(get_userscript_end())

if __name__ == "__main__":
    main()
