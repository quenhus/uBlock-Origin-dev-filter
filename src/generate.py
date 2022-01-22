from pathlib import Path

LINE_SEP = "\n"

def to_css_attr(url):
    return url.replace("*://", "").replace("*.", ".").replace("/*", "")

def to_google(url):
    return f'google.*##.g:has(a[href*="{to_css_attr(url)}"])'

def to_duckduckgo(url):
    return f'duckduckgo.*##.results > div:has(a[href*="{to_css_attr(url)}"])'

def to_brave(url):
    return f'search.brave.com###results > div:has(a[href*="{to_css_attr(url)}"])'

def to_startpage(url):
    return f'startpage.com##.w-gl__result:has(a[href*="{to_css_attr(url)}"])'

def get_ublock_filters_header(name):
    return f"""! Title: uBlock-Origin-dev-filter – {name}
! Expires: 1 day
! Description: Filters to block and remove copycat-websites from DuckDuckGo and Google. Specific to dev websites like StackOverflow or GitHub.
! Homepage: https://github.com/quenhus/uBlock-Origin-dev-filter
! Licence: https://github.com/quenhus/uBlock-Origin-dev-filter/blob/main/LICENSE
!
! GitHub issues: https://github.com/quenhus/uBlock-Origin-dev-filter/issues
! GitHub pull requests: https://github.com/quenhus/uBlock-Origin-dev-filter/pulls
"""

def main():
    root_path = Path(__file__).parent.joinpath("../")
    dist_path = root_path.joinpath("dist")

    tmp_txt = dist_path.joinpath("tmp.txt")

    g_all = dist_path.joinpath("google", "all.txt")
    d_all = dist_path.joinpath("duckduckgo", "all.txt")
    gd_all = dist_path.joinpath("google_duckduckgo", "all.txt")
    b_all = dist_path.joinpath("brave", "all.txt")
    sp_all = dist_path.joinpath("startpage", "all.txt")

    for f in [g_all, d_all, gd_all, b_all, sp_all]:
        f.parent.mkdir(parents=True, exist_ok=True)

    with g_all.open("w", encoding="utf8") as g_all, \
         d_all.open("w", encoding="utf8") as d_all, \
         gd_all.open("w", encoding="utf8") as gd_all, \
         b_all.open("w", encoding="utf8") as b_all, \
         sp_all.open("w", encoding="utf8") as sp_all:

        g_all.write(get_ublock_filters_header("Google – All"))
        d_all.write(get_ublock_filters_header("DuckDuckGo – All"))
        gd_all.write(get_ublock_filters_header("Google+DuckDuckGo – All"))
        b_all.write(get_ublock_filters_header("Brave – All"))
        sp_all.write(get_ublock_filters_header("Startpage – All"))

        for file in root_path.joinpath("data").glob("*.txt"):
            filename = file.name.split(".")[0]

            # Sort and find duplicates
            with file.open("r") as i, tmp_txt.open("w") as tmp:
                already_in = set()
                for line in i:
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
            tmp_txt.replace(file)

            with dist_path.joinpath("google", f"{filename}.txt").open("w", encoding="utf8") as g, \
                dist_path.joinpath("duckduckgo", f"{filename}.txt").open("w", encoding="utf8") as d, \
                dist_path.joinpath("google_duckduckgo", f"{filename}.txt").open("w", encoding="utf8") as gd, \
                dist_path.joinpath("brave", f"{filename}.txt").open("w", encoding="utf8") as b, \
                dist_path.joinpath("startpage", f"{filename}.txt").open("w", encoding="utf8") as sp, \
                file.open("r") as i:

                filter_name = file.stem.replace("_copycats", "")
                g.write(get_ublock_filters_header(f"Google – {filter_name}"))
                d.write(get_ublock_filters_header(f"DuckDuckGo – {filter_name}"))
                gd.write(get_ublock_filters_header(f"Google+DuckDuckGo – {filter_name}"))
                b.write(get_ublock_filters_header(f"Brave – {filter_name}"))
                sp.write(get_ublock_filters_header(f"Startpage – {filter_name}"))

                for line in i:
                    if line.startswith("!") or not line.strip():
                        continue
                    url = line.strip()
                    for f in [
                        g, g_all,
                        d, d_all,
                        gd, gd_all,
                        b, b_all,
                        sp, sp_all
                    ]:
                        f.write(url + LINE_SEP)

                    url_google = to_google(url)
                    url_duckduckgo = to_duckduckgo(url)
                    url_brave = to_brave(url)
                    url_sp = to_startpage(url)
                    for f in [
                        g, g_all,
                        gd, gd_all
                    ]:
                        f.write(url_google + LINE_SEP)
                    for f in [
                        d, d_all,
                        gd, gd_all
                    ]:
                        f.write(url_duckduckgo + LINE_SEP)
                    for f in [
                        b, b_all
                    ]:
                        f.write(url_brave + LINE_SEP)
                    for f in [
                        sp, sp_all
                    ]:
                        f.write(url_sp + LINE_SEP)

if __name__ == "__main__":
    main()