"""Look up motion references on prompt-motion.com while planning a video (reference use only).

  python motion_refs.py tags                         the tags (Product UI, Kinetic type, Characters, ...)
  python motion_refs.py list kinetic-type [-n 10]    newest entries for a tag: title, author, size, link
  python motion_refs.py show <url or slug>           one entry: title, tags, author, and its prompt or skill text

The site says (robots.txt) its content may be used for reference, not for training, so this script reads a
few pages on demand, prints them, and stores nothing. Do not save or bulk-copy the prompts. Read 2 or 3
entries, take the ideas (structure, timing, transitions, gotchas), build them with this skill's own engine,
and credit the entries you learned from (author + link) in the project notes. See references/prompt-motion.md.
"""
import html, json, re, sys, time, urllib.request

BASE = 'https://prompt-motion.com'
TAGS = ['product-ui', 'phone', 'charts', 'diagrams', 'kinetic-type', 'shapes', 'particles', 'characters', 'photos', 'music', 'code']


def get(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'metis-demo-video/1.4 (reference lookup)'})
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read().decode('utf-8', 'replace')


def meta(page):
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', page, re.S):
        try:
            d = json.loads(m.group(1))
        except ValueError:
            continue
        if d.get('@type') == 'VideoObject':
            return d
    return {}


def text_of(page):
    m = re.search(r'<main[^>]*>(.*)</main>', page, re.S)
    t = re.sub(r'<script.*?</script>', '', m.group(1) if m else page, flags=re.S)
    t = re.sub(r'<br\s*/?>|</p>|</div>|</h\d>|</li>', '\n', t)
    t = html.unescape(re.sub(r'<[^>]+>', ' ', t))
    return re.sub(r'[ \t]+', ' ', re.sub(r'\n\s*\n+', '\n', t)).strip()


def cmd_list(tag, n):
    page = get('%s/tags/%s' % (BASE, tag))
    slugs = list(dict.fromkeys(re.findall(r'href="/([a-z0-9_-]+-[0-9a-f]{6,7})"', page)))[:n]
    if not slugs:
        sys.exit('No entries found for tag "%s". Tags: %s' % (tag, ', '.join(TAGS)))
    for s in slugs:
        d = meta(get('%s/%s' % (BASE, s)))
        print('- %s  (@%s, %sx%s)\n  %s/%s' % (d.get('name', s), (d.get('creator') or {}).get('url', '').rsplit('/', 1)[-1],
                                             d.get('width', '?'), d.get('height', '?'), BASE, s))
        time.sleep(0.4)                                    # be gentle with the site


def cmd_show(ref):
    url = ref if ref.startswith('http') else '%s/%s' % (BASE, ref.strip('/'))
    page = get(url)
    d = meta(page)
    body = text_of(page)
    start = body.find('Copy')
    end = body.find('This prompt was taken')
    core = body[start + 4:end if end > 0 else None].strip() if start >= 0 else body
    print('# %s\nby %s  |  %sx%s  |  %s\nvideo: %s\n' % (d.get('name', ''), (d.get('creator') or {}).get('url', ''), d.get('width', '?'),
                                                      d.get('height', '?'), url, d.get('contentUrl', '')))
    print(core[:6000])
    print('\n(reference only: adapt the ideas, do not paste this text into the project; credit %s)' % url)


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    a = sys.argv[1:]
    if not a or a[0] == 'tags':
        print('\n'.join(TAGS)); return
    if a[0] == 'list':
        n = int(a[a.index('-n') + 1]) if '-n' in a else 10
        cmd_list(a[1] if len(a) > 1 else 'product-ui', n); return
    if a[0] == 'show' and len(a) > 1:
        cmd_show(a[1]); return
    print(__doc__)


if __name__ == '__main__':
    main()
