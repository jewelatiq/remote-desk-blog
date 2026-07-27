# The Remote Desk — English Affiliate Blog

A free, static, SEO-friendly blog focused on the Home Office / Remote Work niche —
built to pair with NordVPN and Amazon Associates affiliate links.

## What's inside
```
remote-blog/
├── index.html          ← homepage (auto-generated, don't edit by hand)
├── about.html          ← about page (auto-generated)
├── disclosure.html     ← affiliate disclosure page (auto-generated)
├── posts/              ← one static HTML page per post (auto-generated)
├── posts.json          ← YOUR CONTENT — add new posts here
├── build.py             ← regenerates all HTML from posts.json
├── css/style.css
├── js/script.js
├── sitemap.xml         ← auto-generated
└── robots.txt          ← auto-generated
```

## Adding a new post
1. Open `posts.json`.
2. Add a new object like this:

```json
{
  "slug": "your-post-slug",
  "title": "Your Post Title",
  "excerpt": "One or two sentence summary — shown in search results.",
  "date": "2026-07-20",
  "tags": ["Home Office"],
  "content": [
    "First paragraph.",
    "Second paragraph with a [product link](https://amazon.com/your-affiliate-link) inside it."
  ]
}
```

Note the `[text](URL)` format — this automatically becomes a clickable affiliate link.

3. Run:
```bash
python3 build.py
```

## Adding your affiliate links
Once approved by NordVPN and/or Amazon Associates, replace plain text mentions like
"NordVPN" or "a laptop stand" in `posts.json` with `[NordVPN](https://your-affiliate-link)`
or `[laptop stand](https://amazon.com/your-affiliate-link)`, then run `python3 build.py` again.

## Deploying for free
Same process as before — no domain or hosting cost required.

### Netlify (drag & drop)
1. Go to app.netlify.com and log in (or create a free account).
2. "Add new site" → "Deploy manually".
3. Drag the whole `remote-blog` folder (or its zip) into the upload box.
4. You'll get a free link like `https://something-random.netlify.app`.

### After deploying
Open `build.py`, update `SITE_URL` at the top with your real live link, then run
`python3 build.py` again and re-upload — this keeps your sitemap and SEO tags accurate.

## Before applying to NordVPN / Amazon Associates
Update `SITE_URL` first (see above) so you have a real link to put in the affiliate
application forms.
