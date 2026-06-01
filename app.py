import streamlit as st
import json, os, io, zipfile, csv
from datetime import datetime, timedelta
from pathlib import Path
from templates import generate_all, CONTENT_CALENDAR

st.set_page_config(page_title="Lime Tree SEO Agent", page_icon="🌿", layout="wide", initial_sidebar_state="expanded")

ARCHIVE_DIR = Path("archive")
ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
START_DATE  = datetime(2026, 5, 31)          # plan start

# ─────────────────────────────────────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:wght@600;700&display=swap');
:root{
  --bg:#080E09;--card:#0F1A10;--card2:#142016;--accent:#6BBF4E;--ag:#6BBF4E22;
  --ad:#3D7A28;--gold:#D4AF37;--g2:#D4AF3722;--text:#E8F0E9;--muted:#6B9B72;
  --border:#1B2E1D;--ba:#3D7A2844;--red:#E05252;--blue:#4A90D9;--r:12px;--rl:18px;
}
html,body,[class*="css"],.stApp{background:var(--bg)!important;font-family:'Inter',sans-serif!important;color:var(--text)!important;}
#MainMenu,footer,header,.stDeployButton{display:none!important;visibility:hidden!important;}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#0A1A0C,#070E08)!important;border-right:1px solid var(--border)!important;}
[data-testid="stSidebar"] *{color:var(--text)!important;}
.main .block-container{padding:1.75rem 2.25rem!important;max-width:1460px!important;}
::-webkit-scrollbar{width:5px;height:5px}::-webkit-scrollbar-track{background:var(--bg)}::-webkit-scrollbar-thumb{background:var(--border);border-radius:3px}
.stRadio label{display:block!important;padding:9px 14px!important;border-radius:7px!important;font-size:13px!important;font-weight:500!important;color:var(--muted)!important;cursor:pointer!important;transition:.15s!important;}
.stRadio label:hover{background:var(--ag)!important;color:var(--accent)!important;}
.page-hdr{background:linear-gradient(135deg,#0A2A0D,#091A0B,#060F07);border:1px solid var(--ba);border-radius:var(--rl);padding:1.75rem 2.25rem;margin-bottom:1.75rem;position:relative;overflow:hidden;}
.page-hdr::before{content:'';position:absolute;top:-50px;right:-50px;width:160px;height:160px;background:var(--ag);border-radius:50%;filter:blur(55px);}
.page-hdr h1{font-family:'Playfair Display',serif!important;font-size:1.85rem!important;font-weight:700!important;color:var(--text)!important;margin:0!important;}
.page-hdr p{color:var(--muted)!important;font-size:.9rem!important;margin:.4rem 0 0!important;}
.badge{display:inline-block;background:var(--ag);color:var(--accent);border:1px solid var(--ad);border-radius:20px;padding:2px 11px;font-size:.7rem;font-weight:700;margin-bottom:.6rem;letter-spacing:.06em;text-transform:uppercase;}
.mc{background:var(--card);border:1px solid var(--border);border-radius:var(--r);padding:1.1rem 1.35rem;position:relative;overflow:hidden;}
.mc::after{content:'';position:absolute;bottom:0;left:0;right:0;height:2px;background:linear-gradient(90deg,var(--accent),transparent);}
.mc .lbl{font-size:.7rem;color:var(--muted);text-transform:uppercase;letter-spacing:.07em;font-weight:600;}
.mc .val{font-size:1.8rem;font-weight:700;color:var(--accent);line-height:1.15;margin:.2rem 0;}
.mc .sub{font-size:.75rem;color:var(--muted);}
.mc .ico{position:absolute;top:.9rem;right:1.1rem;font-size:1.3rem;opacity:.28;}
.sc{background:var(--card);border:1px solid var(--border);border-radius:var(--r);padding:1.4rem;margin-bottom:.85rem;}
.sc h3{font-size:.92rem!important;font-weight:700!important;color:var(--text)!important;margin:0 0 .9rem!important;padding-bottom:.65rem!important;border-bottom:1px solid var(--border)!important;}
.tag{display:inline-block;padding:2px 9px;border-radius:11px;font-size:.68rem;font-weight:700;margin:2px;}
.tg{background:#1A3D1A;color:#6BBF4E}.tb{background:#0F1E35;color:#4A90D9}.tgo{background:#2A2310;color:#D4AF37}
.tr{background:#2A0F0F;color:#E05252}.tp{background:#1A1030;color:#9B7DE8}.tgr{background:#1A1F1B;color:#7A9B80}
.stButton>button{background:linear-gradient(135deg,var(--ad),#2D5E1A)!important;color:#fff!important;border:1px solid var(--ad)!important;border-radius:8px!important;font-weight:600!important;font-size:.85rem!important;transition:.2s all!important;}
.stButton>button:hover{background:linear-gradient(135deg,var(--accent),var(--ad))!important;transform:translateY(-1px)!important;box-shadow:0 4px 15px var(--ag)!important;}
.stTabs [data-baseweb="tab-list"]{background:var(--card)!important;border:1px solid var(--border)!important;border-bottom:none!important;border-radius:var(--r) var(--r) 0 0!important;gap:0!important;}
.stTabs [data-baseweb="tab"]{background:transparent!important;color:var(--muted)!important;font-weight:500!important;font-size:.82rem!important;padding:.65rem 1.1rem!important;border-bottom:2px solid transparent!important;}
.stTabs [aria-selected="true"]{color:var(--accent)!important;border-bottom:2px solid var(--accent)!important;}
.stTabs [data-baseweb="tab-panel"]{background:var(--card)!important;border:1px solid var(--border)!important;border-top:none!important;border-radius:0 0 var(--r) var(--r)!important;padding:1.4rem!important;}
.stExpander{background:var(--card)!important;border:1px solid var(--border)!important;border-radius:var(--r)!important;}
.krow{display:flex;align-items:center;justify-content:space-between;padding:.6rem .85rem;border-radius:8px;margin-bottom:.35rem;background:var(--card2);border:1px solid var(--border);font-size:.85rem;transition:.15s border-color;}
.krow:hover{border-color:var(--ad);}
.stProgress>div>div{background:linear-gradient(90deg,var(--ad),var(--accent))!important;}
.stTextInput input,.stSelectbox [data-baseweb="select"],.stTextArea textarea{background:var(--card2)!important;border:1px solid var(--border)!important;color:var(--text)!important;border-radius:8px!important;}
hr{border-color:var(--border)!important;}
.run-btn>button{background:linear-gradient(135deg,#1B5E20,#2E7D32,#388E3C)!important;color:#fff!important;border:none!important;border-radius:12px!important;font-size:1.05rem!important;font-weight:700!important;padding:.8rem 2rem!important;box-shadow:0 4px 20px #2E7D3244!important;width:100%!important;transition:.2s!important;}
.run-btn>button:hover{background:linear-gradient(135deg,#2E7D32,#4CAF50)!important;box-shadow:0 6px 30px #4CAF5055!important;transform:translateY(-2px)!important;}
.step-box{background:var(--card2);border:1px solid var(--border);border-radius:9px;padding:.7rem 1rem;margin-bottom:.4rem;display:flex;align-items:center;gap:.8rem;}
.step-n{background:var(--ag);color:var(--accent);border:1px solid var(--ad);border-radius:50%;width:24px;height:24px;display:flex;align-items:center;justify-content:center;font-size:.7rem;font-weight:700;flex-shrink:0;}
[data-baseweb="popover"],[data-baseweb="menu"]{background:var(--card)!important;border:1px solid var(--border)!important;}
[data-baseweb="option"]{background:var(--card)!important;color:var(--text)!important;}
[data-baseweb="option"]:hover{background:var(--ag)!important;}
/* ── Plan styles */
.week-hdr{background:linear-gradient(90deg,#0D2A10,#091A0B);border:1px solid var(--ba);border-radius:9px;padding:.75rem 1.1rem;margin:1rem 0 .5rem;display:flex;align-items:center;justify-content:space-between;}
.week-hdr .wn{font-family:'Playfair Display',serif;font-size:1rem;font-weight:700;color:var(--accent);}
.week-hdr .wd{font-size:.78rem;color:var(--muted);}
.plan-row{display:flex;align-items:flex-start;gap:.85rem;padding:.75rem .9rem;border-radius:8px;margin-bottom:.4rem;background:var(--card2);border:1px solid var(--border);}
.plan-row:hover{border-color:var(--ad);}
.plan-date{min-width:90px;text-align:center;padding:.35rem .6rem;border-radius:7px;}
.plan-date .pd{font-size:1rem;font-weight:700;}
.plan-date .pm{font-size:.68rem;text-transform:uppercase;letter-spacing:.05em;margin-top:1px;}
.plan-content{flex:1;}
.plan-label{font-size:.65rem;font-weight:700;text-transform:uppercase;letter-spacing:.08em;margin-bottom:.25rem;}
.plan-title{font-size:.87rem;font-weight:600;color:var(--text);}
.plan-kw{font-size:.73rem;color:var(--muted);margin-top:.2rem;}
.plan-badge{display:flex;flex-direction:column;align-items:flex-end;gap:.3rem;flex-shrink:0;}
.type-blog{background:#1A3D1A55;border:1px solid #3D7A28;}.type-blog .pd{color:#6BBF4E;}.type-blog .pm{color:#3D7A28;}
.type-gbp{background:#2A231055;border:1px solid #7A6020;}.type-gbp .pd{color:#D4AF37;}.type-gbp .pm{color:#7A6020;}
.type-ig{background:#1A103055;border:1px solid #6030A0;}.type-ig .pd{color:#B07DE8;}.type-ig .pm{color:#6030A0;}
.type-fb{background:#0F1E3555;border:1px solid #2050A0;}.type-fb .pd{color:#4A90D9;}.type-fb .pm{color:#2050A0;}
.type-li{background:#1A1F1B55;border:1px solid #3A5040;}.type-li .pd{color:#8AB090;}.type-li .pm{color:#3A5040;}
.type-multi{background:var(--card2);border:1px solid var(--border);}
/* ── Review styles */
.rev-card{background:var(--card2);border-radius:var(--r);padding:1.25rem 1.5rem;margin-bottom:1rem;border:1px solid var(--border);position:relative;}
.rev-card:hover{border-color:var(--ad);}
.rev-context{font-size:.68rem;font-weight:700;color:var(--accent);text-transform:uppercase;letter-spacing:.08em;margin-bottom:.5rem;}
.rev-kw-bar{display:flex;flex-wrap:wrap;gap:.35rem;margin:.75rem 0 .5rem;}
.rev-kw{background:#1A3D1A;color:#6BBF4E;border:1px solid #3D7A28;border-radius:6px;padding:2px 9px;font-size:.7rem;font-weight:600;}
.sidebar-logo{text-align:center;padding:1.25rem 1rem .75rem;border-bottom:1px solid var(--border);margin-bottom:.75rem;}
.sidebar-logo .li{font-size:2.2rem;}.sidebar-logo .ln{font-family:'Playfair Display',serif;font-size:.95rem;font-weight:700;}
.sidebar-logo .ls{font-size:.65rem;color:var(--accent);text-transform:uppercase;letter-spacing:.1em;}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────
def load_archive():
    records = []
    for f in ARCHIVE_DIR.glob("*.json"):
        if f.stat().st_size > 0:
            try:
                with open(f, encoding="utf-8") as fp:
                    records.append(json.load(fp))
            except Exception:
                pass
    return sorted(records, key=lambda x: x.get("generated_at",""), reverse=True)

def save_archive(data):
    fname = ARCHIVE_DIR / f"{data['id']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(fname, "w", encoding="utf-8") as fp:
        json.dump(data, fp, indent=2, ensure_ascii=False)

def make_zip(data):
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        for key, ext in [("article","md"),("social","md"),("gbp","md"),("schema","md")]:
            if data.get(key): z.writestr(f"{data['id']}_{key}.{ext}", data[key])
        z.writestr(f"{data['id']}_full.json", json.dumps(data, indent=2, ensure_ascii=False))
    return buf.getvalue()

def p_color(p):
    return {10:"#6BBF4E",9:"#89D162",8:"#A8DC8A",7:"#D4AF37",6:"#E8C547"}.get(p,"#7A9B80")

# ─────────────────────────────────────────────────────────────────────────────
# 60-Day plan generator
# ─────────────────────────────────────────────────────────────────────────────
GBP_SCHEDULE = [
    ("Medical Stay",       "Looking for accommodation near Medanta or Artemis Hospital? Lime Tree's serviced apartments include a full kitchen, laundry and 24/7 caretaker support — perfect for families on extended medical visits. Call +91 74 7900 0111."),
    ("Corporate Housing",  "Corporate teams in Gurgaon — Lime Tree offers 1BHK to 3BHK fully furnished apartments near Cyber City, Golf Course Road and DLF Phase 5. Weekly & monthly rates available. Book at limetreehotels.com."),
    ("Long Stay Deal",     "Planning a month-long stay in Gurgaon? Ask about our weekly and monthly rates — significantly lower than standard nightly hotel pricing. Full kitchen, laundry and 24/7 support included. Call +91 74 7900 0111."),
    ("Exhibition Visitor", "Visiting India Expo Mart, Greater Noida? Lime Tree Hotels' Greater Noida properties give you easy access to the venue. Group discounts available. Book early — rooms fill fast during exhibitions."),
    ("Women Travelers",    "Traveling solo in Gurgaon? Lime Tree Hotels has specific provisions for solo women travelers: lower floor rooms, lady executive assistance and 24/7 front desk security. Book at limetreehotels.com."),
    ("Direct Booking Win", "Skip the OTA fee — book directly with Lime Tree Hotels for our Best Price Guarantee. No middlemen, no markup, no hassle. limetreehotels.com | +91 74 7900 0111."),
    ("Family Stay",        "Families visiting Gurgaon for any reason — our 2BHK and 3BHK serviced apartments give you real space and a full kitchen. Far better than squeezing into two hotel rooms. Call +91 74 7900 0111."),
    ("Airport Shuttle",    "Flying into IGI Airport and heading to Gurgaon? Lime Tree Hotels offers airport shuttle service. Confirm when booking at +91 74 7900 0111 or reservation@limetreehotels.com."),
    ("Relocation Help",    "Relocating to Gurgaon? Start with a Lime Tree serviced apartment — fully furnished, all utilities included, flexible monthly stays. Buys you time to find a permanent home without the PG compromise."),
    ("Review Invite",      "Stayed with us recently? Your honest review on Google helps other families and corporate travelers find trusted serviced apartments in Gurgaon. It means more than you know — thank you! 🙏"),
    ("IT Professionals",   "IT professionals on Gurgaon projects — Lime Tree's serviced apartments near Cyber City and Golf Course Road offer fast Wi-Fi, dedicated workspace and monthly corporate rates. limetreehotels.com."),
    ("Best Rate Promise",  "Did you know our best rates are never on OTA platforms? Booking directly at limetreehotels.com or calling +91 74 7900 0111 always gives you the lowest price — guaranteed."),
    ("3BHK Special",       "Need space for a larger family or a team of 3–5? Lime Tree's 3BHK serviced apartments in Gurgaon include a full kitchen, living area and laundry — at a fraction of booking multiple rooms."),
    ("Vrindavan Trips",    "Planning a spiritual visit to Vrindavan? Lime Tree Hotels & Banquet in Vrindavan offers comfortable accommodation near the key temples. Book at +91 74 7900 0111."),
    ("Goa Villa",          "Need a complete escape from Delhi NCR? Lime Tree's 4BHK private pool villa in Anjuna, Goa is available for group bookings. Contact reservation@limetreehotels.com for details."),
    ("12 Years Strong",    "12 years. 500+ rooms. 6 cities. Lime Tree Hotels has been Gurgaon's trusted name in serviced apartments since 2013. Find your ideal stay at limetreehotels.com."),
    ("Noida Stay",         "Visiting Noida? Lime Tree Hotel & 1BHK Serviced Apartment in Sector 50 (near Grand Central Metro) offers all the comfort of our Gurgaon properties — kitchen, laundry, 24/7 support."),
]

SOCIAL_SCHEDULE = [
    ("instagram", "5 Reasons Families Choose Serviced Apartments Over Hotels Near Medanta Hospital 🏥", "Medical Tourism"),
    ("facebook",  "The Honest Cost Comparison: Hotel Room vs. Serviced Apartment for a 3-Week Gurgaon Stay", "Corporate"),
    ("linkedin",  "HR Guide: Managing Corporate Accommodation in Gurgaon Without the OTA Markup", "B2B"),
    ("instagram", "Your Kitchen. Your Laundry. Your Schedule. Why Lime Tree Apartments Beat Hotels for Long Stays 🏡", "Long Stay"),
    ("facebook",  "Exhibiting at India Expo Mart? Here's Why You Should Book Accommodation Now, Not Later", "Exhibition"),
    ("instagram", "Golf Course Road, IFFCO Chowk, DLF Phase 5 — Where to Stay in Gurgaon for Business 📍", "Local SEO"),
    ("linkedin",  "The Real Reason Corporate Travel Budgets Explode in Gurgaon (And How to Fix It)", "B2B"),
    ("instagram", "Medical Tourism in Gurgaon: What Families Wish They Knew Before Booking Accommodation 🩺", "Medical"),
    ("facebook",  "Relocating to Gurgaon? Why a Serviced Apartment Beats a PG for the First 3 Months", "Relocation"),
    ("instagram", "Women Traveling Solo in Gurgaon: What Safe Accommodation Actually Looks Like 🔒", "Safety"),
    ("linkedin",  "Why Your Company Should Never Book Hotel Rooms for Employees Staying 7+ Nights", "B2B"),
    ("facebook",  "Direct Booking vs OTA: The Price Difference No One Talks About at Lime Tree Hotels", "Direct Booking"),
    ("instagram", "2BHK Serviced Apartment vs Two Hotel Rooms: A Family's Guide to Smarter Stays in Gurgaon", "Family"),
    ("linkedin",  "Medanta, Artemis, Fortis — Gurgaon's Hospital Corridor and the Accommodation Crisis Nobody Plans For", "Medical Tourism"),
    ("instagram", "Cyber City's Best-Kept Secret: Serviced Apartments That Beat Every Business Hotel on the Strip 🏢", "Corporate"),
    ("facebook",  "12 Years. 500+ Rooms. Here's What Makes Lime Tree Hotels Different from Every OTA Listing", "Brand"),
    ("instagram", "Before You Book on MakeMyTrip — Read This About Gurgaon Serviced Apartments 📱", "Direct Booking"),
    ("linkedin",  "The HUDA City Centre Metro Corridor: Gurgaon's Most Underrated Corporate Stay Zone", "Local SEO"),
]

def build_60day_plan():
    plan = []
    blog_idx, gbp_idx, social_idx = 0, 0, 0
    for day_num in range(60):
        date    = START_DATE + timedelta(days=day_num)
        weekday = date.weekday()  # 0=Mon … 6=Sun
        items   = []

        # Blog: Monday(0) + Thursday(3)
        if weekday in [0, 3] and blog_idx < len(CONTENT_CALENDAR):
            art = CONTENT_CALENDAR[blog_idx]
            items.append({"type":"blog","emoji":"✍️","label":"BLOG POST","color":"tg",
                          "title":art["title"],"article_id":art["id"],
                          "keyword":art["kw"],"priority":art["priority"]})
            blog_idx += 1

        # GBP: Tuesday(1) + Friday(4)
        if weekday in [1, 4]:
            g = GBP_SCHEDULE[gbp_idx % len(GBP_SCHEDULE)]
            items.append({"type":"gbp","emoji":"📮","label":"GBP POST","color":"tgo",
                          "title":g[0],"detail":g[1]})
            gbp_idx += 1

        # Social
        if weekday in [0, 2, 5]:       # Mon / Wed / Sat → Instagram
            s = SOCIAL_SCHEDULE[social_idx % len(SOCIAL_SCHEDULE)]
            items.append({"type":"instagram","emoji":"📸","label":"INSTAGRAM","color":"tp",
                          "title":s[1],"category":s[2]})
            social_idx += 1
        if weekday in [1, 3]:          # Tue / Thu → Facebook
            s = SOCIAL_SCHEDULE[social_idx % len(SOCIAL_SCHEDULE)]
            items.append({"type":"facebook","emoji":"👥","label":"FACEBOOK","color":"tb",
                          "title":s[1],"category":s[2]})
            social_idx += 1
        if weekday == 2:               # Wed → LinkedIn (in addition to IG)
            s = SOCIAL_SCHEDULE[social_idx % len(SOCIAL_SCHEDULE)]
            items.append({"type":"linkedin","emoji":"💼","label":"LINKEDIN","color":"tgr",
                          "title":s[1],"category":s[2]})
            social_idx += 1

        plan.append({
            "day":          day_num + 1,
            "date":         date.strftime("%Y-%m-%d"),
            "display_date": date.strftime("%d %b"),
            "weekday":      date.strftime("%A"),
            "week":         day_num // 7 + 1,
            "items":        items,
        })
    return plan

# ─────────────────────────────────────────────────────────────────────────────
# Review reply templates  (keyword-rich for SEO indexing by Google)
# ─────────────────────────────────────────────────────────────────────────────
REVIEW_REPLIES = {
    5: [
        {
            "context": "General — Any Stay",
            "keywords": ["serviced apartments Gurgaon", "limetreehotels.com"],
            "reply": """Thank you so much for this wonderful review, [Guest Name]! 🙏

It means the world to our entire team at Lime Tree Hotels to know your stay was a genuinely positive experience. We put a great deal of care into ensuring our serviced apartments in Gurgaon feel like home — not just a hotel room — and feedback like yours confirms we are on the right path.

We hope to welcome you back very soon. Remember, you always get our Best Price Guarantee when booking directly at limetreehotels.com or by calling +91 74 7900 0111.

Warm regards,
Team Lime Tree Hotels""",
        },
        {
            "context": "Medical Stay (Medanta / Artemis / Fortis)",
            "keywords": ["hotels near Medanta Hospital Gurgaon", "serviced apartments near hospital Gurgaon", "medical tourism accommodation Gurgaon"],
            "reply": """Dear [Guest Name], thank you sincerely for taking the time to share this review — especially given what you were going through during your medical visit. 🙏

Supporting families staying near Medanta Hospital, Artemis Hospital, and Fortis Hospital in Gurgaon is something we take very seriously at Lime Tree Hotels. Our medical stay serviced apartments are built around your needs — the full kitchen, in-room laundry, and 24/7 caretaker support — and we are grateful it made a difficult time a little more manageable.

For your next medical visit to Gurgaon, please contact us directly at +91 74 7900 0111 — we will take care of all the arrangements personally.

With warmest regards,
Team Lime Tree Hotels""",
        },
        {
            "context": "Corporate / Business Stay",
            "keywords": ["corporate housing Gurgaon", "long stay hotels Gurgaon", "furnished apartments Gurgaon"],
            "reply": """Thank you for this excellent review, [Guest Name]!

We are delighted to know that Lime Tree Hotels delivered on what you needed for your corporate stay in Gurgaon. Long-term corporate housing is one of our specialities — and we work hard to ensure every professional feels genuinely at home, from the fully equipped kitchen to the reliable Wi-Fi and dedicated caretaker support across our furnished apartments in Gurgaon.

Should your team need accommodation in Gurgaon again — near Cyber City, Golf Course Road, or DLF Phase 5 — please reach out at reservation@limetreehotels.com. We would love to arrange a corporate rate for your company.

Best regards,
Team Lime Tree Hotels""",
        },
        {
            "context": "Family Stay",
            "keywords": ["2BHK serviced apartment Gurgaon", "family hotels Gurgaon with kitchen", "serviced apartments Gurgaon"],
            "reply": """What a lovely review — thank you so much, [Guest Name]! 😊

Family stays hold a very special place for us at Lime Tree Hotels. Our 2BHK and 3BHK serviced apartments in Gurgaon are designed precisely for families like yours — real space, a proper working kitchen, and the comfort of a home rather than the squeeze of a standard hotel room.

We hope the whole family had a wonderful time and we look forward to welcoming you back. Book directly at limetreehotels.com for our guaranteed best rates — no OTA markup.

Warmly,
Team Lime Tree Hotels""",
        },
        {
            "context": "Long Stay / Monthly",
            "keywords": ["furnished apartments Gurgaon monthly", "long stay hotels Gurgaon", "monthly rental apartments Gurgaon"],
            "reply": """Thank you so much for this generous review, [Guest Name]!

Long stays are what we do best at Lime Tree Hotels. Knowing you chose our furnished apartments in Gurgaon for your extended stay, and that it genuinely felt like home over those weeks, means a great deal to the whole team.

If you return to Gurgaon — whether for work, relocation or another long project — please contact us directly at +91 74 7900 0111. We can arrange a customised monthly rate for you. We would be honoured to host you again.

Best wishes,
Team Lime Tree Hotels""",
        },
    ],
    4: [
        {
            "context": "Good Stay — Minor Issue",
            "keywords": ["serviced apartments Gurgaon", "Lime Tree Hotels direct booking"],
            "reply": """Thank you for your kind review, [Guest Name], and for choosing Lime Tree Hotels for your Gurgaon stay!

We are glad the overall experience was positive. We have noted your feedback regarding [specific point mentioned] and will share it directly with our team — these insights genuinely help us improve our serviced apartments in Gurgaon to deliver a consistently excellent experience every time.

We hope to earn that fifth star on your next visit! Book directly at limetreehotels.com or call +91 74 7900 0111 for our best rates.

Best regards,
Team Lime Tree Hotels""",
        },
        {
            "context": "Medical Visit — Good",
            "keywords": ["hotels near Medanta Gurgaon", "accommodation near Artemis Hospital", "medical stay Gurgaon"],
            "reply": """Dear [Guest Name], thank you for sharing your experience during what we know was a challenging time for your family.

We are grateful our accommodation near Medanta Hospital provided comfort during your medical visit. Your feedback regarding [mentioned concern] is important — we have noted it and escalated it to our property team to ensure improvement.

We wish you and your family continued good health. If you need to stay near any of Gurgaon's hospitals again, please reach out to us directly at +91 74 7900 0111 so we can personally ensure everything is right.

With care,
Team Lime Tree Hotels""",
        },
        {
            "context": "Corporate — Good",
            "keywords": ["corporate housing Gurgaon", "long stay hotels Gurgaon", "business hotels Gurgaon"],
            "reply": """Thank you for your review and for choosing Lime Tree Hotels for your corporate stay in Gurgaon, [Guest Name].

It is great to hear the stay was largely comfortable. We have taken note of your feedback on [mentioned point] — for corporate guests especially, we know consistency and reliability matter above all else in long-stay accommodation.

For your next Gurgaon assignment, please get in touch directly at reservation@limetreehotels.com — we can discuss corporate housing rates and ensure everything is arranged to your exact specifications before check-in.

Best,
Team Lime Tree Hotels""",
        },
    ],
    3: [
        {
            "context": "Average Experience",
            "keywords": ["serviced apartments Gurgaon", "Lime Tree Hotels"],
            "reply": """Dear [Guest Name], thank you for taking the time to share your honest experience with Lime Tree Hotels.

We are sorry your stay did not fully meet your expectations — this is not the standard we hold ourselves to across our serviced apartments in Gurgaon. We have shared your specific feedback with our property management team, and it will be addressed directly.

We would genuinely love the opportunity to make it right. Please contact us at reservation@limetreehotels.com before your next visit — we will make sure everything is arranged personally this time.

Sincerely,
Management, Lime Tree Hotels""",
        },
        {
            "context": "Maintenance or Housekeeping Issue",
            "keywords": ["hotels Gurgaon", "Lime Tree Hotels Gurgaon", "serviced apartments Gurgaon"],
            "reply": """Dear [Guest Name], thank you for this honest feedback.

We sincerely apologise that the issue you mentioned affected your stay. That is not the standard we maintain across our Gurgaon properties and it falls short of what we promise — especially for guests who have chosen our serviced apartments in Gurgaon for an extended visit.

We have already escalated this internally. If you are visiting Gurgaon again, please reach out to us at +91 74 7900 0111 before your stay — we will personally ensure everything is in order.

Regards,
Management, Lime Tree Hotels""",
        },
        {
            "context": "Value Concern",
            "keywords": ["long stay hotels Gurgaon", "direct booking Lime Tree Hotels", "best rate serviced apartment Gurgaon"],
            "reply": """Dear [Guest Name], thank you for your candid feedback.

We understand your concern about value. We want to be transparent: our very best rates for long stay hotels in Gurgaon are always available on direct booking — via limetreehotels.com or by calling +91 74 7900 0111 — rather than through OTA platforms which add a 15–25% commission to the room rate.

Please reach out to us at reservation@limetreehotels.com before your next stay. We can offer a customised rate that we believe will change your perception entirely.

Regards,
Management, Lime Tree Hotels""",
        },
    ],
    2: [
        {
            "context": "Below Expectations",
            "keywords": ["serviced apartments Gurgaon", "Lime Tree Hotels 12 years"],
            "reply": """Dear [Guest Name], thank you for sharing this feedback — though we are sincerely sorry to read about your experience.

This is not who Lime Tree Hotels is. We have been providing serviced apartments in Gurgaon since 2013 — over 12 years — and a review like this tells us something went seriously wrong during your stay. We take full responsibility and want to understand exactly what happened.

Please contact our management directly at reservation@limetreehotels.com or +91 74 7900 0111. We will investigate this thoroughly and follow up with you personally.

Our sincerest apologies,
Management, Lime Tree Hotels""",
        },
        {
            "context": "Service Failure",
            "keywords": ["hotels Gurgaon", "serviced apartment Gurgaon 24/7 support"],
            "reply": """Dear [Guest Name], we are truly sorry for the experience you have described.

At Lime Tree Hotels, every guest at our serviced apartments in Gurgaon deserves to be met by our team within 24 hours of check-in, have their specific requirements understood, and receive consistent support throughout their stay. Clearly that did not happen in your case, and we are deeply sorry.

Please reach out directly to our management team at reservation@limetreehotels.com. We would like to understand the full situation and take corrective action. Your experience will not be ignored.

With our sincere apologies,
Management, Lime Tree Hotels""",
        },
    ],
    1: [
        {
            "context": "Strongly Negative",
            "keywords": ["Lime Tree Hotels Gurgaon", "serviced apartments Gurgaon management"],
            "reply": """Dear [Guest Name], thank you for this review — though we are deeply sorry to read it.

There is no excuse for the experience you have described. Lime Tree Hotels has been operating serviced apartments in Gurgaon since 2013 and every guest deserves to leave satisfied, cared for, and feeling the full value of what we offer. This review tells us we failed you, and we take that seriously.

Please contact our management team directly — not a front desk, but management — at reservation@limetreehotels.com or +91 74 7900 0111. We will investigate immediately and respond to you personally.

With our deepest apologies,
Management, Lime Tree Hotels""",
        },
        {
            "context": "Critical Service Issue",
            "keywords": ["hotels near Medanta Gurgaon management", "Lime Tree Hotels resolve complaint"],
            "reply": """Dear [Guest Name], we are profoundly sorry for the experience you have described.

Whether you came to us for a medical stay near a Gurgaon hospital, a corporate project, or a family visit, you deserved a stay that was comfortable, professional, and fully supported. This review suggests we fell far short of that, and we are committed to understanding why.

Please email reservation@limetreehotels.com directly — mark it for Management attention. We will respond within 24 hours, investigate fully, and take whatever corrective action is needed. This matters to us.

With our sincerest apologies,
Management, Lime Tree Hotels""",
        },
    ],
}

STAR_LABELS = {5:"⭐⭐⭐⭐⭐ Five Star", 4:"⭐⭐⭐⭐ Four Star", 3:"⭐⭐⭐ Three Star", 2:"⭐⭐ Two Star", 1:"⭐ One Star"}

# ─────────────────────────────────────────────────────────────────────────────
# Keyword value table
# ─────────────────────────────────────────────────────────────────────────────
TOP_KEYWORDS = [
    ("hotels near Medanta hospital Gurgaon",     "1,600–2,400", "Low",      10, "Transactional"),
    ("serviced apartments Gurgaon",              "4,000–6,000", "High",      8, "Commercial"),
    ("corporate housing Gurgaon",                "1,200–2,000", "Medium",   10, "B2B"),
    ("hotels near Artemis hospital Gurgaon",     "800–1,200",   "Low",      10, "Transactional"),
    ("long stay hotels Gurgaon",                 "800–1,200",   "Medium",    9, "Commercial"),
    ("furnished apartments Gurgaon monthly",     "1,000–1,500", "Medium",    8, "Commercial"),
    ("2BHK serviced apartment Gurgaon",          "700–1,000",   "Medium",    9, "Commercial"),
    ("hotels near India Expo Mart Greater Noida","800–1,200",   "Low",      10, "Local"),
    ("hotels near Fortis hospital Gurgaon",      "600–900",     "Low",       9, "Transactional"),
    ("hotels near Golf Course Road Gurgaon",     "600–900",     "Medium",    8, "Local"),
    ("hotels near HUDA City Centre Gurgaon",     "500–800",     "Low",       8, "Local"),
    ("3BHK serviced apartment Gurgaon",          "400–600",     "Low-Med",   7, "Commercial"),
    ("luxury serviced apartments Gurgaon",       "500–800",     "Medium",    7, "Commercial"),
    ("medical tourism accommodation Gurgaon",    "200–400",     "Very Low",  9, "Informational"),
    ("best serviced apartments Gurgaon",         "600–900",     "Medium",    7, "Informational"),
]

# ─────────────────────────────────────────────────────────────────────────────
# Sidebar
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-logo"><div class="li">🌿</div><div class="ln">Lime Tree Hotels</div><div class="ls">AI SEO Agent</div></div>', unsafe_allow_html=True)
    page = st.radio("nav", [
        "🤖  AI Agent",
        "📅  60-Day SEO Plan",
        "⭐  Review Replies",
        "📊  Dashboard",
        "📋  Calendar",
        "📁  Archive",
    ], label_visibility="collapsed")
    archive_count = len(list(ARCHIVE_DIR.glob("*.json")))
    st.markdown(f"""<hr><div style="padding:.4rem;font-size:.74rem;line-height:1.9;color:var(--muted);">
    <div>🟢 <b style="color:var(--text)">Engine:</b> Ready — No API needed</div>
    <div>✍️ <b style="color:var(--text)">Generated:</b> {archive_count}/50 articles</div>
    <div>📅 <b style="color:var(--text)">Plan starts:</b> 31 May 2026</div>
    <div>🏨 <b style="color:var(--text)">Properties:</b> 500+ rooms · 6 cities</div>
    </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  🤖 AI AGENT
# ══════════════════════════════════════════════════════════════════════════════
if page == "🤖  AI Agent":
    st.markdown('<div class="page-hdr"><div class="badge">🤖 Zero-API Automation</div><h1>SEO Content Agent</h1><p>One click generates a full SEO article, social captions, GBP posts, schema markup — with images. No API key needed.</p></div>', unsafe_allow_html=True)

    archive  = load_archive()
    done_ids = {r.get("id") for r in archive}
    remaining = [a for a in CONTENT_CALENDAR if a["id"] not in done_ids]

    col_l, col_r = st.columns([2, 3], gap="large")

    with col_l:
        st.markdown('<div class="sc"><h3>📋 Select Article</h3>', unsafe_allow_html=True)
        auto_mode = st.toggle("🎯 Auto Mode — highest priority first", value=True)
        if auto_mode:
            if not remaining:
                st.success("🎉 All 50 articles generated!")
                st.stop()
            article = sorted(remaining, key=lambda x: -x["priority"])[0]
            st.markdown(f"""<div style="background:var(--card2);border:1px solid var(--ba);border-radius:9px;padding:.9rem 1.1rem;margin:.5rem 0 0;">
            <div style="font-size:.7rem;color:var(--accent);font-weight:700;margin-bottom:.3rem;">AUTO-SELECTED · Priority {article['priority']}/10</div>
            <div style="font-size:.88rem;font-weight:600;color:var(--text);">{article['title']}</div>
            <div style="font-size:.75rem;color:var(--muted);margin-top:.3rem;">🔑 {article['kw']}</div>
            </div>""", unsafe_allow_html=True)
        else:
            opts = {f"[{a['id']}] P{a['priority']} · {a['title'][:52]}...": a for a in CONTENT_CALENDAR}
            article = opts[st.selectbox("Choose", list(opts.keys()), label_visibility="collapsed")]
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="sc"><h3>⚡ What Gets Generated</h3>', unsafe_allow_html=True)
        for ico, title, sub in [
            ("🖼️", "Article + Images",     "~1,400 words with 3 curated photos"),
            ("📱", "Social captions",      "Instagram ×2, Facebook ×2, LinkedIn"),
            ("📮", "GBP posts",            "2 Google Business Profile posts + Q&As"),
            ("🏗️", "Schema markup",        "FAQPage + Article + LocalBusiness JSON-LD"),
            ("💾", "Archive & download",   "ZIP with all files"),
        ]:
            st.markdown(f'<div class="step-box"><div class="step-n">{ico}</div><div><div style="font-size:.85rem;font-weight:600;color:var(--text);">{title}</div><div style="font-size:.73rem;color:var(--muted);">{sub}</div></div></div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="run-btn">', unsafe_allow_html=True)
        run = st.button("▶  GENERATE NOW", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_r:
        if not run and "last_result" not in st.session_state:
            st.markdown("""<div style="background:var(--card);border:1px solid var(--border);border-radius:var(--rl);padding:3rem;text-align:center;">
            <div style="font-size:3rem;margin-bottom:1rem;">🌿</div>
            <div style="font-family:'Playfair Display',serif;font-size:1.3rem;color:var(--text);margin-bottom:.6rem;">Ready to Generate</div>
            <div style="color:var(--muted);font-size:.88rem;line-height:1.9;max-width:300px;margin:0 auto;">
            Select an article and click<br><b style="color:var(--accent)">▶ GENERATE NOW</b><br><br>
            No API key. No cost. Instant output.<br>Images auto-added from Unsplash.
            </div></div>""", unsafe_allow_html=True)

        if run:
            with st.spinner("Generating full content package…"):
                result = generate_all(article)
                save_archive(result)
                st.session_state["last_result"] = result
            st.success(f"✅ {result['id']} generated — {result['word_count']:,} words, {result['article'].count('unsplash')} images")

        if "last_result" in st.session_state:
            res = st.session_state["last_result"]
            st.markdown(f"""<div style="background:var(--card2);border:1px solid var(--ba);border-radius:var(--r);padding:1rem 1.35rem;margin-bottom:1rem;display:flex;justify-content:space-between;align-items:center;">
            <div><div style="font-size:.72rem;color:var(--accent);font-weight:700;text-transform:uppercase;">Generated · {res.get('generated_at','')}</div>
            <div style="font-size:.92rem;font-weight:600;color:var(--text);">{res.get('title','')}</div>
            <div style="font-size:.73rem;color:var(--muted);margin-top:3px;">Template: {res.get('template','').replace('_',' ').title()} · {res.get('word_count',0):,} words</div></div>
            <div style="display:flex;gap:.4rem;flex-wrap:wrap;justify-content:flex-end;">
            <span class="tag tg">✓ Article</span><span class="tag tb">✓ Social</span>
            <span class="tag tgo">✓ GBP</span><span class="tag tp">✓ Schema</span></div></div>""", unsafe_allow_html=True)

            t1,t2,t3,t4,t5 = st.tabs(["🖼️ Article","📱 Social","📮 GBP","🏗️ Schema","⬇️ Download"])
            with t1:
                st.markdown(res["article"])
                st.download_button("⬇️ Download (.md)", res["article"], f"{res['id']}_article.md","text/markdown")
            with t2:
                st.markdown(res["social"])
                st.download_button("⬇️ Download", res["social"], f"{res['id']}_social.md","text/markdown")
            with t3:
                st.markdown(res["gbp"])
                st.download_button("⬇️ Download", res["gbp"], f"{res['id']}_gbp.md","text/markdown")
            with t4:
                st.markdown(res["schema"])
                st.download_button("⬇️ Download", res["schema"], f"{res['id']}_schema.md","text/markdown")
            with t5:
                st.download_button("⬇️ Download Everything (ZIP)", make_zip(res), f"{res['id']}_complete.zip","application/zip",use_container_width=True)
                if res.get("meta"):
                    st.markdown("---")
                    m = res["meta"]
                    st.code(f"Meta Title:       {m.get('meta_title','')}\nMeta Description: {m.get('meta_description','')}\nURL Slug:         {m.get('url_slug','')}\nFocus Keyword:    {m.get('focus_keyword','')}", language="text")


# ══════════════════════════════════════════════════════════════════════════════
#  📅 60-DAY SEO PLAN
# ══════════════════════════════════════════════════════════════════════════════
elif page == "📅  60-Day SEO Plan":
    plan = build_60day_plan()
    archive  = load_archive()
    done_ids = {r.get("id") for r in archive}

    end_date = (START_DATE + timedelta(days=59)).strftime("%d %b %Y")
    blogs_total  = sum(1 for d in plan for i in d["items"] if i["type"]=="blog")
    gbp_total    = sum(1 for d in plan for i in d["items"] if i["type"]=="gbp")
    social_total = sum(1 for d in plan for i in d["items"] if i["type"] in ["instagram","facebook","linkedin"])

    st.markdown(f'<div class="page-hdr"><div class="badge">📅 60-Day Plan · 31 May – {end_date}</div><h1>60-Day SEO Content Plan</h1><p>Auto-scheduled blog posts, GBP updates, and social content — every item date-stamped and ready to execute.</p></div>', unsafe_allow_html=True)

    c1,c2,c3,c4,c5 = st.columns(5)
    for col,(val,lbl,sub,ico) in zip([c1,c2,c3,c4,c5],[
        (blogs_total,  "Blog Posts",    "Published Mon & Thu",   "✍️"),
        (gbp_total,    "GBP Updates",   "Posted Tue & Fri",      "📮"),
        (social_total, "Social Posts",  "IG + FB + LinkedIn",    "📱"),
        (60,           "Days Covered",  f"Until {end_date}",     "📅"),
        (blogs_total+gbp_total+social_total,"Total Actions","Across 60 days","⚡"),
    ]):
        with col:
            st.markdown(f'<div class="mc"><div class="ico">{ico}</div><div class="lbl">{lbl}</div><div class="val">{val}</div><div class="sub">{sub}</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Filter
    fc1,fc2,fc3 = st.columns(3)
    with fc1: filter_type = st.selectbox("Filter by type", ["All","Blog Posts","GBP Posts","Instagram","Facebook","LinkedIn"])
    with fc2: filter_week = st.selectbox("Filter by week", ["All Weeks"]+[f"Week {i}" for i in range(1,10)])
    with fc3:
        # CSV download
        rows = []
        for d in plan:
            for it in d["items"]:
                rows.append({
                    "Day":d["day"],"Date":d["date"],"Weekday":d["weekday"],
                    "Type":it["type"].title(),"Title":it.get("title",""),
                    "Keyword":it.get("keyword",""),"Article_ID":it.get("article_id",""),
                    "Priority":it.get("priority",""),
                })
        csv_buf = io.StringIO()
        writer  = csv.DictWriter(csv_buf, fieldnames=rows[0].keys())
        writer.writeheader(); writer.writerows(rows)
        st.download_button("⬇️ Export Plan as CSV", csv_buf.getvalue().encode("utf-8"),
                           "lime_tree_60day_plan.csv","text/csv",use_container_width=True)

    # Type map for display
    TYPE_CSS = {"blog":"type-blog","gbp":"type-gbp","instagram":"type-ig","facebook":"type-fb","linkedin":"type-li"}
    TYPE_LABEL = {"blog":"✍️ BLOG","gbp":"📮 GBP","instagram":"📸 IG","facebook":"👥 FB","linkedin":"💼 LI"}

    # Group by week
    from itertools import groupby
    for week_num, week_days in groupby(plan, key=lambda d: d["week"]):
        week_days = list(week_days)
        wk_start  = week_days[0]["display_date"]
        wk_end    = week_days[-1]["display_date"]

        if filter_week != "All Weeks" and f"Week {week_num}" != filter_week:
            continue

        # Check if week has matching content
        has_content = any(
            i for d in week_days for i in d["items"]
            if filter_type == "All" or i["type"].title() in filter_type or i["label"].lower() in filter_type.lower()
        )
        if not has_content:
            continue

        blogs_in_wk  = [i for d in week_days for i in d["items"] if i["type"]=="blog"]
        gbp_in_wk    = [i for d in week_days for i in d["items"] if i["type"]=="gbp"]
        social_in_wk = [i for d in week_days for i in d["items"] if i["type"] in ["instagram","facebook","linkedin"]]

        st.markdown(f"""<div class="week-hdr">
        <div><div class="wn">Week {week_num}</div><div class="wd">{wk_start} — {wk_end}</div></div>
        <div style="display:flex;gap:.5rem;">
          {'<span class="tag tg">'+str(len(blogs_in_wk))+' blogs</span>' if blogs_in_wk else ''}
          {'<span class="tag tgo">'+str(len(gbp_in_wk))+' GBP</span>' if gbp_in_wk else ''}
          {'<span class="tag tp">'+str(len(social_in_wk))+' social</span>' if social_in_wk else ''}
        </div></div>""", unsafe_allow_html=True)

        for day in week_days:
            for item in day["items"]:
                # Apply filter
                if filter_type != "All":
                    match = (
                        (filter_type=="Blog Posts"   and item["type"]=="blog") or
                        (filter_type=="GBP Posts"    and item["type"]=="gbp")  or
                        (filter_type=="Instagram"    and item["type"]=="instagram") or
                        (filter_type=="Facebook"     and item["type"]=="facebook")  or
                        (filter_type=="LinkedIn"     and item["type"]=="linkedin")
                    )
                    if not match: continue

                css    = TYPE_CSS.get(item["type"],"")
                tlabel = TYPE_LABEL.get(item["type"],"")
                pc     = p_color(item.get("priority",5)) if item.get("priority") else "#7A9B80"
                done   = item.get("article_id","") in done_ids
                status = '<span class="tag tg">✓ Generated</span>' if done else ""

                kw_html = ""
                if item.get("keyword"):
                    kw_html = f'<div class="plan-kw">🔑 {item["keyword"]}</div>'
                elif item.get("detail"):
                    detail_short = item["detail"][:100] + "…" if len(item["detail"]) > 100 else item["detail"]
                    kw_html = f'<div class="plan-kw" style="font-style:italic;">{detail_short}</div>'
                elif item.get("category"):
                    kw_html = f'<div class="plan-kw">📂 {item["category"]}</div>'

                pri_html = f'<div style="font-size:1rem;font-weight:700;color:{pc};">P{item["priority"]}</div>' if item.get("priority") else ""

                st.markdown(f"""<div class="plan-row">
                <div class="plan-date {css}">
                  <div class="pd">{day['display_date'].split()[0]}</div>
                  <div class="pm">{day['display_date'].split()[1] if ' ' in day['display_date'] else ''}<br>{day['weekday'][:3]}</div>
                </div>
                <div class="plan-content">
                  <div class="plan-label" style="color:{'#6BBF4E' if item['type']=='blog' else '#D4AF37' if item['type']=='gbp' else '#9B7DE8' if item['type']=='instagram' else '#4A90D9' if item['type']=='facebook' else '#7A9B80'}">{tlabel}</div>
                  <div class="plan-title">{item['title']}</div>
                  {kw_html}
                </div>
                <div class="plan-badge">{pri_html}{status}</div>
                </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  ⭐ REVIEW REPLIES
# ══════════════════════════════════════════════════════════════════════════════
elif page == "⭐  Review Replies":
    st.markdown('<div class="page-hdr"><div class="badge">⭐ Review Management</div><h1>Keyword-Rich Review Replies</h1><p>SEO-optimised review responses — Google indexes these replies, embedding high-value keywords directly into your GBP profile.</p></div>', unsafe_allow_html=True)

    # Keyword value panel
    st.markdown('<div class="sc"><h3>🔑 High-Value Keywords Embedded in These Replies</h3>', unsafe_allow_html=True)
    kw_cols = st.columns(3)
    for i,(kw,vol,comp,pri,intent) in enumerate(TOP_KEYWORDS):
        with kw_cols[i%3]:
            pc = p_color(pri)
            comp_cls = {"Very Low":"tg","Low":"tg","Low-Med":"tg","Medium":"tgo","High":"tr"}.get(comp,"tgr")
            st.markdown(f"""<div class="krow" style="margin-bottom:.5rem;">
            <div><div style="font-size:.82rem;font-weight:600;color:var(--text);">{kw}</div>
            <div style="font-size:.71rem;color:var(--muted);margin-top:2px;">{vol}/mo &nbsp;·&nbsp; <span class="tag {comp_cls}" style="font-size:.62rem;">{comp} competition</span></div></div>
            <div style="text-align:right;"><div style="font-size:.95rem;font-weight:700;color:{pc};">P{pri}</div><div style="font-size:.65rem;color:var(--muted);">{intent}</div></div>
            </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<p style="color:var(--muted);font-size:.82rem;margin:.25rem 0 1.25rem;">Select a star rating to view reply templates. Replace <code>[Guest Name]</code> and <code>[specific point mentioned]</code> with real details before posting.</p>', unsafe_allow_html=True)

    tab_labels = [STAR_LABELS[s] for s in [5,4,3,2,1]]
    tabs = st.tabs(tab_labels)

    for tab, stars in zip(tabs, [5,4,3,2,1]):
        with tab:
            replies = REVIEW_REPLIES[stars]
            col_info, col_tip = st.columns([3,1])
            with col_info:
                count = len(replies)
                st.markdown(f'<p style="color:var(--muted);font-size:.82rem;">{count} reply template{"s" if count>1 else ""} — each uses different high-value keywords for maximum SEO coverage.</p>', unsafe_allow_html=True)
            with col_tip:
                st.markdown(f'<div style="background:var(--g2);border:1px solid #7A602055;border-radius:8px;padding:.6rem .85rem;font-size:.75rem;color:var(--gold);">💡 Rotate between templates so no two replies are identical.</div>', unsafe_allow_html=True)

            for idx, r in enumerate(replies, 1):
                kw_tags = "".join(f'<span class="rev-kw">{k}</span>' for k in r["keywords"])
                st.markdown(f"""<div class="rev-card">
                <div class="rev-context">Reply {idx} — {r['context']}</div>
                <div class="rev-kw-bar">{kw_tags}</div>
                </div>""", unsafe_allow_html=True)
                st.code(r["reply"], language=None)
                st.markdown("<br>", unsafe_allow_html=True)

    # Full download
    st.markdown("---")
    all_replies_md = "# Lime Tree Hotels — Keyword-Rich Review Reply Templates\n\n"
    for stars in [5,4,3,2,1]:
        all_replies_md += f"\n## {'⭐'*stars} Reviews\n\n"
        for i,r in enumerate(REVIEW_REPLIES[stars],1):
            all_replies_md += f"### Template {i} — {r['context']}\n"
            all_replies_md += f"**Keywords:** {', '.join(r['keywords'])}\n\n"
            all_replies_md += r["reply"] + "\n\n---\n\n"
    st.download_button("⬇️ Download All Reply Templates (.md)", all_replies_md, "lime_tree_review_replies.md","text/markdown",use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
#  📊 DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
elif page == "📊  Dashboard":
    archive  = load_archive()
    done_ids = {r.get("id") for r in archive}
    remaining = [a for a in CONTENT_CALENDAR if a["id"] not in done_ids]
    next_a   = sorted(remaining, key=lambda x:-x["priority"])[0] if remaining else None
    plan     = build_60day_plan()
    today_str= datetime.now().strftime("%Y-%m-%d")
    today_items = [i for d in plan if d["date"]==today_str for i in d["items"]]

    st.markdown('<div class="page-hdr"><div class="badge">📊 Overview</div><h1>SEO Engine Dashboard</h1><p>Live progress across all 50 articles, the 60-day plan, and your content pipeline.</p></div>', unsafe_allow_html=True)

    c1,c2,c3,c4,c5 = st.columns(5)
    for col,(val,lbl,sub,ico) in zip([c1,c2,c3,c4,c5],[
        (len(archive),"Generated",f"of 50 articles","✍️"),
        (50-len(archive),"Remaining","Articles to produce","📋"),
        (f"{len(archive)/50*100:.0f}%","Complete","Pipeline progress","📈"),
        (len(today_items),"Today's Tasks","Blog/GBP/Social","📅"),
        (next_a["priority"] if next_a else "✓","Next Priority",next_a["id"] if next_a else "All done!","🎯"),
    ]):
        with col:
            st.markdown(f'<div class="mc"><div class="ico">{ico}</div><div class="lbl">{lbl}</div><div class="val">{val}</div><div class="sub">{sub}</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    cl,cr = st.columns([3,2],gap="large")

    with cl:
        st.markdown('<div class="sc"><h3>📈 Pipeline Progress</h3>', unsafe_allow_html=True)
        st.progress(len(archive)/50)
        st.caption(f"{len(archive)}/50 complete · {50-len(archive)} remaining")
        if next_a:
            st.markdown(f"""<div style="background:var(--card2);border:1px solid var(--ba);border-radius:9px;padding:1rem 1.25rem;margin-top:.75rem;">
            <div style="font-size:.7rem;color:var(--accent);font-weight:700;margin-bottom:.3rem;">NEXT UP IN AUTO MODE</div>
            <div style="font-size:.9rem;font-weight:700;color:var(--text);">{next_a['title']}</div>
            <div style="margin-top:.5rem;"><span class="tag tg">P{next_a['priority']}</span><span class="tag tb">{next_a['intent']}</span><span class="tag tgr">Week {next_a['week']}</span></div>
            </div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="sc" style="margin-top:1rem;"><h3>🕐 Recently Generated</h3>', unsafe_allow_html=True)
        if archive:
            for r in archive[:5]:
                wc = r.get("word_count",0)
                imgs = r.get("article","").count("unsplash")
                st.markdown(f"""<div class="krow"><div>
                <div style="font-size:.87rem;font-weight:600;color:var(--text);">{r.get('title','')[:60]}{'…' if len(r.get('title',''))>60 else ''}</div>
                <div style="font-size:.73rem;color:var(--muted);margin-top:2px;">{r.get('id','')} · {r.get('generated_at','')[:16]} · {wc:,} words · {imgs} imgs</div>
                </div><span class="tag tg">Done</span></div>""", unsafe_allow_html=True)
        else:
            st.markdown('<p style="color:var(--muted);font-size:.85rem;">No articles yet. Click ▶ Generate Now in 🤖 AI Agent.</p>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with cr:
        st.markdown('<div class="sc"><h3>🎯 Cluster Progress</h3>', unsafe_allow_html=True)
        for name, ids, color in [
            ("Medical Tourism",  ["LT-001","LT-002","LT-007","LT-011","LT-028","LT-036","LT-046","LT-049"],"#6BBF4E"),
            ("Corporate / B2B",  ["LT-004","LT-005","LT-008","LT-014","LT-019","LT-033","LT-042"],"#89D162"),
            ("Local SEO",        ["LT-009","LT-010","LT-013","LT-015","LT-017","LT-021","LT-024","LT-030","LT-031","LT-032","LT-034","LT-044"],"#D4AF37"),
            ("Exhibition/Event", ["LT-003","LT-021"],"#4A90D9"),
            ("GEO / AI Search",  ["LT-046","LT-047","LT-048","LT-049","LT-050"],"#9B7DE8"),
        ]:
            done = sum(1 for i in ids if i in done_ids)
            total= len(ids); pct = done/total if total else 0
            st.markdown(f"""<div style="margin-bottom:.8rem;">
            <div style="display:flex;justify-content:space-between;font-size:.8rem;margin-bottom:.25rem;">
              <span style="color:var(--text);font-weight:500;">{name}</span>
              <span style="color:{color};font-weight:700;">{done}/{total}</span>
            </div>
            <div style="background:var(--border);border-radius:4px;height:6px;">
              <div style="background:{color};width:{pct*100:.0f}%;height:6px;border-radius:4px;"></div>
            </div></div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="sc" style="margin-top:1rem;"><h3>📅 60-Day Plan Stats</h3>', unsafe_allow_html=True)
        blogs_done = sum(1 for d in plan for i in d["items"] if i["type"]=="blog" and i.get("article_id","") in done_ids)
        blogs_total= sum(1 for d in plan for i in d["items"] if i["type"]=="blog")
        for lbl,done_c,total_c,cls in [
            ("Blog Posts",   blogs_done, blogs_total, "tg"),
            ("GBP Posts",    0,          sum(1 for d in plan for i in d["items"] if i["type"]=="gbp"), "tgo"),
            ("Social Posts", 0,          sum(1 for d in plan for i in d["items"] if i["type"] in ["instagram","facebook","linkedin"]), "tp"),
        ]:
            pct = done_c/total_c if total_c else 0
            st.markdown(f"""<div style="margin-bottom:.65rem;">
            <div style="display:flex;justify-content:space-between;font-size:.78rem;margin-bottom:.2rem;">
              <span style="color:var(--text);">{lbl}</span>
              <span class="tag {cls}" style="font-size:.65rem;">{done_c}/{total_c}</span>
            </div>
            <div style="background:var(--border);border-radius:3px;height:5px;">
              <div style="background:var(--accent);width:{pct*100:.0f}%;height:5px;border-radius:3px;"></div>
            </div></div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  📋 CALENDAR
# ══════════════════════════════════════════════════════════════════════════════
elif page == "📋  Calendar":
    archive  = load_archive()
    done_ids = {r.get("id") for r in archive}

    st.markdown('<div class="page-hdr"><div class="badge">📋 Content Calendar</div><h1>50-Article Publishing Plan</h1><p>All 50 articles filterable by tier, intent, and status. Green border = already generated.</p></div>', unsafe_allow_html=True)

    c1,c2,c3 = st.columns(3)
    with c1: tier_f   = st.selectbox("Tier", ["All","Tier 1","Tier 2","Tier 3","Tier 4"])
    with c2: intent_f = st.selectbox("Intent", ["All","Transactional","Commercial","B2B","Local","Informational","GEO"])
    with c3: status_f = st.selectbox("Status", ["All","Generated","Pending"])

    cal = CONTENT_CALENDAR
    if tier_f   != "All": cal = [a for a in cal if a["tier"]==int(tier_f[-1])]
    if intent_f != "All": cal = [a for a in cal if a["intent"]==intent_f]
    if status_f == "Generated": cal = [a for a in cal if a["id"] in done_ids]
    if status_f == "Pending":   cal = [a for a in cal if a["id"] not in done_ids]

    st.caption(f"Showing {len(cal)} articles · {len(done_ids)} generated · {50-len(done_ids)} pending")

    ic = {"Transactional":"tg","Commercial":"tb","B2B":"tp","Local":"tgo","Informational":"tgr","GEO":"tp"}
    for a in cal:
        done = a["id"] in done_ids
        pc   = p_color(a["priority"])
        st.markdown(f"""<div class="krow" style="border-color:{'var(--ad)' if done else 'var(--border)'}">
        <div style="flex:1;">
          <div style="display:flex;align-items:center;gap:.4rem;margin-bottom:.3rem;">
            <span style="font-size:.67rem;font-weight:700;color:var(--muted);background:var(--card);border:1px solid var(--border);border-radius:4px;padding:0 5px;">{a['id']}</span>
            <span class="tag {ic.get(a['intent'],'tgr')}">{a['intent']}</span>
            <span class="tag tgr">Wk {a['week']}</span>
            {'<span class="tag tg">✓ Generated</span>' if done else ''}
          </div>
          <div style="font-size:.87rem;font-weight:600;color:var(--text);">{a['title']}</div>
          <div style="font-size:.72rem;color:var(--muted);margin-top:.2rem;">🔑 {a['kw']}</div>
        </div>
        <div style="text-align:right;margin-left:1.25rem;flex-shrink:0;">
          <div style="font-size:1.15rem;font-weight:700;color:{pc};">P{a['priority']}</div>
          <div style="font-size:.68rem;color:var(--muted);">Tier {a['tier']}</div>
        </div></div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  📁 ARCHIVE
# ══════════════════════════════════════════════════════════════════════════════
elif page == "📁  Archive":
    archive = load_archive()
    st.markdown('<div class="page-hdr"><div class="badge">📁 Archive</div><h1>Generated Content</h1><p>Every article produced — view, download, or re-generate anytime.</p></div>', unsafe_allow_html=True)

    if not archive:
        st.markdown("""<div style="text-align:center;padding:3rem;background:var(--card);border:1px solid var(--border);border-radius:var(--rl);">
        <div style="font-size:2.5rem;margin-bottom:.75rem;">📭</div>
        <div style="font-size:1.1rem;color:var(--text);font-weight:600;margin-bottom:.4rem;">No Articles Yet</div>
        <div style="color:var(--muted);font-size:.88rem;">Go to 🤖 AI Agent → click ▶ Generate Now.</div></div>""", unsafe_allow_html=True)
    else:
        total_words = sum(r.get("word_count",0) for r in archive)
        c1,c2,c3 = st.columns(3)
        with c1: st.markdown(f'<div class="mc"><div class="lbl">Articles</div><div class="val">{len(archive)}</div><div class="sub">of 50 planned</div></div>', unsafe_allow_html=True)
        with c2: st.markdown(f'<div class="mc"><div class="lbl">Total Words</div><div class="val">{total_words:,}</div><div class="sub">Across all articles</div></div>', unsafe_allow_html=True)
        with c3:
            avg_imgs = sum(r.get("article","").count("unsplash") for r in archive) // max(len(archive),1)
            st.markdown(f'<div class="mc"><div class="lbl">Avg Images/Article</div><div class="val">{avg_imgs}</div><div class="sub">From Unsplash</div></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        for r in archive:
            with st.expander(f"**{r.get('id','')}** · {r.get('title','')[:65]}{'…' if len(r.get('title',''))>65 else ''}"):
                ca,cb = st.columns([3,1])
                with ca:
                    st.markdown(f"**Keyword:** {r.get('kw','')}")
                    st.markdown(f"**Generated:** {r.get('generated_at','')[:16]} · **Words:** {r.get('word_count',0):,} · **Template:** {r.get('template','').replace('_',' ').title()}")
                    images_in = r.get("article","").count("unsplash")
                    st.markdown(f"**Images:** {images_in} Unsplash photos embedded")
                with cb:
                    if r.get("article"): st.download_button("📄 Article",r["article"],f"{r['id']}_article.md","text/markdown",key=f"a_{r['id']}")
                    st.download_button("⬇️ ZIP",make_zip(r),f"{r['id']}.zip","application/zip",key=f"z_{r['id']}")
                if r.get("article"):
                    st.markdown("---")
                    st.markdown(r["article"][:900]+"\n\n*[Truncated — download for full article]*")
