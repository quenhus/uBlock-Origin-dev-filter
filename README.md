# uBlock-Origin-dev-filter
Filters to block and remove copycat-websites from DuckDuckGo, Google and other search engines. Used to be specific to dev websites like StackOverflow or GitHub, but it currently supports others like Wikipedia.

## Import into uBlock Origin

Select the filters flavors you want, depending on your needs and search engine:

💻 **`dev`** supports StackOverflow + GitHub + NPM  
🌐 **`all`** supports StackOverflow + GitHub + NPM + Wikipedia

|            | dev                                                                                                                                                                                                                                                                                                                                           | all                                                                                                                                                                                                                                                                                                                                            |
|------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Google     | [![uBO - add this filter](https://img.shields.io/static/v1?label=uBO&message=add+this+filter&color=de3f32&style=flat&logo=uBlock+Origin)](https://subscribe.adblockplus.org/?location=https%3A%2F%2Fraw.githubusercontent.com%2Fquenhus%2FuBlock-Origin-dev-filter%2Fmain%2Fdist%2Fgoogle%2Fall.txt&title=Google%20%2D%20All) | [![uBO - add this filter](https://img.shields.io/static/v1?label=uBO&message=add+this+filter&color=de3f32&style=flat&logo=uBlock+Origin)](https://subscribe.adblockplus.org/?location=https%3A%2F%2Fraw.githubusercontent.com%2Fquenhus%2FuBlock-Origin-dev-filter%2Fmain%2Fdist%2Fgoogle%2Fall.txt&title=Google%20%2D%20All) |
| DuckDuckGo | [![uBO - add this filter](https://img.shields.io/static/v1?label=uBO&message=add+this+filter&color=fdd20a&style=flat&logo=uBlock+Origin)](https://subscribe.adblockplus.org/?location=https%3A%2F%2Fraw.githubusercontent.com%2Fquenhus%2FuBlock-Origin-dev-filter%2Fmain%2Fdist%2Fduckduckgo%2Fall.txt&title=DuckDuckGo%20%2D%20All) | [![uBO - add this filter](https://img.shields.io/static/v1?label=uBO&message=add+this+filter&color=fdd20a&style=flat&logo=uBlock+Origin)](https://subscribe.adblockplus.org/?location=https%3A%2F%2Fraw.githubusercontent.com%2Fquenhus%2FuBlock-Origin-dev-filter%2Fmain%2Fdist%2Fduckduckgo%2Fall.txt&title=DuckDuckGo%20%2D%20All) |
| Google+DDG | [![uBO - add this filter](https://img.shields.io/static/v1?label=uBO&message=add+this+filter&color=9b59b6&style=flat&logo=uBlock+Origin)](https://subscribe.adblockplus.org/?location=https%3A%2F%2Fraw.githubusercontent.com%2Fquenhus%2FuBlock-Origin-dev-filter%2Fmain%2Fdist%2Fgoogle_duckduckgo%2Fall.txt&title=Google%2BDuckDuckGo%20%2D%20All) | [![uBO - add this filter](https://img.shields.io/static/v1?label=uBO&message=add+this+filter&color=9b59b6&style=flat&logo=uBlock+Origin)](https://subscribe.adblockplus.org/?location=https%3A%2F%2Fraw.githubusercontent.com%2Fquenhus%2FuBlock-Origin-dev-filter%2Fmain%2Fdist%2Fgoogle_duckduckgo%2Fall.txt&title=Google%2BDuckDuckGo%20%2D%20All) |
| Startpage  | [![uBO - add this filter](https://img.shields.io/static/v1?label=uBO&message=add+this+filter&color=5b7bca&style=flat&logo=uBlock+Origin)](https://subscribe.adblockplus.org/?location=https%3A%2F%2Fraw.githubusercontent.com%2Fquenhus%2FuBlock-Origin-dev-filter%2Fmain%2Fdist%2Fstartpage%2Fall.txt&title=Startpage%20%2D%20All) | [![uBO - add this filter](https://img.shields.io/static/v1?label=uBO&message=add+this+filter&color=5b7bca&style=flat&logo=uBlock+Origin)](https://subscribe.adblockplus.org/?location=https%3A%2F%2Fraw.githubusercontent.com%2Fquenhus%2FuBlock-Origin-dev-filter%2Fmain%2Fdist%2Fstartpage%2Fall.txt&title=Startpage%20%2D%20All) |
| Brave      | [![uBO - add this filter](https://img.shields.io/static/v1?label=uBO&message=add+this+filter&color=f25100&style=flat&logo=uBlock+Origin)](https://subscribe.adblockplus.org/?location=https%3A%2F%2Fraw.githubusercontent.com%2Fquenhus%2FuBlock-Origin-dev-filter%2Fmain%2Fdist%2Fbrave%2Fall.txt&title=Brave%20%2D%20All) | [![uBO - add this filter](https://img.shields.io/static/v1?label=uBO&message=add+this+filter&color=f25100&style=flat&logo=uBlock+Origin)](https://subscribe.adblockplus.org/?location=https%3A%2F%2Fraw.githubusercontent.com%2Fquenhus%2FuBlock-Origin-dev-filter%2Fmain%2Fdist%2Fbrave%2Fall.txt&title=Brave%20%2D%20All) |
| Ecosia     | [![uBO - add this filter](https://img.shields.io/static/v1?label=uBO&message=add+this+filter&color=36acb8&style=flat&logo=uBlock+Origin)](https://subscribe.adblockplus.org/?location=https%3A%2F%2Fraw.githubusercontent.com%2Fquenhus%2FuBlock-Origin-dev-filter%2Fmain%2Fdist%2Fecosia%2Fall.txt&title=Ecosia%20%2D%20All) | [![uBO - add this filter](https://img.shields.io/static/v1?label=uBO&message=add+this+filter&color=36acb8&style=flat&logo=uBlock+Origin)](https://subscribe.adblockplus.org/?location=https%3A%2F%2Fraw.githubusercontent.com%2Fquenhus%2FuBlock-Origin-dev-filter%2Fmain%2Fdist%2Fecosia%2Fall.txt&title=Ecosia%20%2D%20All) |

<details>
  <summary>How to import uBlock filters manually</summary>
  
### Manually import filters

  1. Open uBlock Origin settings
  2. Under the "Filter lists" tab, scroll to the bottom where it says “Custom” and click the “Import” checkbox to reveal the custom URL textbox
  3. Append the URL `https://raw.githubusercontent.com/quenhus/uBlock-Origin-dev-filter/main/dist/google_duckduckgo/all.txt` in the textbox
  4. Press `Apply Changes` in the upper left

  Note: In `dist/`, you can find filters for other search engines (Google, DuckDuckGo, Startpage or Brave). You can use and combine these filters by using the raw URL of `dist/` files.
</details>

<details>
  <summary>macOS Userscript</summary>
  
### macOS Userscript

For macOS users, this project also provide some Userscripts for Google+DuckDuckGo in `dist/userscript/google_duckduckgo/`

</details>

## Adding URL's

Please create a pull-request or [start an issue](https://github.com/quenhus/uBlock-Origin-dev-filter/issues/new?assignees=&labels=block-request&template=request-to-add-a-website-to-the-filter.md&title=Request%3A+add+COPYCAT_URL+to+the+filter) with evidence against the "copycats".

## Security

For simplicity and auto-updates, uBlock Origin filters rely on the last commit of the `main` branch, as every other uBO filters. For now, it seems this method does not raise security issues. However, you can import uBlock Origin filters with a reference to a given commit, not the `main` branch. Filters won't auto-update but they will be auditable by your own eyes.

## Sources

* [uBlacklist Stack Overflow Translation](https://github.com/arosh/ublacklist-stackoverflow-translation)
* [uBlacklist GitHub Translation](https://github.com/arosh/ublacklist-github-translation)
* [uBlock Origin - Shitty Copy-Paste websites filter](https://github.com/stroobants-dev/ublock-origin-shitty-copies-filter)
* [Quenhus Stackoverflow/Github copy-cats](https://gist.github.com/quenhus/6bd2c47e5780f726f0c96c0a2ee762a4)

## Do your own

1. List URL that you want to block in a `.txt` in the `data/` folder
2. Use `src/generate.py`, which generate files in `dist/` you can use as uBlock filters

Note: You can use [letsblock.it](https://letsblock.it/filters/search-results) to create your own filter.
