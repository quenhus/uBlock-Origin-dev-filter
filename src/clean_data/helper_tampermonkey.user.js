// ==UserScript==
// @name         Review domains for uBlock-Origin-dev-filter
// @namespace    https://https://github.com/quenhus/uBlock-Origin-dev-filter/
// @version      0.1
// @description  Review a list of domains for the uBlock filter: uBlock-Origin-dev-filter
// @author       Quenhus
// @match        ^https://www.google.com/*$
// @icon         https://www.google.com/s2/favicons?sz=64&domain=ublockorigin.com
// @grant        GM_addStyle
// @grant        GM_addElement
// @grant        GM_getValue
// @grant        GM_setValue
// ==/UserScript==

(function() {
    'use strict';

    let DEFAULT_CONFIG = {currentDomainIndex: 0, domainList: []};

    GM_addStyle(`
        .uBlock_Origin_dev_filter__container {
            position: fixed;
            top: 5em;
            right: 1em;
            padding: 1em;
            background-color: rgba(0, 0, 0, 0.2);
            z-index: 100000;
        }
        .uBlock_Origin_dev_filter__container button, .uBlock_Origin_dev_filter__container input[type=submit]{
            all: revert;
        }

        .uBlock_Origin_dev_filter__container hr {
            margin: 0.5em 0;
        }

        .uBlock_Origin_dev_filter__hidden {
            display: none;
        }
    `);

    const getConfig = () => {
        return JSON.parse(GM_getValue("config", JSON.stringify(DEFAULT_CONFIG)))
    }
    const setConfig = (config) => {
        return GM_setValue("config", JSON.stringify(config));
    }

    const generateLinks = (parent, domain, go_to_next_domain = false) => {
        for(const q of ["How to Linux site:{DOMAIN}", "How to site:{DOMAIN}", "site:{DOMAIN}"]){
            const el = document.createElement("a");
            el.href = "#";
            el.addEventListener("click", e => {
                if(go_to_next_domain){
                    const config = getConfig();
                    config.currentDomainIndex += 1;
                    setConfig(config);
                }
                e.preventDefault(); doGoogleQuery(q.replaceAll("{DOMAIN}", domain));
            });
            el.textContent = q;
            parent.appendChild(el)
            parent.appendChild(document.createElement("br"))
        }
    }

    const doGoogleQuery = (query) => {
        const input = document.querySelector("input.gLFyf, textarea.gLFyf");
        input.value = query;
        input.form.submit();
    }

    const generateUI = () => {
        let config = DEFAULT_CONFIG;
        let current_domain, next_domain, current_domain_index;
        try{
            config = JSON.parse(GM_getValue("config", JSON.stringify(DEFAULT_CONFIG)));

            const current_domain_index = config.currentDomainIndex || 0;
            current_domain = config.domainList[current_domain_index];
            next_domain = config.domainList[current_domain_index + 1];
        } catch (error) {
            console.exception(error);
        }

        const old_container = document.querySelector(".uBlock_Origin_dev_filter__container");
        if(old_container){
            old_container.remove();
        }
        const container = document.createElement("div");
        container.classList.add("uBlock_Origin_dev_filter__container");

        container.innerHTML = `
uBlock-Origin-dev-filter/Review<br>
<button class="uBlock_Origin_dev_filter__edit_list_open_button">Edit domain list</button>
<hr>
<form class="uBlock_Origin_dev_filter__edit_list_form uBlock_Origin_dev_filter__hidden">
List of domains to review:<p>
<textarea name="uBlock_Origin_dev_filter__edit_list_textarea" rows="5" cols="40"></textarea><br>
<input type="submit" value="Submit">
<hr>
</form>`;

        if(current_domain){
            container.innerHTML += `
Current: <strong><a href="//${current_domain}">${current_domain}</a></strong>
<div class="uBlock_Origin_dev_filter__current_domain_links"></div>`;
        }

        if(next_domain){
            container.innerHTML += `
<hr>
Next: ${next_domain}<br>
<div class="uBlock_Origin_dev_filter__next_domain_links"></div>`;
        }
        document.body.appendChild(container);

        if(current_domain){
            generateLinks(container.querySelector(".uBlock_Origin_dev_filter__current_domain_links"), current_domain);
        }
        if(next_domain){
            generateLinks(container.querySelector(".uBlock_Origin_dev_filter__next_domain_links"), next_domain, true);
        }

        const edit_list_form = document.querySelector(".uBlock_Origin_dev_filter__edit_list_form");
        edit_list_form.addEventListener("submit", e => {
            e.preventDefault();
            const form_data = new FormData(edit_list_form);
            let edit_list = form_data.get("uBlock_Origin_dev_filter__edit_list_textarea");
            edit_list = edit_list.replaceAll("*://", "").replaceAll("/*", "");

            const new_config = JSON.parse(JSON.stringify(DEFAULT_CONFIG));
            new_config.domainList = edit_list.split("\n");

            setConfig(new_config);

            generateUI();
        });

        document.querySelector(".uBlock_Origin_dev_filter__edit_list_open_button").addEventListener("click", () => {
            console.log(config);
            edit_list_form.classList.remove("uBlock_Origin_dev_filter__hidden");
            edit_list_form.querySelector("textarea[name=uBlock_Origin_dev_filter__edit_list_textarea]").value = config.domainList.join("\n");
        });
    }

    generateUI();
})();
