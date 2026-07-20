#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the redesigned Unbreakable Strength Home page (_elementor_data) per client design."""
import json, secrets

UP = "https://syn04ae.syd5.hostyourservices.net/~unbreaka/wp-content/uploads/2026/07/"
CONTACT = "https://syn04ae.syd5.hostyourservices.net/~unbreaka/contact/"
IMG = {
    "hero":   (257, UP + "centre-for-ageing-better-qxoyXncsJUA-unsplash.jpg"),
    "band1":  (154, UP + "victor-freitas-WvDYdXDzkhs-unsplash.jpg"),
    "band2":  (152, UP + "john-arano-h4i9G-de7Po-unsplash.jpg"),
    "founder":(205, UP + "danielle-cerullo-CQfNt66ttZM-unsplash.jpg"),
}

def nid():
    return secrets.token_hex(4)[:7]

def con(children, s=None, **kw):
    d = {"id": nid(), "elType": "container", "settings": (s or {}) | kw, "elements": children}
    return d

def wid(wt, s=None, **kw):
    return {"id": nid(), "elType": "widget", "widgetType": wt, "settings": (s or {}) | kw, "elements": []}

def heading(title, cls, tag="h2", **extra):
    return wid("heading", {"title": title, "header_size": tag, "_css_classes": cls} | extra)

def para(html, cls, **extra):
    return wid("text-editor", {"editor": html, "_css_classes": cls} | extra)

def button(text, cls="ub2-btn ub-btn-gold", url=CONTACT, align=None):
    s = {"text": text, "link": {"url": url}, "_css_classes": cls}
    if align: s["align"] = align
    return wid("button", s)

def image(mid_url, cls, **extra):
    mid, url = mid_url
    return wid("image", {"image": {"url": url, "id": mid, "size": "", "alt": "", "source": "library"}, "_css_classes": cls} | extra)

def pad(t, r, b, l):
    return {"unit": "px", "top": str(t), "right": str(r), "bottom": str(b), "left": str(l), "isLinked": False}

BOX = {"boxed_width": {"unit": "px", "size": 1180}}

def section(inner_children, section_cls, inner_cls="ub2-wrap", bg=None, extra_sec=None, inner_extra=None):
    inner = con(inner_children, {"css_classes": inner_cls} | (inner_extra or {}))
    sset = {"content_width": "full", "css_classes": "ub2-sec " + section_cls,
            "flex_direction": "column", "flex_align_items": "center"}
    if bg:
        mid, url = bg
        sset |= {"background_background": "classic", "background_color": "#0f0f0f",
                 "background_image": {"url": url, "id": mid, "size": "", "alt": "", "source": "library"},
                 "background_size": "cover", "background_position": "center center",
                 "background_overlay_background": "classic",
                 "background_overlay_color": "rgba(6,6,6,0.7)"}
    if extra_sec: sset |= extra_sec
    return con([inner], sset)

data = []

# ---------- STYLE (injected via HTML widget at very top) ----------
CSS = open("home_ub2.css", encoding="utf-8").read()
style_widget = wid("html", {"html": "<style>\n" + CSS + "\n</style>"})
data.append(con([style_widget], {"content_width": "full", "css_classes": "ub2-styleholder",
                                 "padding": pad(0, 0, 0, 0), "margin": pad(0, 0, 0, 0),
                                 "min_height": {"unit": "px", "size": 0}}))

# ---------- S0 HERO ----------
mid, url = IMG["hero"]
hero_inner = con([
    heading("Lift better.<br>Move better.<br>Live better.", "ub2-hero-title", tag="h1"),
], {"css_classes": "ub2-wrap"} | BOX, padding=pad(0, 24, 0, 24))
hero = con([hero_inner], {
    "content_width": "full", "_element_id": "ub2-hero",
    "flex_direction": "column", "flex_justify_content": "flex-end", "flex_align_items": "center",
    "min_height": {"unit": "vh", "size": 88},
    "padding": pad(0, 0, 70, 0),
    "background_background": "classic", "background_color": "#0d0d0d",
    "background_image": {"url": url, "id": mid, "size": "", "alt": "", "source": "library"},
    "background_size": "cover", "background_position": "center center",
    "background_overlay_background": "gradient",
    "background_overlay_color": "rgba(0,0,0,0.82)", "background_overlay_color_b": "rgba(10,10,10,0.35)",
    "background_overlay_gradient_angle": {"unit": "deg", "size": 90},
})
data.append(hero)

# ---------- S1 THREE VALUE COLUMNS ----------
def vcol(plus, body):
    return con([
        heading("Unbreakable Strength", "ub2-vk", tag="h3"),
        heading(plus, "ub2-vplus", tag="h4"),
        para("<p>%s</p>" % body, "ub2-lead", margin=pad(10, 0, 0, 0)),
    ], {"css_classes": "ub2-vcol"})
vcols = con([
    vcol("+ Longevity", "Boost strength, support healthy bones and stay active for life."),
    vcol("+ Performance", "Designed for athletes and those wanting to train like one."),
    vcol("+ Recovery", "Regain muscle function, joint stability and improve mobility."),
], {"css_classes": "ub2-wrap ub2-vcols"})
data.append(con([vcols], {"content_width": "full", "css_classes": "ub2-sec ub2-cream",
                          "flex_direction": "column", "flex_align_items": "center",
                          "background_background": "classic", "background_color": "#F4F0E8"}))

# ---------- S2 INTRO ----------
intro = para(
    "<p>We help everyday people build strength in a safe, supportive, and welcoming environment. "
    "Whether you're completely new to the gym or looking to take your training further, our coaching is "
    "designed to help you move better, get stronger, and perform at your best.</p>"
    "<p>Strength training is one of the most effective ways to improve your health, mobility, and confidence "
    "&ndash; especially as you get older.</p>"
    "<p>Whether you're an aspiring athlete, a busy professional, or enjoying your retirement, our personalised "
    "approach helps you train safely, progress consistently, and unlock your full potential.</p>"
    "<p>Wherever you're starting, we'll help you build strength that lasts.</p>",
    "ub2-lead ub2-center")
data.append(section([intro], "ub2-white", inner_cls="ub2-narrow ub2-center",
                    extra_sec={"background_background": "classic", "background_color": "#ffffff"}))

# ---------- S3 BAND: Strong body ----------
band1 = section([
    heading("Strong body.<br>Unbreakable mind.", "ub2-h ub2-gold ub2-center", tag="h2"),
    para("<p>Unbreakable Strength is built around expert coaching, structured programming, "
         "technique development and long term progress.</p>", "ub2-lead ub2-center ub2-oncdark",
         margin=pad(18, 0, 26, 0)),
    con([button("Book Free Consult")], {"css_classes": "ub2-center", "flex_direction": "row",
                                         "flex_justify_content": "center"}),
], "ub2-dark ub2-center", inner_cls="ub2-narrow ub2-center", bg=IMG["band1"])
data.append(band1)

# ---------- S4 FOUNDER ----------
founder = section([
    con([wid("html", {"html": '<div class="ub2-mono">TG</div>'})], {"css_classes": "ub2-center",
        "flex_direction": "row", "flex_justify_content": "center"}),
    heading("Founder", "ub2-eyebrow ub2-center", tag="h4", margin=pad(22, 0, 4, 0)),
    heading("Tim Genikov", "ub2-h ub2-center", tag="h2", margin=pad(0, 0, 16, 0)),
    para(
        "<p>As a Strength and Conditioning Coach, I'm passionate about helping people move better, perform "
        "at their best, and build strength that lasts. I hold a Diploma of Exercise Science from Bond "
        "University and am currently studying Chiropractic Science, combining evidence-based training with a "
        "growing clinical understanding of the human body.</p>"
        "<p>With wins in both powerlifting and Brazilian Jiu-Jitsu competitions, I bring both practical "
        "experience and proven coaching methods to every session. I believe strength training is one of the "
        "most powerful tools for improving performance, preventing injury, supporting rehabilitation, and "
        "enhancing long-term health &ndash; helping people of all ages become stronger, more capable, and more "
        "resilient.</p>",
        "ub2-lead ub2-center"),
], "ub2-white ub2-center", inner_cls="ub2-narrow ub2-center",
   extra_sec={"background_background": "classic", "background_color": "#ffffff"})
data.append(founder)

# ---------- S5 CONSULT FORM ----------
form_fields = [
    {"custom_id": "name", "field_type": "text", "field_label": "Name", "placeholder": "Name",
     "required": "true", "width": "100", "_id": nid()},
    {"custom_id": "email", "field_type": "email", "field_label": "Email", "placeholder": "Email",
     "required": "true", "width": "100", "_id": nid()},
    {"custom_id": "phone", "field_type": "tel", "field_label": "Phone", "placeholder": "Phone",
     "required": "false", "width": "100", "_id": nid()},
]
form = wid("form", {
    "form_name": "Free Consultation",
    "form_fields": form_fields,
    "button_text": "Send",
    "button_width": "100",
    "submit_actions": ["save-to-database"],
    "show_labels": "",
    "input_size": "md",
    "_css_classes": "ub2-form",
})
formsec = section([
    heading("Book your free consultation", "ub2-h ub2-center", tag="h2"),
    para("<p>15 minutes. No pressure. Just a chat about your goals.</p>", "ub2-lead ub2-center",
         margin=pad(10, 0, 26, 0)),
    con([form], {"css_classes": "ub2-formwrap"}),
], "ub2-cream ub2-center", inner_cls="ub2-formnarrow ub2-center",
   extra_sec={"background_background": "classic", "background_color": "#F4F0E8"})
data.append(formsec)

# ---------- S6 THREE REASONS ----------
def reason(num, title, body):
    return con([
        heading(num, "ub2-num", tag="div"),
        heading(title, "ub2-rk", tag="h3", margin=pad(18, 0, 8, 0)),
        para("<p>%s</p>" % body, "ub2-lead"),
    ], {"css_classes": "ub2-reason"})
reasons = con([
    reason("1", "Build long-term health and longevity",
           "Strength is the foundation for an active, independent life. Regular strength training helps "
           "maintain muscle mass, increase bone density, improve metabolic health, and support healthy ageing."),
    reason("2", "Improve performance and prevent injury",
           "A stronger body is a more resilient body. Strength training enhances athletic performance, "
           "improves balance and coordination, and reduces the risk of injury by strengthening muscles, "
           "joints, and connective tissues."),
    reason("3", "Boost confidence and mental wellbeing",
           "Progress in the gym builds more than physical strength. Setting goals, overcoming challenges, "
           "and seeing measurable improvements can increase confidence, reduce stress, and improve overall "
           "mental wellbeing."),
], {"css_classes": "ub2-wrap ub2-grid3"})
data.append(con([
    con([heading("3 powerful reasons to start strength training", "ub2-h ub2-center", tag="h2",
                 margin=pad(0, 0, 44, 0))], {"css_classes": "ub2-wrap ub2-center"}),
    reasons,
], {"content_width": "full", "css_classes": "ub2-sec ub2-white", "flex_direction": "column",
    "flex_align_items": "center", "background_background": "classic", "background_color": "#ffffff"}))

# ---------- S7 TAILORED ----------
def tcard(title, body):
    return con([
        heading(title, "ub2-ck", tag="h3"),
        para("<p>%s</p>" % body, "ub2-lead", margin=pad(10, 0, 0, 0)),
    ], {"css_classes": "ub2-card"})
tailored_cards = con([
    tcard("One-on-one training", "1 hour private session focused on correct form and technique with "
          "flexible scheduling."),
    tcard("Micro-group training", "Train in a high-touch, small-group setting with a maximum of 3 people."),
], {"css_classes": "ub2-wrap ub2-grid2"})
data.append(con([
    con([
        heading("Strength training tailored to you", "ub2-h ub2-center", tag="h2"),
        para("<p>Designed to fit you, your goals, and your schedule.</p>", "ub2-lead ub2-center",
             margin=pad(10, 0, 40, 0)),
    ], {"css_classes": "ub2-wrap ub2-center"}),
    tailored_cards,
    con([button("Book Free Consult")], {"css_classes": "ub2-center", "flex_direction": "row",
        "flex_justify_content": "center", "margin": pad(44, 0, 0, 0)}),
], {"content_width": "full", "css_classes": "ub2-sec ub2-cream", "flex_direction": "column",
    "flex_align_items": "center", "background_background": "classic", "background_color": "#F4F0E8"}))

# ---------- S8 FAQ ----------
faq = wid("accordion", {
    "tabs": [
        {"tab_title": "Is strength training suitable for beginners?",
         "tab_content": "Absolutely. Every program starts with an assessment and is built around your current "
         "ability. We teach correct technique from day one and progress you at a pace that's safe and "
         "sustainable &ndash; no experience required.", "_id": nid()},
        {"tab_title": "Is there a lock-in contract?",
         "tab_content": "No lock-in contracts. Our coaching is designed to fit your life, and you're free to "
         "adjust or pause your sessions as your schedule and goals change.", "_id": nid()},
        {"tab_title": "Can I train if I have an injury or illness?",
         "tab_content": "In most cases, yes. Strength training is one of the best tools for rehabilitation and "
         "resilience. We tailor every session around your history and, where needed, work alongside your "
         "health professionals.", "_id": nid()},
        {"tab_title": "Is parking available?",
         "tab_content": "Yes &ndash; there is convenient parking close to the studio in Five Dock, so getting to "
         "your session is quick and easy.", "_id": nid()},
        {"tab_title": "What age groups do you train?",
         "tab_content": "We coach people of all ages &ndash; from aspiring athletes and busy professionals to "
         "active retirees. Programs are always personalised to suit your age, ability and goals.", "_id": nid()},
    ],
    "title_html_tag": "h3",
    "faq_schema": "yes",
    "_css_classes": "ub2-faq",
})
data.append(con([
    con([heading("FAQ", "ub2-faqhead ub2-center", tag="h2", margin=pad(0, 0, 30, 0))],
        {"css_classes": "ub2-wrap ub2-center"}),
    con([faq], {"css_classes": "ub2-narrow"}),
], {"content_width": "full", "css_classes": "ub2-sec ub2-white", "flex_direction": "column",
    "flex_align_items": "center", "background_background": "classic", "background_color": "#ffffff"}))

# ---------- S9 BAND: Every rep ----------
band2 = section([
    heading("Every rep builds resilience.", "ub2-h ub2-gold ub2-center", tag="h2"),
    para("<p>Adults lose approximately 3&ndash;8% of muscle mass per decade after 30 if they don't regularly "
         "strength train. After age 60, muscle loss often speeds up.</p>", "ub2-lead ub2-center ub2-oncdark",
         margin=pad(18, 0, 0, 0)),
], "ub2-dark ub2-center", inner_cls="ub2-narrow ub2-center", bg=IMG["band2"])
data.append(band2)

# ---------- S10 TESTIMONIALS ----------
def testi(quote, name):
    return con([
        para("<p>%s</p>" % quote, "ub2-quote"),
        heading(name, "ub2-tname", tag="h4"),
    ], {"css_classes": "ub2-tcard"})
testis = con([
    testi("&ldquo;I wish I started many years ago! Tim has fine-tuned my program not only for ongoing "
          "strength improvements, but also to take account of a longstanding injury and specialist advice. He "
          "explains technique well, including small but important adjustments, and is incredibly patient as "
          "one learns over many weeks how to lift properly.&rdquo;", "S.M. Potter"),
    testi("&ldquo;Genuinely the most supportive training environment I've been part of. The coaching is "
          "detailed, personal, and I've never felt stronger or more confident in the gym.&rdquo;", "Client Name"),
    testi("&ldquo;Tim's approach completely changed how I train. Every session has a purpose and I can see "
          "real, measurable progress week to week.&rdquo;", "Client Name"),
], {"css_classes": "ub2-wrap ub2-grid3"})
data.append(con([
    con([heading("Our clients say it best...", "ub2-h ub2-center", tag="h2", margin=pad(0, 0, 44, 0))],
        {"css_classes": "ub2-wrap ub2-center"}),
    testis,
], {"content_width": "full", "css_classes": "ub2-sec ub2-white", "flex_direction": "column",
    "flex_align_items": "center", "background_background": "classic", "background_color": "#ffffff"}))

# ---------- S11 CONTACT + MAP ----------
mapw = wid("google_maps", {"address": "1 McKinnon Ave, Five Dock NSW 2046, Australia",
                           "zoom": {"unit": "px", "size": 15}, "height": {"unit": "px", "size": 380},
                           "_css_classes": "ub2-map"})
contact = con([
    con([
        para("<p>Unbreakable Strength is a private strength training gym located at "
             "<strong>1 McKinnon Ave, Five Dock NSW 2046</strong>.<br>"
             "Call <strong>0400 000 000</strong> or email at "
             "<strong>info@unbreakablestrength.com.au</strong></p>", "ub2-lead ub2-center",
             margin=pad(0, 0, 34, 0)),
    ], {"css_classes": "ub2-narrow ub2-center"}),
    con([mapw], {"css_classes": "ub2-wrap ub2-map-wrap"}),
], {"content_width": "full", "css_classes": "ub2-sec ub2-cream", "flex_direction": "column",
    "flex_align_items": "center", "background_background": "classic", "background_color": "#F4F0E8"})
data.append(contact)

json.dump(data, open("new_home.json", "w", encoding="utf-8"), ensure_ascii=False)
print("Built %d top-level sections -> new_home.json (%d bytes)" % (len(data), len(json.dumps(data))))
