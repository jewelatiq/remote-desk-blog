#!/usr/bin/env python3
"""
Blog build script
------------------
Reads posts.json and generates static, SEO-friendly HTML pages:
  - index.html
  - posts/<slug>.html (one static page per post, for search engines)
  - sitemap.xml
  - robots.txt

Usage:
    python3 build.py

To add a new post, add an object to posts.json and re-run this script.
"""
import json, os, html, re
from datetime import datetime

# ---- SITE SETTINGS ----
SITE_NAME = "The Remote Desk"
SITE_TAGLINE = "Honest gear picks and tools for remote workers and freelancers"
SITE_URL = "https://jewelatiq.github.io/remote-desk-blog"   # UPDATE after deploying
AUTHOR_NAME = "The Remote Desk"
SITE_DESCRIPTION = "Practical, no-nonsense reviews of gadgets, tools, and software for people who work from home."
GA_MEASUREMENT_ID = "G-9RYHH8NSSM"   # add your Google Analytics Measurement ID here, e.g. G-XXXXXXXXXX
GOOGLE_SITE_VERIFICATION = "pC2yzblnEojDcejnRtOFEmRbPtyA6bJozd5lT84xbW8"
# ------------------------

ROOT = os.path.dirname(os.path.abspath(__file__))

def load_posts():
    with open(os.path.join(ROOT, "posts.json"), encoding="utf-8") as f:
        posts = json.load(f)
    posts.sort(key=lambda p: p["date"], reverse=True)
    return posts

def read_time(content_paragraphs):
    words = sum(len(p.split()) for p in content_paragraphs)
    minutes = max(1, round(words / 200))
    return f"{minutes} min read"

def fmt_date(iso_date):
    d = datetime.strptime(iso_date, "%Y-%m-%d")
    return d.strftime("%B %-d, %Y") if os.name != "nt" else d.strftime("%B %d, %Y")

def all_tags(posts):
    tags = []
    for p in posts:
        for t in p["tags"]:
            if t not in tags:
                tags.append(t)
    return tags

LINK_RE = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')

def render_paragraph(text):
    """[label](URL) becomes a clickable link — use this to insert affiliate links."""
    escaped = html.escape(text)
    def repl(m):
        label, url = m.group(1), m.group(2)
        return f'<a href="{url}" target="_blank" rel="nofollow sponsored noopener" style="color:var(--teal-deep);border-bottom:1px solid var(--teal-deep);">{label}</a>'
    return LINK_RE.sub(repl, escaped)

TAG_COLOR_MAP = {
    "Home Office": "teal", "Gadgets": "gold", "Security": "blue",
    "Remote Work": "plum", "Furniture": "rust",
}

def tag_class(tag):
    return f"tag tag-{TAG_COLOR_MAP.get(tag, 'rust')}"

def ga_snippet():
    if not GA_MEASUREMENT_ID:
        return ""
    return f"""<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id={GA_MEASUREMENT_ID}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', '{GA_MEASUREMENT_ID}');
</script>"""

HEAD_TEMPLATE = """<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="google-site-verification" content="{google_verify}">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{canonical}">
<meta property="og:site_name" content="{site_name}">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{description}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,600;9..144,700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
{extra_css_path}
{jsonld}
"""

def head(title, description, canonical, css_path, og_type="website", jsonld=""):
    return HEAD_TEMPLATE.format(
        title=html.escape(title),
        description=html.escape(description),
        canonical=canonical,
        og_type=og_type,
        site_name=SITE_NAME,
        extra_css_path=f'<link rel="stylesheet" href="{css_path}">',
        jsonld=jsonld,
        google_verify=GOOGLE_SITE_VERIFICATION
    ) + "\n" + ga_snippet()

def masthead(nav_prefix="", tags=None):
    tags = tags or []
    tag_links = "".join(
        f'<a href="{nav_prefix}index.html#" data-tag-filter="{html.escape(t)}">{html.escape(t)}</a>'
        for t in tags[:4]
    )
    return f"""
<header class="masthead">
  <div class="wrap">
    <a href="{nav_prefix}index.html" class="logo">{SITE_NAME}<span>.</span></a>
    <nav class="nav">
      <a href="{nav_prefix}index.html" data-tag-filter="all">All Posts</a>
      {tag_links}
      <a href="{nav_prefix}about.html">About</a>
    </nav>
    <div class="search-box">
      <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
      <input id="searchInput" type="text" placeholder="Search articles…" autocomplete="off">
    </div>
  </div>
  <div class="masthead-meta">
    <div class="wrap">
      <span>{SITE_TAGLINE}</span>
      <span>Est. {datetime.now().year}</span>
    </div>
  </div>
</header>
"""

def footer(nav_prefix=""):
    return f"""
<footer>
  <div class="wrap">
    <span><span class="foot-logo">{SITE_NAME}</span> &nbsp;·&nbsp; &copy; {datetime.now().year} All rights reserved.</span>
    <span><a href="{nav_prefix}about.html">About</a> &nbsp;·&nbsp; <a href="{nav_prefix}disclosure.html">Affiliate Disclosure</a> &nbsp;·&nbsp; <a href="{nav_prefix}sitemap.xml">Sitemap</a></span>
  </div>
</footer>
"""

def build_index(posts):
    tags = all_tags(posts)
    featured, rest = posts[0], posts[1:]

    jsonld = f"""<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Blog",
  "name": "{SITE_NAME}",
  "description": "{SITE_DESCRIPTION}",
  "url": "{SITE_URL}/"
}}
</script>"""

    cards_html = ""
    for p in rest:
        tags_attr = " ".join(p["tags"])
        search_attr = (p["title"] + " " + p["excerpt"] + " " + " ".join(p["tags"])).lower()
        cards_html += f"""
      <a class="card card-{TAG_COLOR_MAP.get(p['tags'][0], 'rust')}" href="posts/{p['slug']}.html" data-card data-tags="{html.escape(tags_attr)}" data-search="{html.escape(search_attr)}">
        <span class="{tag_class(p['tags'][0])}">{html.escape(p['tags'][0])}</span>
        <h3>{html.escape(p['title'])}</h3>
        <p>{html.escape(p['excerpt'])}</p>
        <div class="byline"><span>{fmt_date(p['date'])}</span><span class="dot">{read_time(p['content'])}</span></div>
      </a>"""

    body = f"""<!DOCTYPE html>
<html lang="en">
<head>
{head(SITE_NAME + " — " + SITE_TAGLINE, SITE_DESCRIPTION, SITE_URL + "/", "css/style.css", jsonld=jsonld)}
</head>
<body>
{masthead(tags=tags)}
<main class="wrap">
  <section class="featured">
    <span class="eyebrow">Latest Post</span>
    <a href="posts/{featured['slug']}.html"><h1>{html.escape(featured['title'])}</h1></a>
    <p class="excerpt">{html.escape(featured['excerpt'])}</p>
    <div class="byline">
      <span>{fmt_date(featured['date'])}</span>
      <span class="dot">{read_time(featured['content'])}</span>
      <span class="dot">{html.escape(featured['tags'][0])}</span>
    </div>
    <a class="read-more" href="posts/{featured['slug']}.html">Read the full post →</a>
  </section>

  <h2 class="section-label">All Posts</h2>
  <div class="grid" id="postGrid">{cards_html}
  </div>
  <p class="empty-state" id="emptyState" style="display:none;">No posts found. Try a different search term.</p>
</main>
{footer()}
<script src="js/script.js"></script>
</body>
</html>"""
    with open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8") as f:
        f.write(body)

def build_post(post, all_posts):
    description = post["excerpt"]
    canonical = f"{SITE_URL}/posts/{post['slug']}.html"
    jsonld = f"""<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "headline": {json.dumps(post['title'], ensure_ascii=False)},
  "description": {json.dumps(description, ensure_ascii=False)},
  "datePublished": "{post['date']}",
  "author": {{"@type": "Person", "name": "{AUTHOR_NAME}"}},
  "url": "{canonical}"
}}
</script>"""

    paragraphs_html = "\n".join(f"<p>{render_paragraph(p)}</p>" for p in post["content"])
    tags_html = "".join(f'<span class="{tag_class(t)}">{html.escape(t)}</span> ' for t in post["tags"])

    related = [p for p in all_posts if p["slug"] != post["slug"]][:2]
    related_html = ""
    for r in related:
        related_html += f"""
      <a class="card card-{TAG_COLOR_MAP.get(r['tags'][0], 'rust')}" href="{r['slug']}.html">
        <span class="{tag_class(r['tags'][0])}">{html.escape(r['tags'][0])}</span>
        <h3>{html.escape(r['title'])}</h3>
        <p>{html.escape(r['excerpt'])}</p>
        <div class="byline"><span>{fmt_date(r['date'])}</span></div>
      </a>"""

    body = f"""<!DOCTYPE html>
<html lang="en">
<head>
{head(post['title'] + " — " + SITE_NAME, description, canonical, "../css/style.css", og_type="article", jsonld=jsonld)}
</head>
<body>
<div class="progress" id="progressBar"></div>
{masthead(nav_prefix="../")}
<main>
  <div class="wrap">
    <div class="post-head">
      <span class="eyebrow">{html.escape(post['tags'][0])}</span>
      <h1>{html.escape(post['title'])}</h1>
      <div class="byline">
        <span>{fmt_date(post['date'])}</span>
        <span class="dot">{read_time(post['content'])}</span>
        <span class="dot">{tags_html}</span>
      </div>
    </div>
    <article class="post-body">
      {paragraphs_html}
    </article>
    <div class="post-foot">
      <a href="../index.html" style="font-size:14px;color:var(--muted);">← Back to all posts</a>
      <button class="share-btn" id="copyLinkBtn">Copy link</button>
    </div>
  </div>
  {"<div class='related'><h2 class='section-label'>Related Posts</h2><div class='grid'>" + related_html + "</div></div>" if related_html else ""}
</main>
{footer(nav_prefix="../")}
<script src="../js/script.js"></script>
</body>
</html>"""
    os.makedirs(os.path.join(ROOT, "posts"), exist_ok=True)
    with open(os.path.join(ROOT, "posts", f"{post['slug']}.html"), "w", encoding="utf-8") as f:
        f.write(body)

def build_about():
    canonical = f"{SITE_URL}/about.html"
    body = f"""<!DOCTYPE html>
<html lang="en">
<head>
{head("About — " + SITE_NAME, SITE_DESCRIPTION, canonical, "css/style.css")}
</head>
<body>
{masthead()}
<main class="wrap">
  <div class="post-head" style="border-bottom:none;">
    <span class="eyebrow">About</span>
    <h1>About This Site</h1>
  </div>
  <article class="post-body" style="margin-top:10px;">
    <p>{html.escape(SITE_TAGLINE)}. This site publishes honest, practical reviews of gadgets, software, and tools for people who work remotely — from laptop stands to VPNs to home office furniture.</p>
    <p>Contact: <a href="mailto:hello@example.com" style="color:var(--teal-deep);border-bottom:1px solid var(--teal-deep);">hello@example.com</a></p>
  </article>
</main>
{footer()}
</body>
</html>"""
    with open(os.path.join(ROOT, "about.html"), "w", encoding="utf-8") as f:
        f.write(body)

def build_disclosure():
    canonical = f"{SITE_URL}/disclosure.html"
    body = f"""<!DOCTYPE html>
<html lang="en">
<head>
{head("Affiliate Disclosure — " + SITE_NAME, "How this site earns money through affiliate links.", canonical, "css/style.css")}
</head>
<body>
{masthead()}
<main class="wrap">
  <div class="post-head" style="border-bottom:none;">
    <span class="eyebrow">Transparency</span>
    <h1>Affiliate Disclosure</h1>
  </div>
  <article class="post-body" style="margin-top:10px;">
    <p>Some posts on this site contain affiliate links, including links to Amazon and NordVPN. If you click one of these links and make a purchase or sign up, I may earn a commission at no additional cost to you.</p>
    <p>I only recommend products and services that I believe are genuinely useful for remote workers and freelancers. Affiliate relationships never influence which products I choose to write about.</p>
    <p>As an Amazon Associate, I earn from qualifying purchases.</p>
  </article>
</main>
{footer()}
</body>
</html>"""
    with open(os.path.join(ROOT, "disclosure.html"), "w", encoding="utf-8") as f:
        f.write(body)

def build_sitemap(posts):
    urls = [f"{SITE_URL}/", f"{SITE_URL}/about.html", f"{SITE_URL}/disclosure.html"] + [f"{SITE_URL}/posts/{p['slug']}.html" for p in posts]
    body = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for u in urls:
        body += f"  <url><loc>{u}</loc></url>\n"
    body += "</urlset>"
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(body)

def build_robots():
    body = f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n"
    with open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(body)

def main():
    posts = load_posts()
    build_index(posts)
    for p in posts:
        build_post(p, posts)
    build_about()
    build_disclosure()
    build_sitemap(posts)
    build_robots()
    print(f"Build complete: {len(posts)} posts, index.html, about.html, disclosure.html, sitemap.xml, robots.txt")

if __name__ == "__main__":
    main()
