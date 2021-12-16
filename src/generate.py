from glob import glob
from pathlib import Path

LINE_SEP = "\n"

def to_css_attr(url):
    return url.replace("*://", "").replace("*.", ".").replace("/*", "")

def to_google(url):
    return f'google.*##.g:has(a[href*="{to_css_attr(url)}"])'

def to_duckduckgo(url):
    return f'duckduckgo.*##.results > div:has(a[href*="{to_css_attr(url)}"])'

def main():
    root_path = Path(__file__).parent.joinpath("../")
    dist_path = root_path.joinpath("dist")

    g_all = dist_path.joinpath("google", "all.txt")
    d_all = dist_path.joinpath("duckduckgo", "all.txt")
    gd_all = dist_path.joinpath("google_duckduckgo", "all.txt")

    for f in [g_all, d_all, gd_all]:
        f.parent.mkdir(parents=True, exist_ok=True)

    with g_all.open("w") as g_all, \
         d_all.open("w") as d_all, \
         gd_all.open("w") as gd_all:

        for file in root_path.joinpath("data").glob("*.txt"):
            filename = file.name.split(".")[0]

            with dist_path.joinpath("google", f"{filename}.txt").open("w") as g, \
                dist_path.joinpath("duckduckgo", f"{filename}.txt").open("w") as d, \
                dist_path.joinpath("google_duckduckgo", f"{filename}.txt").open("w") as gd, \
                file.open("r") as i:
                for line in i:
                    if line.startswith("!") or not line.strip():
                        continue
                    url = line.strip()
                    for f in [g, d, gd, g_all, d_all, gd_all]:
                        f.write(url + LINE_SEP)

                    url_google = to_google(url)
                    url_duckduckgo = to_duckduckgo(url)
                    for f in [g, gd, g_all, gd_all]:
                        f.write(url_google + LINE_SEP)
                    for f in [d, gd, d_all, gd_all]:
                        f.write(url_duckduckgo + LINE_SEP)

if __name__ == "__main__":
    main()