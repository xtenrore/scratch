import os, hashlib, xml.etree.ElementTree as ET
import db_chemistry

def make_svg_asset(svg_text, name, cx, cy):
    # Verify valid XML
    try:
        ET.fromstring(svg_text)
    except Exception as e:
        print(f"ERROR in SVG for {name}: {e}")
        raise e
    
    raw = svg_text.encode("utf-8")
    md5 = hashlib.md5(raw).hexdigest()
    path = f"/workspaces/scratch/assets/{md5}.svg"
    with open(path, "wb") as f:
        f.write(raw)
    return {
        "name": name,
        "assetId": md5,
        "dataFormat": "svg",
        "md5ext": f"{md5}.svg",
        "rotationCenterX": cx,
        "rotationCenterY": cy,
        "raw": raw
    }

def format_subscripts(formula):
    sub_map = {
        '0': '₀', '1': '₁', '2': '₂', '3': '₃', '4': '₄',
        '5': '₅', '6': '₆', '7': '₇', '8': '₈', '9': '₉',
        '+': '⁺', '-': '⁻'
    }
    res = ""
    for ch in formula:
        res += sub_map.get(ch, ch)
    return res

# --- 1. 129 Species Costumes ---
def generate_species_svg(s):
    sym = s["symbol"]
    charge = s["charge"]
    color = s["color"]
    border = s["border"]
    stype = s["type"]
    sid = s["id"]

    is_ion = charge != 0
    is_radical = "•" in sym
    is_element = sid <= 19

    disp_text = format_subscripts(sym)
    text_len = len(disp_text)
    if text_len > 7:
        font_size = "10"
    elif text_len > 5:
        font_size = "11"
    elif text_len > 3:
        font_size = "13"
    elif text_len > 2:
        font_size = "15"
    else:
        font_size = "18"

    svg = ['<svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 64 64">']
    grad_id = f"g_{sid}"
    svg.append('  <defs>')
    svg.append(f'    <radialGradient id="{grad_id}" cx="32%" cy="30%" r="68%">')
    svg.append(f'      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.9"/>')
    svg.append(f'      <stop offset="40%" stop-color="{color}" stop-opacity="0.95"/>')
    svg.append(f'      <stop offset="100%" stop-color="{border}" stop-opacity="1.0"/>')
    svg.append('    </radialGradient>')

    if is_ion:
        halo_color = "#38BDF8" if charge > 0 else "#F59E0B"
        svg.append(f'    <filter id="glow_{sid}" x="-25%" y="-25%" width="150%" height="150%">')
        svg.append(f'      <feDropShadow dx="0" dy="0" stdDeviation="3" flood-color="{halo_color}" flood-opacity="0.9"/>')
        svg.append('    </filter>')
    svg.append('  </defs>')

    text_color = "#0A0F1A" if color in ["#E2E8F0", "#FACC15", "#A3E635", "#67E8F9"] else "#FFFFFF"

    if is_element:
        # Elements (1-19): Periodic radius scaling
        z = s.get("z", 1)
        if z <= 2:
            r = 20
        elif z <= 10:
            r = 22
        elif z <= 18:
            r = 24
        else:
            r = 26

        # Outer subtle valence electron track
        svg.append(f'  <circle cx="32" cy="32" r="{r+3}" fill="none" stroke="{border}" stroke-width="0.8" stroke-dasharray="2,3" opacity="0.5"/>')
        # Core sphere
        svg.append(f'  <circle cx="32" cy="32" r="{r}" fill="url(#{grad_id})" stroke="{border}" stroke-width="2"/>')
        # Atomic number badge in upper left
        svg.append(f'  <rect x="{32-r}" y="{32-r}" width="14" height="10" rx="3" fill="#0A0F1A" stroke="{border}" stroke-width="1" opacity="0.85"/>')
        svg.append(f'  <text x="{32-r+7}" y="{32-r+8}" font-family="monospace, sans-serif" font-size="7" font-weight="bold" fill="#38BDF8" text-anchor="middle">{z}</text>')
        # Symbol
        svg.append(f'  <text x="32" y="37" font-family="sans-serif" font-size="{font_size}" font-weight="bold" fill="{text_color}" text-anchor="middle">{disp_text}</text>')

    elif is_ion:
        halo_color = "#38BDF8" if charge > 0 else "#F59E0B"
        # Glowing ionization ring
        svg.append(f'  <circle cx="32" cy="32" r="27" fill="none" stroke="{halo_color}" stroke-width="2" stroke-dasharray="4,2" filter="url(#glow_{sid})"/>')
        # Ion core
        svg.append(f'  <circle cx="32" cy="32" r="22" fill="url(#{grad_id})" stroke="{border}" stroke-width="2"/>')
        # Formula
        svg.append(f'  <text x="32" y="37" font-family="sans-serif" font-size="{font_size}" font-weight="bold" fill="{text_color}" text-anchor="middle">{disp_text}</text>')
        # Charge badge in upper right
        ch_text = "+" if charge == 1 else ("-" if charge == -1 else (f"{charge}+" if charge > 0 else f"{abs(charge)}-"))
        svg.append(f'  <circle cx="49" cy="15" r="9" fill="#0A0F1A" stroke="{halo_color}" stroke-width="1.8"/>')
        svg.append(f'  <text x="49" y="19" font-family="sans-serif" font-size="9" font-weight="bold" fill="{halo_color}" text-anchor="middle">{ch_text}</text>')

    else:
        # Molecules & Radicals
        # Diatomic check: e.g. H2, O2, N2, CO, HCl, HF...
        is_diatomic = any(sym.endswith("2") and len(sym) <= 3 for _ in [0]) or sym in ["CO", "NO•", "NH•", "HCl", "HF", "HBr", "HI", "NaCl", "KCl", "CaO", "SiO", "PN", "NaF", "KF", "NaBr", "KBr", "NaI", "KI", "CN"]
        if is_diatomic:
            # Dual-lobe bonded barbell geometry
            svg.append(f'  <rect x="8" y="16" width="48" height="32" rx="16" fill="url(#{grad_id})" stroke="{border}" stroke-width="2"/>')
            # Covalent bond bridge line
            svg.append(f'  <line x1="18" y1="32" x2="46" y2="32" stroke="#FFFFFF" stroke-width="1" stroke-opacity="0.4" stroke-dasharray="2,2"/>')
        else:
            # Polyatomic cluster capsule
            svg.append(f'  <rect x="5" y="15" width="54" height="34" rx="12" fill="url(#{grad_id})" stroke="{border}" stroke-width="2"/>')
            # Cross bond structure lines
            svg.append(f'  <line x1="12" y1="26" x2="52" y2="26" stroke="#FFFFFF" stroke-width="1" stroke-opacity="0.3" stroke-dasharray="3,3"/>')
            svg.append(f'  <line x1="12" y1="38" x2="52" y2="38" stroke="#FFFFFF" stroke-width="1" stroke-opacity="0.3" stroke-dasharray="3,3"/>')

        # Formula text
        svg.append(f'  <text x="32" y="37" font-family="sans-serif" font-size="{font_size}" font-weight="bold" fill="{text_color}" text-anchor="middle">{disp_text}</text>')

        # Radical dot indicator
        if is_radical:
            svg.append(f'  <circle cx="51" cy="16" r="5" fill="#EF4444" stroke="#FFFFFF" stroke-width="1.2"/>')
            svg.append(f'  <circle cx="51" cy="16" r="2" fill="#FFFFFF"/>')

    svg.append('</svg>')
    return "\n".join(svg)


# --- 2. Stage Backdrops ---
def generate_backdrops():
    # 480x360, center 240, 180
    def base_frame():
        return '''
  <!-- Outer Instrument Chassis -->
  <rect width="480" height="360" fill="#070A12"/>
  
  <!-- Top Branded Header Bar (Y: 0 to 22) -->
  <rect x="0" y="0" width="480" height="22" fill="#0A0F1A" stroke="#1E293B" stroke-width="1"/>
  <text x="14" y="15" font-family="monospace, sans-serif" font-size="9" font-weight="bold" fill="#38BDF8" letter-spacing="1">VACUUM CHEMISTRY SIMULATOR // VC-3000</text>
  <text x="260" y="15" font-family="monospace, sans-serif" font-size="8" fill="#64748B" text-anchor="middle">PRESSURE: 10⁻¹⁰ TORR • ULTRA-HIGH VACUUM</text>
  <text x="466" y="15" font-family="monospace, sans-serif" font-size="8" font-weight="bold" fill="#94A3B8" text-anchor="end">LABORATORY SPEC</text>
  
  <!-- Tool Rail Mounting Bay (Y: 22 to 58) -->
  <rect x="0" y="22" width="480" height="36" fill="#0D1424" stroke="#1E293B" stroke-width="1"/>
  <!-- Bezel screw indicators -->
  <circle cx="8" cy="40" r="1.5" fill="#334155"/>
  <circle cx="472" cy="40" r="1.5" fill="#334155"/>

  <!-- Vacuum Chamber Containment Area (Y: 60 to 328, height 268, width 464, x: 8 to 472) -->
  <rect x="8" y="60" width="464" height="268" rx="6" fill="#050811" stroke="#1E293B" stroke-width="2"/>
  <rect x="10" y="62" width="460" height="264" rx="4" fill="none" stroke="#0F172A" stroke-width="1"/>

  <!-- Cosmic Vacuum Fluctuation Particles (Ambient dust) -->
  <circle cx="45" cy="95" r="0.8" fill="#FFFFFF" opacity="0.6"/>
  <circle cx="110" cy="180" r="1.2" fill="#38BDF8" opacity="0.4"/>
  <circle cx="195" cy="115" r="0.7" fill="#FACC15" opacity="0.5"/>
  <circle cx="280" cy="245" r="1.1" fill="#FFFFFF" opacity="0.5"/>
  <circle cx="365" cy="140" r="0.8" fill="#38BDF8" opacity="0.4"/>
  <circle cx="435" cy="270" r="1.0" fill="#A855F7" opacity="0.4"/>
  <circle cx="85" cy="285" r="0.8" fill="#FFFFFF" opacity="0.5"/>
  <circle cx="230" cy="290" r="0.9" fill="#38BDF8" opacity="0.4"/>
  <circle cx="410" cy="90" r="0.7" fill="#FFFFFF" opacity="0.6"/>

  <!-- Laser Alignment Precision Reticles -->
  <!-- Center crosshair at (240, 194) -->
  <line x1="230" y1="194" x2="250" y2="194" stroke="#1E293B" stroke-width="1"/>
  <line x1="240" y1="184" x2="240" y2="204" stroke="#1E293B" stroke-width="1"/>
  <circle cx="240" cy="194" r="6" fill="none" stroke="#1E293B" stroke-width="0.8"/>
  
  <!-- Coordinate grid lines -->
  <line x1="125" y1="62" x2="125" y2="326" stroke="#0F172A" stroke-width="1" stroke-dasharray="3,3"/>
  <line x1="355" y1="62" x2="355" y2="326" stroke="#0F172A" stroke-width="1" stroke-dasharray="3,3"/>
  <line x1="10" y1="128" x2="470" y2="128" stroke="#0F172A" stroke-width="1" stroke-dasharray="3,3"/>
  <line x1="10" y1="260" x2="470" y2="260" stroke="#0F172A" stroke-width="1" stroke-dasharray="3,3"/>

  <!-- Chamber Corner Brackets -->
  <path d="M 16 74 L 16 66 L 24 66" fill="none" stroke="#334155" stroke-width="1.5"/>
  <path d="M 464 74 L 464 66 L 456 66" fill="none" stroke="#334155" stroke-width="1.5"/>
  <path d="M 16 314 L 16 322 L 24 322" fill="none" stroke="#334155" stroke-width="1.5"/>
  <path d="M 464 314 L 464 322 L 456 322" fill="none" stroke="#334155" stroke-width="1.5"/>

  <!-- Bottom Telemetry Console Chassis (Y: 330 to 358) -->
  <rect x="0" y="330" width="480" height="30" fill="#0A0F1A" stroke="#1E293B" stroke-width="1"/>
  <circle cx="16" cy="345" r="3" fill="#10B981"/>
  <text x="26" y="348" font-family="monospace, sans-serif" font-size="9" fill="#10B981" font-weight="bold">&gt; DETECTOR ONLINE</text>
  <text x="140" y="348" font-family="monospace, sans-serif" font-size="8" fill="#64748B">COLLIDE PARTICLES • PHOTOCHEMICAL &amp; COSMIC IONIZATION ACTIVE</text>
'''

    # Standard Vacuum
    bg_std = f'''<svg xmlns="http://www.w3.org/2000/svg" width="480" height="360" viewBox="0 0 480 360">
{base_frame()}
</svg>'''

    # UV Active
    bg_uv = f'''<svg xmlns="http://www.w3.org/2000/svg" width="480" height="360" viewBox="0 0 480 360">
  <defs>
    <linearGradient id="uv_cascade" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#A855F7" stop-opacity="0.35"/>
      <stop offset="25%" stop-color="#A855F7" stop-opacity="0.12"/>
      <stop offset="100%" stop-color="#A855F7" stop-opacity="0.0"/>
    </linearGradient>
  </defs>
{base_frame()}
  <!-- Top UV Quartz Arc Lamp Tube -->
  <rect x="10" y="62" width="460" height="6" rx="2" fill="#C084FC" stroke="#A855F7" stroke-width="1"/>
  <rect x="10" y="68" width="460" height="180" fill="url(#uv_cascade)"/>
  <!-- Status Tag -->
  <rect x="140" y="74" width="200" height="16" rx="3" fill="#0A0F1A" stroke="#A855F7" stroke-width="1" opacity="0.9"/>
  <text x="240" y="86" font-family="monospace, sans-serif" font-size="8" font-weight="bold" fill="#E9D5FF" text-anchor="middle" letter-spacing="1">⚡ UV RADIANCE ACTIVE • 254 nm</text>
</svg>'''

    # Frozen Cryo Stasis
    bg_freeze = f'''<svg xmlns="http://www.w3.org/2000/svg" width="480" height="360" viewBox="0 0 480 360">
  <defs>
    <radialGradient id="frost_corner" cx="0%" cy="0%" r="100%">
      <stop offset="0%" stop-color="#38BDF8" stop-opacity="0.4"/>
      <stop offset="70%" stop-color="#38BDF8" stop-opacity="0.08"/>
      <stop offset="100%" stop-color="#38BDF8" stop-opacity="0.0"/>
    </radialGradient>
  </defs>
{base_frame()}
  <!-- Frost Corner Overlays -->
  <rect x="10" y="62" width="80" height="80" fill="url(#frost_corner)"/>
  <rect x="390" y="62" width="80" height="80" fill="url(#frost_corner)" transform="scale(-1, 1) translate(-480, 0)"/>
  <!-- Cryo Highlight Border -->
  <rect x="8" y="60" width="464" height="268" rx="6" fill="none" stroke="#38BDF8" stroke-width="2" opacity="0.85"/>
  <!-- Status Tag -->
  <rect x="130" y="74" width="220" height="16" rx="3" fill="#0A0F1A" stroke="#38BDF8" stroke-width="1" opacity="0.9"/>
  <text x="240" y="86" font-family="monospace, sans-serif" font-size="8" font-weight="bold" fill="#7DD3FC" text-anchor="middle" letter-spacing="1">❄ CRYO STASIS ENGAGED • 0 K • PAUSED</text>
</svg>'''

    return bg_std, bg_uv, bg_freeze


# --- 3. Precision Vector Buttons (No Emojis!) ---
def generate_vector_button(tool_name, label, active=False, custom_active_col=None):
    # 44x28, center 22, 14
    act_col = custom_active_col or "#38BDF8"
    bg = "#0C2338" if active else "#111827"
    border = act_col if active else "#2D3748"
    fg = act_col if active else "#CBD5E1"
    sub_fg = act_col if active else "#64748B"

    icons = {
        "add": '''
          <circle cx="22" cy="10" r="7" fill="none" stroke="{fg}" stroke-width="1.2" stroke-dasharray="2,2"/>
          <line x1="22" y1="6" x2="22" y2="14" stroke="{fg}" stroke-width="2" stroke-linecap="round"/>
          <line x1="18" y1="10" x2="26" y2="10" stroke="{fg}" stroke-width="2" stroke-linecap="round"/>
        ''',
        "del": '''
          <circle cx="22" cy="10" r="7" fill="none" stroke="{fg}" stroke-width="1.2"/>
          <line x1="17" y1="10" x2="27" y2="10" stroke="{fg}" stroke-width="2.2" stroke-linecap="round"/>
        ''',
        "insp": '''
          <circle cx="22" cy="10" r="6" fill="none" stroke="{fg}" stroke-width="1.5"/>
          <circle cx="22" cy="10" r="2" fill="{fg}"/>
          <line x1="22" y1="2" x2="22" y2="6" stroke="{fg}" stroke-width="1.2"/>
          <line x1="22" y1="14" x2="22" y2="18" stroke="{fg}" stroke-width="1.2"/>
          <line x1="14" y1="10" x2="18" y2="10" stroke="{fg}" stroke-width="1.2"/>
          <line x1="26" y1="10" x2="30" y2="10" stroke="{fg}" stroke-width="1.2"/>
        ''',
        "uv": '''
          <rect x="18" y="7" width="8" height="6" rx="2" fill="none" stroke="{fg}" stroke-width="1.5"/>
          <line x1="15" y1="4" x2="18" y2="7" stroke="{fg}" stroke-width="1.2" stroke-linecap="round"/>
          <line x1="22" y1="3" x2="22" y2="6" stroke="{fg}" stroke-width="1.2" stroke-linecap="round"/>
          <line x1="29" y1="4" x2="26" y2="7" stroke="{fg}" stroke-width="1.2" stroke-linecap="round"/>
          <line x1="20" y1="15" x2="20" y2="17" stroke="{fg}" stroke-width="1.2" stroke-linecap="round"/>
          <line x1="24" y1="15" x2="24" y2="17" stroke="{fg}" stroke-width="1.2" stroke-linecap="round"/>
        ''',
        "freeze": '''
          <line x1="22" y1="4" x2="22" y2="16" stroke="{fg}" stroke-width="1.5" stroke-linecap="round"/>
          <line x1="17" y1="7" x2="27" y2="13" stroke="{fg}" stroke-width="1.5" stroke-linecap="round"/>
          <line x1="17" y1="13" x2="27" y2="7" stroke="{fg}" stroke-width="1.5" stroke-linecap="round"/>
          <circle cx="22" cy="10" r="1.5" fill="{fg}"/>
        ''',
        "catalog": '''
          <rect x="16" y="5" width="12" height="10" rx="1.5" fill="none" stroke="{fg}" stroke-width="1.3"/>
          <line x1="22" y1="5" x2="22" y2="15" stroke="{fg}" stroke-width="1"/>
          <line x1="16" y1="10" x2="28" y2="10" stroke="{fg}" stroke-width="1"/>
          <circle cx="19" cy="7.5" r="1" fill="{fg}"/>
        ''',
        "audio": '''
          <polygon points="16,8 19,8 23,5 23,15 19,12 16,12" fill="{fg}"/>
          <path d="M 25 7 Q 27 10 25 13" fill="none" stroke="{fg}" stroke-width="1.2" stroke-linecap="round"/>
          <path d="M 27 5 Q 30 10 27 15" fill="none" stroke="{fg}" stroke-width="1.2" stroke-linecap="round"/>
        ''',
        "audio_muted": '''
          <polygon points="16,8 19,8 23,5 23,15 19,12 16,12" fill="{fg}"/>
          <line x1="15" y1="16" x2="29" y2="4" stroke="#EF4444" stroke-width="1.8" stroke-linecap="round"/>
        ''',
        "save": '''
          <rect x="17" y="6" width="10" height="8" rx="1" fill="none" stroke="{fg}" stroke-width="1.4"/>
          <line x1="15" y1="8" x2="17" y2="8" stroke="{fg}" stroke-width="1.2"/>
          <line x1="15" y1="12" x2="17" y2="12" stroke="{fg}" stroke-width="1.2"/>
          <line x1="27" y1="8" x2="29" y2="8" stroke="{fg}" stroke-width="1.2"/>
          <line x1="27" y1="12" x2="29" y2="12" stroke="{fg}" stroke-width="1.2"/>
        ''',
        "help": '''
          <circle cx="22" cy="10" r="7" fill="none" stroke="{fg}" stroke-width="1.3"/>
          <circle cx="22" cy="7" r="1" fill="{fg}"/>
          <line x1="22" y1="9.5" x2="22" y2="13.5" stroke="{fg}" stroke-width="1.5" stroke-linecap="round"/>
        ''',
        "purge": '''
          <path d="M 22 5 A 5 5 0 1 1 17 12" fill="none" stroke="{fg}" stroke-width="1.4" stroke-linecap="round"/>
          <polyline points="20,4 23,5 22,8" fill="none" stroke="{fg}" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"/>
          <circle cx="22" cy="10" r="1.5" fill="{fg}"/>
        '''
    }

    icon_svg = icons.get(tool_name, "").replace("{fg}", fg)

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="44" height="28" viewBox="0 0 44 28">
  <rect x="1" y="1" width="42" height="26" rx="4" fill="{bg}" stroke="{border}" stroke-width="1.5"/>
  <line x1="3" y1="3" x2="41" y2="3" stroke="#FFFFFF" stroke-width="0.8" stroke-opacity="0.1"/>
  {icon_svg}
  <text x="22" y="24" font-family="monospace, sans-serif" font-size="6.5" font-weight="bold" fill="{sub_fg}" text-anchor="middle" letter-spacing="0.5">{label}</text>
</svg>'''
    return svg


# --- 4. Categorized Spawner Palette ---
def generate_palette_drawer():
    # 460x105, center 230, 52
    svg = ['<svg xmlns="http://www.w3.org/2000/svg" width="460" height="105" viewBox="0 0 460 105">']
    svg.append('  <!-- Drawer Background -->')
    svg.append('  <rect width="460" height="105" rx="6" fill="#0A0F1D" stroke="#1E293B" stroke-width="2"/>')
    svg.append('  <!-- Header / Tabs -->')
    svg.append('  <rect x="0" y="0" width="460" height="20" rx="4" fill="#0F172A" stroke="#1E293B" stroke-width="1"/>')
    svg.append('  <text x="16" y="14" font-family="monospace, sans-serif" font-size="8.5" font-weight="bold" fill="#38BDF8">MATERIAL SPAWNER // PERIODIC PALETTE</text>')
    svg.append('  <text x="444" y="14" font-family="monospace, sans-serif" font-size="8" fill="#64748B" text-anchor="end">CLICK ELEMENT TO SPAWN</text>')

    row1 = db_chemistry.SPECIES[:10]
    row2 = db_chemistry.SPECIES[10:19]

    for i, el in enumerate(row1):
        x = 14 + i * 44
        y = 26
        color = el["color"]
        border = el["border"]
        fg = "#0A0F1A" if color in ["#E2E8F0", "#FACC15", "#A3E635", "#67E8F9"] else "#FFFFFF"
        svg.append(f'  <g>')
        svg.append(f'    <rect x="{x}" y="{y}" width="40" height="34" rx="4" fill="#131C2E" stroke="{border}" stroke-width="1.2"/>')
        svg.append(f'    <circle cx="{x+20}" cy="{y+14}" r="9" fill="{color}" stroke="{border}" stroke-width="1"/>')
        svg.append(f'    <text x="{x+20}" y="{y+17.5}" font-family="sans-serif" font-size="8.5" font-weight="bold" fill="{fg}" text-anchor="middle">{el["symbol"]}</text>')
        svg.append(f'    <text x="{x+20}" y="{y+30}" font-family="monospace, sans-serif" font-size="6" fill="#94A3B8" text-anchor="middle">Z={el["z"]}</text>')
        svg.append(f'  </g>')

    for i, el in enumerate(row2):
        x = 36 + i * 44
        y = 64
        color = el["color"]
        border = el["border"]
        fg = "#0A0F1A" if color in ["#E2E8F0", "#FACC15", "#A3E635", "#67E8F9"] else "#FFFFFF"
        svg.append(f'  <g>')
        svg.append(f'    <rect x="{x}" y="{y}" width="40" height="34" rx="4" fill="#131C2E" stroke="{border}" stroke-width="1.2"/>')
        svg.append(f'    <circle cx="{x+20}" cy="{y+14}" r="9" fill="{color}" stroke="{border}" stroke-width="1"/>')
        svg.append(f'    <text x="{x+20}" y="{y+17.5}" font-family="sans-serif" font-size="8.5" font-weight="bold" fill="{fg}" text-anchor="middle">{el["symbol"]}</text>')
        svg.append(f'    <text x="{x+20}" y="{y+30}" font-family="monospace, sans-serif" font-size="6" fill="#94A3B8" text-anchor="middle">Z={el["z"]}</text>')
        svg.append(f'  </g>')

    svg.append('</svg>')
    return "\n".join(svg)


# --- 5. Selected Entity Inspector (129 Pre-rendered HUD Cards) ---
def generate_inspector_card(s):
    # 180x155, center 90, 77
    sid = s["id"]
    sym = s["symbol"]
    name = s["name"]
    formula = s["formula"]
    stype = s["type"]
    charge = s["charge"]
    atoms = s["atoms"]
    desc = s["desc"]
    color = s["color"]
    border = s["border"]

    ch_str = "0 (Neutral)" if charge == 0 else (f"+{charge} (Cation)" if charge > 0 else f"{charge} (Anion)")
    ch_col = "#94A3B8" if charge == 0 else ("#38BDF8" if charge > 0 else "#F59E0B")

    if len(desc) > 60:
        desc = desc[:57] + "..."

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="180" height="155" viewBox="0 0 180 155">
  <rect width="180" height="155" rx="6" fill="#0A0F1D" stroke="#1E293B" stroke-width="1.5"/>
  <path d="M 8 16 L 8 8 L 16 8" fill="none" stroke="#38BDF8" stroke-width="1.5"/>
  <path d="M 172 16 L 172 8 L 164 8" fill="none" stroke="#38BDF8" stroke-width="1.5"/>
  <path d="M 8 139 L 8 147 L 16 147" fill="none" stroke="#38BDF8" stroke-width="1.5"/>
  <path d="M 172 139 L 172 147 L 164 147" fill="none" stroke="#38BDF8" stroke-width="1.5"/>

  <rect x="18" y="6" width="144" height="14" rx="2" fill="#0F172A"/>
  <text x="90" y="16" font-family="monospace, sans-serif" font-size="7.5" font-weight="bold" fill="#38BDF8" text-anchor="middle">SPECTROMETER HUD // #{sid}</text>

  <rect x="12" y="24" width="46" height="34" rx="4" fill="{color}" stroke="{border}" stroke-width="1.5"/>
  <text x="35" y="47" font-family="sans-serif" font-size="14" font-weight="bold" fill="#0A0F1A" text-anchor="middle">{format_subscripts(sym)}</text>

  <text x="66" y="36" font-family="sans-serif" font-size="9" font-weight="bold" fill="#FFFFFF">{name[:18]}</text>
  <text x="66" y="48" font-family="monospace, sans-serif" font-size="7" fill="#38BDF8">{stype[:22]}</text>
  <text x="66" y="58" font-family="monospace, sans-serif" font-size="7" fill="{ch_col}">CHARGE: {ch_str}</text>

  <line x1="12" y1="64" x2="168" y2="64" stroke="#1E293B" stroke-width="1"/>

  <text x="14" y="76" font-family="monospace, sans-serif" font-size="7" fill="#64748B">COMPOSITION:</text>
  <text x="76" y="76" font-family="sans-serif" font-size="7.5" font-weight="bold" fill="#E2E8F0">{atoms[:20]}</text>

  <text x="14" y="90" font-family="monospace, sans-serif" font-size="7" fill="#64748B">FORMULA:</text>
  <text x="76" y="90" font-family="sans-serif" font-size="7.5" font-weight="bold" fill="#38BDF8">{formula[:18]}</text>

  <text x="14" y="104" font-family="monospace, sans-serif" font-size="7" fill="#64748B">STATUS:</text>
  <text x="76" y="104" font-family="monospace, sans-serif" font-size="7" font-weight="bold" fill="#10B981">CATALOGED ★</text>

  <rect x="12" y="112" width="156" height="34" rx="3" fill="#070C16" stroke="#1E293B" stroke-width="1"/>
  <text x="16" y="125" font-family="sans-serif" font-size="6.5" fill="#94A3B8">{desc[:32]}</text>
  <text x="16" y="136" font-family="sans-serif" font-size="6.5" fill="#94A3B8">{desc[32:64]}</text>
</svg>'''
    return svg


# --- 6. First-Run Onboarding HUD ---
def generate_onboarding_card():
    # 420x220, center 210, 110
    return '''<svg xmlns="http://www.w3.org/2000/svg" width="420" height="220" viewBox="0 0 420 220">
  <rect width="420" height="220" rx="8" fill="#0A0F1D" stroke="#38BDF8" stroke-width="1.8"/>
  <rect x="0" y="0" width="420" height="28" rx="6" fill="#0F172A" stroke="#1E293B" stroke-width="1"/>
  <text x="18" y="19" font-family="monospace, sans-serif" font-size="9.5" font-weight="bold" fill="#38BDF8" letter-spacing="1">VACUUM SPECTROSCOPY SYSTEM // OPERATIONAL MANUAL</text>
  <text x="404" y="18" font-family="sans-serif" font-size="10" font-weight="bold" fill="#64748B" text-anchor="end">v2.0</text>

  <rect x="16" y="38" width="188" height="66" rx="4" fill="#0E1626" stroke="#1E293B" stroke-width="1"/>
  <circle cx="32" cy="54" r="9" fill="#10B981"/>
  <text x="32" y="58" font-family="monospace, sans-serif" font-size="9" font-weight="bold" fill="#0A0F1A" text-anchor="middle">1</text>
  <text x="48" y="52" font-family="sans-serif" font-size="8.5" font-weight="bold" fill="#FFFFFF">ADD REAGENTS</text>
  <text x="48" y="64" font-family="sans-serif" font-size="7" fill="#94A3B8">Click [+] to toggle the 19-element</text>
  <text x="48" y="74" font-family="sans-serif" font-size="7" fill="#94A3B8">periodic spawner drawer.</text>

  <rect x="216" y="38" width="188" height="66" rx="4" fill="#0E1626" stroke="#1E293B" stroke-width="1"/>
  <circle cx="232" cy="54" r="9" fill="#38BDF8"/>
  <text x="232" y="58" font-family="monospace, sans-serif" font-size="9" font-weight="bold" fill="#0A0F1A" text-anchor="middle">2</text>
  <text x="248" y="52" font-family="sans-serif" font-size="8.5" font-weight="bold" fill="#FFFFFF">DRAG &amp; COLLIDE</text>
  <text x="248" y="64" font-family="sans-serif" font-size="7" fill="#94A3B8">Drag atoms together to test chemical</text>
  <text x="248" y="74" font-family="sans-serif" font-size="7" fill="#94A3B8">affinity and synthesize molecules.</text>

  <rect x="16" y="112" width="188" height="66" rx="4" fill="#0E1626" stroke="#1E293B" stroke-width="1"/>
  <circle cx="32" cy="128" r="9" fill="#A855F7"/>
  <text x="32" y="132" font-family="monospace, sans-serif" font-size="9" font-weight="bold" fill="#0A0F1A" text-anchor="middle">3</text>
  <text x="48" y="126" font-family="sans-serif" font-size="8.5" font-weight="bold" fill="#FFFFFF">ENERGY &amp; RADIATION</text>
  <text x="48" y="138" font-family="sans-serif" font-size="7" fill="#94A3B8">Toggle [UV] for photolysis. Cosmic rays</text>
  <text x="48" y="148" font-family="sans-serif" font-size="7" fill="#94A3B8">spontaneously ionize neutral species.</text>

  <rect x="216" y="112" width="188" height="66" rx="4" fill="#0E1626" stroke="#1E293B" stroke-width="1"/>
  <circle cx="232" cy="128" r="9" fill="#F59E0B"/>
  <text x="232" y="132" font-family="monospace, sans-serif" font-size="9" font-weight="bold" fill="#0A0F1A" text-anchor="middle">4</text>
  <text x="248" y="126" font-family="sans-serif" font-size="8.5" font-weight="bold" fill="#FFFFFF">CRYO &amp; CATALOG</text>
  <text x="248" y="138" font-family="sans-serif" font-size="7" fill="#94A3B8">Freeze time to inspect structures. Track</text>
  <text x="248" y="148" font-family="sans-serif" font-size="7" fill="#94A3B8">all 129 species in the compendium.</text>

  <rect x="130" y="186" width="160" height="24" rx="4" fill="#0C2338" stroke="#38BDF8" stroke-width="1.2"/>
  <text x="210" y="202" font-family="monospace, sans-serif" font-size="8.5" font-weight="bold" fill="#38BDF8" text-anchor="middle">INITIALIZE EXPERIMENT (SPACE)</text>
</svg>'''


# --- 7. Particles and Visual Effects ---
def generate_fx_assets():
    costumes = {}

    # Cosmic Ray Streak (64x14, center 32, 7)
    cosmic_svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="64" height="14" viewBox="0 0 64 14">
  <defs>
    <linearGradient id="cosmic_streak" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#C084FC" stop-opacity="0.0"/>
      <stop offset="40%" stop-color="#38BDF8" stop-opacity="0.6"/>
      <stop offset="85%" stop-color="#FFFFFF" stop-opacity="0.95"/>
      <stop offset="100%" stop-color="#38BDF8" stop-opacity="1.0"/>
    </linearGradient>
  </defs>
  <line x1="2" y1="7" x2="60" y2="7" stroke="url(#cosmic_streak)" stroke-width="4" stroke-linecap="round"/>
  <circle cx="58" cy="7" r="4" fill="#FFFFFF"/>
</svg>'''
    costumes["cosmic_ray"] = make_svg_asset(cosmic_svg, "cosmic_ray", 32, 7)

    # Photon Wave-packet (26x26, center 13, 13)
    photon_svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="26" height="26" viewBox="0 0 26 26">
  <circle cx="13" cy="13" r="10" fill="#FACC15" fill-opacity="0.25"/>
  <circle cx="13" cy="13" r="6" fill="#FACC15" fill-opacity="0.7"/>
  <circle cx="13" cy="13" r="3" fill="#FFFFFF"/>
  <path d="M 5 13 Q 9 6, 13 13 T 21 13" fill="none" stroke="#FEF08A" stroke-width="2"/>
</svg>'''
    costumes["photon_wave"] = make_svg_asset(photon_svg, "photon_wave", 13, 13)

    # Exothermic plasma shockwave (3 frames)
    for frame, r, col in [(1, 16, "#F97316"), (2, 28, "#EF4444"), (3, 38, "#DC2626")]:
        fx_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="84" height="84" viewBox="0 0 84 84">
  <circle cx="42" cy="42" r="{r}" fill="{col}" fill-opacity="0.45" stroke="#FEF08A" stroke-width="2.5"/>
  <circle cx="42" cy="42" r="{max(4, r-8)}" fill="#FFFFFF" fill-opacity="0.3"/>
  <line x1="42" y1="{42-r-5}" x2="42" y2="{42-r+5}" stroke="#FFFFFF" stroke-width="2"/>
  <line x1="42" y1="{42+r-5}" x2="42" y2="{42+r+5}" stroke="#FFFFFF" stroke-width="2"/>
  <line x1="{42-r-5}" y1="42" x2="{42-r+5}" y2="42" stroke="#FFFFFF" stroke-width="2"/>
  <line x1="{42+r-5}" y1="42" x2="{42+r+5}" y2="42" stroke="#FFFFFF" stroke-width="2"/>
</svg>'''
        costumes[f"fx_exo_{frame}"] = make_svg_asset(fx_svg, f"fx_exo_{frame}", 42, 42)

    # Bond sparkle (2 frames)
    for frame, r in [(1, 14), (2, 24)]:
        fx_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="60" height="60" viewBox="0 0 60 60">
  <circle cx="30" cy="30" r="{r}" fill="none" stroke="#38BDF8" stroke-width="2.5" stroke-dasharray="3,3"/>
  <circle cx="30" cy="30" r="{r-5}" fill="#38BDF8" fill-opacity="0.3"/>
  <circle cx="30" cy="30" r="3" fill="#FFFFFF"/>
</svg>'''
        costumes[f"fx_bond_{frame}"] = make_svg_asset(fx_svg, f"fx_bond_{frame}", 30, 30)

    # Ionization electric zap (2 frames)
    for frame, pts in [(1, "30,8 22,26 34,24 26,52"), (2, "30,8 36,26 24,24 32,52")]:
        fx_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="60" height="60" viewBox="0 0 60 60">
  <circle cx="30" cy="30" r="18" fill="#38BDF8" fill-opacity="0.2"/>
  <polyline points="{pts}" fill="none" stroke="#67E8F9" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
</svg>'''
        costumes[f"fx_zap_{frame}"] = make_svg_asset(fx_svg, f"fx_zap_{frame}", 30, 30)

    # Annihilation poof (2 frames)
    for frame, r in [(1, 12), (2, 22)]:
        fx_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="60" height="60" viewBox="0 0 60 60">
  <circle cx="30" cy="30" r="{r}" fill="#A855F7" fill-opacity="0.35" stroke="#C084FC" stroke-width="2"/>
  <circle cx="30" cy="30" r="{max(2, r-6)}" fill="none" stroke="#FFFFFF" stroke-width="1.2" stroke-dasharray="2,2"/>
</svg>'''
        costumes[f"fx_poof_{frame}"] = make_svg_asset(fx_svg, f"fx_poof_{frame}", 30, 30)

    # Toast Banner (240x36, center 120, 18)
    toast_svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="240" height="36" viewBox="0 0 240 36">
  <rect width="240" height="36" rx="6" fill="#0A0F1D" stroke="#38BDF8" stroke-width="1.5"/>
  <circle cx="20" cy="18" r="10" fill="#38BDF8"/>
  <text x="20" y="22" font-family="sans-serif" font-size="11" font-weight="bold" fill="#0A0F1A" text-anchor="middle">★</text>
  <text x="38" y="16" font-family="sans-serif" font-size="8.5" font-weight="bold" fill="#38BDF8">DISCOVERY CATALOGED</text>
  <text x="38" y="27" font-family="monospace, sans-serif" font-size="8" fill="#E2E8F0">Species verified and saved</text>
</svg>'''
    costumes["toast_banner"] = make_svg_asset(toast_svg, "toast_banner", 120, 18)

    return costumes


# --- 8. Master Generation Routine ---
# --- 9. Compendium Browser Pages ---
def generate_compendium_assets():
    costumes = {}

    def base_comp_modal(active_tab_idx, title, subtitle):
        tabs = [
            (1, "SUMMARY", 14, 78, "#6366F1"),
            (2, "ATOMS", 96, 78, "#10B981"),
            (3, "MOLECULES", 178, 86, "#38BDF8"),
            (4, "RADICALS", 268, 80, "#EF4444"),
            (5, "IONS", 352, 74, "#A855F7")
        ]
        tab_svg = []
        for tid, tname, tx, tw, tcol in tabs:
            is_active = (tid == active_tab_idx)
            bg = "#162032" if is_active else "#0E1522"
            border = tcol if is_active else "#1E293B"
            fg = tcol if is_active else "#64748B"
            weight = "bold" if is_active else "normal"
            tab_svg.append(f'<rect x="{tx}" y="28" width="{tw}" height="18" rx="2" fill="{bg}" stroke="{border}" stroke-width="1"/>')
            tab_svg.append(f'<text x="{tx + tw/2}" y="40.5" font-family="monospace, sans-serif" font-size="7" font-weight="{weight}" fill="{fg}" text-anchor="middle">[{tid}] {tname}</text>')
            if is_active:
                tab_svg.append(f'<line x1="{tx+2}" y1="46" x2="{tx+tw-2}" y2="46" stroke="{tcol}" stroke-width="1.8"/>')

        tabs_str = "\n  ".join(tab_svg)

        return f'''
  <!-- Chassis Frame -->
  <rect width="440" height="250" rx="4" fill="#080D18" stroke="#1E293B" stroke-width="1.5"/>
  
  <!-- Header Bar (Y: 0 to 26) -->
  <rect x="0" y="0" width="440" height="26" rx="4" fill="#0C1424" stroke="#1E293B" stroke-width="1"/>
  <circle cx="14" cy="13" r="3.5" fill="#38BDF8"/>
  <text x="24" y="16.5" font-family="monospace, sans-serif" font-size="8.5" font-weight="bold" fill="#38BDF8" letter-spacing="0.8">{title}</text>
  <text x="390" y="16.5" font-family="monospace, sans-serif" font-size="7.5" fill="#64748B" text-anchor="end">{subtitle}</text>
  
  <!-- Close button in top right -->
  <rect x="406" y="5" width="22" height="16" rx="2" fill="#1C121A" stroke="#EF4444" stroke-width="1"/>
  <text x="417" y="16.5" font-family="sans-serif" font-size="11" font-weight="bold" fill="#EF4444" text-anchor="middle">×</text>

  <!-- Tab Bar (Y: 28 to 48) -->
  {tabs_str}

  <!-- Bottom Action Bar (Y: 222 to 244) -->
  <rect x="0" y="222" width="440" height="28" fill="#0A0F1D" stroke="#1E293B" stroke-width="1"/>
  
  <!-- Reset Button [D] -->
  <rect x="14" y="226" width="110" height="20" rx="2" fill="#1A0F14" stroke="#EF4444" stroke-width="1"/>
  <text x="69" y="239" font-family="monospace, sans-serif" font-size="7" font-weight="bold" fill="#F87171" text-anchor="middle">RESET ARCHIVE [D]</text>
  
  <!-- Center Status -->
  <text x="220" y="239" font-family="monospace, sans-serif" font-size="7" fill="#64748B" text-anchor="middle">CLICK SPECIES TO INJECT OR INSPECT • [×] TO CLOSE</text>
  
  <!-- Close Catalog Button -->
  <rect x="316" y="226" width="110" height="20" rx="2" fill="#0B1C2E" stroke="#38BDF8" stroke-width="1"/>
  <text x="371" y="239" font-family="monospace, sans-serif" font-size="7.5" font-weight="bold" fill="#38BDF8" text-anchor="middle">CLOSE CATALOG [×]</text>
'''

    # Helper to render an 8-card grid
    def render_8_card_grid(tab_idx, title, sub_title, page_nav_left, page_nav_right, cards):
        svg = ['<svg xmlns="http://www.w3.org/2000/svg" width="440" height="250" viewBox="0 0 440 250">']
        svg.append(base_comp_modal(tab_idx, title, sub_title))
        
        # Sub-header with page switcher
        svg.append('  <!-- Sub-header -->')
        svg.append('  <rect x="14" y="52" width="412" height="18" rx="2" fill="#0D1525" stroke="#1E293B" stroke-width="1"/>')
        svg.append('  <text x="24" y="64.5" font-family="monospace, sans-serif" font-size="7" fill="#64748B">CLICK SPECIES CARD TO INJECT INTO CHAMBER &amp; INSPECT</text>')
        
        # Page buttons on right
        svg.append(f'  <rect x="270" y="54" width="70" height="14" rx="2" fill="{page_nav_left[2]}" stroke="{page_nav_left[3]}" stroke-width="0.8"/>')
        svg.append(f'  <text x="305" y="64" font-family="monospace, sans-serif" font-size="6" font-weight="bold" fill="{page_nav_left[4]}" text-anchor="middle">{page_nav_left[0]}</text>')
        
        svg.append(f'  <rect x="348" y="54" width="70" height="14" rx="2" fill="{page_nav_right[2]}" stroke="{page_nav_right[3]}" stroke-width="0.8"/>')
        svg.append(f'  <text x="383" y="64" font-family="monospace, sans-serif" font-size="6" font-weight="bold" fill="{page_nav_right[4]}" text-anchor="middle">{page_nav_right[0]}</text>')

        # 2 rows of 4 cards
        for idx, card in enumerate(cards):
            row = idx // 4
            col = idx % 4
            x = 14 + col * 104
            y = 74 + row * 72
            
            formula = card['formula']
            disp_form = format_subscripts(formula)
            name = card['name'][:14]
            desc = card.get('recipe', card.get('desc', ''))[:20]
            tag = card.get('tag', 'INJECT')
            col_accent = card.get('accent', '#38BDF8')
            
            svg.append(f'  <g>')
            svg.append(f'    <rect x="{x}" y="{y}" width="98" height="68" rx="3" fill="#0D1525" stroke="{col_accent}" stroke-width="1"/>')
            # Formula box
            svg.append(f'    <rect x="{x+6}" y="{y+6}" width="86" height="24" rx="2" fill="#131E33"/>')
            svg.append(f'    <text x="{x+49}" y="{y+23}" font-family="sans-serif" font-size="13" font-weight="bold" fill="{col_accent}" text-anchor="middle">{disp_form}</text>')
            # Name
            svg.append(f'    <text x="{x+49}" y="{y+41}" font-family="sans-serif" font-size="7" font-weight="bold" fill="#F8FAFC" text-anchor="middle">{name}</text>')
            # Recipe / Description
            svg.append(f'    <text x="{x+49}" y="{y+51}" font-family="monospace, sans-serif" font-size="6" fill="#94A3B8" text-anchor="middle">{desc}</text>')
            # Button pill
            svg.append(f'    <rect x="{x+24}" y="{y+56}" width="50" height="9" rx="1.5" fill="#082032" stroke="{col_accent}" stroke-width="0.6"/>')
            svg.append(f'    <text x="{x+49}" y="{y+63.5}" font-family="monospace, sans-serif" font-size="5.5" font-weight="bold" fill="{col_accent}" text-anchor="middle">{tag}</text>')
            svg.append(f'  </g>')

        svg.append('</svg>')
        return "\n".join(svg)

    # 1. comp_summary (Overview Page)
    p1 = f'''<svg xmlns="http://www.w3.org/2000/svg" width="440" height="250" viewBox="0 0 440 250">
{base_comp_modal(1, "ARCHIVAL COMPENDIUM // OVERVIEW", "129 TOTAL SPECIES")}
  <!-- Archival Progress Meter (Y: 52 to 84) -->
  <rect x="14" y="52" width="412" height="32" rx="3" fill="#0D1525" stroke="#1E293B" stroke-width="1"/>
  <text x="26" y="65" font-family="monospace, sans-serif" font-size="7.5" fill="#64748B">ARCHIVAL COMPLETION STATUS</text>
  <text x="414" y="65" font-family="monospace, sans-serif" font-size="7.5" font-weight="bold" fill="#38BDF8" text-anchor="end">129 TARGET SPECIES</text>
  <rect x="26" y="71" width="388" height="6" rx="2" fill="#151E2E"/>
  <rect x="26" y="71" width="110" height="6" rx="2" fill="#38BDF8"/>

  <!-- 4 Interactive Category Jump Cards (Y: 90 to 216) -->
  <!-- Card 1: Atoms -->
  <rect x="14" y="90" width="98" height="124" rx="3" fill="#0D1626" stroke="#10B981" stroke-width="1"/>
  <text x="63" y="106" font-family="sans-serif" font-size="8" font-weight="bold" fill="#10B981" text-anchor="middle">BASE ATOMS</text>
  <text x="63" y="136" font-family="monospace, sans-serif" font-size="22" font-weight="bold" fill="#FFFFFF" text-anchor="middle">19</text>
  <text x="63" y="154" font-family="monospace, sans-serif" font-size="7" fill="#10B981" text-anchor="middle">100% UNLOCKED</text>
  <text x="63" y="168" font-family="monospace, sans-serif" font-size="6.5" fill="#64748B" text-anchor="middle">H through I</text>
  <rect x="22" y="186" width="82" height="18" rx="2" fill="#0E231C" stroke="#10B981" stroke-width="0.8"/>
  <text x="63" y="198" font-family="monospace, sans-serif" font-size="6.5" font-weight="bold" fill="#10B981" text-anchor="middle">OPEN ATOMS →</text>

  <!-- Card 2: Molecules -->
  <rect x="118" y="90" width="98" height="124" rx="3" fill="#0D1626" stroke="#38BDF8" stroke-width="1"/>
  <text x="167" y="106" font-family="sans-serif" font-size="8" font-weight="bold" fill="#38BDF8" text-anchor="middle">MOLECULES</text>
  <text x="167" y="136" font-family="monospace, sans-serif" font-size="22" font-weight="bold" fill="#FFFFFF" text-anchor="middle">75</text>
  <text x="167" y="154" font-family="monospace, sans-serif" font-size="7" fill="#FACC15" text-anchor="middle">SYNTHESIS REQ</text>
  <text x="167" y="168" font-family="monospace, sans-serif" font-size="6.5" fill="#64748B" text-anchor="middle">Water, Acids, Salts</text>
  <rect x="126" y="186" width="82" height="18" rx="2" fill="#0B2136" stroke="#38BDF8" stroke-width="0.8"/>
  <text x="167" y="198" font-family="monospace, sans-serif" font-size="6.5" font-weight="bold" fill="#38BDF8" text-anchor="middle">BROWSE MOLECULES →</text>

  <!-- Card 3: Radicals -->
  <rect x="222" y="90" width="98" height="124" rx="3" fill="#0D1626" stroke="#EF4444" stroke-width="1"/>
  <text x="271" y="106" font-family="sans-serif" font-size="8" font-weight="bold" fill="#EF4444" text-anchor="middle">RADICALS</text>
  <text x="271" y="136" font-family="monospace, sans-serif" font-size="22" font-weight="bold" fill="#FFFFFF" text-anchor="middle">13</text>
  <text x="271" y="154" font-family="monospace, sans-serif" font-size="7" fill="#EF4444" text-anchor="middle">UNPAIRED e⁻</text>
  <text x="271" y="168" font-family="monospace, sans-serif" font-size="6.5" fill="#64748B" text-anchor="middle">•CH3, •OH, •NO</text>
  <rect x="230" y="186" width="82" height="18" rx="2" fill="#241014" stroke="#EF4444" stroke-width="0.8"/>
  <text x="271" y="198" font-family="monospace, sans-serif" font-size="6.5" font-weight="bold" fill="#EF4444" text-anchor="middle">BROWSE RADICALS →</text>

  <!-- Card 4: Ions -->
  <rect x="326" y="90" width="98" height="124" rx="3" fill="#0D1626" stroke="#A855F7" stroke-width="1"/>
  <text x="375" y="106" font-family="sans-serif" font-size="8" font-weight="bold" fill="#A855F7" text-anchor="middle">CHARGED IONS</text>
  <text x="375" y="136" font-family="monospace, sans-serif" font-size="22" font-weight="bold" fill="#FFFFFF" text-anchor="middle">22</text>
  <text x="375" y="154" font-family="monospace, sans-serif" font-size="7" fill="#A855F7" text-anchor="middle">COSMIC IONIZED</text>
  <text x="375" y="168" font-family="monospace, sans-serif" font-size="6.5" fill="#64748B" text-anchor="middle">Cations &amp; Anions</text>
  <rect x="334" y="186" width="82" height="18" rx="2" fill="#1C102E" stroke="#A855F7" stroke-width="0.8"/>
  <text x="375" y="198" font-family="monospace, sans-serif" font-size="6.5" font-weight="bold" fill="#A855F7" text-anchor="middle">BROWSE IONS →</text>
</svg>'''
    costumes["comp_summary"] = make_svg_asset(p1, "comp_summary", 220, 125)

    # 2. comp_elements (Atoms Injection Array)
    el_svg = ['<svg xmlns="http://www.w3.org/2000/svg" width="440" height="250" viewBox="0 0 440 250">']
    el_svg.append(base_comp_modal(2, "ARCHIVAL COMPENDIUM // 19 BASE ATOMS", "INJECTION ARRAY"))
    el_svg.append('  <!-- Header Sub-banner -->')
    el_svg.append('  <rect x="14" y="52" width="412" height="16" rx="2" fill="#0C1F2E" stroke="#0284C7" stroke-width="0.8"/>')
    el_svg.append('  <text x="220" y="63" font-family="monospace, sans-serif" font-size="7" font-weight="bold" fill="#38BDF8" text-anchor="middle">ATOMIC INJECTOR — CLICK ANY ELEMENT TO INJECT INTO VACUUM CHAMBER</text>')

    row1 = db_chemistry.SPECIES[:10]
    row2 = db_chemistry.SPECIES[10:19]

    # Row 1 (10 elements)
    for i, el in enumerate(row1):
        x = 14 + i * 41.2
        y = 72
        color = el["color"]
        border = el["border"]
        fg = "#0A0F1A" if color in ["#E2E8F0", "#FACC15", "#A3E635", "#67E8F9"] else "#FFFFFF"
        el_svg.append(f'  <g>')
        el_svg.append(f'    <rect x="{x}" y="{y}" width="39" height="68" rx="3" fill="#0E1626" stroke="{border}" stroke-width="1"/>')
        el_svg.append(f'    <text x="{x+5}" y="{y+11}" font-family="monospace, sans-serif" font-size="6.5" fill="#64748B">{el["z"]}</text>')
        el_svg.append(f'    <circle cx="{x+19.5}" cy="{y+26}" r="11" fill="{color}" stroke="{border}" stroke-width="1"/>')
        el_svg.append(f'    <text x="{x+19.5}" y="{y+30}" font-family="sans-serif" font-size="9" font-weight="bold" fill="{fg}" text-anchor="middle">{el["symbol"]}</text>')
        el_svg.append(f'    <text x="{x+19.5}" y="{y+48}" font-family="sans-serif" font-size="5.5" font-weight="bold" fill="#CBD5E1" text-anchor="middle">{el["name"][:7]}</text>')
        el_svg.append(f'    <text x="{x+19.5}" y="{y+60}" font-family="monospace, sans-serif" font-size="5.5" fill="#10B981" text-anchor="middle">INJECT</text>')
        el_svg.append(f'  </g>')

    # Row 2 (9 elements)
    for i, el in enumerate(row2):
        x = 34 + i * 41.2
        y = 144
        color = el["color"]
        border = el["border"]
        fg = "#0A0F1A" if color in ["#E2E8F0", "#FACC15", "#A3E635", "#67E8F9"] else "#FFFFFF"
        el_svg.append(f'  <g>')
        el_svg.append(f'    <rect x="{x}" y="{y}" width="39" height="68" rx="3" fill="#0E1626" stroke="{border}" stroke-width="1"/>')
        el_svg.append(f'    <text x="{x+5}" y="{y+11}" font-family="monospace, sans-serif" font-size="6.5" fill="#64748B">{el["z"]}</text>')
        el_svg.append(f'    <circle cx="{x+19.5}" cy="{y+26}" r="11" fill="{color}" stroke="{border}" stroke-width="1"/>')
        el_svg.append(f'    <text x="{x+19.5}" y="{y+30}" font-family="sans-serif" font-size="9" font-weight="bold" fill="{fg}" text-anchor="middle">{el["symbol"]}</text>')
        el_svg.append(f'    <text x="{x+19.5}" y="{y+48}" font-family="sans-serif" font-size="5.5" font-weight="bold" fill="#CBD5E1" text-anchor="middle">{el["name"][:7]}</text>')
        el_svg.append(f'    <text x="{x+19.5}" y="{y+60}" font-family="monospace, sans-serif" font-size="5.5" fill="#10B981" text-anchor="middle">INJECT</text>')
        el_svg.append(f'  </g>')

    el_svg.append('</svg>')
    costumes["comp_elements"] = make_svg_asset("\n".join(el_svg), "comp_elements", 220, 125)

    # 3. comp_molecules_1
    mol1_cards = [
        {"formula": "H2", "name": "Hydrogen Gas", "recipe": "H + H → H2", "accent": "#38BDF8"},
        {"formula": "H2O", "name": "Water", "recipe": "2H + O → H2O", "accent": "#38BDF8"},
        {"formula": "O2", "name": "Oxygen Gas", "recipe": "O + O → O2", "accent": "#38BDF8"},
        {"formula": "N2", "name": "Nitrogen Gas", "recipe": "N + N → N2", "accent": "#38BDF8"},
        {"formula": "CO", "name": "Carbon Monoxide", "recipe": "C + O → CO", "accent": "#38BDF8"},
        {"formula": "CO2", "name": "Carbon Dioxide", "recipe": "CO + O → CO2", "accent": "#38BDF8"},
        {"formula": "CH4", "name": "Methane", "recipe": "C + 4H → CH4", "accent": "#38BDF8"},
        {"formula": "NH3", "name": "Ammonia", "recipe": "N + 3H → NH3", "accent": "#38BDF8"}
    ]
    p3 = render_8_card_grid(
        3, "ARCHIVAL COMPENDIUM // NEUTRAL MOLECULES (1/2)", "COMMON COMPOUNDS",
        ("PAGE 1 (CURR)", 1, "#0B2238", "#38BDF8", "#38BDF8"),
        ("NEXT: P2", 2, "#111827", "#334155", "#94A3B8"),
        mol1_cards
    )
    costumes["comp_molecules_1"] = make_svg_asset(p3, "comp_molecules_1", 220, 125)

    # 4. comp_molecules_2
    mol2_cards = [
        {"formula": "HCl", "name": "Hydrochloric Acid", "recipe": "H + Cl → HCl", "accent": "#38BDF8"},
        {"formula": "NaCl", "name": "Sodium Chloride", "recipe": "Na + Cl → NaCl", "accent": "#38BDF8"},
        {"formula": "H2S", "name": "Hydrogen Sulfide", "recipe": "2H + S → H2S", "accent": "#38BDF8"},
        {"formula": "SO2", "name": "Sulfur Dioxide", "recipe": "S + O2 → SO2", "accent": "#38BDF8"},
        {"formula": "H2SO4", "name": "Sulfuric Acid", "recipe": "SO3 + H2O → H2SO4", "accent": "#38BDF8"},
        {"formula": "SiO2", "name": "Silicon Dioxide", "recipe": "Si + O2 → SiO2", "accent": "#38BDF8"},
        {"formula": "P4O10", "name": "Phosphorus Oxide", "recipe": "P4 + 5O2 → P4O10", "accent": "#38BDF8"},
        {"formula": "CaCO3", "name": "Calcium Carbonate", "recipe": "CaO + CO2 → CaCO3", "accent": "#38BDF8"}
    ]
    p4 = render_8_card_grid(
        3, "ARCHIVAL COMPENDIUM // NEUTRAL MOLECULES (2/2)", "ACIDS &amp; SALTS",
        ("PREV: P1", 1, "#111827", "#334155", "#94A3B8"),
        ("PAGE 2 (CURR)", 2, "#0B2238", "#38BDF8", "#38BDF8"),
        mol2_cards
    )
    costumes["comp_molecules_2"] = make_svg_asset(p4, "comp_molecules_2", 220, 125)

    # 5. comp_radicals
    rad_cards = [
        {"formula": "CH•", "name": "Methylidyne", "recipe": "Photolysis C-H", "accent": "#EF4444"},
        {"formula": "CH2•", "name": "Methylene", "recipe": "Photolysis CH3", "accent": "#EF4444"},
        {"formula": "CH3•", "name": "Methyl Radical", "recipe": "CH4 + hν → CH3•", "accent": "#EF4444"},
        {"formula": "NH•", "name": "Imidogen", "recipe": "Photolysis NH2", "accent": "#EF4444"},
        {"formula": "NH2•", "name": "Amino Radical", "recipe": "NH3 + hν → NH2•", "accent": "#EF4444"},
        {"formula": "NO•", "name": "Nitric Oxide", "recipe": "N + O radical", "accent": "#EF4444"},
        {"formula": "OH•", "name": "Hydroxyl Radical", "recipe": "H2O + hν → •OH", "accent": "#EF4444"},
        {"formula": "HS•", "name": "Mercapto Radical", "recipe": "H2S + hν → HS•", "accent": "#EF4444"}
    ]
    p5 = render_8_card_grid(
        4, "ARCHIVAL COMPENDIUM // RADICAL SPECIES", "UNPAIRED ELECTRONS",
        ("RADICALS", 1, "#251015", "#EF4444", "#EF4444"),
        ("UV ACTIVE", 2, "#111827", "#334155", "#64748B"),
        rad_cards
    )
    costumes["comp_radicals"] = make_svg_asset(p5, "comp_radicals", 220, 125)

    # 6. comp_ions
    ion_cards = [
        {"formula": "H+", "name": "Hydron Cation", "recipe": "H - e⁻ → H+", "accent": "#A855F7"},
        {"formula": "OH-", "name": "Hydroxide Anion", "recipe": "H2O + e⁻ → OH-", "accent": "#A855F7"},
        {"formula": "Na+", "name": "Sodium Cation", "recipe": "Na - e⁻ → Na+", "accent": "#A855F7"},
        {"formula": "Cl-", "name": "Chloride Anion", "recipe": "Cl + e⁻ → Cl-", "accent": "#A855F7"},
        {"formula": "H3O+", "name": "Hydronium Cation", "recipe": "H+ + H2O → H3O+", "accent": "#A855F7"},
        {"formula": "SO4-2", "name": "Sulfate Dianion", "recipe": "H2SO4 deproton", "accent": "#A855F7"},
        {"formula": "CO3-2", "name": "Carbonate Dianion", "recipe": "H2CO3 deproton", "accent": "#A855F7"},
        {"formula": "PO4-3", "name": "Phosphate Trianion", "recipe": "H3PO4 deproton", "accent": "#A855F7"}
    ]
    p6 = render_8_card_grid(
        5, "ARCHIVAL COMPENDIUM // CHARGED IONS", "COSMIC IONIZATION",
        ("IONS", 1, "#1D102E", "#A855F7", "#A855F7"),
        ("COSMIC RAYS", 2, "#111827", "#334155", "#64748B"),
        ion_cards
    )
    costumes["comp_ions"] = make_svg_asset(p6, "comp_ions", 220, 125)

    return costumes

# --- 10. Live Telemetry Console Strips ---
def generate_telemetry_assets():
    costumes = {}
    messages = [
        ("telem_ready", "#10B981", "> CHAMBER DETECTOR ONLINE • ULTRA-HIGH VACUUM 10⁻¹⁰ TORR • READY FOR REACTIONS"),
        ("telem_react", "#38BDF8", "> CHEMICAL REACTION: Molecular bond synthesized successfully"),
        ("telem_exo", "#F97316", "⚡ EXOTHERMIC REACTION: Thermal energy burst released • Photon emitted"),
        ("telem_uv_req", "#C084FC", "⚡ UV RADIANCE REQUIRED: Photolysis requires ultraviolet lamp activation"),
        ("telem_cosmic", "#38BDF8", "⚡ COSMIC RAY IMPACT: Relativistic collision created ionized species"),
        ("telem_inert", "#64748B", "> INERT COLLISION: Reagents have no reactive pathway under current conditions"),
        ("telem_discover", "#FACC15", "★ NEW DISCOVERY: Novel chemical compound cataloged in laboratory archive"),
        ("telem_frozen", "#7DD3FC", "❄ CRYO STASIS ENGAGED: Thermal velocities and reaction clocks suspended"),
        ("telem_save", "#60A5FA", "> DATA REGISTER: Discovery snapshot successfully exported"),
        ("telem_load", "#818CF8", "> DATA REGISTER: Chemical discoveries restored from snapshot"),
        ("telem_purge", "#F87171", "> VACUUM FLUSH: Particle containment purged • Chamber evacuated")
    ]

    for name, col, text in messages:
        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="460" height="22" viewBox="0 0 460 22">
  <rect width="460" height="22" rx="3" fill="#080C16" stroke="#1E293B" stroke-width="1"/>
  <circle cx="10" cy="11" r="3" fill="{col}"/>
  <text x="20" y="14" font-family="monospace, sans-serif" font-size="7.5" font-weight="bold" fill="{col}">{text[:75]}</text>
</svg>'''
        costumes[name] = make_svg_asset(svg, name, 230, 11)

    return costumes


# --- Master Generation Routine ---
def generate_all_assets():
    os.makedirs("/workspaces/scratch/assets", exist_ok=True)
    costumes = {}

    # 1. 129 Species Costumes
    for s in db_chemistry.SPECIES:
        svg_text = generate_species_svg(s)
        asset = make_svg_asset(svg_text, f"species_{s['id']}", 32, 32)
        costumes[f"species_{s['id']}"] = asset

    # 2. Stage Backdrops
    bg_std, bg_uv, bg_freeze = generate_backdrops()
    costumes["backdrop_vacuum"] = make_svg_asset(bg_std, "backdrop_vacuum", 240, 180)
    costumes["backdrop_uv"] = make_svg_asset(bg_uv, "backdrop_uv", 240, 180)
    costumes["backdrop_frozen"] = make_svg_asset(bg_freeze, "backdrop_frozen", 240, 180)

    # 3. Precision Buttons (10 Tools)
    tools = [
        ("add", "ADD", "#10B981"),
        ("del", "DEL", "#EF4444"),
        ("insp", "INSP", "#F59E0B"),
        ("uv", "UV", "#A855F7"),
        ("freeze", "CRYO", "#38BDF8"),
        ("catalog", "CATALOG", "#6366F1"),
        ("audio", "AUDIO", "#14B8A6"),
        ("save", "REGISTER", "#3B82F6"),
        ("help", "GUIDE", "#8B5CF6"),
        ("purge", "PURGE", "#DC2626")
    ]
    for tool_name, label, act_col in tools:
        svg_norm = generate_vector_button(tool_name, label, active=False)
        svg_act = generate_vector_button(tool_name, label, active=True, custom_active_col=act_col)
        costumes[f"btn_{tool_name}"] = make_svg_asset(svg_norm, f"btn_{tool_name}", 22, 14)
        costumes[f"btn_{tool_name}_active"] = make_svg_asset(svg_act, f"btn_{tool_name}_active", 22, 14)

    # Special audio muted costume
    svg_mut = generate_vector_button("audio_muted", "MUTED", active=True, custom_active_col="#64748B")
    costumes["btn_audio_muted"] = make_svg_asset(svg_mut, "btn_audio_muted", 22, 14)

    # 4. Spawner Palette Drawer
    pal_svg = generate_palette_drawer()
    costumes["palette_drawer"] = make_svg_asset(pal_svg, "palette_drawer", 230, 52)

    # 5. Inspector Cards (129 HUD cards)
    for s in db_chemistry.SPECIES:
        c_svg = generate_inspector_card(s)
        costumes[f"card_{s['id']}"] = make_svg_asset(c_svg, f"card_{s['id']}", 90, 77)

    # 6. Onboarding Card
    onb_svg = generate_onboarding_card()
    costumes["onboarding_card"] = make_svg_asset(onb_svg, "onboarding_card", 210, 110)

    # 7. Compendium Pages
    costumes.update(generate_compendium_assets())

    # 8. Live Telemetry Strips
    costumes.update(generate_telemetry_assets())

    # 9. Visual Effects & Particles
    fx_dict = generate_fx_assets()
    costumes.update(fx_dict)

    print(f"SUCCESS: Generated {len(costumes)} verified vector graphic assets!")
    return costumes

if __name__ == "__main__":
    generate_all_assets()
