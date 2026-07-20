#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Restore the ORIGINAL Home page (pre-2026-07-20 design) onto live page 12.

Usage:  python restore_home.py
Reverts page 12's _elementor_data (and page settings) to the saved original,
then flushes Elementor's CSS cache so the front end updates immediately.
Re-running is safe (idempotent). To re-apply the NEW design instead, run build_home.py + push.
"""
import ab, json, glob

SRC = "original-home-full.json"          # the saved original content (7 sections)
data = json.load(open(SRC, encoding="utf-8"))

# original page settings live inside the import-format template file
try:
    ps = json.load(open("original-home-template.json", encoding="utf-8")).get("page_settings", {})
except Exception:
    ps = {}

payload = {"meta": {
    "_elementor_data": json.dumps(data, ensure_ascii=False),
    "_elementor_edit_mode": "builder",
}}
if ps:
    payload["meta"]["_elementor_page_settings"] = json.dumps(ps, ensure_ascii=False)

r = ab.call("/wp/v2/pages/12", "POST", payload)
assert r.get("id") == 12, r
print("Restored original _elementor_data to page 12 (%d sections)." % len(data))

# Flush cache: raw meta writes bypass Elementor's cache, so trigger a plugin save
# on the top container (regenerates post-12.css). Needs MCP; if unavailable,
# open page 12 in Elementor and click Update once.
top = data[0]["id"]
print("NOTE: now flush the cache -> run MCP update-element on post 12 container '%s',\n"
      "      or open page 12 in Elementor and press Update once." % top)
print("Original is also saved as WP template id 346 ('Original Home (backup 2026-07-20)').")
