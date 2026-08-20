"""Add the Google Tag Manager container to every page.

    python3 add_gtm.py GTM-XXXXXXX              # add GTM, leave GA4 alone
    python3 add_gtm.py GTM-XXXXXXX --drop-ga4   # add GTM, remove hardcoded GA4

Run --drop-ga4 only once marketing has published the GA4 tag inside GTM,
otherwise analytics goes dark in between. Idempotent: re-running skips
pages that already have the container.
"""

import os
import re
import sys

GA4_ID = "G-ZQLC2P562C"
FOLDERS = [".", "us", "ca", "hk", "in"]
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


def head_snippet(gtm_id):
    return f"""<!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':
new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
}})(window,document,'script','dataLayer','{gtm_id}');</script>
<!-- End Google Tag Manager -->"""


def body_snippet(gtm_id):
    # noscript fallback must be the first thing inside <body>
    return f"""<!-- Google Tag Manager (noscript) -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id={gtm_id}"
height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<!-- End Google Tag Manager (noscript) -->"""


def strip_ga4(content):
    """Remove the hardcoded gtag.js block, leaving GA4 to GTM."""
    pattern = re.compile(
        r"\s*<!-- Google tag \(gtag\.js\) -->.*?gtag\('config',\s*'"
        + re.escape(GA4_ID)
        + r"'\);\s*</script>",
        re.DOTALL,
    )
    return pattern.sub("", content)


def main():
    if len(sys.argv) < 2 or not sys.argv[1].upper().startswith("GTM-"):
        sys.exit("usage: python3 add_gtm.py GTM-XXXXXXX [--drop-ga4]")

    gtm_id = sys.argv[1].upper()
    drop_ga4 = "--drop-ga4" in sys.argv
    head, body = head_snippet(gtm_id), body_snippet(gtm_id)
    changed = skipped = 0

    for folder in FOLDERS:
        folder_path = os.path.join(ROOT_DIR, folder)
        if not os.path.isdir(folder_path):
            continue
        for name in sorted(os.listdir(folder_path)):
            if not name.endswith(".html"):
                continue
            path = os.path.join(folder_path, name)
            with open(path, encoding="utf-8") as f:
                content = original = f.read()

            # Already-tagged pages still need the GA4 strip, so don't skip the
            # whole file here — only skip re-inserting the container.
            if gtm_id in content:
                skipped += 1
            elif "<head>" in content or "</head>" in content:
                if "<head>" in content:
                    content = content.replace("<head>", f"<head>\n{head}", 1)
                else:
                    content = content.replace("</head>", f"{head}\n</head>", 1)

                # <body> may carry attributes, so match the whole opening tag
                m = re.search(r"<body[^>]*>", content, re.IGNORECASE)
                if m:
                    content = content[: m.end()] + f"\n{body}" + content[m.end():]
                else:
                    print(f"WARN    {folder}/{name}: no <body>, head tag only")
            else:
                print(f"WARN    {folder}/{name}: no <head>, skipped")
                continue

            if drop_ga4:
                content = strip_ga4(content)

            if content != original:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"ok      {folder}/{name}")
                changed += 1
            else:
                print(f"skip    {folder}/{name} (nothing to do)")

    print(f"\n{changed} updated, {skipped} already had {gtm_id}"
          + (", GA4 stripped where present" if drop_ga4 else ""))


def demo():
    """Self-check: run with no GTM id -> python3 add_gtm.py --test"""
    page = (
        "<!DOCTYPE html>\n<html>\n<head>\n"
        "<!-- Google tag (gtag.js) -->\n"
        '<script async src="https://www.googletagmanager.com/gtag/js?id=G-ZQLC2P562C"></script>\n'
        "<script>\n  window.dataLayer = window.dataLayer || [];\n"
        "  function gtag(){dataLayer.push(arguments);}\n  gtag('js', new Date());\n\n"
        "  gtag('config', 'G-ZQLC2P562C');\n</script>\n"
        "<title>x</title>\n</head>\n<body class='a'>\n<h1>hi</h1>\n</body>\n</html>"
    )
    out = page.replace("<head>", "<head>\n" + head_snippet("GTM-TEST123"), 1)
    m = re.search(r"<body[^>]*>", out, re.IGNORECASE)
    out = out[: m.end()] + "\n" + body_snippet("GTM-TEST123") + out[m.end():]

    assert out.count("GTM-TEST123") == 2, "need head + noscript tag"
    assert out.index("gtm.js?id=") < out.index("<title>"), "head tag must precede title"
    assert out.index("ns.html?id=") > out.index("<body class='a'>"), "noscript goes inside body"
    assert GA4_ID in out, "GA4 untouched without --drop-ga4"

    stripped = strip_ga4(out)
    assert GA4_ID not in stripped, "--drop-ga4 must remove every GA4 reference"
    assert "GTM-TEST123" in stripped, "stripping GA4 must not touch GTM"
    assert "<title>x</title>" in stripped, "stripping GA4 must not eat other head tags"
    print("self-check passed")


if __name__ == "__main__":
    demo() if "--test" in sys.argv else main()
