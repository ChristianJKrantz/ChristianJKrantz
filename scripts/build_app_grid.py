"""Rebuild the app grid sections of README.md from apps.json.

Each app needs a name, a slug and a description. By default the slug is used for:
  live app:   https://christianjkrantz.github.io/<slug>/
  repo:       https://github.com/ChristianJKrantz/<slug>
  screenshot: https://christianjkrantz.github.io/assets/img/projects/<slug>.jpg
Set "live", "repo" or "image" on an app to override any of these.

Everything between the apps:start and apps:end markers in README.md is replaced.
"""
import html
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
README = ROOT / "README.md"
APPS = ROOT / "apps.json"
START = "<!-- apps:start (generated from apps.json, edit that file instead) -->"
END = "<!-- apps:end -->"
SITE = "https://christianjkrantz.github.io"
GITHUB = "https://github.com/ChristianJKrantz"


def cell(app):
    slug = app.get("slug", "")
    live = app.get("live") or f"{SITE}/{slug}/"
    repo = app.get("repo") or f"{GITHUB}/{slug}"
    image = app.get("image") or f"{SITE}/assets/img/projects/{slug}.jpg"
    name = html.escape(app["name"])
    desc = html.escape(app["description"], quote=False)
    return (
        '    <td width="50%" valign="top">\n'
        f'      <a href="{live}"><img src="{image}" alt="{name} screenshot" width="100%"></a>\n'
        "      <br>\n"
        f'      <strong><a href="{live}">{name}</a></strong> · <a href="{repo}">repo</a>\n'
        "      <br>\n"
        f"      <sub>{desc}</sub>\n"
        "    </td>"
    )


def section(sec):
    apps = sec["apps"]
    rows = []
    for i in range(0, len(apps), 2):
        cells = "\n".join(cell(a) for a in apps[i : i + 2])
        rows.append(f"  <tr>\n{cells}\n  </tr>\n")
    parts = [f"## {sec['title']}\n\n"]
    if sec.get("intro"):
        parts.append(f"{sec['intro']}\n\n")
    parts.append("<table>\n" + "".join(rows) + "</table>\n")
    return "".join(parts)


def main():
    data = json.loads(APPS.read_text(encoding="utf-8"))
    body = "\n".join(section(s) for s in data["sections"] if s.get("apps"))
    readme = README.read_text(encoding="utf-8")
    if START not in readme or END not in readme:
        sys.exit("README.md is missing the apps:start / apps:end markers")
    head, rest = readme.split(START, 1)
    _, tail = rest.split(END, 1)
    new = f"{head}{START}\n{body}{END}{tail}"
    if new != readme:
        README.write_text(new, encoding="utf-8")
        print("README.md updated")
    else:
        print("README.md already up to date")


if __name__ == "__main__":
    main()
