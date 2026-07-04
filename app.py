import streamlit as st
import json, os, io, zipfile, csv
from datetime import datetime, timedelta
from pathlib import Path
from templates import generate_all, CONTENT_CALENDAR

st.set_page_config(page_title="Lime Tree SEO Agent", page_icon="🌿", layout="wide", initial_sidebar_state="expanded")

ARCHIVE_DIR = Path("archive")
ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
START_DATE  = datetime(2026, 7, 3)           # plan start
TOTAL_ARTICLES = len(CONTENT_CALENDAR)

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
    # ── Big chain / competitor comparison posts (added 2026-07-03) ─────────────
    ("Vs 5-Star Chains",   "Paying Taj/Oberoi/ITC nightly rates for a 2-week stay in Gurgaon? A Lime Tree serviced apartment gives you a full kitchen, laundry and a genuine monthly rate — for less. Call +91 74 7900 0111."),
    ("Vs Marriott/Hyatt",  "JW Marriott and Hyatt are built for a 1-night business trip — not a month-long project. Lime Tree's corporate housing gives your team a kitchen, laundry and a real monthly rate. reservation@limetreehotels.com."),
    ("Vs Lemon Tree",      "Comparing Lemon Tree Hotels for a long Gurgaon stay? Ask about our monthly rate first — full kitchen and laundry included, not just a room. limetreehotels.com."),
    ("Vs Co-Living",       "Zolo, Stanza Living, Nestaway — great for shared living. If you need your own private apartment with a dedicated caretaker, Lime Tree Hotels is built for exactly that. Call +91 74 7900 0111."),
    ("Vs Airbnb",          "Before you book an Airbnb for a 3-week Gurgaon stay, compare it to Lime Tree: verified property, 24/7 on-site support, GST invoicing, and a direct-booking best rate. limetreehotels.com."),
    ("No Loyalty Lock-In", "No Marriott Bonvoy points needed. No Hyatt status required. Just a genuinely better rate for stays of a week or more — book direct at limetreehotels.com."),
    ("Kitchen Advantage",  "Every major hotel chain in Gurgaon charges restaurant prices for every meal. Every Lime Tree serviced apartment includes a full kitchen. Do the math over 30 nights. Call +91 74 7900 0111."),
    ("HR Budget Tip",      "HR managers: before renewing a corporate rate with a 5-star chain, ask Lime Tree Hotels for a like-for-like monthly quote. reservation@limetreehotels.com — most teams save significantly."),
    ("Vs OYO/Treebo",      "OYO and Treebo are fine for one night. For a 2-week medical stay near Medanta or Artemis, you need a kitchen and a caretaker — that's Lime Tree Hotels. Call +91 74 7900 0111."),
    ("Vs Golf-Resort Hotels","Golf-resort hotels are built for leisure, not a Monday-to-Friday business stay. Lime Tree's corporate housing near Cyber City and Golf Course Road is built for exactly that. limetreehotels.com."),
    ("Direct Booking Math","OTA commission is 15–25%. Loyalty programs need points you may not have. Direct booking at limetreehotels.com is simply the lowest real price — every time."),
    ("Family vs Luxury Room","One luxury hotel room vs a 2BHK Lime Tree apartment for a family of four — same nights, very different cost and space. Call +91 74 7900 0111 to compare."),
    ("Relocating Employees","New joiners relocating to Gurgaon: a serviced apartment gets you settled faster than a hotel and cheaper than 90 days at a 5-star chain. reservation@limetreehotels.com."),
    ("12 Years vs New Platforms","Zolo, Nestaway, Airbnb — all newer to Gurgaon than Lime Tree Hotels. 12+ years, 500+ rooms, one consistent standard. Book at limetreehotels.com."),
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
    # ── Big chain / competitor comparison posts (added 2026-07-03) ─────────────
    ("instagram", "Taj, Oberoi, ITC — Beautiful for a Weekend. Here's What They Don't Offer for a Month-Long Stay 🏨", "Comparison"),
    ("linkedin",  "The Real Cost Difference: 5-Star Hotel Chain vs Serviced Apartment for a 30-Day Corporate Stay", "B2B"),
    ("facebook",  "JW Marriott, Hyatt, Radisson — Great Hotels, Wrong Product for a 2-Week Medical Stay Near Medanta", "Comparison"),
    ("instagram", "Lemon Tree vs Lime Tree: Same City, Very Different Long-Stay Value 🌿", "Comparison"),
    ("linkedin",  "Why HR Teams Are Rethinking Corporate Housing Budgets Beyond 5-Star Chains", "B2B"),
    ("instagram", "Zolo Stays, Stanza Living, Nestaway — Co-Living Is Great. Here's When You Need Your Own Apartment Instead 🔑", "Comparison"),
    ("facebook",  "Before You Book an Airbnb for 3 Weeks in Gurgaon, Read This", "Comparison"),
    ("instagram", "Trident, ITC Grand Bharat — Golf-Resort Luxury Isn't Built for a Monday Business Trip ⛳", "Comparison"),
    ("linkedin",  "OTA Commission + Loyalty Points ≠ The Real Best Price. Here's the Direct-Booking Math", "B2B"),
    ("instagram", "A Kitchen Changes Everything: Why No Major Hotel Chain in Gurgaon Can Match This 🍳", "Comparison"),
    ("facebook",  "Four Seasons-Style Luxury vs a Family Serviced Apartment: What Actually Matters for 4 People, 2 Weeks", "Comparison"),
    ("instagram", "OYO, Treebo — Perfect for One Night. Not for a Medical Stay Near Artemis Hospital 🏥", "Comparison"),
    ("linkedin",  "The Ascott, Citadines, Oakwood — Global Serviced Apartment Brands vs a Local 12-Year Standard in Gurgaon", "B2B"),
    ("instagram", "Relocating to Gurgaon? Here's Why 90 Days at a 5-Star Chain Doesn't Make Financial Sense 📦", "Relocation"),
    ("facebook",  "Marriott Bonvoy, Hyatt, IHG Points — Or a Genuinely Lower Direct Rate? We Did the Math", "Comparison"),
    ("instagram", "Same Nights, Same City — Hotel Room vs 2BHK Serviced Apartment for a Family of Four 👨‍👩‍👧‍👦", "Family"),
    ("linkedin",  "2026 Accommodation Comparison: Where Serviced Apartments Beat Full-Service Hotel Chains in Gurgaon", "B2B"),
    ("instagram", "Verified 12+ Years vs a New Listing: Why Hospitality Track Record Matters for Long Stays ✅", "Trust"),
    ("facebook",  "The Oberoi, ITC, Leela — World-Class Hospitality, Wrong Tool for a 3-Week Corporate Deployment", "Comparison"),
    ("instagram", "No Points. No Platform Fees. No Markup. Just a Direct Rate That's Actually Lower 💸", "Direct Booking"),
    ("linkedin",  "Why Corporate Travel Desks Should Request a Serviced Apartment Quote Before Renewing a Hotel Contract", "B2B"),
    ("instagram", "Co-Living Was Built for Students. Corporate Long Stays Need Something Else Entirely 🏢", "Comparison"),
    ("facebook",  "Everything a Taj or Oberoi Stay Doesn't Include for a 30-Night Booking (And What Lime Tree Does)", "Comparison"),
    ("instagram", "Big Chain Name, Bigger Bill: The Hidden Cost of Booking Luxury for an Extended Stay 💰", "Comparison"),
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

Team Lime Tree Hotels""",
        },
        {
            "context": "Medical Stay (Medanta / Artemis / Fortis)",
            "keywords": ["hotels near Medanta Hospital Gurgaon", "serviced apartments near hospital Gurgaon", "medical tourism accommodation Gurgaon"],
            "reply": """Dear [Guest Name], thank you sincerely for taking the time to share this review — especially given what you were going through during your medical visit. 🙏

Supporting families staying near Medanta Hospital, Artemis Hospital, and Fortis Hospital in Gurgaon is something we take very seriously at Lime Tree Hotels. Our medical stay serviced apartments are built around your needs — the full kitchen, in-room laundry, and 24/7 caretaker support — and we are grateful it made a difficult time a little more manageable.

For your next medical visit to Gurgaon, please contact us directly at +91 74 7900 0111 — we will take care of all the arrangements personally.

Team Lime Tree Hotels""",
        },
        {
            "context": "Corporate / Business Stay",
            "keywords": ["corporate housing Gurgaon", "long stay hotels Gurgaon", "furnished apartments Gurgaon"],
            "reply": """Thank you for this excellent review, [Guest Name]!

We are delighted to know that Lime Tree Hotels delivered on what you needed for your corporate stay in Gurgaon. Long-term corporate housing is one of our specialities — and we work hard to ensure every professional feels genuinely at home, from the fully equipped kitchen to the reliable Wi-Fi and dedicated caretaker support across our furnished apartments in Gurgaon.

Should your team need accommodation in Gurgaon again — near Cyber City, Golf Course Road, or DLF Phase 5 — please reach out at reservation@limetreehotels.com. We would love to arrange a corporate rate for your company.

Team Lime Tree Hotels""",
        },
        {
            "context": "Family Stay",
            "keywords": ["2BHK serviced apartment Gurgaon", "family hotels Gurgaon with kitchen", "serviced apartments Gurgaon"],
            "reply": """What a lovely review — thank you so much, [Guest Name]! 😊

Family stays hold a very special place for us at Lime Tree Hotels. Our 2BHK and 3BHK serviced apartments in Gurgaon are designed precisely for families like yours — real space, a proper working kitchen, and the comfort of a home rather than the squeeze of a standard hotel room.

We hope the whole family had a wonderful time and we look forward to welcoming you back. Book directly at limetreehotels.com for our guaranteed best rates — no OTA markup.

Team Lime Tree Hotels""",
        },
        {
            "context": "Long Stay / Monthly",
            "keywords": ["furnished apartments Gurgaon monthly", "long stay hotels Gurgaon", "monthly rental apartments Gurgaon"],
            "reply": """Thank you so much for this generous review, [Guest Name]!

Long stays are what we do best at Lime Tree Hotels. Knowing you chose our furnished apartments in Gurgaon for your extended stay, and that it genuinely felt like home over those weeks, means a great deal to the whole team.

If you return to Gurgaon — whether for work, relocation or another long project — please contact us directly at +91 74 7900 0111. We can arrange a customised monthly rate for you. We would be honoured to host you again.

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

Team Lime Tree Hotels""",
        },
        {
            "context": "Medical Visit — Good",
            "keywords": ["hotels near Medanta Gurgaon", "accommodation near Artemis Hospital", "medical stay Gurgaon"],
            "reply": """Dear [Guest Name], thank you for sharing your experience during what we know was a challenging time for your family.

We are grateful our accommodation near Medanta Hospital provided comfort during your medical visit. Your feedback regarding [mentioned concern] is important — we have noted it and escalated it to our property team to ensure improvement.

We wish you and your family continued good health. If you need to stay near any of Gurgaon's hospitals again, please reach out to us directly at +91 74 7900 0111 so we can personally ensure everything is right.

Team Lime Tree Hotels""",
        },
        {
            "context": "Corporate — Good",
            "keywords": ["corporate housing Gurgaon", "long stay hotels Gurgaon", "business hotels Gurgaon"],
            "reply": """Thank you for your review and for choosing Lime Tree Hotels for your corporate stay in Gurgaon, [Guest Name].

It is great to hear the stay was largely comfortable. We have taken note of your feedback on [mentioned point] — for corporate guests especially, we know consistency and reliability matter above all else in long-stay accommodation.

For your next Gurgaon assignment, please get in touch directly at reservation@limetreehotels.com — we can discuss corporate housing rates and ensure everything is arranged to your exact specifications before check-in.

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

Management, Lime Tree Hotels""",
        },
        {
            "context": "Maintenance or Housekeeping Issue",
            "keywords": ["hotels Gurgaon", "Lime Tree Hotels Gurgaon", "serviced apartments Gurgaon"],
            "reply": """Dear [Guest Name], thank you for this honest feedback.

We sincerely apologise that the issue you mentioned affected your stay. That is not the standard we maintain across our Gurgaon properties and it falls short of what we promise — especially for guests who have chosen our serviced apartments in Gurgaon for an extended visit.

We have already escalated this internally. If you are visiting Gurgaon again, please reach out to us at +91 74 7900 0111 before your stay — we will personally ensure everything is in order.

Management, Lime Tree Hotels""",
        },
        {
            "context": "Value Concern",
            "keywords": ["long stay hotels Gurgaon", "direct booking Lime Tree Hotels", "best rate serviced apartment Gurgaon"],
            "reply": """Dear [Guest Name], thank you for your candid feedback.

We understand your concern about value. We want to be transparent: our very best rates for long stay hotels in Gurgaon are always available on direct booking — via limetreehotels.com or by calling +91 74 7900 0111 — rather than through OTA platforms which add a 15–25% commission to the room rate.

Please reach out to us at reservation@limetreehotels.com before your next stay. We can offer a customised rate that we believe will change your perception entirely.

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

Management, Lime Tree Hotels""",
        },
        {
            "context": "Service Failure",
            "keywords": ["hotels Gurgaon", "serviced apartment Gurgaon 24/7 support"],
            "reply": """Dear [Guest Name], we are truly sorry for the experience you have described.

At Lime Tree Hotels, every guest at our serviced apartments in Gurgaon deserves to be met by our team within 24 hours of check-in, have their specific requirements understood, and receive consistent support throughout their stay. Clearly that did not happen in your case, and we are deeply sorry.

Please reach out directly to our management team at reservation@limetreehotels.com. We would like to understand the full situation and take corrective action. Your experience will not be ignored.

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

Management, Lime Tree Hotels""",
        },
        {
            "context": "Critical Service Issue",
            "keywords": ["hotels near Medanta Gurgaon management", "Lime Tree Hotels resolve complaint"],
            "reply": """Dear [Guest Name], we are profoundly sorry for the experience you have described.

Whether you came to us for a medical stay near a Gurgaon hospital, a corporate project, or a family visit, you deserved a stay that was comfortable, professional, and fully supported. This review suggests we fell far short of that, and we are committed to understanding why.

Please email reservation@limetreehotels.com directly — mark it for Management attention. We will respond within 24 hours, investigate fully, and take whatever corrective action is needed. This matters to us.

Management, Lime Tree Hotels""",
        },
    ],
}

STAR_LABELS = {5:"⭐⭐⭐⭐⭐ Five Star", 4:"⭐⭐⭐⭐ Four Star", 3:"⭐⭐⭐ Three Star", 2:"⭐⭐ Two Star", 1:"⭐ One Star"}

# ─────────────────────────────────────────────────────────────────────────────
# Review chatbot — analysis + reply engine  (we-voice, Lime Tree specific)
# ─────────────────────────────────────────────────────────────────────────────
_TOPICS = {
    "kitchen":     (["kitchen","cook","cooking","food","meal","microwave","stove","induction","refrigerator","fridge","utensil","pantry","ingredients","boil","heat up","groceries"],
                    "Kitchen & Cooking Facilities"),
    "cleanliness": (["clean","dirty","hygiene","dust","spotless","tidy","mess","stain","smell","filthy","unhygienic","swept","mopped","cobweb","pest","cockroach","bedsheet","linen changed"],
                    "Cleanliness & Housekeeping"),
    "wifi":        (["wifi","wi-fi","internet","connection","network","bandwidth","slow internet","disconnected","connectivity","broadband","router","signal","mbps"],
                    "Wi-Fi & Internet"),
    "staff":       (["staff","team","service","helpful","rude","friendly","reception","front desk","check-in","checkin","caretaker","behaviour","behavior","attitude","polite","unprofessional","ignored","responded","attentive","prompt","rude","dismissive","warm","welcoming","24 hours","within 24"],
                    "Staff & Service"),
    "location":    (["location","distance","near","close","far","hospital","metro","medanta","artemis","fortis","golf course","cyber city","iffco","huda","sector","walkable","cab","auto","proximity","accessible","connected"],
                    "Location & Proximity"),
    "price":       (["price","value","expensive","cheap","costly","rate","worth","money","overpriced","affordable","charge","bill","invoice","cost","budget","pricing","ota","booking.com","makemytrip"],
                    "Pricing & Value"),
    "room":        (["room","apartment","space","spacious","small","bathroom","toilet","bed","mattress","pillow","comfortable","dark","bright","balcony","furniture","sofa","wardrobe","cupboard","storage","cramped","roomy","airy"],
                    "Room / Apartment"),
    "laundry":     (["laundry","washing","machine","washer","clothes","linen","dryer","washing powder","washing machine","spin","rinse"],
                    "Laundry"),
    "parking":     (["parking","car","park","vehicle","bike","two-wheeler","scooter","space for car","basement","open parking"],
                    "Parking"),
    "ac":          (["ac","air conditioning","air-conditioning","temperature","hot","cold","cool","heating","aircon","hvac","too hot","too cold","sweating","freezing"],
                    "Air Conditioning"),
    "noise":       (["noise","quiet","loud","sound","noisy","disturb","disturbance","construction","traffic","barking","party","music","thin walls"],
                    "Noise Level"),
    "maintenance": (["maintenance","repair","broken","not working","didn't work","issue","problem","fault","leaking","leak","plumbing","electrical","geyser","water heater","tap","flush","switch","light","bulb","power cut"],
                    "Maintenance"),
    "security":    (["security","safe","safety","lock","key","access","guard","cctv","unsafe","suspicious","entry","gate","cctv","intercom"],
                    "Security"),
    "breakfast":   (["breakfast","food quality","meals","restaurant","snack","hungry","pantry service","evening snack","tea","coffee","milk","toast"],
                    "Breakfast / Food"),
    "checkin":     (["check-in","checkin","check out","checkout","delay","wait","waiting","late","early","arrival","reception time","key handover","process","welcome","greeted"],
                    "Check-in / Check-out"),
    "housekeeping":([" housekeeping","daily cleaning","sweeping","maid","room service","towel","fresh towel","linen change","room cleaned","not cleaned","cleaning schedule"],
                    "Daily Housekeeping"),
    "water":       (["water","geyser","hot water","cold water","pressure","water pressure","supply","tank","shortage","no water","borewell"],
                    "Water Supply"),
    "power":       (["power cut","power backup","electricity","load shedding","generator","inverter","ug","power gone","no electricity","light gone"],
                    "Power Backup"),
}

# ─────────────────────────────────────────────────────────────────────────────
# Reply-engine vocabulary  (trained on Taj / Oberoi / ITC / Leela patterns)
# ─────────────────────────────────────────────────────────────────────────────

_NEG_WORDS = [
    "bad","poor","terrible","awful","horrible","disappointing","dirty","broken","slow","rude",
    "not working","issue","problem","worst","never again","waste","overpriced","leaking","noisy",
    "unhappy","dissatisfied","below average","inadequate","unfortunately","sadly","regret",
    "expected better","did not meet","failed","disgrace","unacceptable","pathetic","useless",
    "mess","disaster","frustrated","upset","angry","annoyed","complaint","didn't work",
    "not clean","no hot water","power went","no power","ac not working","wifi not working",
    "couldn't sleep","broken down","smell bad","smell terrible","pest","cockroach","rude staff",
    "unprofessional","delayed","late checkin","overcharged","billed extra","maintenance ignored",
    "no response","no one came","waited hours","dark room","small room","cramped","noisy room",
    "not satisfied","not happy","below par","substandard","negligent","ignored","dismissive",
    "stale","mould","mold","rusty","broken tap","no geyser","geyser not working","cold water",
    "not maintained","needs repair","outdated","dated","poorly maintained","smelly","damp",
    "leaky","no parking","charged extra","hidden charges","false promises","not as described",
    "misleading","deceptive","false advertising","dirty bathroom","unclean","not swept",
    "no response from staff","staff absent","nobody at reception","long wait","attitude problem",
]

_POS_WORDS = [
    "great","good","excellent","amazing","wonderful","perfect","comfortable","clean","helpful",
    "friendly","spacious","love","loved","enjoyed","fantastic","brilliant","highly recommend",
    "will visit again","best","outstanding","superb","satisfied","impressed","happy","pleased",
    "thank you","5 star","five star","beautiful","nice","pleasant","cozy","cosy","homely",
    "value for money","well maintained","well-maintained","prompt","quick","fast","smooth","easy",
    "convenient","worth it","exceeded","above expectations","delighted","lovely","appreciated",
    "professional","attentive","responsive","warm welcome","felt at home","like home","peaceful",
    "quiet","safe","secure","highly satisfied","exceeded expectations","top notch","spotless",
    "immaculate","impeccable","pristine","well-equipped","fully equipped","extremely helpful",
    "very supportive","always available","immediate response","went above","beyond expectations",
    "like family","home away from home","highly professional","top class","world class",
    "first class","would recommend","100 percent","perfect location","great value",
    "money well spent","no complaints","absolutely loved","thoroughly enjoyed","genuinely good",
    "very impressed","pleasantly surprised","exceeded","will return","recommended to friends",
]

# ── Departments for authentic attribution (Taj / Oberoi / ITC style) ─────────
_DEPT = {
    "kitchen":     "our Kitchen & Hospitality Manager",
    "cleanliness": "our Executive Housekeeper",
    "wifi":        "our Technical Services Manager",
    "staff":       "our Guest Relations Manager",
    "location":    "our Reservations and Guest Relations team",
    "price":       "our Revenue Management and Guest Relations team",
    "room":        "our Property Manager",
    "laundry":     "our Housekeeping Supervisor",
    "parking":     "our Facilities Manager",
    "ac":          "our Chief Maintenance Engineer",
    "noise":       "our Property Manager and Building Superintendent",
    "maintenance": "our Maintenance Supervisor",
    "security":    "our Head of Security",
    "breakfast":   "our Food & Hospitality Manager",
    "checkin":     "our Front Office Manager",
    "housekeeping":"our Executive Housekeeper",
    "water":       "our Facilities and Engineering team",
    "power":       "our Electrical and Maintenance Supervisor",
}


def _pick(variants: list, seed: str) -> str:
    """Select a variant deterministically from the review text so the same review always gets the same reply."""
    return variants[hash(seed[:60]) % len(variants)]


# Professional apology language — replaces casual "sorry" phrases throughout
_APOLOGY_MAP = [
    ("We are genuinely and deeply sorry",  "We sincerely apologise"),
    ("we are genuinely and deeply sorry",  "we sincerely apologise"),
    ("We are deeply sorry",                "We sincerely apologise"),
    ("we are deeply sorry",                "we sincerely apologise"),
    ("We are profoundly sorry",            "We deeply regret"),
    ("we are profoundly sorry",            "we deeply regret"),
    ("We are truly sorry",                 "We sincerely regret"),
    ("we are truly sorry",                 "we sincerely regret"),
    ("We are very sorry",                  "We sincerely regret"),
    ("we are very sorry",                  "we sincerely regret"),
    ("We are sincerely sorry",             "We extend our sincerest apologies"),
    ("we are sincerely sorry",             "we extend our sincerest apologies"),
    ("We are genuinely sorry",             "We sincerely apologise"),
    ("we are genuinely sorry",             "we sincerely apologise"),
    ("we are sorry to",                    "we sincerely regret to"),
    ("We are sorry to",                    "We sincerely regret to"),
    ("deeply sorry for the experience",    "sincerely apologise for the experience"),
    ("sorry to learn",                     "regret to learn"),
    ("sorry for any",                      "sincerely apologise for any"),
    ("so sorry",                           "sincerely apologetic"),
]


def _sanitize(text: str) -> str:
    """Apply professional apology language throughout the reply."""
    for casual, formal in _APOLOGY_MAP:
        text = text.replace(casual, formal)
    return text


def _cap_reply(opening: str, body_parts: list, closing: str, signature: str, max_words: int = 108) -> str:
    """Assemble reply so opening+body+closing fits within max_words (signature excluded).
    Targets ~130-150 total words when combined with the ~25-word signature block."""
    import re
    def sentence_trim(para: str, budget: int) -> str:
        sentences = re.split(r'(?<=[.!?])\s+', para.strip())
        out, count = [], 0
        for s in sentences:
            w = len(s.split())
            if count + w > budget and out:
                break
            out.append(s)
            count += w
        return " ".join(out)

    open_words    = len(opening.split())
    remaining     = max(max_words - open_words, 45)
    close_budget  = min(32, remaining // 2)          # closing gets at most 32 words
    body_budget   = remaining - close_budget          # body gets the rest

    trimmed_close = sentence_trim(closing, close_budget)

    parts = [opening]
    if body_parts:
        parts.append(sentence_trim(body_parts[0], max(body_budget, 22)))
    parts.append(trimmed_close)
    if signature:
        parts.append(signature)
    return "\n\n".join(parts)

# ── Positive variants — 3 per topic (Taj/Oberoi/ITC/Leela/Marriott/Hyatt/Four Seasons) ─
_POS_VARIANTS = {
    "kitchen": [
        "We are heartened to learn that our fully equipped kitchen — the induction stove, refrigerator, microwave, and complete utensil set — contributed so meaningfully to the quality of your stay. At Lime Tree Hotels, we believe every serviced apartment should function as a genuine home, and the freedom to prepare one's own meals is a facility we invest in and maintain to the highest standard across all our properties.",
        "It brings us great joy to know that our in-apartment kitchen made such a positive difference. We are particularly conscious of how important this facility is for guests on extended stays, for families accompanying patients during medical visits, and for professionals who prefer the ease and economy of home-cooked meals — and we are delighted it served you exactly as intended.",
        "We are truly delighted to hear that the kitchen facilities in your apartment met your expectations. Our commitment is to ensure every Lime Tree kitchen is fully stocked, impeccably maintained, and ready to function from the moment of check-in — the induction stove, refrigerator, microwave, and utensil set are inspected before every arrival, and we are glad this showed.",
    ],
    "cleanliness": [
        "We are delighted to note your appreciation of the cleanliness and upkeep of the apartment. Our Executive Housekeeper follows a structured protocol — a deep clean before every check-in, followed by scheduled daily maintenance throughout the stay — and your acknowledgement is a testament to that commitment. Please be assured that we shall continue to hold this standard without compromise.",
        "It is truly gratifying to receive your compliments on the cleanliness of the property. A spotless, well-maintained apartment is the foundation of every Lime Tree stay, and our Housekeeping team takes considerable pride in maintaining that standard — not just at check-in, but every single day of a guest's visit.",
        "We are thrilled to learn that the cleanliness of your apartment exceeded your expectations. Maintaining immaculate standards of hygiene and upkeep across all our serviced apartments in Gurgaon is a responsibility we hold to the highest level, and we are very encouraged to know this was clearly evident throughout your stay.",
    ],
    "wifi": [
        "It is gratifying to learn that our high-speed internet connectivity met your expectations throughout your stay. We are fully aware that reliable Wi-Fi is not a luxury but a necessity — whether one is a corporate professional working remotely, a medical companion coordinating with specialists, or a family staying in touch with loved ones. Please be assured that we monitor network performance continuously across all our Gurgaon properties.",
        "We are delighted to know that the internet connectivity provided you with the reliable, high-speed experience you needed. At Lime Tree Hotels, we regard fast and stable Wi-Fi as a core part of the serviced apartment offering — particularly for corporate guests and medical companions who depend on it for professional and personal coordination throughout the day.",
        "Thank you for specifically mentioning our internet connectivity. We invest in and maintain robust broadband infrastructure across all our properties precisely because we understand that a dropped connection is not just an inconvenience — for a working professional or a family managing a medical situation remotely, it can be a genuine disruption. We are very glad it performed well.",
    ],
    "staff": [
        "We are truly delighted to read your appreciation of our team. Your kind words have been shared with our Guest Relations Manager and the individual team members concerned — it is the highest form of recognition for them and motivates the entire property. At Lime Tree Hotels, we commit to meeting every guest within 24 hours of check-in to understand their specific needs and remain fully accessible throughout their stay.",
        "It is always wonderful to receive such generous feedback about our team. We are especially pleased because our people are the heart of the Lime Tree experience — their attentiveness, warmth, and genuine commitment to every guest's comfort is something we nurture carefully and take great pride in. We shall ensure your kind words reach the specific individuals who made a difference.",
        "We are absolutely delighted to learn that our team made such a positive impression. On behalf of the entire Lime Tree Hotels family, thank you for recognising their efforts. We believe the best hospitality is personal — not procedural — and it is deeply rewarding to know that came through clearly during your stay.",
    ],
    "location": [
        "We are pleased to learn that our location served your purpose so well. Our properties in Gurgaon are deliberately positioned near Medanta–The Medicity, Artemis Hospital, Fortis Memorial, Golf Course Road, Cyber City, IFFCO Chowk, and HUDA City Centre — so that whether you are here for a medical visit, a corporate assignment, or an extended family stay, the distance to your destination is always considered.",
        "It is gratifying to know that our location proved to be such a convenient base for your visit. The strategic positioning of our Gurgaon properties — within close proximity to the city's key hospitals, business districts, and transport hubs — is a deliberate choice we made to serve the diverse needs of our guests, and we are very glad it delivered exactly that value for you.",
        "We are delighted that the location of your apartment worked so well for the purpose of your visit. Accessibility is one of the key pillars of the Lime Tree experience — and whether a guest is navigating to a hospital in Sector 38 or 51, a corporate campus in Cyber City, or a metro station, we want the journey from our door to theirs to be as short and straightforward as possible.",
    ],
    "price": [
        "We are heartened to know that you found your stay to represent genuine value. Please be assured that our Best Price Guarantee is a firm commitment — guests who book directly at limetreehotels.com always receive rates that no OTA platform can match, without additional commission markups. We are glad this was reflected in your experience.",
        "We are truly pleased to know that our rates felt fair and our stay delivered genuine value for money. At Lime Tree Hotels, we are committed to offering the best available rate exclusively through direct booking at limetreehotels.com — and to ensuring that every rupee spent is matched by the quality of the apartment, the facilities, and the service you receive.",
        "It is wonderful to learn that the value proposition of your stay met your expectations. We put considerable thought into our pricing — particularly for long-stay and corporate guests — and we are glad the experience reflected that. We always encourage guests to book directly at limetreehotels.com for our guaranteed best rate and for any customised long-stay pricing requests.",
    ],
    "room": [
        "It is wonderful to learn that the apartment felt like a true home. Every Lime Tree serviced apartment — from our 1BHK to our 3BHK configurations — is designed with careful attention to space, natural light, furniture quality, and storage, because we understand that a guest staying for two weeks or two months should feel genuinely settled, not merely housed.",
        "We are absolutely delighted that the apartment lived up to your expectations. Our design philosophy at Lime Tree is simple: a serviced apartment should be spacious, well-furnished, and genuinely liveable — not just a hotel room with a kitchen attached. We are very glad the space served you well throughout your stay.",
        "It brings us immense satisfaction to know that the apartment felt like a proper home during your visit. We invest significantly in the quality of our furnishings, the thoughtfulness of our layouts, and the functionality of every room — because we believe a guest on a two-week or two-month stay deserves to feel settled and comfortable from day one.",
    ],
    "laundry": [
        "We are glad our in-room laundry facility added to the convenience of your stay. It is one of those provisions that becomes indispensable on an extended visit — and we include it across all our serviced apartments in Gurgaon precisely for that reason. We are pleased it served you well.",
        "We are delighted to know that our in-apartment washing machine made a meaningful difference to your daily routine. At Lime Tree, we include in-room laundry across all properties because we understand that for long-stay guests — particularly those managing the demands of a medical visit or an extended work assignment — laundry independence is a quiet but significant comfort.",
        "It is pleasing to know that the in-room laundry facility contributed positively to your stay. This is a feature we regard as essential rather than supplementary — particularly for guests staying for a week or more — and we are glad it performed reliably and conveniently throughout your visit.",
    ],
    "parking": [
        "We are delighted that our complimentary parking facility proved convenient. We maintain dedicated parking across all our Gurgaon properties because we recognise how important it is — particularly for guests driving in from other cities or keeping a vehicle during a long stay. Please be assured this will continue to be available on every visit.",
        "We are glad our complimentary parking arrangement worked well for you. The ability to bring and park one's own vehicle without additional cost or complexity is something we make available at all our properties, and we are pleased it removed one less thing to worry about during your stay.",
        "Thank you for specifically mentioning our parking facility. We are committed to maintaining complimentary, convenient parking across all our Gurgaon properties — because we understand that for guests driving in from other cities, or keeping a car for hospital or office commutes, easy and accessible parking is genuinely important.",
    ],
    "ac": [
        "We are pleased to note that the air conditioning maintained the right environment throughout your stay. Our Maintenance team conducts thorough pre-check-in inspections of all HVAC units — particularly critical given Delhi NCR's extreme seasonal temperatures — and your confirmation that it performed well is very gratifying.",
        "We are delighted to know that the air conditioning in your apartment provided the comfortable environment you needed. At Lime Tree Hotels, we regard climate control as one of the most critical aspects of a guest's daily comfort — and our maintenance team tests and services every HVAC unit before each new arrival to ensure it performs exactly as expected.",
        "It is gratifying to know that the temperature within your apartment was well-maintained throughout. We are fully aware of how significantly the climate impacts a guest's comfort and rest — particularly during Delhi NCR's extreme summers and winters — and we ensure every unit is inspected and set correctly before each check-in.",
    ],
    "noise": [
        "We are heartened to learn that you found the environment peaceful and restful. We recognise that a quiet, undisturbed atmosphere is especially vital for guests recovering from medical procedures or managing demanding corporate schedules, and our team actively ensures that noise levels remain controlled across the property.",
        "We are truly glad that the noise environment allowed you to rest and work without disturbance. A peaceful apartment is fundamental to the Lime Tree experience — whether our guest is recovering from a medical procedure, working on a demanding project, or simply in need of genuine rest after a long day — and we are pleased this was achieved throughout your stay.",
        "It is wonderful to know that the tranquillity of the property contributed positively to your experience. We take the acoustic environment of our apartments very seriously — working with building management to manage noise levels, and selecting properties in areas that minimise unnecessary external disturbance.",
    ],
    "security": [
        "We are very pleased that you felt safe and secure throughout your stay. At Lime Tree Hotels, security is treated as a foundational responsibility — not an afterthought. From controlled entry access and CCTV coverage to a dedicated on-site caretaker available round the clock, every measure is in place to ensure every guest feels completely protected.",
        "We are delighted to know that the security provisions at the property gave you a sense of complete safety throughout your stay. At Lime Tree, this is not optional — we maintain controlled entry systems, 24/7 CCTV monitoring, and a resident caretaker across all properties because every guest, regardless of the purpose of their visit, deserves to feel unconditionally secure.",
        "Thank you for noting the security standards at our property. The safety of every guest — solo travellers, families, medical companions — is a commitment we maintain through layered security protocols: access-controlled entry, round-the-clock on-site presence, and regular security reviews at each property. We are very glad it was evident and reassuring throughout your stay.",
    ],
    "breakfast": [
        "We are glad our breakfast and pantry service met your expectations. Providing quality meal options — particularly for guests who may not always be in a position to step out — is part of the full serviced apartment experience we commit to, and your appreciation means a great deal to our Food & Hospitality team.",
        "We are delighted to know that our breakfast and pantry provisions were to your satisfaction. For guests on extended stays or navigating busy schedules, the availability of good-quality, accessible food options within the property is a meaningful convenience — and one we invest in carefully at every Lime Tree property.",
        "It is very pleasing to receive your positive feedback on our food and pantry services. We work hard to ensure that our breakfast provisions and in-house food options are consistently fresh, adequate, and of good quality — because we understand that for many of our guests, stepping out for every meal is not always practical or desirable.",
    ],
    "checkin": [
        "We are delighted that your arrival experience set a positive tone for the stay. A warm, efficient, and personalised welcome is something we regard as the first and most important impression of Lime Tree Hotels, and our Front Office team works hard to ensure every guest is fully settled and informed within the first thirty minutes of arrival.",
        "It brings us great joy to know that the check-in process was smooth and welcoming. We believe the first impression of an accommodation is critical — and at Lime Tree Hotels, we are committed to ensuring every guest is greeted warmly, briefed thoroughly, and settled comfortably from the very moment of arrival.",
        "We are truly glad to know that your check-in experience reflected the standard we aspire to. Our commitment is simple: every guest should feel genuinely welcomed and completely oriented within the first half hour of arriving — not just handed a key. We are delighted the team delivered on this from the outset.",
    ],
    "housekeeping": [
        "We are heartened to know that our housekeeping standard held consistently throughout your stay. Daily upkeep — not just a one-time clean at check-in — is a non-negotiable commitment at every Lime Tree property, and your recognition of that sustained effort is very encouraging for our team.",
        "We are delighted to receive your positive feedback on our housekeeping services. Consistent daily cleaning and upkeep of every apartment is a commitment our Executive Housekeeper oversees personally — not just a one-time effort at check-in — and we are very glad it was maintained to your satisfaction throughout the full duration of your stay.",
        "It is truly gratifying to know that the daily housekeeping service throughout your visit met a high standard. At Lime Tree Hotels, we regard ongoing cleanliness as a live commitment — our team schedules and executes daily cleaning for every occupied apartment, and we are glad this was clearly reflected in your experience.",
    ],
    "water": [
        "We are pleased that the hot water supply and water pressure were consistent throughout your visit. Reliable water systems are something our Facilities team monitors and maintains proactively, and it is gratifying to know this contributed positively to your daily comfort.",
        "We are glad that the water supply — both the geyser performance and the pressure — met your expectations throughout the stay. Our Facilities team runs routine checks on water systems across all our properties, and we are pleased that this attention to infrastructure was reflected in an uninterrupted and comfortable experience for you.",
        "Thank you for noting the reliability of our water supply. We invest in and maintain the geyser, tank, and pressure systems at every property specifically to ensure that hot water and adequate pressure are never an afterthought — they are baseline comforts that every Lime Tree guest should be able to rely on throughout their stay.",
    ],
    "power": [
        "We are glad our 24/7 power backup system ensured an uninterrupted stay. Our inverter and generator infrastructure across all Gurgaon properties is maintained specifically to eliminate any disruption from the load shedding that is common across Delhi NCR — and we are pleased it performed exactly as intended.",
        "We are truly delighted that our power backup provisions meant your stay was never disrupted by electricity fluctuations. Maintaining reliable inverter and generator systems across all our properties is a specific investment we make because we understand how significantly a power cut impacts a guest — whether they are working, resting, or managing a medical situation.",
        "It is very gratifying to know that our backup power infrastructure delivered an uninterrupted experience throughout your visit. We are fully aware that load shedding is a reality across Gurgaon and the wider Delhi NCR region — and our commitment to 24/7 power continuity through maintained inverter and generator systems is a direct response to that.",
    ],
    "maintenance": [
        "It is pleasing to know that all facilities and fittings were in good working order throughout your stay. Our Maintenance team conducts pre-check-in inspections of every apartment — reviewing all appliances, plumbing, electrical fittings, and climate control — and your confirmation that this standard was met is very much appreciated.",
        "We are delighted to know that the apartment's facilities and fittings performed reliably throughout your stay. Our maintenance protocol requires a thorough pre-arrival inspection of every unit — covering all critical systems from plumbing and electrical fittings to appliances and climate control — and we are glad this preparation was evident in your experience.",
        "Thank you for noting that the apartment was well-maintained and fully functional. This is something our Maintenance team takes considerable pride in — every unit is checked systematically before each arrival, and issues are addressed immediately when reported during a stay. We are glad the standard held throughout your visit.",
    ],
}

# ── Negative variants — 3 per topic (Taj "sincerely regret" + Oberoi "note with concern" + Marriott/Hyatt action patterns) ─
_NEG_VARIANTS = {
    "kitchen": [
        "We note with deep concern your feedback regarding the kitchen facilities during your stay, and we sincerely regret the inconvenience caused. The matter has been escalated immediately to our Kitchen & Hospitality Manager, and the specific fault — whether in the induction stove, refrigerator, microwave, or utensil set — has been identified and resolved. We have implemented a mandatory pre-arrival appliance inspection to ensure no future guest encounters this. Our kitchen is a flagship feature of every Lime Tree serviced apartment, and a lapse of this nature is taken with complete seriousness.",
        "We are truly sorry to learn that the kitchen facilities fell short of the standard we commit to at Lime Tree Hotels. Please be assured that your feedback has been reviewed by our Kitchen & Hospitality Manager personally, the fault has been investigated and corrected, and a daily functionality check of all in-unit appliances has been added to our housekeeping protocol. This should not have been the experience of any guest, and we regret sincerely that it was yours.",
        "Your feedback regarding the kitchen facilities has been received with genuine concern, and we wish to assure you that it has not been taken lightly. We have reviewed the maintenance record of the specific unit, confirmed and resolved the fault, and put in place a structured pre-check-in and daily appliance checklist. At Lime Tree Hotels, the ability to cook independently is one of the core promises we make to every guest — when that promise is broken, we take immediate and direct action.",
    ],
    "cleanliness": [
        "We are genuinely concerned to note your feedback regarding cleanliness, and we wish to address it directly and without reservation. We have reviewed the housekeeping record for your stay, spoken individually with our Executive Housekeeper, and identified where the protocol was not followed. A corrective action plan has been implemented immediately — covering both the pre-check-in deep clean and the daily maintenance schedule. This is not reflective of the standard we set for ourselves, and we sincerely regret that it fell short during your visit.",
        "We are deeply sorry to learn that the cleanliness of your apartment did not meet the standard we hold ourselves to. Please be assured that your feedback has been shared directly with our Executive Housekeeper, the cleaning record for your unit has been reviewed in full, and corrective measures have been implemented with immediate effect. A spotless, consistently maintained apartment is a basic and non-negotiable promise at Lime Tree Hotels — we regret profoundly that this was not delivered during your stay.",
        "We note with deep concern your comments regarding the cleanliness of the apartment, and we wish to be completely direct in our response: this is unacceptable. We have reviewed the housekeeping schedule for your stay, spoken with the team responsible, and put in place a daily cleaning sign-off protocol for every occupied unit at the property. The specific gap you experienced has been identified and corrected. We sincerely regret the inconvenience and the impression it created of our standards.",
    ],
    "wifi": [
        "We note with concern your experience with internet connectivity during your stay, and we sincerely regret the disruption this caused. A reliable, high-speed connection is a non-negotiable facility at every Lime Tree property. We have had our Technical Services Manager conduct a full diagnostic and upgrade of the router configuration for the affected unit. A Wi-Fi speed verification has also been added to our pre-check-in checklist. Please be assured this will not recur.",
        "We are truly sorry to learn that the internet connectivity did not meet the standard we commit to. Your feedback has been shared with our Technical Services Manager, a full diagnostic has been conducted, the router and broadband configuration have been upgraded, and connectivity speed is now being tested before every new arrival. We understand how critical a reliable connection is — for work, for coordination during a medical stay, for staying connected with family — and we regret sincerely that this let you down.",
        "We are genuinely concerned by your feedback on Wi-Fi connectivity, and we wish to assure you that it has been treated as a technical failure requiring immediate correction — not a minor inconvenience to be logged. Our Technical Services team has reviewed, upgraded, and re-tested the internet infrastructure for the affected unit. We are sorry for the disruption and have taken the steps necessary to ensure no future guest encounters the same problem.",
    ],
    "staff": [
        "We are deeply concerned by the service experience you have described, and we wish to be direct: this falls below the standard we hold ourselves to at Lime Tree Hotels. We have shared your feedback with our Guest Relations Manager and addressed the matter directly with the team members involved. Our commitment is to meet every guest within 24 hours of check-in, anticipate their needs, and remain genuinely responsive throughout their stay — that clearly did not happen, and we sincerely regret it.",
        "We are genuinely sorry to learn of the service shortfall you experienced during your stay. Your feedback has been reviewed by our Guest Relations Manager and escalated directly to the property team involved. At Lime Tree Hotels, professional, warm, and responsive service is the foundation — not the finishing touch — of what we offer. When this standard is not met, we treat it as an accountability matter, not an isolated incident, and we have done exactly that here.",
        "The service experience you have described is one we take with complete and direct seriousness. We have reviewed the specific interactions you described, spoken individually with the team members involved, and put in place a structured retraining and accountability protocol at the property level. A guest who feels ignored, dismissed, or poorly served at a Lime Tree property has experienced a fundamental failure on our part — and we sincerely regret that this was your experience.",
    ],
    "location": [
        "We understand that the distance to your specific destination may not have met your expectations, and we appreciate you sharing this candidly. Our portfolio covers Gurgaon, Greater Noida, Delhi, and Noida — with properties near Medanta–The Medicity, Artemis Hospital, Fortis Memorial, Cyber City, Golf Course Road, and India Expo Mart. We encourage you to share your destination with our Reservations team at the time of enquiry so we can recommend the most convenient property and ensure this is not a concern on your next visit.",
        "We appreciate your candid feedback on the location and fully understand that distance to one's destination is a critical factor in choosing accommodation. We would like to highlight that our Guest Relations team is specifically available at the time of enquiry to map your destination to the most convenient property from our portfolio — whether your visit is to a hospital in Gurgaon, a corporate campus in Cyber City, or an exhibition venue in Greater Noida. We regret that this guidance was not provided proactively before your arrival.",
        "We are sorry to learn that the location did not serve your specific needs as well as you had hoped. Please be assured that our Reservations and Guest Relations team is always available before booking to recommend the most suitable property based on your destination — and we would actively encourage you to use this facility on any future visit. We have also noted your feedback as a prompt for us to improve the information we provide at the enquiry stage.",
    ],
    "price": [
        "We note your concern regarding value and wish to address it directly. Please be assured that our absolute best rates are available exclusively through direct booking at limetreehotels.com — OTA platforms add a 15–25% commission that is built into the displayed price. For long stays, the difference is substantial. We would be pleased to have our Guest Relations team prepare a customised rate for your next visit that represents a materially better proposition.",
        "We are sorry to learn that the stay did not feel like fair value for the experience you received. We would like to address this on two levels. First, our best rate guarantee means that direct bookings at limetreehotels.com will always be priced lower than any OTA, without platform surcharges. Second, and more importantly, value is only real if the stay quality matches the rate — and if this fell short, that is a service failure we take seriously and have addressed with the property team.",
        "We take seriously your feedback on pricing and value, and we wish to be transparent. Every Lime Tree long-stay rate is structured to be competitive, and we always recommend booking directly at limetreehotels.com or speaking with our Guest Relations team for customised monthly pricing. If the stay quality did not match the rate you paid, we regard that as a gap we are responsible for closing — and we have reviewed the property's service standard in light of your feedback.",
    ],
    "room": [
        "We are concerned to note your feedback regarding the room or apartment, and we sincerely regret that it did not meet your expectations. Your comments have been shared with our Property Manager, who has reviewed the specific unit and addressed the issue. Every Lime Tree serviced apartment is designed to deliver genuine space, quality furnishing, and a sense of home — and when this falls short, we treat it as a priority. Please be assured that the unit has been inspected, corrected, and added to our enhanced pre-check-in review protocol.",
        "We are genuinely sorry to learn that the apartment did not live up to the standard we commit to at Lime Tree Hotels. Your feedback has been reviewed by our Property Manager and the specific concerns about the room have been addressed directly. We regard every apartment as a home we are entrusting to our guest — the space, the furnishings, the lighting, the storage — and when any of these fall short, it is a failure we correct immediately and permanently.",
        "We are deeply concerned by your feedback on the quality and condition of the apartment, and we wish to assure you it has not been treated as a routine complaint. Our Property Manager has personally reviewed the unit, addressed the specific issue you described, and initiated a pre-check-in quality review that will apply to every future guest in that apartment. We sincerely regret the inconvenience and the gap between what you were promised and what you experienced.",
    ],
    "laundry": [
        "We sincerely regret the inconvenience caused by the in-room laundry facility during your stay. The issue has been identified by our Housekeeping Supervisor, the washing machine has been repaired and certified operational, and a functionality check has been added to our daily pre-check-in inspection. This should have been caught before your arrival and we take full responsibility for the oversight.",
        "We are very sorry to learn that the in-room washing machine was not functioning correctly during your stay. This is a facility we specifically maintain because we know how critical it is for guests on extended visits — and a failure here is one we take seriously. Our Housekeeping Supervisor has reviewed and resolved the issue, and washing machine performance is now part of our mandatory pre-arrival inspection checklist.",
        "Your feedback regarding the laundry facility has been shared with our Housekeeping Supervisor and the fault has been repaired and confirmed operational. We regret that this was not identified before your check-in — it is precisely the kind of lapse that our pre-arrival inspection should catch, and we have strengthened that protocol as a direct result of your feedback.",
    ],
    "parking": [
        "We regret the inconvenience caused by the parking arrangements during your stay and have noted it with complete seriousness. Our Facilities Manager has reviewed the parking allocation process at the property and implemented changes to ensure consistent availability for every arriving guest. Complimentary parking is a commitment we make at all our Gurgaon properties, and we are sorry it was not delivered as expected on this occasion.",
        "We are sorry to learn that our parking arrangements caused inconvenience during your visit. This is not the experience we want any guest to have — particularly those who have driven in from another city or are depending on a vehicle for daily hospital or office commutes. Our Facilities team has reviewed the allocation system and implemented changes to prevent this from recurring.",
        "We sincerely apologise for the parking inconvenience you experienced. Complimentary and accessible parking is a stated commitment at every Lime Tree property in Gurgaon, and we regret that this was not delivered seamlessly during your stay. Our Facilities Manager has reviewed the situation and put corrective measures in place. Please be assured that on your next visit, we will confirm parking availability as part of the check-in preparation.",
    ],
    "ac": [
        "We sincerely regret the discomfort caused by the air conditioning issue during your stay — particularly given Delhi NCR's extreme temperatures. Our Chief Maintenance Engineer has conducted a full service of the HVAC unit in the affected apartment, confirmed it fully operational, and added a mandatory 24-hour pre-check-in performance test to the property checklist. This was an unacceptable lapse and we have ensured it will not recur.",
        "We are deeply sorry that a malfunctioning air conditioner impacted the comfort of your stay. This is one of the most critical systems in any apartment — particularly during peak summer or winter months in Delhi NCR — and a failure here is one we take with the highest urgency. Our Chief Maintenance Engineer has fully serviced the unit, confirmed its operation, and introduced a pre-arrival HVAC performance test across the property. Please be assured of our commitment to ensuring this standard is maintained.",
        "Your feedback regarding the air conditioning has been received with genuine concern. A comfortable, properly temperature-controlled environment is fundamental to a good night's rest and a productive day — and when this fails, it affects the entire stay experience. Our maintenance team has serviced and tested the unit in question, and we have introduced a pre-check-in climate system inspection. We sincerely regret the inconvenience.",
    ],
    "noise": [
        "We are sincerely sorry that noise disturbance affected the quality of your stay, and we have taken this concern to our Property Manager and Building Superintendent immediately. We have committed to specific remedial steps — including scheduling enforcement and noise-hour management at the building level — and are following up to ensure implementation. Our guests deserve an undisturbed environment, and we regret deeply that this was not the case.",
        "We note with genuine concern your feedback about noise disturbance during your stay. A quiet, restful environment is something every Lime Tree guest has a right to — whether they are recovering from a medical procedure, working through a high-pressure assignment, or simply in need of proper rest. We have escalated this to our Property Manager and Building Superintendent, committed to specific structural remediation steps, and will personally follow up on their implementation.",
        "We are very sorry to learn that noise levels interfered with your comfort and rest. This feedback has been shared with our Property Manager and the building management, and specific measures — including noise scheduling enforcement and structural assessments — have been initiated. We recognise that this type of disturbance is one of the most difficult to remedy quickly, but we are committed to addressing it at the root level rather than with a temporary fix.",
    ],
    "maintenance": [
        "We note with deep concern that a maintenance issue remained unresolved during your stay, and we sincerely regret the inconvenience this caused. Your feedback has been shared with our Maintenance Supervisor, the specific fault has been identified and repaired, and a comprehensive pre-check-in inspection protocol — covering all critical systems including plumbing, electrical fittings, geyser, flush, and climate control — has been implemented immediately.",
        "We are genuinely sorry to learn that a maintenance issue disrupted your stay and was not resolved promptly. This is a failure at the operational level that we take very seriously. Our Maintenance Supervisor has reviewed the log for your unit, corrected the specific fault, and we have put in place a daily systems check for all occupied apartments so that issues are identified and addressed proactively rather than after a guest has already been inconvenienced.",
        "Your feedback about the maintenance issue has been reviewed by our Maintenance Supervisor and the property management team. The fault has been identified, repaired, and confirmed operational. More importantly, we have reviewed our response protocol — because the issue you faced should have been resolved before it required you to raise a concern at all. We have put in place a preventive daily inspection and a faster response escalation process. We sincerely regret the disruption.",
    ],
    "security": [
        "We are deeply concerned by the security-related feedback you have shared, and we wish to assure you that it has been elevated to our Head of Security and the Property Manager immediately. A full review of entry access control, CCTV coverage, and caretaker protocols has been conducted, and corrective action has been taken. Every guest has an unconditional right to feel completely safe — this is non-negotiable, and we regret that your experience fell short of that standard.",
        "We take the security concern you have raised with the highest seriousness and wish to address it directly. The matter has been escalated to our Head of Security, who has conducted a thorough review of the access control system, CCTV coverage, and on-site caretaker protocols at the property. Corrective measures have been implemented immediately. Please be assured that safety is a foundational commitment at Lime Tree Hotels — never a secondary consideration.",
        "Your security-related feedback has been treated as a matter of the highest priority at our management level. Our Head of Security has reviewed the specific concern you raised, conducted a property-level audit of all security systems and protocols, and implemented corrective action. We sincerely regret any sense of unease you experienced — and we want to assure you that the measures now in place reflect how seriously we regard every guest's safety.",
    ],
    "breakfast": [
        "We regret to learn that our breakfast and pantry service did not meet your expectations. Your feedback has been shared with our Food & Hospitality Manager and the vendor responsible for supply. A quality review of our provisions — covering freshness, adequacy, and variety — has been initiated immediately and improvements will be in place for every guest going forward.",
        "We are genuinely sorry that our breakfast and food provisions fell short during your stay. This is a part of the serviced apartment experience we take seriously — particularly for guests who depend on in-property meal options due to medical schedules or demanding work days. We have reviewed the feedback with our Food & Hospitality Manager and implemented changes to quality, replenishment timing, and variety with immediate effect.",
        "Your feedback on the breakfast and pantry service has been taken seriously by our Food & Hospitality team, and we sincerely regret that it did not meet your expectations. We have reviewed the provisions, the vendor supply chain, and the replenishment protocol — and specific changes have been implemented as a direct result of your comments. We are committed to ensuring that guests on their next visit find a material improvement.",
    ],
    "checkin": [
        "We are concerned to note that the check-in experience did not reflect the standard we set at Lime Tree Hotels, and we sincerely regret the impression this created. Your feedback has been shared with our Front Office Manager and the team on duty at the time of your arrival. A seamless, warm welcome within thirty minutes of arrival is a commitment we make to every guest — we failed to deliver on it in your case and have addressed this directly.",
        "We are genuinely sorry that the check-in process did not create the right first impression. A poorly handled arrival — whether due to a delay, a lack of preparedness, or a failure of warmth — sets the wrong tone for everything that follows, and we regard it as a serious operational lapse. We have reviewed the check-in record with our Front Office Manager, identified the specific failure, and put in place corrective protocols that apply to every future arrival at this property.",
        "Your feedback regarding the check-in experience has been shared with our Front Office Manager and we regret the impression it created. The arrival experience is the first and most important moment in any guest's stay — and when it is delayed, cold, or poorly executed, it reflects a failure that we are accountable for. We have identified what went wrong, spoken directly with the team on duty, and implemented a structured welcome protocol to ensure no future guest faces the same experience.",
    ],
    "housekeeping": [
        "We note with genuine concern that housekeeping standards were inconsistent during your stay, and we sincerely regret the inconvenience this caused. We have reviewed the cleaning schedule with our Executive Housekeeper, identified the gaps in execution, and implemented a daily sign-off protocol for every occupied unit at the property. Daily upkeep is a firm commitment at every Lime Tree serviced apartment — and this has been reinforced immediately.",
        "We are truly sorry that the housekeeping standard did not hold consistently throughout your stay. Daily cleaning and upkeep of every occupied apartment is a non-negotiable commitment at Lime Tree Hotels — and a lapse here impacts not just one day but the entire experience of a guest on an extended stay. We have reviewed the schedule with our Executive Housekeeper, identified where execution fell short, and implemented a mandatory daily sign-off to ensure consistent delivery going forward.",
        "Your feedback on housekeeping has been reviewed by our Executive Housekeeper and taken very seriously. At Lime Tree, daily cleaning is not an optional add-on — it is part of the core commitment we make to every guest staying with us. The specific gaps you experienced have been identified, the team has been briefed, and a daily accountability protocol has been introduced. We sincerely regret the disruption to your comfort.",
    ],
    "water": [
        "We sincerely regret the disruption caused by water supply issues during your stay. Our Facilities Engineer has reviewed the geyser, tank levels, and pressure systems for the affected unit and confirmed all have been serviced and corrected. A water system performance check has been added to our daily property review. Please be assured this has been treated with the urgency it deserves.",
        "We are very sorry to learn that water supply or pressure issues affected the comfort of your stay. This is a basic and non-negotiable facility — and when it fails, it disrupts the most fundamental aspects of a guest's daily routine. Our Facilities team has inspected and corrected the geyser, tank, and pressure system for your unit, and has added a daily water systems check to the property's maintenance protocol.",
        "Your feedback about water supply has been escalated to our Facilities and Engineering team and treated as a priority. The geyser, tank level, and pressure system have been inspected, serviced, and confirmed operational. We have also introduced a proactive daily check on water systems at the property to ensure no future guest faces this inconvenience. We sincerely regret the disruption it caused.",
    ],
    "power": [
        "We are genuinely sorry that power backup failed to perform as expected during your stay. We maintain inverter and generator systems specifically to ensure uninterrupted supply for all our guests — a failure in this system is unacceptable. Our Electrical and Maintenance Supervisor has conducted a full inspection and load test of the backup infrastructure and the fault has been resolved. This standard will be maintained going forward without exception.",
        "We are deeply sorry that a failure in our power backup system disrupted your stay. This is one of the specific provisions we invest in and maintain for all our Gurgaon properties — precisely because load shedding across Delhi NCR is a known and recurring reality. A failure here is treated as a critical infrastructure lapse, not a minor inconvenience. Our Electrical and Maintenance team has inspected, repaired, and load-tested the backup systems at the property, and the issue has been resolved.",
        "Your feedback on power backup has been reviewed by our Electrical and Maintenance Supervisor and the matter has been taken with full seriousness. Our inverter and generator systems are maintained to provide complete continuity — when this fails, it reflects a maintenance gap we are accountable for. The system has been fully inspected and restored, and we have introduced periodic load-testing to ensure reliability. We sincerely regret the inconvenience this caused.",
    ],
}

# ── Negative segments — Oberoi "we note with concern" + Taj "immediate action" style ─
_NEG_SEGMENT = {
    "kitchen":
        "We note with deep concern your feedback regarding the kitchen facilities during your stay. Please be assured that this has been escalated immediately to our Kitchen & Hospitality team and the specific fault — whether in the induction stove, refrigerator, microwave, or utensil set — has been identified and resolved. Our kitchen is a flagship feature of every Lime Tree serviced apartment, designed to give every guest the independence of home cooking. We have implemented a mandatory daily appliance inspection to ensure no future guest encounters this. We sincerely regret the inconvenience caused.",

    "cleanliness":
        "We are genuinely concerned to note your feedback regarding cleanliness, and we wish to address it directly and without reservation. We have reviewed the housekeeping record for your stay, spoken individually with our Housekeeping Manager, and identified where the protocol was not followed. A corrective action plan has been put in place immediately — covering both the pre-check-in deep clean and the daily maintenance schedule. This is not reflective of the standard we set for ourselves, and we sincerely regret that it fell short during your visit.",

    "wifi":
        "We note with concern your experience with internet connectivity during your stay, and we sincerely regret the disruption this caused. A reliable, high-speed connection is a non-negotiable facility at every Lime Tree property — whether our guest is a corporate professional working remotely, a medical companion coordinating with specialists, or a student on a long stay. We have had our Technical Services team conduct a full diagnostic and upgrade of the router configuration for the affected unit. A Wi-Fi speed verification has also been added to our pre-check-in checklist.",

    "staff":
        "We are deeply concerned by the service experience you have described, and we wish to be direct: this falls below the standard we hold ourselves to at Lime Tree Hotels. We have shared your feedback with our Guest Relations Manager and addressed the matter directly with the team members involved. At Lime Tree, our commitment is to meet every guest within 24 hours of check-in, anticipate their needs, and remain genuinely responsive throughout the stay — that clearly did not happen in your case, and we sincerely regret it. Please be assured that this has been treated as a training and accountability matter at the property level.",

    "location":
        "We understand that the proximity to your specific destination may not have been as expected, and we appreciate you sharing this. We would like to note that our portfolio spans Gurgaon, Greater Noida, Delhi, and Noida — with properties deliberately positioned near Medanta–The Medicity, Artemis Hospital, Fortis Memorial, Cyber City, Golf Course Road, and India Expo Mart. We encourage you to share your destination with our Reservations team at the time of enquiry so we can recommend the most convenient property from our portfolio — one that we are confident will serve you better on your next visit.",

    "price":
        "We note your concern regarding value, and we would like to address it directly. Please be assured that our absolute best rates are available exclusively through direct booking at limetreehotels.com — OTA platforms such as Booking.com, MakeMyTrip, and Goibibo add a 15–25% commission that is inevitably built into the displayed price. For long stays of 7, 14, or 30+ nights, this difference is very significant. We would be pleased to have our Guest Relations team prepare a customised rate for your next visit that we are confident would represent a materially better proposition.",

    "room":
        "We are concerned to note your feedback regarding the room or apartment, and we sincerely regret that it did not meet your expectations. Your comments have been shared with our Property Manager, who has reviewed the specific unit and addressed the issue noted. Every Lime Tree serviced apartment is designed to deliver genuine space, quality furnishing, and a sense of home — and when this falls short, we treat it as a priority, not a footnote. Please be assured that the unit has been inspected and corrected, and a pre-check-in review protocol is now in place for every future guest.",

    "laundry":
        "We sincerely regret the inconvenience caused by the in-room laundry facility during your stay. The issue has been identified by our Housekeeping Supervisor, the washing machine has been repaired and certified operational, and a functionality check has been added to our daily pre-check-in inspection. This should have been caught before your arrival — please be assured that it has been treated as a systems failure, not a minor oversight.",

    "parking":
        "We regret the inconvenience caused by the parking arrangements during your stay and we have noted it with full seriousness. Our Facilities team has reviewed the parking allocation process at the property and implemented changes to ensure consistent availability for every arriving guest. Complimentary parking is a commitment we make at all our Gurgaon properties, and we are sorry it was not delivered as promised on this occasion.",

    "ac":
        "We sincerely regret the discomfort caused by the air conditioning issue during your stay — particularly given Delhi NCR's extreme temperatures. Please be assured that our Maintenance Engineer has conducted a full service of the HVAC unit in the affected apartment, confirmed it fully operational, and added a mandatory 24-hour pre-check-in performance test to the property checklist. This was an unacceptable lapse, and we have ensured it will not recur.",

    "noise":
        "We are sincerely sorry to note that noise disturbance affected the quality of your stay, and we have taken this concern to our Property Manager and Building Management immediately. We have committed to specific remedial steps — including scheduling and noise-hour enforcement at the building level — and are following up directly to ensure implementation. Our guests — whether recovering from a procedure, working on a corporate deadline, or resting after a long journey — deserve an undisturbed environment, and we regret that we did not deliver this.",

    "maintenance":
        "We note with deep concern that a maintenance issue remained unresolved during your stay, and we sincerely regret the inconvenience this caused. Your feedback has been shared with our Maintenance Supervisor, the specific fault has been identified and repaired, and a comprehensive pre-check-in inspection protocol covering all critical systems — plumbing, electrical fittings, geyser, flush, and climate control — has been put in place. Please be assured this has been treated as a systems failure requiring immediate corrective action, not a one-time exception.",

    "security":
        "We are deeply concerned by the security-related feedback you have shared, and we want to assure you that it has been elevated to our Security Manager and the Property Manager immediately. A review of entry access control, CCTV coverage, and caretaker protocols has been conducted at the property, and corrective action has been taken. Every guest at a Lime Tree Hotel has an unconditional right to feel completely safe — this is non-negotiable, and we regret that your experience fell short of that standard.",

    "breakfast":
        "We regret to learn that our breakfast and pantry service did not meet your expectations, and we have shared your specific feedback with our Food & Hospitality team and the vendor responsible for supply. A review of quality benchmarks and replenishment frequency has been initiated immediately. Please be assured that this aspect of the serviced apartment experience is one we take seriously, and we are implementing improvements that will be in place for every guest going forward.",

    "checkin":
        "We are concerned to note that the check-in experience did not reflect the standard we set at Lime Tree Hotels, and we sincerely regret the impression this created. Your feedback has been shared with our Front Office Manager and the team on duty at the time of your arrival — the specific lapse has been identified and addressed directly. A seamless, warm, and well-prepared welcome within thirty minutes of arrival is a commitment we make to every guest, and we failed to deliver on it in your case. Please be assured this has been corrected.",

    "housekeeping":
        "We note with genuine concern that housekeeping standards were inconsistent during your stay, and we sincerely regret the inconvenience this caused. We have reviewed the cleaning schedule with our Housekeeping Manager, identified the gaps in execution, and implemented a daily sign-off protocol for every occupied unit at the property. Daily upkeep — not just a check-in clean — is a firm commitment at every Lime Tree serviced apartment, and this has been reinforced across the team.",

    "water":
        "We sincerely regret the disruption caused by water supply or pressure issues during your stay. Our Facilities Engineer has reviewed the geyser, tank levels, and pressure system for the affected unit and confirmed all have been serviced and corrected. A water system performance check has also been added to our daily property review. Please be assured this has been treated with the urgency it deserves.",

    "power":
        "We are genuinely sorry that power backup failed to perform as expected during your stay. We maintain inverter and generator systems specifically to ensure uninterrupted supply for all our guests, and a failure in this system is unacceptable. Our Electrical & Maintenance team has conducted a full inspection and load test of the backup infrastructure at the property, and the fault has been resolved. This standard will be maintained going forward without exception.",
}

# ── Context variants — 2 per type (ITC/Leela/Taj/Marriott/Fairmont patterns) ─
_CONTEXT_VARIANTS = {
    "Medical Stay": [
        "We recognise that a stay near a hospital — whether as a patient facing a medical procedure or as a family member providing care and support — carries a weight that goes far beyond accommodation. Our serviced apartments near Medanta–The Medicity in Sector 38, Artemis Hospital in Sector 51, and Fortis Memorial Research Institute are specifically configured for this purpose: a fully equipped kitchen for dietary requirements, in-room laundry for independence, 24/7 on-site caretaker access, and a dedicated check-in briefing within 24 hours of arrival. Please be assured that on any future medical visit to Gurgaon, we are fully committed to making every aspect of your stay seamless.",
        "We are deeply conscious of the unique demands that a medical stay places on every guest — the anxiety, the irregular schedules, the need for dietary control and complete practical independence. Our apartments near Medanta, Artemis, and Fortis are maintained specifically for this purpose. On behalf of the entire Lime Tree team, we are honoured to have been your base during what we recognise was a significant time, and we are fully committed to ensuring that every future medical visit to Gurgaon is supported with complete professionalism and care.",
    ],
    "Corporate Stay": [
        "We are fully aware that for corporate guests on assignments, projects, or short-term postings in Gurgaon's business corridors — Cyber City, Golf Course Road, DLF Phase 5, IFFCO Chowk — accommodation must perform reliably and without friction. There is no margin for disruption when managing professional commitments. Your feedback has been reviewed in this context and the relevant corrective steps have been taken. We look forward to supporting your team's future stays in Gurgaon with the consistency that a corporate housing arrangement demands.",
        "We understand that for a corporate guest, accommodation is not a comfort choice — it is a professional infrastructure decision. The apartment must work flawlessly, the connectivity must be reliable, the team must be responsive, and the environment must be conducive to productive work and genuine rest. When any of these elements fail, it is not just an inconvenience — it is a disruption to a professional schedule. We take that context very seriously and have addressed your feedback accordingly.",
    ],
    "Family Stay": [
        "We understand that a family stay — particularly in a demanding city like Gurgaon — requires a living environment where every member, from the youngest to the most senior, feels genuinely comfortable and secure. Our 2BHK and 3BHK serviced apartments are designed with precisely this in mind: multiple private rooms, a fully equipped shared kitchen, and the space for a family to settle in properly rather than feel confined. We have taken your feedback very seriously and look forward to welcoming your family again.",
        "We are conscious that a family stay creates its own distinct set of needs — space for children to be at ease, a kitchen to manage different schedules and dietary requirements, and an environment where every family member feels safe and at home. At Lime Tree Hotels, our larger configurations are designed with exactly this in mind. We have reviewed your feedback in that context and taken the necessary corrective steps. We genuinely look forward to the opportunity to deliver a stay that your entire family remembers warmly.",
    ],
    "Long Stay / Monthly": [
        "We are acutely aware that for guests on weekly or monthly stays, every detail compounds in significance. What might be a minor inconvenience on a one-night hotel visit becomes a sustained disruption over two or four weeks. It is precisely for this reason that we hold our long-stay furnished apartments in Gurgaon to a higher standard of pre-arrival preparation and ongoing upkeep — and why your feedback has triggered an immediate internal review rather than a standard response.",
        "For guests who choose a Lime Tree serviced apartment for a month or more, the relationship is different — closer to a home than a hotel. The expectation is not just cleanliness and functionality at check-in, but sustained quality throughout the entire duration. We are fully aware of this higher standard and regret sincerely that it was not met consistently during your stay. Your feedback has prompted an immediate review of ongoing maintenance protocols, not just a one-time correction.",
    ],
    "Exhibition / Business": [
        "We fully appreciate that visitors attending exhibitions at India Expo Mart or corporate events across Delhi NCR operate on schedules where every hour is accounted for. Accommodation must function as a quiet, efficient base — never a source of additional complexity. We regret that your stay did not fully reflect this, and we have taken direct remedial steps to ensure that future business visitors experience the seamless support they require.",
        "Business visitors attending exhibitions or corporate events have very specific needs from their accommodation: proximity, reliability, connectivity, and a team that is responsive and proactive. We understand that your time here is professional and purposeful — and that any lapse in the accommodation experience has a real impact on your ability to perform. We have reviewed your feedback in this context and taken corrective action accordingly.",
    ],
    "Relocation / New Joiner": [
        "We understand that relocating to a new city — particularly at the start of a new professional chapter — is a significant transition that demands a stable, comfortable, and fully functional base from day one. Our serviced apartments for relocation and new joiners are designed to remove as much friction as possible from that process. We have noted your feedback and taken it seriously, and we look forward to ensuring your continued stay in Gurgaon reflects the standard we are committed to.",
        "Relocating is one of the most personally demanding transitions a professional can make — a new city, a new role, and the need to find one's footing while managing the unfamiliar. Our role during that period is to be an uncomplicated, reliable home base. When that falls short, we are adding to a burden that is already significant — and we regret sincerely that this was the case. We have acted on your feedback with that context firmly in mind.",
    ],
    "Solo Women Traveler": [
        "We regard the safety, comfort, and dignity of every solo woman traveler as an unconditional commitment. At Lime Tree Hotels, this means controlled entry access, round-the-clock caretaker presence, lower-floor room allocation on request, and a dedicated lady executive contact at the property. We have reviewed the specific concern you raised, strengthened our protocols at the property level, and will ensure these provisions are fully in effect on any future visit.",
        "The safety and comfort of solo women travelers is a responsibility we hold to without compromise. Every Lime Tree property maintains controlled entry systems, 24/7 on-site support, and lady-specific service provisions — because we understand that traveling alone demands an environment that is not just functional but genuinely secure and respectful. We have reviewed your feedback at the management level and taken the specific steps necessary to strengthen these provisions.",
    ],
}

# ── Closing variants — 2 per star rating (Taj/Oberoi/Fairmont/Marriott patterns) ─
_CLOSING_VARIANTS = {
    5: [
        "We very much look forward to welcoming you back to Lime Tree Hotels & Service Apartments. Whenever your next visit to Gurgaon brings you here — whether near Medanta Hospital, Artemis Hospital, Golf Course Road, Cyber City, or any of our locations across Delhi, Noida, Greater Noida, Vrindavan, and Goa — please book directly at limetreehotels.com for our guaranteed best rate, with the full assurance of our personal attention.",
        "It has been our genuine privilege to host you, and we look forward with great enthusiasm to welcoming you back. On behalf of the entire Lime Tree team across Gurgaon, Delhi, Noida, Greater Noida, Vrindavan, and Goa — thank you sincerely for your patronage and for the time you took to share this review. Please always book directly at limetreehotels.com or call +91 74 7900 0111 for our best rate and guaranteed personal service.",
    ],
    4: [
        "We very much hope to have the pleasure of welcoming you back to Lime Tree Hotels & Service Apartments and earning the full five stars we aim to deserve. Please book directly at limetreehotels.com or call us at +91 74 7900 0111 — you will always receive our best available rate, no OTA markup, and a team that is fully prepared for your arrival.",
        "We are grateful for your patronage and genuinely hope to welcome you back on a future visit. We are committed to addressing the small areas where we fell short this time, and we are confident your next stay will reflect the full standard Lime Tree Hotels & Service Apartments is built to deliver. Please book directly at limetreehotels.com for our best guaranteed rate.",
    ],
    3: [
        "We sincerely hope that the steps we have taken give you reason to consider Lime Tree Hotels & Service Apartments once more. When you do, please book directly at limetreehotels.com so that our Guest Relations team can ensure every detail of your stay is prepared and confirmed to your satisfaction before arrival.",
        "We hope to have the opportunity to restore your confidence in Lime Tree Hotels & Service Apartments with a future visit that reflects our true standard. Please reach us directly at +91 74 7900 0111 or reservation@limetreehotels.com — our Guest Relations team will personally ensure your next stay is prepared to the last detail.",
    ],
    2: [
        "We take full ownership of everything that fell short during your stay. The corrective actions described above have been implemented as a team — not noted and filed. We genuinely hope to have the opportunity to demonstrate what Lime Tree Hotels & Service Apartments is truly capable of delivering.",
        "We want to be direct: the experience you had is not who we are, and it is not what we stand for. We have acted on every concern you raised, and we would be honoured to have the opportunity to show you that on a future visit. Please contact our Guest Relations team directly at +91 74 7900 0111 before your next visit — we will personally oversee every detail.",
    ],
    1: [
        "We wish to assure you that this matter has been addressed with complete seriousness at the leadership level of Lime Tree Hotels — not passed to a department, not acknowledged and shelved. If you are ever willing to give us another opportunity, we will ensure every aspect of your stay is personally overseen from arrival to departure.",
        "We have addressed every concern you raised as a management team — with accountability, not deflection. We understand that trust, once lost, must be earned back through action — not words alone. If you are ever willing to give us another chance, please contact us directly at reservation@limetreehotels.com. We will ensure your next experience is one we are proud of.",
    ],
}


def _detect_context(text: str) -> dict:
    t = text.lower()
    out = {}
    # Hospital detection
    if "medanta" in t:                                   out["hospital"] = "Medanta–The Medicity, Sector 38"
    elif "artemis" in t:                                 out["hospital"] = "Artemis Hospital, Sector 51"
    elif "fortis" in t:                                  out["hospital"] = "Fortis Memorial Research Institute"
    elif "max hospital" in t or "max super" in t:        out["hospital"] = "Max Super Speciality Hospital"
    elif "paras hospital" in t:                          out["hospital"] = "Paras Hospitals"
    elif "columbia asia" in t:                           out["hospital"] = "Columbia Asia Hospital"
    elif "hospital" in t or "patient" in t:              out["hospital"] = "the hospital"
    # Business area detection
    if "cyber city" in t or "cybercity" in t:            out["area"] = "Cyber City"
    elif "golf course" in t:                             out["area"] = "Golf Course Road"
    elif "dlf phase" in t or "dlf city" in t:           out["area"] = "DLF City"
    elif "dlf" in t:                                     out["area"] = "DLF corridor"
    elif "iffco" in t:                                   out["area"] = "IFFCO Chowk"
    elif "huda" in t:                                    out["area"] = "HUDA City Centre"
    elif "expo mart" in t or "exhibition" in t:          out["area"] = "India Expo Mart, Greater Noida"
    elif "sohna road" in t:                              out["area"] = "Sohna Road"
    elif "mg road" in t:                                 out["area"] = "MG Road"
    elif "sector 14" in t:                               out["area"] = "Sector 14"
    # Guest type detection
    medical_kws   = ["patient","surgery","treatment","procedure","operation","recovery","chemotherapy",
                     "dialysis","doctor","oncology","radiation","transplant","medical","icu","ward",
                     "attendant","caregiver","post surgery","post-surgery","discharge","admitted"]
    corporate_kws = ["project","office","client","corporate","business trip","assignment","deployment",
                     "work from","on deputation","company","posted","deputed","offsite","training"]
    family_kws    = ["family","kids","children","son","daughter","spouse","parents","wife","husband",
                     "grandmother","grandfather","in-laws","toddler","baby","infant","grandparents"]
    longstay_kws  = ["month","monthly","weeks","long stay","extended stay","relocated","relocation",
                     "new joiner","joined","new job","internship","semester","pg","paying guest"]
    solo_kws      = ["alone","solo","woman alone","travelling alone","single lady","by myself",
                     "single woman","independent traveler","woman traveler"]
    if any(w in t for w in medical_kws):     out["guest_type"] = "medical"
    elif any(w in t for w in corporate_kws): out["guest_type"] = "corporate"
    elif any(w in t for w in family_kws):    out["guest_type"] = "family"
    elif any(w in t for w in longstay_kws):  out["guest_type"] = "long_stay"
    elif any(w in t for w in solo_kws):      out["guest_type"] = "solo_women"
    return out


def analyze_review(text: str) -> dict:
    t = text.lower()
    found = []
    for key, (kws, label) in _TOPICS.items():
        if any(k in t for k in kws):
            found.append({"key": key, "label": label})
    # Weighted sentiment — stronger negative words count more
    strong_neg = ["terrible","horrible","awful","disgusting","pathetic","worst","never again","unacceptable","disgrace"]
    neg = sum(2 if w in t else 0 for w in strong_neg) + sum(1 for w in _NEG_WORDS if w in t)
    pos = sum(1 for w in _POS_WORDS if w in t)
    if neg >= 6:     intensity = "very_negative"
    elif neg >= 3:   intensity = "negative"
    elif pos >= 6:   intensity = "very_positive"
    elif pos >= 3:   intensity = "positive"
    else:            intensity = "mixed"
    overall = "positive" if pos > neg else "negative" if neg > pos else "mixed"
    return {
        "topics": found, "sentiment": overall, "intensity": intensity,
        "pos": pos, "neg": neg, "specifics": _detect_context(text),
    }


def generate_chatbot_reply(review_text: str, stars: int, guest_name: str, context: str, analysis: dict) -> tuple:
    name      = f"Dear {guest_name.strip()}" if guest_name.strip() else "Dear Guest"
    topics    = analysis["topics"]
    sent      = analysis["sentiment"]
    intensity = analysis.get("intensity", "mixed")
    specs     = analysis.get("specifics", {})
    use_neg   = (stars <= 3 or sent == "negative")
    seed      = review_text  # used for deterministic variant selection

    # ── Auto-detect context ───────────────────────────────────────────────────
    if context == "General":
        gt = specs.get("guest_type", "")
        if gt == "medical":      context = "Medical Stay"
        elif gt == "corporate":  context = "Corporate Stay"
        elif gt == "family":     context = "Family Stay"
        elif gt == "long_stay":  context = "Long Stay / Monthly"
        elif gt == "solo_women": context = "Solo Women Traveler"

    # ── Personalised opening — 3 variants per star rating ────────────────────
    hospital_note = (f", and we are honoured to have been your base during your visit to "
                     f"{specs['hospital']}") if specs.get("hospital") else ""
    area_note     = f" in {specs['area']}" if specs.get("area") else " in Gurgaon"

    opener_sets = {
        5: [
            f"{name},\n\nThank you so much for staying with us{area_note}{hospital_note} and for taking the time to write such a lovely review. It genuinely made our day.",
            f"{name},\n\nThis is exactly the kind of feedback our team lives for — thank you{hospital_note}! We're so glad the stay{area_note} lived up to what you needed.",
            f"{name},\n\nWe loved reading this. Thank you for the kind words and for choosing to stay with us{area_note}{hospital_note} — it really does mean a lot to the whole team.",
        ],
        4: [
            f"{name},\n\nThank you for staying with us{area_note} and for taking the time to write this. We're really glad most of it went well.",
            f"{name},\n\nThanks so much for the honest feedback{hospital_note} — we're glad the stay was a good one overall, and we've taken note of what you mentioned.",
            f"{name},\n\nWe appreciate you sharing this. It's good to hear the stay{area_note} was largely positive, and your feedback — the good and the constructive — genuinely helps us.",
        ],
        3: [
            f"{name},\n\nThank you for the honest feedback on your stay. We'd rather respond properly to what you actually experienced than send a generic thank-you, so here goes.",
            f"{name},\n\nWe appreciate you taking the time to write this — it's useful to us, and we want to address what you raised directly rather than brush past it.",
            f"{name},\n\nThanks for sharing this. We've read it carefully and want to respond to the specific points, not just acknowledge them.",
        ],
        2: [
            f"{name},\n\nWe're sorry to hear this — a stay{area_note}{hospital_note} shouldn't leave you feeling this way, and we want to address what went wrong directly.",
            f"{name},\n\nThank you for being upfront about this. We've looked into what you've described{hospital_note} and want to respond properly, not just with an apology.",
            f"{name},\n\nWe're genuinely sorry your stay didn't go the way it should have{hospital_note}. We've reviewed this with the team and want to be specific about what we're doing about it.",
        ],
        1: [
            f"{name},\n\nWe're sorry — this is not the stay we want anyone to have{hospital_note}, and we take it seriously. Here's what we've looked into and what we're doing about it.",
            f"{name},\n\nThis one's on us. We've read this at the management level{hospital_note}, and rather than a standard apology, we want to be straightforward about what went wrong.",
            f"{name},\n\nWe're genuinely sorry to read this{hospital_note}. We don't want to just apologise and move on — we've looked into it and want to tell you what we found and what's changing.",
        ],
    }
    opening = _pick(opener_sets.get(stars, opener_sets[3]), seed)

    # ── Single best-match body paragraph (1 only, to stay within word limit) ─
    body_parts = []
    dept_used  = []
    for t_info in topics[:1]:                        # pick the top detected topic only
        key    = t_info["key"]
        dept   = _DEPT.get(key, "our team")
        v_dict = _NEG_VARIANTS if use_neg else _POS_VARIANTS
        v_list = v_dict.get(key, [])
        if v_list:
            body_parts.append(_pick(v_list, seed + key))
            dept_used.append(dept)

    # ── Fallback when no topic detected ──────────────────────────────────────
    if not body_parts:
        fallbacks_pos = [
            "We invest continually in ensuring every Lime Tree serviced apartment delivers the full experience of a well-run home — a fully equipped kitchen, in-room laundry, high-speed internet, and 24/7 caretaker availability. Knowing a guest truly experienced this standard is the confirmation we work toward every day.",
            "It is gratifying to know that your stay reflected the standard we aspire to deliver. We pride ourselves on a genuine home-away-from-home experience, and every piece of positive feedback is a direct validation of that commitment.",
            "We are delighted your stay was a positive one. The Lime Tree experience — a fully functional apartment, a responsive team, and a well-located property — is one we work hard to sustain, and it is very rewarding to know it came through clearly.",
        ]
        fallbacks_neg = [
            "We have reviewed the details of your stay at the management level. Your concerns have been acted upon immediately and directly — not noted for later, not passed to a third party. Please be assured we treat every piece of guest feedback as a direct instruction to improve.",
            "We take full responsibility for the shortfalls you experienced. Your feedback has been reviewed at the management level and acted upon — not acknowledged and filed. Every guest deserves a seamless, comfortable experience, and we are committed to ensuring that standard without exception.",
            "Your feedback has prompted a direct review of the relevant operational protocols at the property level. The concerns you raised have been addressed specifically and immediately — we are committed to ensuring this experience is never repeated.",
        ]
        body_parts.append(_pick(fallbacks_pos if stars >= 4 else fallbacks_neg, seed))

    # ── Closing ───────────────────────────────────────────────────────────────
    closing_list = _CLOSING_VARIANTS.get(stars, _CLOSING_VARIANTS[3])
    closing      = _pick(closing_list, seed + "closing")

    # No formal signature block — Google already attributes this as "Response from the
    # Owner", so a letterhead with brand name, city list and phone/email reads as an ad,
    # not a reply from a person.
    signature = ""

    # ── Assemble within 100-150 word limit, then sanitize apology language ───
    full_reply = _sanitize(_cap_reply(opening, body_parts, closing, signature, max_words=125))

    reply_lower = full_reply.lower()
    kws_used    = [kw for kw, *_ in TOP_KEYWORDS if any(w in reply_lower for w in kw.split()[:3])]
    return full_reply, kws_used[:6]

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
    <div>✍️ <b style="color:var(--text)">Generated:</b> {archive_count}/{TOTAL_ARTICLES} articles</div>
    <div>📅 <b style="color:var(--text)">Plan starts:</b> {START_DATE.strftime('%d %b %Y')}</div>
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
                st.success(f"🎉 All {TOTAL_ARTICLES} articles generated!")
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

    start_date_str = START_DATE.strftime("%d %b %Y")
    end_date = (START_DATE + timedelta(days=59)).strftime("%d %b %Y")
    blogs_total  = sum(1 for d in plan for i in d["items"] if i["type"]=="blog")
    gbp_total    = sum(1 for d in plan for i in d["items"] if i["type"]=="gbp")
    social_total = sum(1 for d in plan for i in d["items"] if i["type"] in ["instagram","facebook","linkedin"])

    st.markdown(f'<div class="page-hdr"><div class="badge">📅 60-Day Plan · {start_date_str} – {end_date}</div><h1>60-Day SEO Content Plan</h1><p>Auto-scheduled blog posts, GBP updates, and social content — every item date-stamped and ready to execute.</p></div>', unsafe_allow_html=True)

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
#  ⭐ REVIEW REPLY CHATBOT
# ══════════════════════════════════════════════════════════════════════════════
elif page == "⭐  Review Replies":
    st.markdown("""<div class="page-hdr">
    <div class="badge">⭐ Review Reply Chatbot</div>
    <h1>Smart Review Reply Generator</h1>
    <p>Paste any review — the engine reads every highlight, detects every topic, and writes a direct, owner-voice reply. No deflection. No "contact our team". You speak for yourself.</p>
    </div>""", unsafe_allow_html=True)

    # ── How it works banner
    st.markdown("""<div style="background:linear-gradient(90deg,#0D2A10,#091A0B);border:1px solid var(--ba);border-radius:10px;padding:.85rem 1.25rem;margin-bottom:1.25rem;display:flex;gap:2rem;flex-wrap:wrap;">
    <div style="font-size:.8rem;color:var(--muted);">🔍 <b style="color:var(--text)">Reads the review</b> — detects every topic mentioned</div>
    <div style="font-size:.8rem;color:var(--muted);">✍️ <b style="color:var(--text)">Writes the reply</b> — direct, first-person, ownership-taking</div>
    <div style="font-size:.8rem;color:var(--muted);">🔑 <b style="color:var(--text)">Embeds SEO keywords</b> — Google indexes your replies</div>
    <div style="font-size:.8rem;color:var(--muted);">🚫 <b style="color:var(--text)">No deflection</b> — never says "contact our team"</div>
    </div>""", unsafe_allow_html=True)

    # ── Main layout
    inp_col, out_col = st.columns([5, 6], gap="large")

    with inp_col:
        st.markdown('<div class="sc"><h3>📋 Review Input</h3>', unsafe_allow_html=True)

        review_text = st.text_area(
            "Paste the guest review here",
            height=200,
            placeholder="e.g. The kitchen was well-stocked but the Wi-Fi was very slow. Staff were friendly. Overall okay stay near Medanta Hospital but the AC stopped working on day 2.",
            label_visibility="collapsed",
        )

        c1, c2 = st.columns(2)
        with c1:
            stars = st.selectbox("Star Rating", [5, 4, 3, 2, 1],
                format_func=lambda x: f"{'⭐'*x} ({x} star{'s' if x>1 else ''})")
        with c2:
            guest_name = st.text_input("Guest Name", placeholder="e.g. Rahul Sharma")

        context = st.selectbox("Stay Context (optional — improves reply)", [
            "General",
            "Medical Stay",
            "Corporate Stay",
            "Family Stay",
            "Long Stay / Monthly",
            "Exhibition / Business",
            "Relocation / New Joiner",
            "Solo Women Traveler",
        ])
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="run-btn">', unsafe_allow_html=True)
        generate_btn = st.button("✍️  GENERATE REPLY", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # ── Keyword value reference
        with st.expander("🔑 High-value keywords this chatbot embeds"):
            for kw, vol, comp, pri, intent in TOP_KEYWORDS:
                pc = p_color(pri)
                cc = {"Very Low":"tg","Low":"tg","Low-Med":"tg","Medium":"tgo","High":"tr"}.get(comp,"tgr")
                st.markdown(f'<div class="krow" style="margin-bottom:.3rem;"><div><div style="font-size:.8rem;font-weight:600;color:var(--text);">{kw}</div><div style="font-size:.7rem;color:var(--muted);">{vol}/mo · <span class="tag {cc}" style="font-size:.6rem;">{comp}</span></div></div><span style="font-size:.9rem;font-weight:700;color:{pc};">P{pri}</span></div>', unsafe_allow_html=True)

    with out_col:
        if generate_btn:
            if not review_text.strip():
                st.warning("Please paste a review on the left before generating.")
            else:
                analysis = analyze_review(review_text)
                reply, kws_used = generate_chatbot_reply(review_text, stars, guest_name, context, analysis)
                st.session_state["chatbot_reply"]    = reply
                st.session_state["chatbot_analysis"] = analysis
                st.session_state["chatbot_kws"]      = kws_used
                st.session_state["chatbot_stars"]    = stars

        if "chatbot_reply" in st.session_state:
            analysis   = st.session_state["chatbot_analysis"]
            reply      = st.session_state["chatbot_reply"]
            kws_used   = st.session_state["chatbot_kws"]
            reply_stars= st.session_state["chatbot_stars"]

            # ── Analysis panel
            topics = analysis["topics"]
            sent   = analysis["sentiment"]
            sent_color = {"positive":"var(--accent)","negative":"var(--red)","mixed":"var(--gold)"}.get(sent,"var(--muted)")
            sent_label = {"positive":"Positive ✅","negative":"Needs careful handling ⚠️","mixed":"Mixed — addressed directly 🟡"}.get(sent,sent)

            st.markdown(f"""<div style="background:var(--card2);border:1px solid var(--border);border-radius:10px;padding:.9rem 1.2rem;margin-bottom:.9rem;">
            <div style="font-size:.7rem;color:var(--muted);text-transform:uppercase;letter-spacing:.07em;margin-bottom:.5rem;">Review Analysis</div>
            <div style="display:flex;flex-wrap:wrap;gap:.5rem;align-items:center;margin-bottom:.6rem;">
              <span style="font-size:.8rem;color:{sent_color};font-weight:700;">{sent_label}</span>
              <span style="color:var(--muted);font-size:.75rem;">· {analysis['pos']} positive signals · {analysis['neg']} negative signals</span>
            </div>
            <div style="font-size:.72rem;color:var(--muted);margin-bottom:.4rem;font-weight:600;">TOPICS DETECTED & ADDRESSED:</div>
            <div style="display:flex;flex-wrap:wrap;gap:.35rem;">
              {'<span class="tag tgr">No specific topics detected</span>' if not topics else
               ''.join(f'<span class="tag {"tg" if sent=="positive" or reply_stars>=4 else "tr"}">{t["label"]}</span>' for t in topics)}
            </div>
            {'<div style="margin-top:.6rem;display:flex;flex-wrap:wrap;gap:.35rem;"><div style="font-size:.7rem;color:var(--muted);width:100%;margin-bottom:.25rem;">SEO KEYWORDS EMBEDDED:</div>' +
             ''.join(f'<span class="rev-kw">{k}</span>' for k in kws_used) + '</div>' if kws_used else ''}
            </div>""", unsafe_allow_html=True)

            # ── Reply display
            st.markdown(f"""<div style="background:var(--card2);border:1px solid var(--ba);border-radius:10px;padding:.75rem 1.2rem;margin-bottom:.6rem;display:flex;justify-content:space-between;align-items:center;">
            <div style="font-size:.8rem;font-weight:700;color:var(--accent);">{'⭐'*reply_stars} Reply — Ready to Post</div>
            <div style="font-size:.73rem;color:var(--muted);">{len(reply.split())} words · {len(reply)} characters</div>
            </div>""", unsafe_allow_html=True)

            st.code(reply, language=None)

            c1, c2 = st.columns(2)
            with c1:
                st.download_button("⬇️ Download Reply (.txt)", reply,
                    f"reply_{stars}star_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                    "text/plain", use_container_width=True)
            with c2:
                # Regenerate tip
                st.markdown(f'<div style="background:var(--g2);border:1px solid #7A602055;border-radius:8px;padding:.6rem .85rem;font-size:.75rem;color:var(--gold);text-align:center;">💡 Adjust context on the left and regenerate for a different angle.</div>', unsafe_allow_html=True)

        else:
            st.markdown("""<div style="background:var(--card);border:1px solid var(--border);border-radius:var(--rl);padding:3rem;text-align:center;height:100%;">
            <div style="font-size:3rem;margin-bottom:1rem;">💬</div>
            <div style="font-family:'Playfair Display',serif;font-size:1.2rem;color:var(--text);margin-bottom:.6rem;">Paste. Click. Reply.</div>
            <div style="color:var(--muted);font-size:.87rem;line-height:1.9;max-width:300px;margin:0 auto;">
            Paste the guest review on the left, set the star rating and context, then click<br>
            <b style="color:var(--accent)">✍️ Generate Reply</b><br><br>
            The chatbot detects every topic in the review and writes a direct, personal response — as the owner.
            </div></div>""", unsafe_allow_html=True)

    # ── Template library as a collapsible reference
    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("📋 Backup Template Library (pre-written by star rating)"):
        tab_labels = [STAR_LABELS[s] for s in [5,4,3,2,1]]
        btabs = st.tabs(tab_labels)
        for tab, s in zip(btabs, [5,4,3,2,1]):
            with tab:
                for idx, r in enumerate(REVIEW_REPLIES[s], 1):
                    kw_tags = "".join(f'<span class="rev-kw">{k}</span>' for k in r["keywords"])
                    st.markdown(f'<div class="rev-card"><div class="rev-context">Template {idx} — {r["context"]}</div><div class="rev-kw-bar">{kw_tags}</div></div>', unsafe_allow_html=True)
                    st.code(r["reply"], language=None)
                    st.markdown("<br>", unsafe_allow_html=True)


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

    st.markdown(f'<div class="page-hdr"><div class="badge">📊 Overview</div><h1>SEO Engine Dashboard</h1><p>Live progress across all {TOTAL_ARTICLES} articles, the 60-day plan, and your content pipeline.</p></div>', unsafe_allow_html=True)

    c1,c2,c3,c4,c5 = st.columns(5)
    for col,(val,lbl,sub,ico) in zip([c1,c2,c3,c4,c5],[
        (len(archive),"Generated",f"of {TOTAL_ARTICLES} articles","✍️"),
        (TOTAL_ARTICLES-len(archive),"Remaining","Articles to produce","📋"),
        (f"{len(archive)/TOTAL_ARTICLES*100:.0f}%","Complete","Pipeline progress","📈"),
        (len(today_items),"Today's Tasks","Blog/GBP/Social","📅"),
        (next_a["priority"] if next_a else "✓","Next Priority",next_a["id"] if next_a else "All done!","🎯"),
    ]):
        with col:
            st.markdown(f'<div class="mc"><div class="ico">{ico}</div><div class="lbl">{lbl}</div><div class="val">{val}</div><div class="sub">{sub}</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    cl,cr = st.columns([3,2],gap="large")

    with cl:
        st.markdown('<div class="sc"><h3>📈 Pipeline Progress</h3>', unsafe_allow_html=True)
        st.progress(len(archive)/TOTAL_ARTICLES)
        st.caption(f"{len(archive)}/{TOTAL_ARTICLES} complete · {TOTAL_ARTICLES-len(archive)} remaining")
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
            ("Big Chain Comparison", ["LT-101","LT-102","LT-103","LT-104","LT-105","LT-106","LT-107","LT-108","LT-109","LT-110","LT-111","LT-112","LT-113","LT-114","LT-115","LT-116","LT-117","LT-118"],"#E8C547"),
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

    st.markdown(f'<div class="page-hdr"><div class="badge">📋 Content Calendar</div><h1>{TOTAL_ARTICLES}-Article Publishing Plan</h1><p>All {TOTAL_ARTICLES} articles filterable by tier, intent, and status. Green border = already generated.</p></div>', unsafe_allow_html=True)

    c1,c2,c3 = st.columns(3)
    with c1: tier_f   = st.selectbox("Tier", ["All","Tier 1","Tier 2","Tier 3","Tier 4"])
    with c2: intent_f = st.selectbox("Intent", ["All","Transactional","Commercial","B2B","Local","Informational","GEO"])
    with c3: status_f = st.selectbox("Status", ["All","Generated","Pending"])

    cal = CONTENT_CALENDAR
    if tier_f   != "All": cal = [a for a in cal if a["tier"]==int(tier_f[-1])]
    if intent_f != "All": cal = [a for a in cal if a["intent"]==intent_f]
    if status_f == "Generated": cal = [a for a in cal if a["id"] in done_ids]
    if status_f == "Pending":   cal = [a for a in cal if a["id"] not in done_ids]

    st.caption(f"Showing {len(cal)} articles · {len(done_ids)} generated · {TOTAL_ARTICLES-len(done_ids)} pending")

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
        with c1: st.markdown(f'<div class="mc"><div class="lbl">Articles</div><div class="val">{len(archive)}</div><div class="sub">of {TOTAL_ARTICLES} planned</div></div>', unsafe_allow_html=True)
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
