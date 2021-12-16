# uBlock-Origin-dev-filter
Filters to block and remove copycat-websites from DuckDuckGo and Google. Specific to dev websites like StackOverflow or GitHub.

## Import into uBlock Origin

1. Open uBlock Origin settings
2. Under the "Filter" tab, scroll to the bottom where it says “Custom” and click the “Import” checkbox to reveal the custom URL textbox
3. Append the URL `https://raw.githubusercontent.com/quenhus/uBlock-Origin-dev-filter/main/dist/google_duckduckgo/all.txt` in the textbox
4. Press `Apply Changes` in the upper right

## Adding URL's

Please create a pull-request or start an issue with evidence against the "copycats".

## Sources

* [uBlacklist Stack Overflow Translation](https://github.com/arosh/ublacklist-stackoverflow-translation)
* [uBlacklist GitHub Translation](https://github.com/arosh/ublacklist-github-translation)
* [uBlock Origin - Shitty Copy-Paste websites filter](https://github.com/stroobants-dev/ublock-origin-shitty-copies-filter)
* [Quenhus Stackoverflow/Github copy-cats](https://gist.github.com/quenhus/6bd2c47e5780f726f0c96c0a2ee762a4)

## Do your own

1. List URL that you want to block in a `.txt` in the `data/` folder
2. Use `src/generate.py`, which generate files in `dist/` you can use as uBlock filters

### Manual Google filter

1. Take an URL `*.abc.example.com` or `iam.copycat.com/*`
2. Remove `*` prefix or `/*` suffix
3. Surround the URL with `google.*##.g:has(a[href*="` and `"])`
4. For example, it gives `google.*##.g:has(a[href*=".abc.example.com"])` and `google.*##.g:has(a[href*="iam.copycat.com"])`

### Manual DuckDuckGo filter

1. Take an URL `*.abc.example.com` or `iam.copycat.com/*`
2. Remove `*` prefix or `/*` suffix
3. Surround the URL with `duckduckgo.*##.results > div:has(a[href*="` and `"])`
4. For example, it gives `duckduckgo.*##.results > div:has(a[href*=".abc.example.com"])` and `duckduckgo.*##.results > div:has(a[href*="iam.copycat.com"])`
