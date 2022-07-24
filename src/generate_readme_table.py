import urllib.parse

from typing import NamedTuple

# What a nightmare to create Markdown table (moreover with image+link...)

NEW_LINE = "\n"

class SearchEngineMeta(NamedTuple):
    name: str
    dist_path: str
    color: str

class FlavorMeta(NamedTuple):
    name: str
    table_name: str
    filename: str

search_engines = (
    SearchEngineMeta("Google", "google", "de3f32"),
    SearchEngineMeta("DuckDuckGo", "duckduckgo", "fdd20a"),
    SearchEngineMeta("Google+DDG", "google_duckduckgo", "9b59b6"),
    SearchEngineMeta("Startpage", "startpage", "5b7bca"),
    SearchEngineMeta("Brave", "brave", "f25100"),
    SearchEngineMeta("Ecosia", "ecosia", "36acb8"),
    SearchEngineMeta("All Search Engines", "all_search_engines", "ffffff")
)

def param_encode(x):
    return urllib.parse.quote(x)

def get_badge(alt: str, icon: str, label: str, message: str, color: str):
    return f"![{alt}](https://img.shields.io/static/v1?label={param_encode(label)}&message={param_encode(message)}&color={color}&style=flat&logo={param_encode(icon)})"


def md_link(content: str, href: str):
    return f"[{content}]({href})"

def md_tr(*td: str):
    return "|".join(("", *td, "")) + NEW_LINE

def get_subscribe_url(dist_path: str, filename: str, title: str):
    return f"https://subscribe.adblockplus.org/?location=https%3A%2F%2Fraw.githubusercontent.com%2Fquenhus%2FuBlock-Origin-dev-filter%2Fmain%2Fdist%2F{dist_path}%2F{filename}.txt&title={param_encode(title)}"

def get_table(*flavors: FlavorMeta):
    ret = md_tr("", *(f.table_name for f in flavors))
    ret += md_tr("---", *(":---:" for f in flavors))

    for se in search_engines:
        ret += md_tr(
            se.name,
            *(
                md_link(
                    get_badge("uBO - add this filter", "uBlock Origin", "uBO", "add this filter", se.color),
                    get_subscribe_url(se.dist_path, f.filename, f"uBlock-Origin-dev-filter - {se.name} - {f.name}")
                )
                for f in flavors
            )
        )

    return ret

def get_table_simple(*flavors: FlavorMeta):
    ret = md_tr("", *(f.table_name for f in flavors))
    ret += md_tr("---", *(":---:" for f in flavors))

    for se in search_engines:
        ret += md_tr(
            se.name,
            *(
                md_link(
                    "add in uBO",
                    get_subscribe_url(se.dist_path, f.filename, f"uBlock-Origin-dev-filter - {se.name} - {f.name}")
                )
                for f in flavors
            )
        )

    return ret


print(get_table(
    # The dev filter was formerly called "all". Dont rename it for compatibility
    FlavorMeta("Dev", "dev", "all"),
    FlavorMeta("Global", "global", "global"),
))

print("\n"*3)

print(get_table_simple(
    FlavorMeta("StackOverflow", "StackOverflow", "stackoverflow_copycats"),
    FlavorMeta("GitHub", "GitHub", "github_copycats"),
    FlavorMeta("NPM", "NPM", "npm_copycats"),
    FlavorMeta("Wikipedia", "Wikipedia", "wikipedia_copycats"),
    FlavorMeta("SEO Spam", "SEO Spam", "seo_spam"),
))
