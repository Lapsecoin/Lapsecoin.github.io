#!/usr/bin/env python3
"""Builds the site: each page in src/pages/ gets the shared head, header and
footer defined here, and the result is written to the repository root, which
is what GitHub Pages serves.

    python src/build.py            write the pages
    python src/build.py --check    exit 1 if the written pages are out of date

Edit src/pages/*.html for content and this file for anything shared
(navigation, footer, share cards). Never edit the generated .html files in
the root.
"""

import html
import os
import sys

SRC = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SRC)

SITE = "https://lapsecoin.github.io"
NAME = "LapseCoin"
LOGO = f"{SITE}/logo-512.png"
SUPPORT_ADDRESS = ("quality.occur.weird.force.hawk.joy.dice."
                   "kid.someone.box.cushion.quarter")
# Also in the README of lapsecoin/core.
BITCOIN_ADDRESS = "bc1q8qxvr5zuws78650wz9rgzpqxfx7dqzl38rdtsw"
DISCORD = "https://discord.gg/FP2d8JmK6r"
GITHUB = "https://github.com/Lapsecoin/core"
RELEASES = "downloads.html"          # the page that lists them; GitHub has the full history
WHITEPAPER = "https://lapsecoin.github.io/core/whitepaper.html"   # published by lapsecoin/core
LIVE_NODE = "https://lapsenode.vicnas.me/"

HOME_DESCRIPTION = (
    "Peer-to-peer electronic cash secured by a Verifiable Delay Function instead "
    "of proof-of-work, with FALCON-512 signatures. About 120 seconds per block, "
    "supply capped at 21 million LAPSE.")

# file, source fragment, <title>, description (also the share card text)
PAGES = [
    ("index.html", "index", NAME, HOME_DESCRIPTION),
    ("api.html", "api", "Public API | LapseCoin",
     "Public read-only HTTP API served by every LapseCoin node: chain info, blocks, "
     "transactions, addresses, fees and broadcast."),
    ("tx.html", "tx", "Transactions | LapseCoin",
     "LapseCoin transaction format, canonical JSON signing with FALCON-512, address "
     "derivation, and Python examples."),
    ("exchange.html", "exchange", "Exchange integration | LapseCoin",
     "Integrating LapseCoin for exchanges: Bitcoin Core RPC equivalents, deposit "
     "detection, withdrawals and cold storage."),
    ("downloads.html", "downloads", "Download LapseCoin",
     "Download LapseCoin for Windows and Linux. The newest releases with the SHA256 and "
     "VirusTotal result of each installer."),
    ("privacy.html", "privacy", "Privacy policy | LapseCoin",
     "What LapseCoin and this website do with your data: no accounts, keys stay on your "
     "device, what the public network shows, and which outside services are contacted."),
    ("wallets.html", "wallets", "Wallet integration | LapseCoin",
     "How a wallet derives a LapseCoin key from the recovery phrase a user already "
     "has, using BIP-39, BIP-85 and seeded FALCON-512 key generation, with test vectors."),
]

DOCS_MENU = [
    ("api.html", "API reference"),
    ("tx.html", "Transactions"),
    ("exchange.html", "Exchange integration"),
    ("wallets.html", "Wallet integration"),
    (WHITEPAPER, "Whitepaper"),
]

ICON_DISCORD = ('<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M13.545 2.907a13.2 13.2 0 0 0-3.257-1.011.05.05 0 0 0-.052.025c-.141.25-.297.577-.406.833a12.2 12.2 0 0 0-3.658 0 8 8 0 0 0-.412-.833.05.05 0 0 0-.052-.025c-1.125.194-2.22.534-3.257 1.011a.04.04 0 0 0-.021.018C.356 6.024-.213 9.047.066 12.032q.003.022.021.037a13.3 13.3 0 0 0 3.995 2.02.05.05 0 0 0 .056-.019q.463-.63.818-1.329a.05.05 0 0 0-.01-.059.05.05 0 0 0-.018-.011 8.9 8.9 0 0 1-1.248-.595.05.05 0 0 1-.02-.066.05.05 0 0 1 .015-.019q.127-.095.248-.195a.05.05 0 0 1 .051-.007c2.619 1.196 5.454 1.196 8.041 0a.05.05 0 0 1 .053.007q.121.1.248.195a.05.05 0 0 1-.004.085 8 8 0 0 1-1.249.594.05.05 0 0 0-.03.03.05.05 0 0 0 .003.041c.24.465.515.909.817 1.329a.05.05 0 0 0 .056.019 13.2 13.2 0 0 0 4.001-2.02.05.05 0 0 0 .021-.037c.334-3.451-.559-6.449-2.366-9.106a.03.03 0 0 0-.02-.019m-8.198 7.307c-.789 0-1.438-.724-1.438-1.612s.637-1.613 1.438-1.613c.807 0 1.45.73 1.438 1.613 0 .888-.637 1.612-1.438 1.612m5.316 0c-.788 0-1.438-.724-1.438-1.612s.637-1.613 1.438-1.613c.807 0 1.451.73 1.438 1.613 0 .888-.631 1.612-1.438 1.612"/></svg>')
ICON_GITHUB = ('<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82a7.6 7.6 0 0 1 4 0c1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.01 8.01 0 0 0 16 8c0-4.42-3.58-8-8-8z"/></svg>')
ICON_CHEVRON = ('<svg class="chev" viewBox="0 0 12 12" aria-hidden="true"><path d="M2.5 4.5 6 8l3.5-3.5" '
                'fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" '
                'stroke-linejoin="round"/></svg>')


def esc(s):
    return html.escape(s, quote=True)


def page_url(filename):
    return SITE + "/" if filename == "index.html" else f"{SITE}/{filename}"


def head(filename, title, description):
    url = page_url(filename)
    card_title = title.removesuffix(" | " + NAME)   # the card already shows the site name above it
    return f"""<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<link rel="icon" type="image/svg+xml" href="lapsecoin.svg">
<link rel="canonical" href="{url}">
<meta property="og:site_name" content="{NAME}">
<meta property="og:type" content="website">
<meta property="og:title" content="{esc(card_title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{LOGO}">
<meta property="og:image:width" content="512">
<meta property="og:image:height" content="512">
<meta name="twitter:card" content="summary">
<meta name="theme-color" content="#f4f1ea">
<link rel="preload" href="css/fonts/Geist-Variable.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="css/site.css">
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-2XWCJKT8GJ"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());

  gtag('config', 'G-2XWCJKT8GJ');
</script>
</head>"""


def header(filename):
    on_docs = any(filename == f for f, _ in DOCS_MENU)
    items = []
    for href, label in DOCS_MENU:
        current = ' aria-current="page"' if href == filename else ""
        items.append(f'<a href="{href}"{current}>{label}</a>')
    menu = (
        '<div class="menu">'
        f'<button class="menu-btn{" on" if on_docs else ""}" type="button" aria-expanded="false" '
        f'aria-controls="menu-docs">Documentation{ICON_CHEVRON}</button>'
        f'<div class="menu-list" id="menu-docs">{"".join(items)}</div></div>')
    return f"""<header class="bar"><div class="bar-in">
<a class="brand" href="index.html"><img src="lapsecoin.svg" alt="" width="22" height="22">{NAME}</a>
<nav class="nav" aria-label="Site"><a href="downloads.html"{' aria-current="page"' if filename == "downloads.html" else ""}>Download</a><a href="index.html#start">Get started</a>{menu}<a href="index.html#community">Community</a><a href="index.html#support">Support</a></nav>
<div class="ext"><a href="{DISCORD}">{ICON_DISCORD}<span>Discord</span></a><a href="{GITHUB}">{ICON_GITHUB}<span>GitHub</span></a></div>
</div></header>"""


def footer():
    docs = "".join(f'<a href="{href}">{label}</a>' for href, label in DOCS_MENU)
    return f"""<footer><div class="wrap">
<div class="foot">
<div class="foot-brand"><a class="brand" href="index.html"><img src="lapsecoin.svg" alt="" width="22" height="22">{NAME}</a><p>Peer-to-peer electronic cash.</p></div>
<div class="foot-col"><b>Start</b><a href="{RELEASES}">Download a release</a><a href="index.html#run">Run a node</a><a href="index.html#how">How it works</a></div>
<div class="foot-col"><b>Documentation</b>{docs}</div>
<div class="foot-col"><b>Community</b><a href="{DISCORD}">Discord</a><a href="{GITHUB}">GitHub</a><a href="{LIVE_NODE}">Live node</a><a href="index.html#support">Support {NAME}</a></div>
</div>
<p class="legal">{NAME} is open source, released under the MIT license. <a href="privacy.html">Privacy policy</a></p>
</div></footer>"""


def render(filename, source, title, description):
    with open(os.path.join(SRC, "pages", source + ".html"), encoding="utf-8") as f:
        body = f.read().strip()
    # Wrap the address between words, never inside one. <wbr> adds no text, so
    # copying the element still gives the plain address.
    body = body.replace("@@SUPPORT_ADDRESS_HTML@@", ".<wbr>".join(SUPPORT_ADDRESS.split(".")))
    body = body.replace("@@BITCOIN_ADDRESS@@", BITCOIN_ADDRESS)
    extra_script = '\n<script src="js/downloads.js" defer></script>' if filename == "downloads.html" else ""
    return f"""<!doctype html>
<!-- Generated by src/build.py from src/pages/{source}.html. Edit those, not this file. -->
<html lang="en">
{head(filename, title, description)}
<body>
{header(filename)}
<main>{body}</main>
{footer()}
<script src="js/site.js" defer></script>{extra_script}
</body>
</html>
"""


def main():
    check = "--check" in sys.argv
    stale = []
    for filename, source, title, description in PAGES:
        out = render(filename, source, title, description)
        path = os.path.join(ROOT, filename)
        if check:
            current = open(path, encoding="utf-8").read() if os.path.exists(path) else None
            if current != out:
                stale.append(filename)
        else:
            with open(path, "w", encoding="utf-8") as f:
                f.write(out)
            print("wrote", filename)
    if check and stale:
        print("out of date:", ", ".join(stale), "(run python src/build.py)")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
