from pathlib import Path
from contextlib import ExitStack


LINE_SEP = "\n"
COMMA_SEP = ","

def left_replace(input_str, old, new, count=1):
    return new.join(input_str.split(old, count))
def right_replace(input_str, old, new, count=1):
    return new.join(input_str.rsplit(old, count))

def format_url(url):
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
    return f"||{format_url(url)}$all"

def to_google(url):
    return f'google.*##.g:has(a[href*="{format_url(url)}"])'

def to_duckduckgo(url):
    return f'duckduckgo.com###links>div:has(a[href*="{format_url(url)}"])'

def to_brave(url):
    return f'search.brave.com###results > div:has(a[href*="{format_url(url)}"])'

def to_startpage(url):
    return f'startpage.com##.w-gl__result:has(a[href*="{format_url(url)}"])'

def to_ecosia(url):
    return f'ecosia.org##.result:has(a[href*="{format_url(url)}"])'

def to_userscript(url):
    return f'[data-domain*="{to_domain_attr(url)}"]'

def append_in_se(shared_fd_per_se, se, source_is_for_dev, value):
    shared_fd_per_se[se]["current"].write(value)
    shared_fd_per_se[se]["global"].write(value)

    if source_is_for_dev:
        # Add in the "all" filter
        # The dev filter was formerly called "all". Dont rename it for compatibility
        shared_fd_per_se[se]["all"].write(value)

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
    dist_path = root_path.joinpath("dist")

    tmp_txt = dist_path.joinpath("tmp.txt")

    # For uBlock
    # File used by all source (stackoverflow_copycats, github_copycats, ...)
    shared_files_per_se = {
        se: {
            "dist": dist_path.joinpath(se),
            "global": dist_path.joinpath(se, "global.txt"),
            "all": dist_path.joinpath(se, "all.txt"),
        }
        for se in ubo_search_engines.keys()
    }

    # For Userscript filters
    shared_files_per_se["userscript_gd"] = {
        "dist": dist_path.joinpath("userscript", "google_duckduckgo"),
        "global": dist_path.joinpath("userscript", "google_duckduckgo", "global.txt"),
        "all": dist_path.joinpath("userscript", "google_duckduckgo", "all.txt"),
    }

    # Create folders for each SE in ./dist/
    for se_files in shared_files_per_se.values():
        se_files["dist"].mkdir(parents=True, exist_ok=True)

    with ExitStack() as global_stack:
        # Open all files (one "all.txt" and one "global.txt" for each search engine)
        shared_fd_per_se = {
            se: {
                "global": global_stack.enter_context(se_files["global"].open("w", encoding="utf8")),
                "all": global_stack.enter_context(se_files["all"].open("w", encoding="utf8")),
            }
            for se, se_files in shared_files_per_se.items()
        }

        # Add header in each general uBlock filter
        for se, se_meta in ubo_search_engines.items():
            se_name = se_meta['name']
            shared_fd_per_se[se]["global"].write(get_ublock_filters_header(f"{se_name} – Global"))
            # The dev filter was formerly called "all". Dont rename it for compatibility
            shared_fd_per_se[se]["all"].write(get_ublock_filters_header(f"{se_name} – Dev"))

        # Add header in each userscript filter
        shared_fd_per_se["userscript_gd"]["global"].write(get_userscript_start("Google+DuckDuckGo - Global"))
        shared_fd_per_se["userscript_gd"]["all"].write(get_userscript_start("Google+DuckDuckGo - Dev"))

        for source_f in sorted(root_path.joinpath("data").glob("*.txt")):
            filename = source_f.name.split(".")[0]

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
                for se in shared_fd_per_se:
                    dist = shared_files_per_se[se]["dist"]
                    f = dist.joinpath(f"{filename}.txt")
                    shared_fd_per_se[se]["current"] = source_stack.enter_context(f.open("w", encoding="utf8"))

                source_name = source_f.stem.replace("_copycats", "")
                source_is_for_dev = source_name in dev_sources_list

                # Add header in each source-specific uBlock filter
                for se, se_meta in ubo_search_engines.items():
                    se_name = se_meta['name']
                    shared_fd_per_se[se]["current"].write(get_ublock_filters_header(f"{se_name} – {source_name}"))

                # Add header in each userscript filter
                shared_fd_per_se["userscript_gd"]["current"].write(get_userscript_start(f"Google+DuckDuckGo - {source_name}"))

                for line in source_fd:
                    if line.startswith("!") or not line.strip():
                        continue
                    url = line.strip()

                    # Block the domain
                    for se, se_meta in ubo_search_engines.items():
                        append_in_se(shared_fd_per_se, se, source_is_for_dev, to_domain_ublock(url) + LINE_SEP)

                        append_in_se(shared_fd_per_se, se, source_is_for_dev, se_meta["formater"](url))

                    append_in_se(shared_fd_per_se, "userscript_gd", source_is_for_dev, to_userscript(url)+ COMMA_SEP + LINE_SEP)


                # Add footer in each userscript filter
                shared_fd_per_se["userscript_gd"]["current"].write(get_userscript_end())

        # Add footer in each userscript filter
        for source_type in ("global", "all"):
            shared_fd_per_se["userscript_gd"][source_type].write(get_userscript_end())

if __name__ == "__main__":
    main()
