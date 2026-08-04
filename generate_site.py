# -*- coding: utf-8 -*-
"""
Static site generator for the People Explained website.

Reads episodes.json (see extract_episodes.py in the main project for how
that file gets built/refreshed from the production pipeline's finished
videos) and renders every page as a plain, flat .html file at the repo
root, so relative links/assets work the same everywhere without needing
a subfolder-aware base path.

Usage: python generate_site.py
"""
import html
import json
import os

REPO = os.path.dirname(os.path.abspath(__file__))
SITE_NAME = "People Explained"
SITE_URL = "https://peopleexplained.github.io/people-explained-legal/"
CONTACT_EMAIL = "peopleexplained.channel@gmail.com"

with open(os.path.join(REPO, "episodes.json"), "r", encoding="utf-8") as f:
    EPISODES = json.load(f)

DETAIL_EPISODES = [e for e in EPISODES if e["has_detail"]]
EPISODE_COUNT = len(EPISODES)

NAV_ITEMS = [
    ("Home", "index.html"),
    ("Episodes", "episodes.html"),
    ("About", "about.html"),
    ("FAQ", "faq.html"),
    ("Contact", "contact.html"),
]

DEFAULT_OG_IMAGE = "assets/thumbs/albert-einstein.jpg"


def e(s):
    return html.escape(s, quote=True)


def render_nav(active):
    links = []
    for label, href in NAV_ITEMS:
        cls = ' class="active"' if href == active else ""
        links.append(f'<a href="{href}"{cls}>{label}</a>')
    return f'''<nav class="topnav">
    <div class="wrap">
      <a class="logo" href="index.html">People <span class="dot">Explained</span></a>
      <div class="links">{"".join(links)}</div>
    </div>
  </nav>'''


FOOTER = f'''<footer>
    <div class="links">
      <a href="privacy.html">Privacy Policy</a>
      <a href="terms.html">Terms of Service</a>
      <a href="imprint.html">Imprint</a>
      <a href="about.html">About</a>
    </div>
    <div>&copy; 2026 People Explained. All content is produced and operated by a single independent creator.</div>
  </footer>'''


def page(filename, title, description, active, body, og_image=DEFAULT_OG_IMAGE):
    full_title = title if title == SITE_NAME else f"{title} - {SITE_NAME}"
    doc = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{e(full_title)}</title>
  <meta name="description" content="{e(description)}">
  <link rel="canonical" href="{SITE_URL}{filename}">
  <link rel="icon" type="image/png" href="favicon.png">
  <link rel="stylesheet" href="assets/style.css">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{e(full_title)}">
  <meta property="og:description" content="{e(description)}">
  <meta property="og:image" content="{SITE_URL}{og_image}">
  <meta property="og:url" content="{SITE_URL}{filename}">
  <meta name="twitter:card" content="summary_large_image">
</head>
<body>
  {render_nav(active)}
{body}
  {FOOTER}
</body>
</html>
'''
    with open(os.path.join(REPO, filename), "w", encoding="utf-8") as fh:
        fh.write(doc)


def episode_card(ep, linkable):
    thumb = f'<div class="thumb"><img src="{ep["thumbnail"]}" alt="{e(ep["name"])} - People Explained episode thumbnail" loading="lazy"></div>'
    body = f'''<div class="body">
        <h3>{e(ep["name"])}</h3>
        <p>{e(ep["summary"])}</p>
        <div class="row">
          <span>Produced {ep["produced"]}</span>
          {'<span class="watch">Watch preview &rarr;</span>' if linkable else ''}
        </div>
      </div>'''
    inner = thumb + body
    if linkable:
        return f'<a class="episode-card" href="episode-{ep["slug"]}.html">{inner}</a>'
    return f'<div class="episode-card">{inner}</div>'


# ---------------------------------------------------------------- HOME ----
def build_home():
    latest = EPISODES[:3]
    cards = "\n        ".join(episode_card(ep, ep["has_detail"]) for ep in latest)
    body = f'''  <header class="hero">
    <div class="wrap">
      <div class="brand">People Explained</div>
      <h1>History, <span>explained</span> in 60 seconds.</h1>
      <p class="tagline">An automated documentary studio that turns historical and public figures into short, fact-checked educational videos, produced for TikTok, YouTube, and Instagram.</p>
      <p class="stat">{EPISODE_COUNT}+ episodes produced &middot; see the full archive below</p>
    </div>
  </header>

  <section id="how-it-works">
    <div class="wrap">
      <h2>How it works</h2>
      <p class="lead">People Explained is an end-to-end content pipeline, not a manual upload tool. Every episode goes through the same three stages.</p>
      <div class="steps">
        <div class="step">
          <div class="num">1</div>
          <h3>Research &amp; Script</h3>
          <p>Each episode starts from a curated list of historical and public figures. A script is generated from verified biographical facts, then structured into narration and on-screen chapters.</p>
        </div>
        <div class="step">
          <div class="num">2</div>
          <h3>Voice &amp; Visuals</h3>
          <p>The script is narrated with synthesized voice-over and paired with AI-generated scenes and captions, then assembled into a finished vertical video with subtitles and overlays.</p>
        </div>
        <div class="step">
          <div class="num">3</div>
          <h3>Human Review &amp; Publishing</h3>
          <p>Every finished episode is reviewed and approved by the operator before it is queued for publishing to the connected TikTok, YouTube, and Instagram accounts.</p>
        </div>
      </div>
    </div>
  </section>

  <section class="alt">
    <div class="wrap">
      <h2>Latest episodes</h2>
      <p class="lead">A small sample of the growing archive &mdash; browse all {EPISODE_COUNT} episodes for the full picture.</p>
      <div class="episode-grid">
        {cards}
      </div>
      <p style="text-align:center; margin-top:28px;"><a href="episodes.html">View the full episode archive &rarr;</a></p>
    </div>
  </section>
'''
    page("index.html", SITE_NAME,
         "People Explained produces short, fact-checked educational documentary videos about historical and public figures, and publishes them across TikTok, YouTube, and Instagram.",
         "index.html", body)


# ----------------------------------------------------------- EPISODES -----
def build_episodes():
    cards = "\n        ".join(episode_card(ep, ep["has_detail"]) for ep in EPISODES)
    body = f'''  <header class="pagehead">
    <div class="wrap">
      <h1>Episode Archive</h1>
      <p>{EPISODE_COUNT} episodes produced so far, each covering one historical or public figure in under 90 seconds.</p>
    </div>
  </header>
  <section>
    <div class="wrap">
      <div class="episode-grid">
        {cards}
      </div>
    </div>
  </section>
'''
    page("episodes.html", "Episode Archive",
         f"Browse all {EPISODE_COUNT} People Explained episodes, from Albert Einstein to Winston Churchill.",
         "episodes.html", body)


# ------------------------------------------------------- EPISODE DETAIL ---
def build_episode_detail(ep):
    slug = ep["slug"]
    preview_path = f"assets/previews/{slug}.mp4"
    has_preview = os.path.isfile(os.path.join(REPO, preview_path))
    media = (
        f'<video controls preload="metadata" poster="{ep["thumbnail"]}"><source src="{preview_path}" type="video/mp4">Your browser does not support embedded video.</video>'
        if has_preview else
        f'<img src="{ep["thumbnail"]}" alt="{e(ep["name"])} episode thumbnail">'
    )
    body = f'''  <section class="tight">
    <div class="wrap">
      <a class="back-link" href="episodes.html">&larr; Back to all episodes</a>
      <div class="detail-hero">
        {media}
        <div>
          <h1>{e(ep["name"])}</h1>
          <div class="meta">Produced {ep["produced"]} &middot; ~60-90 second documentary short</div>
          <p class="desc">{e(ep["description"])}</p>
          <div class="platforms">
            <span>TikTok</span>
            <span>YouTube Shorts</span>
            <span>Instagram Reels</span>
          </div>
          {'<p class="meta" style="margin-top:16px;">This is a compressed preview clip of the finished episode.</p>' if has_preview else ''}
        </div>
      </div>
    </div>
  </section>
'''
    page(f"episode-{slug}.html", ep["name"],
         f"{ep['name']}: {ep['summary']}",
         "episodes.html", body, og_image=ep["thumbnail"])


# ----------------------------------------------------------- ABOUT --------
def build_about():
    body = f'''  <header class="pagehead">
    <div class="wrap">
      <h1>About People Explained</h1>
      <p>Who&rsquo;s behind the channel, and how the episodes actually get made.</p>
    </div>
  </header>
  <section>
    <div class="wrap-narrow doc">
      <p>People Explained is an independently operated educational video project based in Germany. It launched in 2026 with a simple goal: turn well-documented historical and public figures into short, fact-checked documentary videos that fit into a minute of someone&rsquo;s day.</p>

      <h2>How episodes are made</h2>
      <p>Each episode starts from a curated list of historical and public figures. A script is drafted from verified biographical facts and structured into narration and on-screen chapters. The narration is generated with synthesized voice-over and paired with AI-generated illustrations of key scenes, then assembled into a finished vertical video with subtitles and overlays.</p>
      <p>Visuals are AI-generated illustrations of historical scenes and figures &mdash; stylized recreations, not archival photographs or footage.</p>

      <h2>Human review before anything is published</h2>
      <p>Every finished episode passes through a review step in the operator&rsquo;s own production app before it is queued for publishing: the operator watches the finished video and explicitly approves it, requests a re-generation, or holds it back. Nothing reaches TikTok, YouTube, or Instagram without that manual approval.</p>

      <h2>Who runs it</h2>
      <p>People Explained is produced and operated by a single independent creator, Aaron Quazi, based in Wassenberg, Germany. See the <a href="imprint.html">Imprint</a> for full contact details, or reach out directly via the <a href="contact.html">Contact page</a>.</p>
    </div>
  </section>
'''
    page("about.html", "About",
         "Who operates People Explained, and how each episode is researched, produced, and reviewed before publishing.",
         "about.html", body)


# ------------------------------------------------------------- FAQ --------
FAQ_ITEMS = [
    ("How are the videos actually made?",
     "Each episode is produced by an automated pipeline: a fact-based script is generated first, then narrated with synthesized voice-over and paired with AI-generated scene illustrations, subtitles, and overlays. See the <a href=\"about.html\">About page</a> for the full breakdown."),
    ("Are the facts checked, or could the AI make things up?",
     "Scripts are generated from well-documented, publicly known biographical facts about established historical and public figures. Episodes focus on figures with substantial public source material rather than obscure or disputed claims."),
    ("Are the images in the videos real photos?",
     "No. All visuals are AI-generated illustrations, stylized recreations of scenes and figures, not archival photographs or footage. This is disclosed on the About page and in each video's description."),
    ("Is the narration a real human voice?",
     "No, narration is synthesized (AI text-to-speech), not a recorded human voice actor."),
    ("Does a person review the videos before they go live?",
     "Yes. Every finished episode is reviewed by the operator in the production app and explicitly approved before it is queued for publishing &mdash; nothing is posted automatically without that review."),
    ("Which platforms will episodes appear on?",
     "TikTok, YouTube Shorts, and Instagram Reels."),
    ("How often are new episodes produced?",
     "New episodes are produced in ongoing batches; the <a href=\"episodes.html\">episode archive</a> reflects the current count and grows over time."),
    ("Who do I contact with questions?",
     "See the <a href=\"contact.html\">Contact page</a> for a direct email address."),
]


def build_faq():
    items = "\n        ".join(
        f'<details><summary>{e(q)}</summary><p>{a}</p></details>'
        for q, a in FAQ_ITEMS
    )
    body = f'''  <header class="pagehead">
    <div class="wrap">
      <h1>Frequently Asked Questions</h1>
      <p>How the videos are made, what&rsquo;s AI-generated, and where to reach out.</p>
    </div>
  </header>
  <section>
    <div class="wrap">
      <div class="faq-list">
        {items}
      </div>
    </div>
  </section>
'''
    page("faq.html", "FAQ",
         "Answers to common questions about how People Explained videos are made, fact-checked, and reviewed.",
         "faq.html", body)


# ---------------------------------------------------------- CONTACT -------
def build_contact():
    body = f'''  <header class="pagehead">
    <div class="wrap">
      <h1>Contact</h1>
      <p>Questions, feedback, or platform-review inquiries &mdash; reach out directly.</p>
    </div>
  </header>
  <section>
    <div class="wrap-narrow">
      <div class="contact-box">
        <a class="email" href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a>
        <p class="note">People Explained is operated by a single independent creator, so response times may vary. For operator/legal contact details, see the <a href="imprint.html">Imprint</a>.</p>
      </div>
    </div>
  </section>
'''
    page("contact.html", "Contact",
         "Get in touch with the People Explained team by email.",
         "contact.html", body)


# --------------------------------------------------------- PRIVACY --------
def build_privacy():
    body = '''  <header class="pagehead">
    <div class="wrap">
      <h1>Privacy Policy</h1>
      <p class="updated" style="color:#d8d2c0;">Last updated: August 2026</p>
    </div>
  </header>
  <section>
    <div class="wrap-narrow doc">
      <p>This Privacy Policy explains how the People Explained content publishing tool handles data when interacting with social media platform APIs including TikTok, YouTube, and Instagram.</p>
      <h2>1. Data Collected</h2>
      <p>This tool only accesses data necessary to publish video content to the operator's own social media accounts, such as authentication tokens provided directly by the respective platform. No personal data of third parties or platform users is collected, stored, or processed.</p>
      <h2>2. How Data Is Used</h2>
      <p>Authentication credentials are used solely to publish content such as videos, titles, and descriptions to the operator's own connected accounts. No data is shared with third parties, sold, or used for advertising purposes.</p>
      <h2>3. Data Storage</h2>
      <p>Access tokens and API credentials are stored locally and securely on the operator's own device and are not transmitted to any external server beyond the official platform APIs.</p>
      <h2>4. Data Retention</h2>
      <p>Credentials are retained only as long as necessary to operate the connected channels and can be revoked at any time by the operator through the respective platform's developer settings.</p>
      <h2>5. Third-Party Services</h2>
      <p>This tool interacts exclusively with official platform APIs under their respective terms and privacy policies.</p>
      <h2>6. Changes to This Policy</h2>
      <p>This Privacy Policy may be updated periodically.</p>
      <h2>7. Contact</h2>
      <p>For privacy-related questions, please use the <a href="contact.html">Contact page</a>.</p>
    </div>
  </section>
'''
    page("privacy.html", "Privacy Policy",
         "How People Explained handles data when interacting with TikTok, YouTube, and Instagram APIs.",
         "privacy.html", body)


def build_terms():
    body = '''  <header class="pagehead">
    <div class="wrap">
      <h1>Terms of Service</h1>
      <p class="updated" style="color:#d8d2c0;">Last updated: August 2026</p>
    </div>
  </header>
  <section>
    <div class="wrap-narrow doc">
      <p>These Terms of Service govern the use of the "People Explained" content publishing tool and its associated social media channels.</p>
      <h2>1. About This Service</h2>
      <p>People Explained is a personal content creation project that produces short educational documentary videos about historical and public figures. This tool is used to manage and automate the publishing of content to associated social media accounts including TikTok, YouTube, and Instagram.</p>
      <h2>2. Content</h2>
      <p>All content published is created for educational and entertainment purposes. Video content includes AI-assisted and AI-generated visual and audio elements, which are disclosed on the <a href="about.html">About page</a> and in each video's description.</p>
      <h2>3. Use of the Tool</h2>
      <p>This automation tool is used solely by the operator of the People Explained channels to manage their own content publishing across supported platforms. It is not offered as a public service to third parties.</p>
      <h2>4. Intellectual Property</h2>
      <p>All original content is owned by the operator. Any use of third-party trademarks, names, or likenesses is for editorial and educational purposes.</p>
      <h2>5. Limitation of Liability</h2>
      <p>This service is provided as is without warranties of any kind. The operator is not liable for any damages arising from the use of this tool.</p>
      <h2>6. Contact</h2>
      <p>For questions regarding these Terms, please use the <a href="contact.html">Contact page</a>.</p>
    </div>
  </section>
'''
    page("terms.html", "Terms of Service",
         "Terms governing the use of the People Explained content publishing tool and its social media channels.",
         "terms.html", body)


def build_imprint():
    body = '''  <header class="pagehead">
    <div class="wrap">
      <h1>Imprint</h1>
      <p>Information pursuant to &sect;5 of the German Digital Services Act (Digitale-Dienste-Gesetz, DDG).</p>
    </div>
  </header>
  <section>
    <div class="wrap-narrow doc">
      <p>
        Aaron Quazi<br>
        Im Eichengrund 68<br>
        41849 Wassenberg<br>
        Germany
      </p>
      <p>Email: <a href="mailto:peopleexplained.channel@gmail.com">peopleexplained.channel@gmail.com</a></p>
      <h2>Responsible for content</h2>
      <p>Aaron Quazi (address as above).</p>
    </div>
  </section>
'''
    page("imprint.html", "Imprint",
         "Legal imprint for People Explained pursuant to §5 DDG.",
         "imprint.html", body)


def build_404():
    body = '''  <section class="notfound">
    <div class="wrap">
      <h1>404</h1>
      <p>This page doesn&rsquo;t exist. It might have been a typo, or an episode that hasn&rsquo;t been produced yet.</p>
      <p><a href="index.html">Back to the homepage</a> &middot; <a href="episodes.html">Browse episodes</a></p>
    </div>
  </section>
'''
    page("404.html", "Page Not Found", "This page could not be found.", "", body)


def main():
    build_home()
    build_episodes()
    for ep in DETAIL_EPISODES:
        build_episode_detail(ep)
    build_about()
    build_faq()
    build_contact()
    build_privacy()
    build_terms()
    build_imprint()
    build_404()
    print(f"Generated {2 + len(DETAIL_EPISODES) + 7} pages for {EPISODE_COUNT} episodes "
          f"({len(DETAIL_EPISODES)} with detail pages).")


if __name__ == "__main__":
    main()
