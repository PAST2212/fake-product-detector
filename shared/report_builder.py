"""Shared HTML report rendering for Amazon and OTTO counterfeit verdicts."""

import html
import math
from dataclasses import dataclass
from datetime import datetime

VERDICT_COLORS = {
    "LIKELY COUNTERFEIT": ("#c0392b", "#fadbd8"),
    "UNCERTAIN":          ("#d68910", "#fef9e7"),
    "LIKELY AUTHENTIC":   ("#1e8449", "#d5f5e3"),
}

SEVERITY_COLORS = {
    "HIGH":   ("#c0392b", "#fadbd8"),
    "MEDIUM": ("#d68910", "#fef9e7"),
    "LOW":    ("#1e8449", "#d5f5e3"),
}


@dataclass(frozen=True)
class PlatformConfig:
    id_field: str
    id_label: str
    lang: str
    title_prefix: str
    seller_field: str
    seller_label: str
    brand_fallback_field: str | None = None
    analyzed_fallback_field: str | None = None
    rationale_fallback_field: str | None = None
    footer_suffix: str = ""


AMAZON = PlatformConfig(
    id_field="asin",
    id_label="ASIN",
    lang="en",
    title_prefix="Counterfeit Report",
    seller_field="primary_seller",
    seller_label="Primary Seller",
    brand_fallback_field="actual_brand",
    analyzed_fallback_field="investigation_date",
    rationale_fallback_field="confidence_notes",
)

OTTO = PlatformConfig(
    id_field="article_number",
    id_label="Article",
    lang="de",
    title_prefix="OTTO Counterfeit Report",
    seller_field="seller",
    seller_label="Seller",
    footer_suffix=" (OTTO)",
)


def escape_html(text) -> str:
    if text is None:
        return ""
    return html.escape(str(text), quote=True)


def _score_color(score: float) -> str:
    if score < 0.4:
        return "#27ae60"
    if score < 0.6:
        return "#f39c12"
    return "#c0392b"


def score_bar(score: float, width: int = 200) -> str:
    pct = round(score * 100)
    color = _score_color(score)
    return (
        f'<div style="display:flex;align-items:center;gap:8px;">'
        f'<div style="width:{width}px;height:12px;background:#e0e0e0;border-radius:6px;overflow:hidden;">'
        f'<div style="width:{pct}%;height:100%;background:{color};border-radius:6px;"></div>'
        f'</div>'
        f'<span style="font-size:13px;color:#555;">{score:.2f}</span>'
        f'</div>'
    )


def gauge_svg(score: float) -> str:
    pct = max(0.0, min(1.0, score))
    angle = -180 + pct * 180
    cx, cy, r = 100, 100, 70
    needle_x = cx + r * math.cos(math.radians(angle))
    needle_y = cy + r * math.sin(math.radians(angle))
    needle_color = _score_color(pct)

    return f"""<svg viewBox="0 0 200 110" xmlns="http://www.w3.org/2000/svg" style="width:220px;height:120px;">
  <defs>
    <linearGradient id="gaugeGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%"   stop-color="#27ae60"/>
      <stop offset="40%"  stop-color="#27ae60"/>
      <stop offset="60%"  stop-color="#f39c12"/>
      <stop offset="100%" stop-color="#c0392b"/>
    </linearGradient>
  </defs>
  <path d="M 20 100 A 80 80 0 0 1 180 100" fill="none" stroke="url(#gaugeGrad)" stroke-width="14" stroke-linecap="round"/>
  <path d="M 20 100 A 80 80 0 0 1 180 100" fill="none" stroke="#e0e0e0" stroke-width="14" stroke-linecap="round" stroke-dasharray="251.3" stroke-dashoffset="{251.3 * pct:.1f}" opacity="0.3"/>
  <line x1="{cx}" y1="{cy}" x2="{needle_x:.1f}" y2="{needle_y:.1f}" stroke="{needle_color}" stroke-width="3" stroke-linecap="round"/>
  <circle cx="{cx}" cy="{cy}" r="5" fill="{needle_color}"/>
  <text x="100" y="90" text-anchor="middle" font-size="22" font-weight="bold" fill="{needle_color}">{pct*100:.0f}%</text>
  <text x="22"  y="112" text-anchor="middle" font-size="9" fill="#888">0</text>
  <text x="178" y="112" text-anchor="middle" font-size="9" fill="#888">1.0</text>
</svg>"""


def render_score_breakdown(data: dict) -> str:
    rows = ""

    if "score_breakdown" in data:
        for key, val in data["score_breakdown"].items():
            if not isinstance(val, (int, float)):
                continue
            label = escape_html(str(key).replace("_", " ").title())
            rows += f"""
            <tr>
              <td style="padding:8px 12px;color:#444;">{label}</td>
              <td style="padding:8px 12px;">{score_bar(val)}</td>
            </tr>"""

    elif "scored_signals" in data:
        for key, sig in data["scored_signals"].items():
            if not isinstance(sig, dict):
                continue
            label = escape_html(str(key).replace("_", " ").title())
            score = sig.get("score", 0) if isinstance(sig.get("score"), (int, float)) else 0
            weight = sig.get("weight", 0) if isinstance(sig.get("weight"), (int, float)) else 0
            notes = escape_html(sig.get("notes", ""))
            rows += f"""
            <tr>
              <td style="padding:8px 12px;color:#444;">
                <div style="font-weight:500;">{label}</div>
                <div style="font-size:12px;color:#888;margin-top:2px;">{notes}</div>
              </td>
              <td style="padding:8px 12px;min-width:220px;">
                {score_bar(score)}
                <div style="font-size:11px;color:#aaa;margin-top:2px;">weight: {weight}</div>
              </td>
            </tr>"""

    if not rows:
        return ""

    return f"""
    <section style="margin-top:32px;">
      <h2 style="font-size:18px;color:#222;border-bottom:2px solid #eee;padding-bottom:8px;">Signal Breakdown</h2>
      <table style="width:100%;border-collapse:collapse;margin-top:12px;">
        <thead>
          <tr style="background:#f8f9fa;">
            <th style="padding:8px 12px;text-align:left;color:#888;font-weight:500;font-size:13px;">Signal</th>
            <th style="padding:8px 12px;text-align:left;color:#888;font-weight:500;font-size:13px;">Score</th>
          </tr>
        </thead>
        <tbody>{rows}
        </tbody>
      </table>
    </section>"""


def render_evidence(data: dict) -> str:
    ev = data.get("evidence_summary", {})
    for_auth = ev.get("for_authentic", [])
    against = ev.get("against_authentic", [])

    if not for_auth and not against:
        return ""

    def items(lst, icon, color):
        return "".join(
            f'<li style="margin-bottom:8px;display:flex;gap:8px;">'
            f'<span style="color:{color};font-size:16px;flex-shrink:0;">{icon}</span>'
            f'<span style="color:#444;font-size:14px;">{escape_html(item)}</span></li>'
            for item in lst
        )

    return f"""
    <section style="margin-top:32px;">
      <h2 style="font-size:18px;color:#222;border-bottom:2px solid #eee;padding-bottom:8px;">Evidence Summary</h2>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-top:16px;">
        <div style="background:#d5f5e3;border-radius:10px;padding:16px;">
          <h3 style="color:#1e8449;margin:0 0 12px;font-size:15px;">For Authentic</h3>
          <ul style="list-style:none;margin:0;padding:0;">{items(for_auth, "✓", "#1e8449")}</ul>
        </div>
        <div style="background:#fadbd8;border-radius:10px;padding:16px;">
          <h3 style="color:#c0392b;margin:0 0 12px;font-size:15px;">Against Authentic</h3>
          <ul style="list-style:none;margin:0;padding:0;">{items(against, "✗", "#c0392b")}</ul>
        </div>
      </div>
    </section>"""


def render_risk_flags(data: dict) -> str:
    flags = data.get("risk_flags", [])
    if not flags:
        return ""

    cards = ""
    for f in flags:
        sev = f.get("severity", "LOW")
        if sev not in SEVERITY_COLORS:
            sev = "LOW"
        fg, bg = SEVERITY_COLORS[sev]
        cards += f"""
        <div style="border-left:4px solid {fg};background:{bg};border-radius:6px;padding:14px 16px;margin-bottom:12px;">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">
            <span style="font-weight:600;color:{fg};font-size:14px;">{escape_html(f.get('flag',''))}</span>
            <span style="font-size:11px;font-weight:700;color:{fg};background:rgba(0,0,0,0.08);padding:2px 8px;border-radius:20px;">{escape_html(sev)}</span>
          </div>
          <p style="margin:0;color:#555;font-size:13px;">{escape_html(f.get('detail',''))}</p>
        </div>"""

    return f"""
    <section style="margin-top:32px;">
      <h2 style="font-size:18px;color:#222;border-bottom:2px solid #eee;padding-bottom:8px;">Risk Flags</h2>
      <div style="margin-top:16px;">{cards}</div>
    </section>"""


def render_recommendations(data: dict) -> str:
    recs = data.get("recommendations", [])
    buying = data.get("buying_verdict", {})

    if not recs and not buying:
        return ""

    items = "".join(
        f'<li style="margin-bottom:8px;color:#444;font-size:14px;">{escape_html(r)}</li>'
        for r in recs
    )

    buying_html = ""
    if buying:
        rows = "".join(
            f'<tr>'
            f'<td style="padding:8px 12px;font-size:13px;color:#555;">{escape_html(k.replace("_"," ").title())}</td>'
            f'<td style="padding:8px 12px;font-size:13px;color:#333;font-weight:500;">{escape_html(v)}</td>'
            f'</tr>'
            for k, v in buying.items()
        )
        buying_html = f"""
        <h3 style="font-size:15px;color:#333;margin-top:20px;">Buying Verdict by Source</h3>
        <table style="width:100%;border-collapse:collapse;margin-top:8px;border:1px solid #eee;border-radius:8px;overflow:hidden;">
          <tbody>{rows}</tbody>
        </table>"""

    return f"""
    <section style="margin-top:32px;">
      <h2 style="font-size:18px;color:#222;border-bottom:2px solid #eee;padding-bottom:8px;">Recommendations</h2>
      <ul style="margin:16px 0 0;padding-left:20px;">{items}</ul>
      {buying_html}
    </section>"""


def render_sources(data: dict) -> str:
    sources = data.get("sources", [])
    if not sources:
        return ""

    def safe_url(s):
        s = str(s)
        if not s.startswith(("http://", "https://")):
            return "https://" + s if s.startswith("www.") else "#"
        return s

    links = "".join(
        f'<li style="margin-bottom:6px;"><a href="{safe_url(s)}" style="color:#2980b9;font-size:13px;word-break:break-all;">{escape_html(s)}</a></li>'
        for s in sources
    )

    return f"""
    <section style="margin-top:32px;">
      <h2 style="font-size:18px;color:#222;border-bottom:2px solid #eee;padding-bottom:8px;">Sources</h2>
      <ul style="margin:12px 0 0;padding-left:20px;">{links}</ul>
    </section>"""


def render_key_finding(data: dict) -> str:
    kf = data.get("key_finding", "")
    if not kf:
        return ""
    return f"""
    <section style="margin-top:32px;">
      <div style="background:#eaf4fb;border-left:4px solid #2980b9;border-radius:6px;padding:16px 18px;">
        <h3 style="margin:0 0 8px;color:#1a5276;font-size:15px;">Key Finding</h3>
        <p style="margin:0;color:#333;font-size:14px;line-height:1.6;">{escape_html(kf)}</p>
      </div>
    </section>"""


def _first_present(verdict: dict, *fields: str) -> str:
    for f in fields:
        if not f:
            continue
        value = verdict.get(f)
        if value is not None and value != "":
            return value
    return ""


def _numeric_or_none(value):
    return value if isinstance(value, (int, float)) else None


def _confidence_html(confidence) -> str:
    if confidence is None:
        return '<div style="font-size:13px;color:#555;">Confidence: <strong>—</strong></div>'
    return f'<div style="font-size:13px;color:#555;">Confidence: <strong>{confidence * 100:.0f}%</strong></div>'


def build_report(verdict: dict, platform: PlatformConfig) -> str:
    ident_raw = verdict.get(platform.id_field, "Unknown")
    ident = escape_html(ident_raw)
    title = escape_html(verdict.get("product_title", "Unknown Product"))
    brand = escape_html(_first_present(verdict, "brand", platform.brand_fallback_field))
    seller = escape_html(_first_present(verdict, platform.seller_field))

    v_raw = verdict.get("verdict", "UNCERTAIN")
    v_text = escape_html(v_raw)

    confidence = _numeric_or_none(verdict.get("confidence"))
    score_value = _numeric_or_none(verdict.get("composite_score"))
    gauge_score = score_value if score_value is not None else 0

    risk_cat = escape_html(verdict.get("risk_category", ""))
    analyzed = escape_html(
        _first_present(verdict, "analyzed_at", platform.analyzed_fallback_field)
    )
    rationale = escape_html(
        _first_present(verdict, "verdict_rationale", platform.rationale_fallback_field)
    )

    v_fg, v_bg = VERDICT_COLORS.get(v_raw, ("#555", "#f0f0f0"))
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    meta_rows = ""
    if brand:
        meta_rows += f'<div><span style="color:#aaa;font-size:12px;">Brand</span><div style="font-weight:500;">{brand}</div></div>'
    if seller:
        meta_rows += f'<div><span style="color:#aaa;font-size:12px;">{escape_html(platform.seller_label)}</span><div style="font-weight:500;font-size:13px;">{seller}</div></div>'
    if risk_cat:
        meta_rows += f'<div><span style="color:#aaa;font-size:12px;">Risk Category</span><div style="font-weight:500;">{risk_cat}</div></div>'
    if analyzed:
        meta_rows += f'<div><span style="color:#aaa;font-size:12px;">Analyzed</span><div style="font-weight:500;">{analyzed}</div></div>'

    rationale_html = (
        f'<p style="margin:8px 0 0;font-size:13px;color:#444;line-height:1.6;">{rationale}</p>'
        if rationale else ""
    )

    return f"""<!DOCTYPE html>
<html lang="{platform.lang}">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>{escape_html(platform.title_prefix)} — {ident}</title>
  <style>
    *, *::before, *::after {{ box-sizing: border-box; }}
    body {{ margin: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: #f2f3f5; color: #222; }}
    a {{ text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
  </style>
</head>
<body>
  <div style="max-width:860px;margin:40px auto;padding:0 16px 60px;">

    <!-- Header -->
    <div style="background:#fff;border-radius:14px;padding:28px 32px;box-shadow:0 2px 12px rgba(0,0,0,.08);margin-bottom:24px;">
      <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:16px;">
        <div style="flex:1;min-width:240px;">
          <p style="margin:0 0 4px;font-size:12px;color:#aaa;letter-spacing:.5px;">{escape_html(platform.id_label)}: {ident}</p>
          <h1 style="margin:0 0 16px;font-size:20px;line-height:1.4;color:#111;">{title}</h1>
          <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:12px;font-size:14px;">
            {meta_rows}
          </div>
        </div>
        <div style="text-align:center;flex-shrink:0;">
          {gauge_svg(gauge_score)}
          <div style="font-size:11px;color:#aaa;margin-top:2px;">Composite Risk Score</div>
        </div>
      </div>

      <!-- Verdict Badge -->
      <div style="margin-top:24px;background:{v_bg};border:2px solid {v_fg};border-radius:10px;padding:16px 20px;display:flex;align-items:center;gap:16px;">
        <div style="font-size:22px;font-weight:800;color:{v_fg};">{v_text}</div>
        <div>
          {_confidence_html(confidence)}
          {rationale_html}
        </div>
      </div>
    </div>

    <!-- Body card -->
    <div style="background:#fff;border-radius:14px;padding:28px 32px;box-shadow:0 2px 12px rgba(0,0,0,.08);">
      {render_score_breakdown(verdict)}
      {render_key_finding(verdict)}
      {render_evidence(verdict)}
      {render_risk_flags(verdict)}
      {render_recommendations(verdict)}
      {render_sources(verdict)}
    </div>

    <p style="text-align:center;font-size:11px;color:#bbb;margin-top:20px;">
      Generated by Fake Product Detector{escape_html(platform.footer_suffix)} &middot; {now}
    </p>
  </div>
</body>
</html>"""
