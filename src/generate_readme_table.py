import urllib.parse

from typing import NamedTuple

# What a nightmare to create Markdown table (moreover with image+link...)

NEW_LINE = "\n"

class FilterMeta(NamedTuple):
    name: str
    dist_path: str
    color: str

class FlavorMeta(NamedTuple):
    name: str
    table_name: str
    filename: str

search_engines = (
    FilterMeta("Google", "google", "de3f32"),
    FilterMeta("DuckDuckGo", "duckduckgo", "fdd20a"),
    FilterMeta("DuckDuckGo Lite", "duckduckgo_lite", "fef1b5"),
    FilterMeta("Google+DDG", "google_duckduckgo", "9b59b6"),
    FilterMeta("Startpage", "startpage", "5b7bca"),
    FilterMeta("Brave", "brave", "f25100"),
    FilterMeta("Ecosia", "ecosia", "36acb8"),
    FilterMeta("All Search Engines", "all_search_engines", "ffffff")
)

other_filters = (
    FilterMeta("uBlacklist", "other_format/uBlacklist", "ffffff"),
    FilterMeta("macOS userscript", "userscript/google_duckduckgo", "ffffff"),
    FilterMeta("Domains filter", "other_format/domains", "ffffff"),
    FilterMeta("DNS hosts filter", "other_format/hosts", "ffffff"),
)

def param_encode(x):
    return urllib.parse.quote(x)

def get_badge(alt: str, icon: str, label: str, message: str, color: str):
    return f"![{alt}](https://img.shields.io/static/v1?label={param_encode(label)}&message={param_encode(message)}&color={color}&style=flat&logo={param_encode(icon)})"


def md_link(content: str, href: str):
    return f"[{content}]({href})"

def md_tr(*td: str):
    return "|".join(("", *td, "")) + NEW_LINE

def get_ubo_subscribe_url(dist_path: str, filename: str, title: str):
    return f"https://subscribe.adblockplus.org/?location=https%3A%2F%2Fraw.githubusercontent.com%2Fquenhus%2FuBlock-Origin-dev-filter%2Fmain%2Fdist%2F{dist_path}%2F{filename}.txt&title={param_encode(title)}"

def get_static_url(dist_path: str, filename: str):
    return f"https://raw.githubusercontent.com/quenhus/uBlock-Origin-dev-filter/main/dist/{dist_path}/{filename}.txt"

def get_main_ubo_table(flavors: list[FlavorMeta]):
    ret = md_tr("", *(f.table_name for f in flavors))
    ret += md_tr("---", *(":---:" for f in flavors))

    for filter_meta in search_engines:
        ret += md_tr(
            filter_meta.name,
            *(
                md_link(
                    get_badge("uBO - add this filter", "uBlock Origin", "uBO", "add this filter", filter_meta.color),
                    get_ubo_subscribe_url(filter_meta.dist_path, f.filename, f"uBlock-Origin-dev-filter - {filter_meta.name} - {f.name}")
                )
                for f in flavors
            )
        )

    return ret

def get_source_flavor_ubo_table(flavors: list[FlavorMeta]):
    ret = md_tr("", *(f.table_name for f in flavors))
    ret += md_tr("---", *(":---:" for f in flavors))

    for filter_meta in search_engines:
        ret += md_tr(
            filter_meta.name,
            *(
                md_link(
                    "add in uBO",
                    get_ubo_subscribe_url(filter_meta.dist_path, f.filename, f"uBlock-Origin-dev-filter - {filter_meta.name} - {f.name}")
                )
                for f in flavors
            )
        )

    return ret

def get_other_filter_table(flavors: list[FlavorMeta]):
    ret = md_tr("", *(f.table_name for f in flavors))
    ret += md_tr("---", *(":---:" for f in flavors))

    for filter_meta in other_filters:
        ret += md_tr(
            filter_meta.name,
            *(
                md_link(
                    "Link",
                    get_static_url(filter_meta.dist_path, f.filename)
                )
                for f in flavors
            )
        )

    return ret


if __name__ == "__main__":
    main_flovors = [
        # The dev filter was formerly called "all". Dont rename it for compatibility
        FlavorMeta("Dev", "dev", "all"),
        FlavorMeta("Global", "global", "global"),
    ]

    source_flavors = [
        FlavorMeta("StackOverflow", "StackOverflow", "stackoverflow_copycats"),
        FlavorMeta("GitHub", "GitHub", "github_copycats"),
        FlavorMeta("NPM", "NPM", "npm_copycats"),
        FlavorMeta("Wikipedia", "Wikipedia", "wikipedia_copycats"),
        FlavorMeta("SEO Spam", "SEO Spam", "seo_spam"),
    ]

    print(get_main_ubo_table(main_flovors))

    print("\n" * 5)

    print(get_source_flavor_ubo_table(source_flavors))

    print("\n" * 5)

    print(get_other_filter_table(main_flovors + source_flavors))
