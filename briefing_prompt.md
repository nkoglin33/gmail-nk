# News & Intelligence Briefing — Agent Prompt

You are a daily news briefing agent for Regency Centers. Complete all 4 steps below.

---

## STEP 1 — Research (run all searches in parallel)

Run ALL searches simultaneously. For each item capture: headline, 1-2 sentence summary, source name, URL.

- "Federal Reserve interest rates latest"
- "inflation CPI PPI latest news"
- "Treasury yields commercial real estate"
- "US economy GDP jobs today"
- "geopolitical news today"
- "trade tariffs US policy news"
- "top US news today Congress"
- "Chicago news today business"
- "Chicago commercial real estate news"
- "Minneapolis commercial real estate news"
- "Indianapolis commercial real estate news"
- "Columbus Ohio commercial real estate news"
- "Cincinnati commercial real estate news"
- "St Louis commercial real estate news"
- "retail REIT stock performance this week"
- "shopping center REIT news Regency Kimco Kite"
- "grocery anchored REIT news same-store NOI lease spreads"
- "net lease REIT news Agree NNN Essential"
- "mall REIT news Simon Macerich"
- "REIT earnings guidance cap rates 2026"

---

## STEP 2 — Write each section to its own file

Write one file per section using the Write tool. Each file contains only the inner HTML for that section. Use this li format for every bullet:

```html
<li style="font-size:13px;line-height:1.65;color:#4B3C30;margin-bottom:9px;"><span style="font-weight:700;color:#00304B;">HEADLINE</span> — SUMMARY. <a href="URL" style="color:#E56D3D;text-decoration:none;">SOURCE →</a></li>
```

Write these files to `/tmp/` one at a time:

1. `/tmp/macro.html` — 4 bullets from Fed, inflation, Treasury, economy searches
2. `/tmp/geo.html` — 3 bullets from geopolitical and tariff searches
3. `/tmp/us.html` — 3 bullets from US news searches
4. `/tmp/chicago.html` — 3 bullets from Chicago searches
5. `/tmp/midwest.html` — 6 bullets from Midwest CRE searches (label each city in the headline)
6. `/tmp/reit.html` — 6 bullets grouped by segment (label segment in headline), followed by this line:
   ```html
   <p style="font-size:12px;color:#005568;font-style:italic;margin:8px 0 0 0;">Regency Read-Through: [one sentence implication for grocery-anchored Midwest strategy]</p>
   ```

---

## STEP 3 — Assemble and send

Run this Python script using Bash:

```bash
python3 << 'EOF'
import json, subprocess, datetime

today = datetime.date.today()
months = ['January','February','March','April','May','June','July','August','September','October','November','December']
days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
datestr = f"{days[today.weekday()]}, {months[today.month-1]} {today.day}, {today.year}"
subject = f"News & Intelligence Briefing — {datestr}"

def sec(label, file):
    items = open(file).read()
    return f'<div style="background:#ffffff;border-left:4px solid #005568;margin:16px 0;padding:16px 20px;"><p style="font-size:10px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:#005568;margin:0 0 10px 0;">{label}</p><ul style="margin:0;padding-left:18px;">{items}</ul></div>'

html = (
    '<!DOCTYPE html><html><body style="margin:0;padding:0;background-color:#F8F6F3;font-family:Arial,sans-serif;">'
    '<div style="max-width:680px;margin:0 auto;">'
    '<div style="background-color:#005568;color:#ffffff;padding:28px 32px;">'
    '<p style="font-family:Georgia,serif;font-size:22px;font-weight:normal;letter-spacing:2px;text-transform:uppercase;margin:0;">News &amp; Intelligence Briefing</p>'
    f'<p style="font-size:12px;color:rgba(255,255,255,0.65);margin-top:6px;letter-spacing:1px;">{datestr}</p>'
    '</div>'
    '<div style="height:3px;background-color:#DC9529;"></div>'
    '<div style="padding:0 24px;">'
    + sec("Macroeconomic", "/tmp/macro.html")
    + sec("Geopolitical", "/tmp/geo.html")
    + sec("U.S. News", "/tmp/us.html")
    + sec("Chicago", "/tmp/chicago.html")
    + sec("Midwest Real Estate", "/tmp/midwest.html")
    + sec("Public REIT Universe", "/tmp/reit.html")
    + f'</div><div style="background-color:#00304B;color:rgba(255,255,255,0.55);font-size:10px;padding:18px 32px;text-align:center;letter-spacing:1px;margin-top:24px;">Regency Centers &middot; Equity Research &amp; Intelligence &middot; Automated Daily Briefing &middot; {datestr}</div></div></body></html>'
)

payload = json.dumps({"to": "nickkoglin@regencycenters.com", "subject": subject, "body": html})
with open('/tmp/payload.json', 'w') as f:
    f.write(payload)

result = subprocess.run([
    'curl', '-s', '-X', 'POST',
    'https://hook.us2.make.com/iqv1fsrvsac5a7ap7bm2wkq8h3unkmo6',
    '-H', 'x-make-apikey: claude-email-send-2026',
    '-H', 'Content-Type: application/json',
    '--data-binary', '@/tmp/payload.json'
], capture_output=True, text=True)

print('Subject:', subject)
print('Response:', result.stdout)
print('Stderr:', result.stderr)
print('Exit code:', result.returncode)
EOF
```

A response of `Accepted` means the email was sent. Output the subject line and item counts per section.
