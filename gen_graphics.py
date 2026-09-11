import os, hashlib, xml.etree.ElementTree as ET
import db_chemistry

def make_svg_asset(svg_text, name, cx, cy):
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

# --- 1. 129 Authentic Chemical Species (Clean, Human-Crafted Vectors) ---
def generate_species_svg(s):
    sym = s["symbol"]
    charge = s["charge"]
    color = s["color"]
    border = s["border"]
    sid = s["id"]

    is_ion = charge != 0
    is_radical = "•" in sym
    is_element = sid <= 19

    disp_text = format_subscripts(sym)
    text_len = len(disp_text)
    if text_len > 7:
        font_size = "9.5"
    elif text_len > 5:
        font_size = "11"
    elif text_len > 3:
        font_size = "13"
    elif text_len > 2:
        font_size = "15"
    else:
        font_size = "17"

    svg = ['<svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 64 64">']
    grad_id = f"g_{sid}"
    svg.append('  <defs>')
    svg.append(f'    <radialGradient id="{grad_id}" cx="35%" cy="32%" r="65%">')
    svg.append(f'      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.85"/>')
    svg.append(f'      <stop offset="45%" stop-color="{color}" stop-opacity="0.95"/>')
    svg.append(f'      <stop offset="100%" stop-color="{border}" stop-opacity="1.0"/>')
    svg.append('    </radialGradient>')
    svg.append('  </defs>')

    text_color = "#0F172A" if color in ["#E2E8F0", "#FACC15", "#A3E635", "#67E8F9"] else "#FFFFFF"

    if is_element:
        # Authentic CPK Element Spheres with proportional atomic radii
        z = s.get("z", 1)
        if z <= 2:
            r = 19
        elif z <= 10:
            r = 21
        elif z <= 18:
            r = 23
        else:
            r = 25

        # Soft outer valence orbit line
        svg.append(f'  <circle cx="32" cy="32" r="{r+2.5}" fill="none" stroke="{border}" stroke-width="0.75" stroke-dasharray="2,2" opacity="0.45"/>')
        # Core atom sphere
        svg.append(f'  <circle cx="32" cy="32" r="{r}" fill="url(#{grad_id})" stroke="{border}" stroke-width="1.8"/>')
        # Atomic number badge in top-left
        svg.append(f'  <rect x="{32-r}" y="{32-r}" width="13" height="10" rx="3" fill="#0F172A" stroke="{border}" stroke-width="0.8" opacity="0.9"/>')
        svg.append(f'  <text x="{32-r+6.5}" y="{32-r+7.5}" font-family="system-ui, -apple-system, sans-serif" font-size="6.5" font-weight="bold" fill="#38BDF8" text-anchor="middle">{z}</text>')
        # Chemical symbol
        svg.append(f'  <text x="32" y="37" font-family="system-ui, -apple-system, sans-serif" font-size="{font_size}" font-weight="bold" fill="{text_color}" text-anchor="middle">{disp_text}</text>')

    elif is_ion:
        # Structured Ions: distinct halo and signed charge badge
        halo_color = "#38BDF8" if charge > 0 else "#FB7185"
        # Ionization boundary halo
        svg.append(f'  <circle cx="32" cy="32" r="26" fill="none" stroke="{halo_color}" stroke-width="1.8" stroke-dasharray="3,2" opacity="0.85"/>')
        # Core sphere
        svg.append(f'  <circle cx="32" cy="32" r="21" fill="url(#{grad_id})" stroke="{border}" stroke-width="1.8"/>')
        # Formula text
        svg.append(f'  <text x="32" y="37" font-family="system-ui, -apple-system, sans-serif" font-size="{font_size}" font-weight="bold" fill="{text_color}" text-anchor="middle">{disp_text}</text>')
        # Signed charge pill in upper right
        ch_text = "+" if charge == 1 else ("-" if charge == -1 else (f"{charge}+" if charge > 0 else f"{abs(charge)}-"))
        svg.append(f'  <circle cx="48" cy="16" r="8" fill="#0F172A" stroke="{halo_color}" stroke-width="1.5"/>')
        svg.append(f'  <text x="48" y="19.5" font-family="system-ui, -apple-system, sans-serif" font-size="8.5" font-weight="bold" fill="{halo_color}" text-anchor="middle">{ch_text}</text>')

    else:
        # Covalent Molecules & Radicals
        is_diatomic = any(sym.endswith("2") and len(sym) <= 3 for _ in [0]) or sym in ["CO", "NO•", "NH•", "HCl", "HF", "HBr", "HI", "NaCl", "KCl", "CaO", "SiO", "PN", "NaF", "KF", "NaBr", "KBr", "NaI", "KI", "CN"]
        if is_diatomic:
            # Overlapping covalent dual-sphere dumbbell
            svg.append(f'  <rect x="9" y="17" width="46" height="30" rx="15" fill="url(#{grad_id})" stroke="{border}" stroke-width="1.8"/>')
            svg.append(f'  <line x1="20" y1="32" x2="44" y2="32" stroke="#FFFFFF" stroke-width="1" stroke-opacity="0.35" stroke-dasharray="2,2"/>')
        else:
            # Polyatomic molecular cluster capsule
            svg.append(f'  <rect x="6" y="16" width="52" height="32" rx="10" fill="url(#{grad_id})" stroke="{border}" stroke-width="1.8"/>')
            svg.append(f'  <line x1="14" y1="27" x2="50" y2="27" stroke="#FFFFFF" stroke-width="0.8" stroke-opacity="0.25" stroke-dasharray="2,2"/>')
            svg.append(f'  <line x1="14" y1="37" x2="50" y2="37" stroke="#FFFFFF" stroke-width="0.8" stroke-opacity="0.25" stroke-dasharray="2,2"/>')

        # Formula text
        svg.append(f'  <text x="32" y="37" font-family="system-ui, -apple-system, sans-serif" font-size="{font_size}" font-weight="bold" fill="{text_color}" text-anchor="middle">{disp_text}</text>')

        # Distinct radical dot indicator
        if is_radical:
            svg.append(f'  <circle cx="50" cy="16" r="4.5" fill="#EF4444" stroke="#FFFFFF" stroke-width="1.2"/>')
            svg.append(f'  <circle cx="50" cy="16" r="1.8" fill="#FFFFFF"/>')

    svg.append('</svg>')
    return "\n".join(svg)


# --- 2. Stage Backdrops: Clean, Approachable Educational Laboratory ---
def generate_backdrops():
    # 480x360 stage
    def base_stage_canvas():
        return '''
  <!-- Main Stage Canvas Background -->
  <rect width="480" height="360" fill="#0F172A"/>
  
  <!-- Clean Top Header Bar (Y: 0 to 24) -->
  <rect x="0" y="0" width="480" height="24" fill="#1E293B"/>
  <line x1="0" y1="24" x2="480" y2="24" stroke="#334155" stroke-width="1"/>
  
  <!-- Header Title & Icon -->
  <circle cx="16" cy="12" r="5" fill="#38BDF8"/>
  <text x="28" y="16" font-family="system-ui, -apple-system, sans-serif" font-size="11" font-weight="bold" fill="#F8FAFC">The Chemistry Lab</text>
  <text x="240" y="16" font-family="system-ui, -apple-system, sans-serif" font-size="8.5" fill="#94A3B8" text-anchor="middle">Interactive Reaction Sandbox • 129 Species to Discover</text>
  <text x="466" y="16" font-family="system-ui, -apple-system, sans-serif" font-size="8.5" font-weight="bold" fill="#F59E0B" text-anchor="end">EXPERIMENT ACTIVE</text>
  
  <!-- Tool Rail Tray (Y: 24 to 56) -->
  <rect x="0" y="24" width="480" height="32" fill="#131D31"/>
  <line x1="0" y1="56" x2="480" y2="56" stroke="#1E293B" stroke-width="1"/>

  <!-- Main Reaction Chamber (Y: 58 to 330, width 468, x: 6 to 474) -->
  <rect x="6" y="58" width="468" height="270" rx="8" fill="#0B1120" stroke="#1E293B" stroke-width="1.5"/>

  <!-- Bottom Event Feedback Bar (Y: 332 to 358) -->
  <rect x="0" y="332" width="480" height="28" fill="#1E293B"/>
  <line x1="0" y1="332" x2="480" y2="332" stroke="#334155" stroke-width="1"/>
'''

    # Standard Neutral Sandbox
    bg_std = f'''<svg xmlns="http://www.w3.org/2000/svg" width="480" height="360" viewBox="0 0 480 360">
{base_stage_canvas()}
</svg>'''

    # Ultraviolet Illumination Mode
    bg_uv = f'''<svg xmlns="http://www.w3.org/2000/svg" width="480" height="360" viewBox="0 0 480 360">
  <defs>
    <linearGradient id="uv_glow" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#8B5CF6" stop-opacity="0.25"/>
      <stop offset="50%" stop-color="#8B5CF6" stop-opacity="0.08"/>
      <stop offset="100%" stop-color="#8B5CF6" stop-opacity="0.0"/>
    </linearGradient>
  </defs>
{base_stage_canvas()}
  <!-- Soft UV Irradiation Wash -->
  <rect x="7" y="59" width="466" height="268" rx="7" fill="url(#uv_glow)"/>
  <rect x="6" y="58" width="468" height="270" rx="8" fill="none" stroke="#8B5CF6" stroke-width="1.5" opacity="0.7"/>
  
  <!-- Subtle State Banner -->
  <rect x="150" y="66" width="180" height="18" rx="4" fill="#1E293B" stroke="#8B5CF6" stroke-width="1"/>
  <text x="240" y="79" font-family="system-ui, -apple-system, sans-serif" font-size="8.5" font-weight="bold" fill="#C084FC" text-anchor="middle">⚡ Ultraviolet Light Active • Photolysis Enabled</text>
</svg>'''

    # Cryostatic Freeze Mode
    bg_freeze = f'''<svg xmlns="http://www.w3.org/2000/svg" width="480" height="360" viewBox="0 0 480 360">
  <defs>
    <linearGradient id="frost_glow" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#0284C7" stop-opacity="0.22"/>
      <stop offset="100%" stop-color="#0284C7" stop-opacity="0.04"/>
    </linearGradient>
  </defs>
{base_stage_canvas()}
  <!-- Soft Cryostatic Tint -->
  <rect x="7" y="59" width="466" height="268" rx="7" fill="url(#frost_glow)"/>
  <rect x="6" y="58" width="468" height="270" rx="8" fill="none" stroke="#38BDF8" stroke-width="1.5" opacity="0.75"/>
  
  <!-- Subtle State Banner -->
  <rect x="160" y="66" width="160" height="18" rx="4" fill="#1E293B" stroke="#38BDF8" stroke-width="1"/>
  <text x="240" y="79" font-family="system-ui, -apple-system, sans-serif" font-size="8.5" font-weight="bold" fill="#7DD3FC" text-anchor="middle">❄ Time Frozen • Clocks Paused</text>
</svg>'''

    return bg_std, bg_uv, bg_freeze


# --- 3. Professional Tactile Tool Rail Buttons ---
def generate_vector_button(tool_name, label, active=False, custom_active_col=None):
    # 44x28 button geometry, center 22, 14
    act_col = custom_active_col or "#38BDF8"
    bg = "#1E293B" if not active else "#0E2A47"
    border = "#334155" if not active else act_col
    fg = "#F1F5F9" if not active else act_col
    sub_fg = "#94A3B8" if not active else act_col

    icons = {
        "add": '''
          <circle cx="22" cy="10" r="6.5" fill="none" stroke="{fg}" stroke-width="1.2"/>
          <line x1="22" y1="6.5" x2="22" y2="13.5" stroke="{fg}" stroke-width="1.8" stroke-linecap="round"/>
          <line x1="18.5" y1="10" x2="25.5" y2="10" stroke="{fg}" stroke-width="1.8" stroke-linecap="round"/>
        ''',
        "del": '''
          <rect x="17" y="7" width="10" height="7" rx="1" fill="none" stroke="{fg}" stroke-width="1.3"/>
          <line x1="15" y1="7" x2="29" y2="7" stroke="{fg}" stroke-width="1.4" stroke-linecap="round"/>
          <line x1="20" y1="5" x2="24" y2="5" stroke="{fg}" stroke-width="1.2" stroke-linecap="round"/>
        ''',
        "insp": '''
          <circle cx="21" cy="9" r="5" fill="none" stroke="{fg}" stroke-width="1.4"/>
          <line x1="25" y1="13" x2="28" y2="16" stroke="{fg}" stroke-width="1.8" stroke-linecap="round"/>
        ''',
        "uv": '''
          <circle cx="22" cy="10" r="4" fill="none" stroke="{fg}" stroke-width="1.3"/>
          <line x1="22" y1="3" x2="22" y2="5" stroke="{fg}" stroke-width="1.3" stroke-linecap="round"/>
          <line x1="22" y1="15" x2="22" y2="17" stroke="{fg}" stroke-width="1.3" stroke-linecap="round"/>
          <line x1="15" y1="10" x2="17" y2="10" stroke="{fg}" stroke-width="1.3" stroke-linecap="round"/>
          <line x1="27" y1="10" x2="29" y2="10" stroke="{fg}" stroke-width="1.3" stroke-linecap="round"/>
        ''',
        "freeze": '''
          <line x1="22" y1="4" x2="22" y2="16" stroke="{fg}" stroke-width="1.3" stroke-linecap="round"/>
          <line x1="16" y1="7" x2="28" y2="13" stroke="{fg}" stroke-width="1.3" stroke-linecap="round"/>
          <line x1="16" y1="13" x2="28" y2="7" stroke="{fg}" stroke-width="1.3" stroke-linecap="round"/>
          <circle cx="22" cy="10" r="1.5" fill="{fg}"/>
        ''',
        "catalog": '''
          <rect x="16" y="5" width="12" height="10" rx="1.5" fill="none" stroke="{fg}" stroke-width="1.3"/>
          <line x1="22" y1="5" x2="22" y2="15" stroke="{fg}" stroke-width="1"/>
          <line x1="18" y1="8" x2="20" y2="8" stroke="{fg}" stroke-width="1"/>
          <line x1="24" y1="8" x2="26" y2="8" stroke="{fg}" stroke-width="1"/>
          <line x1="18" y1="11" x2="20" y2="11" stroke="{fg}" stroke-width="1"/>
          <line x1="24" y1="11" x2="26" y2="11" stroke="{fg}" stroke-width="1"/>
        ''',
        "audio": '''
          <polygon points="16,8 19,8 23,5 23,15 19,12 16,12" fill="{fg}"/>
          <path d="M 25 7 Q 27 10 25 13" fill="none" stroke="{fg}" stroke-width="1.2" stroke-linecap="round"/>
          <path d="M 27 5 Q 30 10 27 15" fill="none" stroke="{fg}" stroke-width="1.2" stroke-linecap="round"/>
        ''',
        "audio_muted": '''
          <polygon points="16,8 19,8 23,5 23,15 19,12 16,12" fill="{fg}"/>
          <line x1="15" y1="15" x2="29" y2="5" stroke="#EF4444" stroke-width="1.8" stroke-linecap="round"/>
        ''',
        "save": '''
          <rect x="17" y="5" width="10" height="9" rx="1.5" fill="none" stroke="{fg}" stroke-width="1.3"/>
          <rect x="19" y="5" width="6" height="4" fill="{fg}"/>
        ''',
        "help": '''
          <circle cx="22" cy="10" r="6.5" fill="none" stroke="{fg}" stroke-width="1.3"/>
          <text x="22" y="13.5" font-family="system-ui, -apple-system, sans-serif" font-size="9" font-weight="bold" fill="{fg}" text-anchor="middle">?</text>
        ''',
        "purge": '''
          <path d="M 22 5 A 5 5 0 1 1 17 12" fill="none" stroke="{fg}" stroke-width="1.4" stroke-linecap="round"/>
          <polyline points="20,4 23,5 22,8" fill="none" stroke="{fg}" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"/>
        '''
    }

    icon_svg = icons.get(tool_name, "").replace("{fg}", fg)

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="44" height="28" viewBox="0 0 44 28">
  <rect x="1" y="1" width="42" height="26" rx="5" fill="{bg}" stroke="{border}" stroke-width="1.2"/>
  {icon_svg}
  <text x="22" y="24" font-family="system-ui, -apple-system, sans-serif" font-size="7" font-weight="bold" fill="{sub_fg}" text-anchor="middle">{label}</text>
</svg>'''
    return svg


# --- 4. Clean Periodic Element Palette Drawer ---
def generate_palette_drawer():
    # 460x105 drawer, center 230, 52
    svg = ['<svg xmlns="http://www.w3.org/2000/svg" width="460" height="105" viewBox="0 0 460 105">']
    svg.append('  <!-- Drawer Surface -->')
    svg.append('  <rect width="460" height="105" rx="6" fill="#131D31" stroke="#334155" stroke-width="1.5"/>')
    svg.append('  <!-- Header Title -->')
    svg.append('  <rect x="0" y="0" width="460" height="22" rx="6" fill="#1E293B"/>')
    svg.append('  <line x1="0" y1="22" x2="460" y2="22" stroke="#334155" stroke-width="1"/>')
    svg.append('  <text x="16" y="15" font-family="system-ui, -apple-system, sans-serif" font-size="9.5" font-weight="bold" fill="#38BDF8">PERIODIC ELEMENT SELECTOR</text>')
    svg.append('  <text x="444" y="15" font-family="system-ui, -apple-system, sans-serif" font-size="8.5" fill="#94A3B8" text-anchor="end">Click any element to add to chamber</text>')

    row1 = db_chemistry.SPECIES[:10]
    row2 = db_chemistry.SPECIES[10:19]

    for i, el in enumerate(row1):
        x = 14 + i * 44
        y = 26
        color = el["color"]
        border = el["border"]
        fg = "#0F172A" if color in ["#E2E8F0", "#FACC15", "#A3E635", "#67E8F9"] else "#FFFFFF"
        svg.append(f'  <g>')
        svg.append(f'    <rect x="{x}" y="{y}" width="40" height="34" rx="4" fill="#1E293B" stroke="{border}" stroke-width="1.2"/>')
        svg.append(f'    <circle cx="{x+20}" cy="{y+14}" r="9.5" fill="{color}" stroke="{border}" stroke-width="1"/>')
        svg.append(f'    <text x="{x+20}" y="{y+17.5}" font-family="system-ui, -apple-system, sans-serif" font-size="9" font-weight="bold" fill="{fg}" text-anchor="middle">{el["symbol"]}</text>')
        svg.append(f'    <text x="{x+20}" y="{y+30}" font-family="system-ui, -apple-system, sans-serif" font-size="6.5" font-weight="bold" fill="#94A3B8" text-anchor="middle">{el["name"][:5]}</text>')
        svg.append(f'  </g>')

    for i, el in enumerate(row2):
        x = 36 + i * 44
        y = 64
        color = el["color"]
        border = el["border"]
        fg = "#0F172A" if color in ["#E2E8F0", "#FACC15", "#A3E635", "#67E8F9"] else "#FFFFFF"
        svg.append(f'  <g>')
        svg.append(f'    <rect x="{x}" y="{y}" width="40" height="34" rx="4" fill="#1E293B" stroke="{border}" stroke-width="1.2"/>')
        svg.append(f'    <circle cx="{x+20}" cy="{y+14}" r="9.5" fill="{color}" stroke="{border}" stroke-width="1"/>')
        svg.append(f'    <text x="{x+20}" y="{y+17.5}" font-family="system-ui, -apple-system, sans-serif" font-size="9" font-weight="bold" fill="{fg}" text-anchor="middle">{el["symbol"]}</text>')
        svg.append(f'    <text x="{x+20}" y="{y+30}" font-family="system-ui, -apple-system, sans-serif" font-size="6.5" font-weight="bold" fill="#94A3B8" text-anchor="middle">{el["name"][:5]}</text>')
        svg.append(f'  </g>')

    svg.append('</svg>')
    return "\n".join(svg)


# --- 5. Clean Compound Inspector Card (129 HUD Cards) ---
def generate_inspector_card(s):
    # 180x155 card, center 90, 77
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

    ch_str = "Neutral (0)" if charge == 0 else (f"Cation (+{charge})" if charge > 0 else f"Anion ({charge})")
    ch_col = "#94A3B8" if charge == 0 else ("#38BDF8" if charge > 0 else "#FB7185")

    text_color = "#0F172A" if color in ["#E2E8F0", "#FACC15", "#A3E635", "#67E8F9"] else "#FFFFFF"

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="180" height="155" viewBox="0 0 180 155">
  <!-- Card Base Surface -->
  <rect width="180" height="155" rx="8" fill="#131D31" stroke="#334155" stroke-width="1.5"/>
  
  <!-- Header Bar -->
  <rect x="0" y="0" width="180" height="22" rx="8" fill="#1E293B"/>
  <line x1="0" y1="22" x2="180" y2="22" stroke="#334155" stroke-width="1"/>
  <text x="12" y="15" font-family="system-ui, -apple-system, sans-serif" font-size="9" font-weight="bold" fill="#38BDF8">Compound Analysis</text>
  <text x="168" y="15" font-family="system-ui, -apple-system, sans-serif" font-size="8" font-weight="bold" fill="#64748B" text-anchor="end">#{sid}</text>

  <!-- Large Visual Formula Box -->
  <rect x="12" y="28" width="46" height="34" rx="6" fill="{color}" stroke="{border}" stroke-width="1.5"/>
  <text x="35" y="50" font-family="system-ui, -apple-system, sans-serif" font-size="14" font-weight="bold" fill="{text_color}" text-anchor="middle">{format_subscripts(sym)}</text>

  <!-- Species Name & Classification -->
  <text x="66" y="39" font-family="system-ui, -apple-system, sans-serif" font-size="10" font-weight="bold" fill="#F8FAFC">{name[:16]}</text>
  <text x="66" y="51" font-family="system-ui, -apple-system, sans-serif" font-size="7.5" fill="#94A3B8">{stype[:20]}</text>
  <text x="66" y="61" font-family="system-ui, -apple-system, sans-serif" font-size="7.5" font-weight="bold" fill="{ch_col}">{ch_str}</text>

  <line x1="12" y1="68" x2="168" y2="68" stroke="#1E293B" stroke-width="1"/>

  <!-- Properties Grid -->
  <text x="14" y="80" font-family="system-ui, -apple-system, sans-serif" font-size="7.5" fill="#64748B">Composition:</text>
  <text x="76" y="80" font-family="system-ui, -apple-system, sans-serif" font-size="8" font-weight="bold" fill="#F1F5F9">{atoms[:20]}</text>

  <text x="14" y="93" font-family="system-ui, -apple-system, sans-serif" font-size="7.5" fill="#64748B">Formula:</text>
  <text x="76" y="93" font-family="system-ui, -apple-system, sans-serif" font-size="8" font-weight="bold" fill="#38BDF8">{formula[:18]}</text>

  <text x="14" y="106" font-family="system-ui, -apple-system, sans-serif" font-size="7.5" fill="#64748B">Catalog Status:</text>
  <text x="76" y="106" font-family="system-ui, -apple-system, sans-serif" font-size="7.5" font-weight="bold" fill="#10B981">Discovered ★</text>

  <!-- Description Box -->
  <rect x="10" y="114" width="160" height="34" rx="4" fill="#0B1120" stroke="#1E293B" stroke-width="1"/>
  <text x="14" y="126" font-family="system-ui, -apple-system, sans-serif" font-size="7" fill="#94A3B8">{desc[:34]}</text>
  <text x="14" y="138" font-family="system-ui, -apple-system, sans-serif" font-size="7" fill="#94A3B8">{desc[34:68]}</text>
</svg>'''
    return svg


# --- 6. Friendly Onboarding Guide Card ---
def generate_onboarding_card():
    # 420x220 dialog, center 210, 110
    return '''<svg xmlns="http://www.w3.org/2000/svg" width="420" height="220" viewBox="0 0 420 220">
  <!-- Dialog Base Surface -->
  <rect width="420" height="220" rx="10" fill="#131D31" stroke="#38BDF8" stroke-width="1.8"/>
  
  <!-- Header Bar -->
  <rect x="0" y="0" width="420" height="30" rx="10" fill="#1E293B"/>
  <line x1="0" y1="30" x2="420" y2="30" stroke="#334155" stroke-width="1"/>
  <text x="20" y="20" font-family="system-ui, -apple-system, sans-serif" font-size="12" font-weight="bold" fill="#F8FAFC">Welcome to The Chemistry Lab</text>
  <text x="400" y="20" font-family="system-ui, -apple-system, sans-serif" font-size="9" fill="#94A3B8" text-anchor="end">Quick Guide</text>

  <!-- 4 Step Cards -->
  <rect x="16" y="42" width="188" height="62" rx="6" fill="#1E293B" stroke="#334155" stroke-width="1"/>
  <circle cx="34" cy="58" r="10" fill="#10B981"/>
  <text x="34" y="62" font-family="system-ui, -apple-system, sans-serif" font-size="10" font-weight="bold" fill="#0F172A" text-anchor="middle">1</text>
  <text x="52" y="56" font-family="system-ui, -apple-system, sans-serif" font-size="9" font-weight="bold" fill="#F8FAFC">Add Elements</text>
  <text x="52" y="68" font-family="system-ui, -apple-system, sans-serif" font-size="7.5" fill="#94A3B8">Click [+] to open the palette</text>
  <text x="52" y="78" font-family="system-ui, -apple-system, sans-serif" font-size="7.5" fill="#94A3B8">and spawn base atoms.</text>

  <rect x="216" y="42" width="188" height="62" rx="6" fill="#1E293B" stroke="#334155" stroke-width="1"/>
  <circle cx="234" cy="58" r="10" fill="#38BDF8"/>
  <text x="234" y="62" font-family="system-ui, -apple-system, sans-serif" font-size="10" font-weight="bold" fill="#0F172A" text-anchor="middle">2</text>
  <text x="252" y="56" font-family="system-ui, -apple-system, sans-serif" font-size="9" font-weight="bold" fill="#F8FAFC">Synthesize</text>
  <text x="252" y="68" font-family="system-ui, -apple-system, sans-serif" font-size="7.5" fill="#94A3B8">Drag atoms together to test</text>
  <text x="252" y="78" font-family="system-ui, -apple-system, sans-serif" font-size="7.5" fill="#94A3B8">affinity and make molecules.</text>

  <rect x="16" y="112" width="188" height="62" rx="6" fill="#1E293B" stroke="#334155" stroke-width="1"/>
  <circle cx="34" cy="128" r="10" fill="#8B5CF6"/>
  <text x="34" y="132" font-family="system-ui, -apple-system, sans-serif" font-size="10" font-weight="bold" fill="#0F172A" text-anchor="middle">3</text>
  <text x="52" y="126" font-family="system-ui, -apple-system, sans-serif" font-size="9" font-weight="bold" fill="#F8FAFC">Energize &amp; Ionize</text>
  <text x="52" y="138" font-family="system-ui, -apple-system, sans-serif" font-size="7.5" fill="#94A3B8">Use UV light for photolysis.</text>
  <text x="52" y="148" font-family="system-ui, -apple-system, sans-serif" font-size="7.5" fill="#94A3B8">Cosmic rays produce ions.</text>

  <rect x="216" y="112" width="188" height="62" rx="6" fill="#1E293B" stroke="#334155" stroke-width="1"/>
  <circle cx="234" cy="128" r="10" fill="#F59E0B"/>
  <text x="234" y="132" font-family="system-ui, -apple-system, sans-serif" font-size="10" font-weight="bold" fill="#0F172A" text-anchor="middle">4</text>
  <text x="252" y="126" font-family="system-ui, -apple-system, sans-serif" font-size="9" font-weight="bold" fill="#F8FAFC">Catalog &amp; Discover</text>
  <text x="252" y="138" font-family="system-ui, -apple-system, sans-serif" font-size="7.5" fill="#94A3B8">Freeze time to inspect bonds.</text>
  <text x="252" y="148" font-family="system-ui, -apple-system, sans-serif" font-size="7.5" fill="#94A3B8">Discover all 129 species!</text>

  <!-- Start Action Button -->
  <rect x="130" y="184" width="160" height="26" rx="5" fill="#0284C7" stroke="#38BDF8" stroke-width="1.2"/>
  <text x="210" y="201" font-family="system-ui, -apple-system, sans-serif" font-size="9.5" font-weight="bold" fill="#FFFFFF" text-anchor="middle">Start Experimenting</text>
</svg>'''


# --- 7. Discovery Compendium Browser ---
def generate_compendium_assets():
    costumes = {}

    def base_comp_modal(active_tab_idx, title, subtitle):
        tabs = [
            (1, "Overview", 14, 78, "#6366F1"),
            (2, "Elements", 96, 78, "#10B981"),
            (3, "Molecules", 178, 86, "#38BDF8"),
            (4, "Radicals", 268, 80, "#EF4444"),
            (5, "Ions", 352, 74, "#A855F7")
        ]
        tab_svg = []
        for tid, tname, tx, tw, tcol in tabs:
            is_active = (tid == active_tab_idx)
            bg = "#1E293B" if is_active else "#111A2E"
            border = tcol if is_active else "#1E293B"
            fg = tcol if is_active else "#64748B"
            weight = "bold" if is_active else "normal"
            tab_svg.append(f'<rect x="{tx}" y="28" width="{tw}" height="18" rx="3" fill="{bg}" stroke="{border}" stroke-width="1"/>')
            tab_svg.append(f'<text x="{tx + tw/2}" y="40.5" font-family="system-ui, -apple-system, sans-serif" font-size="7.5" font-weight="{weight}" fill="{fg}" text-anchor="middle">{tname}</text>')
            if is_active:
                tab_svg.append(f'<line x1="{tx+4}" y1="46" x2="{tx+tw-4}" y2="46" stroke="{tcol}" stroke-width="2"/>')

        tabs_str = "\n  ".join(tab_svg)

        return f'''
  <!-- Chassis Frame -->
  <rect width="440" height="250" rx="8" fill="#131D31" stroke="#334155" stroke-width="1.5"/>
  
  <!-- Header Bar -->
  <rect x="0" y="0" width="440" height="26" rx="8" fill="#1E293B"/>
  <line x1="0" y1="26" x2="440" y2="26" stroke="#334155" stroke-width="1"/>
  <circle cx="14" cy="13" r="4" fill="#38BDF8"/>
  <text x="26" y="17" font-family="system-ui, -apple-system, sans-serif" font-size="9.5" font-weight="bold" fill="#F8FAFC">{title}</text>
  <text x="390" y="17" font-family="system-ui, -apple-system, sans-serif" font-size="8" fill="#94A3B8" text-anchor="end">{subtitle}</text>
  
  <!-- Close Button in Upper Right -->
  <rect x="406" y="5" width="22" height="16" rx="3" fill="#1E293B" stroke="#EF4444" stroke-width="1"/>
  <text x="417" y="16.5" font-family="system-ui, -apple-system, sans-serif" font-size="11" font-weight="bold" fill="#EF4444" text-anchor="middle">×</text>

  <!-- Navigation Tabs -->
  {tabs_str}

  <!-- Bottom Action Bar -->
  <rect x="0" y="222" width="440" height="28" rx="8" fill="#1E293B"/>
  <line x1="0" y1="222" x2="440" y2="222" stroke="#334155" stroke-width="1"/>
  
  <!-- Reset Button [D] -->
  <rect x="14" y="226" width="110" height="20" rx="3" fill="#2A171D" stroke="#EF4444" stroke-width="1"/>
  <text x="69" y="239" font-family="system-ui, -apple-system, sans-serif" font-size="7.5" font-weight="bold" fill="#F87171" text-anchor="middle">Reset Archive [D]</text>
  
  <!-- Center Hint -->
  <text x="220" y="239" font-family="system-ui, -apple-system, sans-serif" font-size="7.5" fill="#94A3B8" text-anchor="middle">Click species to inject or inspect • [×] to close</text>
  
  <!-- Close Catalog Button -->
  <rect x="316" y="226" width="110" height="20" rx="3" fill="#0B2338" stroke="#38BDF8" stroke-width="1"/>
  <text x="371" y="239" font-family="system-ui, -apple-system, sans-serif" font-size="8" font-weight="bold" fill="#38BDF8" text-anchor="middle">Close Catalog [×]</text>
'''

    def render_8_card_grid(tab_idx, title, sub_title, page_nav_left, page_nav_right, cards):
        svg = ['<svg xmlns="http://www.w3.org/2000/svg" width="440" height="250" viewBox="0 0 440 250">']
        svg.append(base_comp_modal(tab_idx, title, sub_title))
        
        # Sub-header
        svg.append('  <rect x="14" y="52" width="412" height="18" rx="3" fill="#111A2E" stroke="#1E293B" stroke-width="1"/>')
        svg.append('  <text x="24" y="64.5" font-family="system-ui, -apple-system, sans-serif" font-size="7.5" fill="#94A3B8">Click any species card to spawn it in the chamber</text>')
        
        # Page buttons on right
        svg.append(f'  <rect x="270" y="54" width="70" height="14" rx="2" fill="{page_nav_left[2]}" stroke="{page_nav_left[3]}" stroke-width="0.8"/>')
        svg.append(f'  <text x="305" y="64" font-family="system-ui, -apple-system, sans-serif" font-size="6.5" font-weight="bold" fill="{page_nav_left[4]}" text-anchor="middle">{page_nav_left[0]}</text>')
        
        svg.append(f'  <rect x="348" y="54" width="70" height="14" rx="2" fill="{page_nav_right[2]}" stroke="{page_nav_right[3]}" stroke-width="0.8"/>')
        svg.append(f'  <text x="383" y="64" font-family="system-ui, -apple-system, sans-serif" font-size="6.5" font-weight="bold" fill="{page_nav_right[4]}" text-anchor="middle">{page_nav_right[0]}</text>')

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
            svg.append(f'    <rect x="{x}" y="{y}" width="98" height="68" rx="4" fill="#1E293B" stroke="{col_accent}" stroke-width="1"/>')
            svg.append(f'    <rect x="{x+6}" y="{y+6}" width="86" height="24" rx="3" fill="#0B1120"/>')
            svg.append(f'    <text x="{x+49}" y="{y+23}" font-family="system-ui, -apple-system, sans-serif" font-size="13" font-weight="bold" fill="{col_accent}" text-anchor="middle">{disp_form}</text>')
            svg.append(f'    <text x="{x+49}" y="{y+41}" font-family="system-ui, -apple-system, sans-serif" font-size="7.5" font-weight="bold" fill="#F8FAFC" text-anchor="middle">{name}</text>')
            svg.append(f'    <text x="{x+49}" y="{y+51}" font-family="system-ui, -apple-system, sans-serif" font-size="6.5" fill="#94A3B8" text-anchor="middle">{desc}</text>')
            svg.append(f'    <rect x="{x+24}" y="{y+56}" width="50" height="9" rx="2" fill="#082032" stroke="{col_accent}" stroke-width="0.6"/>')
            svg.append(f'    <text x="{x+49}" y="{y+63.5}" font-family="system-ui, -apple-system, sans-serif" font-size="6" font-weight="bold" fill="{col_accent}" text-anchor="middle">{tag}</text>')
            svg.append(f'  </g>')

        svg.append('</svg>')
        return "\n".join(svg)

    # 1. comp_summary (Overview Page)
    p1 = f'''<svg xmlns="http://www.w3.org/2000/svg" width="440" height="250" viewBox="0 0 440 250">
{base_comp_modal(1, "Discovery Compendium", "129 Total Species")}
  <!-- Progress Overview -->
  <rect x="14" y="52" width="412" height="32" rx="4" fill="#1E293B" stroke="#334155" stroke-width="1"/>
  <text x="26" y="65" font-family="system-ui, -apple-system, sans-serif" font-size="8" fill="#94A3B8">LABORATORY DISCOVERY PROGRESS</text>
  <text x="414" y="65" font-family="system-ui, -apple-system, sans-serif" font-size="8" font-weight="bold" fill="#38BDF8" text-anchor="end">129 TARGET SPECIES</text>
  <rect x="26" y="71" width="388" height="6" rx="3" fill="#0B1120"/>
  <rect x="26" y="71" width="110" height="6" rx="3" fill="#38BDF8"/>

  <!-- 4 Category Cards -->
  <rect x="14" y="90" width="98" height="124" rx="4" fill="#1E293B" stroke="#10B981" stroke-width="1"/>
  <text x="63" y="106" font-family="system-ui, -apple-system, sans-serif" font-size="8.5" font-weight="bold" fill="#10B981" text-anchor="middle">Base Elements</text>
  <text x="63" y="136" font-family="system-ui, -apple-system, sans-serif" font-size="22" font-weight="bold" fill="#FFFFFF" text-anchor="middle">19</text>
  <text x="63" y="154" font-family="system-ui, -apple-system, sans-serif" font-size="7.5" fill="#10B981" text-anchor="middle">Available</text>
  <text x="63" y="168" font-family="system-ui, -apple-system, sans-serif" font-size="7" fill="#94A3B8" text-anchor="middle">H through I</text>
  <rect x="22" y="186" width="82" height="18" rx="3" fill="#0E2E22" stroke="#10B981" stroke-width="0.8"/>
  <text x="63" y="198" font-family="system-ui, -apple-system, sans-serif" font-size="7.5" font-weight="bold" fill="#10B981" text-anchor="middle">Browse [2]</text>

  <rect x="118" y="90" width="98" height="124" rx="4" fill="#1E293B" stroke="#38BDF8" stroke-width="1"/>
  <text x="167" y="106" font-family="system-ui, -apple-system, sans-serif" font-size="8.5" font-weight="bold" fill="#38BDF8" text-anchor="middle">Molecules</text>
  <text x="167" y="136" font-family="system-ui, -apple-system, sans-serif" font-size="22" font-weight="bold" fill="#FFFFFF" text-anchor="middle">69</text>
  <text x="167" y="154" font-family="system-ui, -apple-system, sans-serif" font-size="7.5" fill="#38BDF8" text-anchor="middle">Synthesizable</text>
  <text x="167" y="168" font-family="system-ui, -apple-system, sans-serif" font-size="7" fill="#94A3B8" text-anchor="middle">Covalent &amp; Salts</text>
  <rect x="126" y="186" width="82" height="18" rx="3" fill="#0C253D" stroke="#38BDF8" stroke-width="0.8"/>
  <text x="167" y="198" font-family="system-ui, -apple-system, sans-serif" font-size="7.5" font-weight="bold" fill="#38BDF8" text-anchor="middle">Browse [3]</text>

  <rect x="222" y="90" width="98" height="124" rx="4" fill="#1E293B" stroke="#EF4444" stroke-width="1"/>
  <text x="271" y="106" font-family="system-ui, -apple-system, sans-serif" font-size="8.5" font-weight="bold" fill="#EF4444" text-anchor="middle">Radicals</text>
  <text x="271" y="136" font-family="system-ui, -apple-system, sans-serif" font-size="22" font-weight="bold" fill="#FFFFFF" text-anchor="middle">19</text>
  <text x="271" y="154" font-family="system-ui, -apple-system, sans-serif" font-size="7.5" fill="#EF4444" text-anchor="middle">UV Photolysis</text>
  <text x="271" y="168" font-family="system-ui, -apple-system, sans-serif" font-size="7" fill="#94A3B8" text-anchor="middle">Unpaired Electrons</text>
  <rect x="230" y="186" width="82" height="18" rx="3" fill="#2E1117" stroke="#EF4444" stroke-width="0.8"/>
  <text x="271" y="198" font-family="system-ui, -apple-system, sans-serif" font-size="7.5" font-weight="bold" fill="#EF4444" text-anchor="middle">Browse [4]</text>

  <rect x="326" y="90" width="98" height="124" rx="4" fill="#1E293B" stroke="#A855F7" stroke-width="1"/>
  <text x="375" y="106" font-family="system-ui, -apple-system, sans-serif" font-size="8.5" font-weight="bold" fill="#A855F7" text-anchor="middle">Ions</text>
  <text x="375" y="136" font-family="system-ui, -apple-system, sans-serif" font-size="22" font-weight="bold" fill="#FFFFFF" text-anchor="middle">22</text>
  <text x="375" y="154" font-family="system-ui, -apple-system, sans-serif" font-size="7.5" fill="#A855F7" text-anchor="middle">Cosmic Ionization</text>
  <text x="375" y="168" font-family="system-ui, -apple-system, sans-serif" font-size="7" fill="#94A3B8" text-anchor="middle">Charged Particles</text>
  <rect x="334" y="186" width="82" height="18" rx="3" fill="#221133" stroke="#A855F7" stroke-width="0.8"/>
  <text x="375" y="198" font-family="system-ui, -apple-system, sans-serif" font-size="7.5" font-weight="bold" fill="#A855F7" text-anchor="middle">Browse [5]</text>
</svg>'''
    costumes["comp_summary"] = make_svg_asset(p1, "comp_summary", 220, 125)

    # 2. comp_elements
    elem_cards = [
        {"formula": "H", "name": "Hydrogen", "recipe": "Z=1 • Nonmetal", "accent": "#10B981"},
        {"formula": "He", "name": "Helium", "recipe": "Z=2 • Noble Gas", "accent": "#10B981"},
        {"formula": "Li", "name": "Lithium", "recipe": "Z=3 • Alkali Metal", "accent": "#10B981"},
        {"formula": "Be", "name": "Beryllium", "recipe": "Z=4 • Alkaline", "accent": "#10B981"},
        {"formula": "C", "name": "Carbon", "recipe": "Z=6 • Nonmetal", "accent": "#10B981"},
        {"formula": "N", "name": "Nitrogen", "recipe": "Z=7 • Pnictogen", "accent": "#10B981"},
        {"formula": "O", "name": "Oxygen", "recipe": "Z=8 • Chalcogen", "accent": "#10B981"},
        {"formula": "F", "name": "Fluorine", "recipe": "Z=9 • Halogen", "accent": "#10B981"}
    ]
    p2 = render_8_card_grid(
        2, "Base Chemical Elements", "19 Available Elements",
        ("Page 1/3", 1, "#0B2E20", "#10B981", "#10B981"),
        ("Page 2 &gt;", 2, "#1E293B", "#334155", "#94A3B8"),
        elem_cards
    )
    costumes["comp_elements"] = make_svg_asset(p2, "comp_elements", 220, 125)

    # 3. comp_molecules_1
    mol1_cards = [
        {"formula": "H2", "name": "Hydrogen Gas", "recipe": "H + H → H2", "accent": "#38BDF8"},
        {"formula": "H2O", "name": "Water", "recipe": "2H + O → H2O", "accent": "#38BDF8"},
        {"formula": "O2", "name": "Oxygen Gas", "recipe": "O + O → O2", "accent": "#38BDF8"},
        {"formula": "CO2", "name": "Carbon Dioxide", "recipe": "C + 2O → CO2", "accent": "#38BDF8"},
        {"formula": "CH4", "name": "Methane", "recipe": "C + 4H → CH4", "accent": "#38BDF8"},
        {"formula": "NH3", "name": "Ammonia", "recipe": "N + 3H → NH3", "accent": "#38BDF8"},
        {"formula": "HCl", "name": "Hydrogen Chloride", "recipe": "H + Cl → HCl", "accent": "#38BDF8"},
        {"formula": "NaCl", "name": "Table Salt", "recipe": "Na + Cl → NaCl", "accent": "#38BDF8"}
    ]
    p3 = render_8_card_grid(
        3, "Neutral Molecules", "Part 1 of 2",
        ("&lt; Back", 1, "#1E293B", "#334155", "#94A3B8"),
        ("Page 2 &gt;", 2, "#0B2338", "#38BDF8", "#38BDF8"),
        mol1_cards
    )
    costumes["comp_molecules_1"] = make_svg_asset(p3, "comp_molecules_1", 220, 125)

    # 4. comp_molecules_2
    mol2_cards = [
        {"formula": "H2SO4", "name": "Sulfuric Acid", "recipe": "SO3 + H2O → H2SO4", "accent": "#38BDF8"},
        {"formula": "H3PO4", "name": "Phosphoric Acid", "recipe": "P4O10 + H2O", "accent": "#38BDF8"},
        {"formula": "CaCO3", "name": "Calcium Carbonate", "recipe": "CaO + CO2", "accent": "#38BDF8"},
        {"formula": "SiO2", "name": "Silicon Dioxide", "recipe": "Si + 2O → SiO2", "accent": "#38BDF8"},
        {"formula": "NaOH", "name": "Sodium Hydroxide", "recipe": "Na + OH", "accent": "#38BDF8"},
        {"formula": "H2O2", "name": "Hydrogen Peroxide", "recipe": "2OH• → H2O2", "accent": "#38BDF8"},
        {"formula": "O3", "name": "Ozone", "recipe": "O2 + O → O3", "accent": "#38BDF8"},
        {"formula": "KCl", "name": "Potassium Salt", "recipe": "K + Cl → KCl", "accent": "#38BDF8"}
    ]
    p4 = render_8_card_grid(
        3, "Neutral Molecules", "Part 2 of 2",
        ("&lt; Page 1", 1, "#0B2338", "#38BDF8", "#38BDF8"),
        ("Page 2", 2, "#1E293B", "#334155", "#94A3B8"),
        mol2_cards
    )
    costumes["comp_molecules_2"] = make_svg_asset(p4, "comp_molecules_2", 220, 125)

    # 5. comp_radicals
    rad_cards = [
        {"formula": "CH•", "name": "Methylidyne", "recipe": "Photolysis CH2", "accent": "#EF4444"},
        {"formula": "CH2•", "name": "Methylene", "recipe": "Photolysis CH3", "accent": "#EF4444"},
        {"formula": "CH3•", "name": "Methyl Radical", "recipe": "CH4 + hν → CH3•", "accent": "#EF4444"},
        {"formula": "NH•", "name": "Imidogen", "recipe": "Photolysis NH2", "accent": "#EF4444"},
        {"formula": "NH2•", "name": "Amino Radical", "recipe": "NH3 + hν → NH2•", "accent": "#EF4444"},
        {"formula": "NO•", "name": "Nitric Oxide", "recipe": "N + O radical", "accent": "#EF4444"},
        {"formula": "OH•", "name": "Hydroxyl Radical", "recipe": "H2O + hν → •OH", "accent": "#EF4444"},
        {"formula": "HS•", "name": "Mercapto Radical", "recipe": "H2S + hν → HS•", "accent": "#EF4444"}
    ]
    p5 = render_8_card_grid(
        4, "Free Radical Species", "UV Photolysis Required",
        ("RADICALS", 1, "#2E1117", "#EF4444", "#EF4444"),
        ("UV ACTIVE", 2, "#1E293B", "#334155", "#94A3B8"),
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
        5, "Structured Ion Species", "Cosmic Ray Ionization",
        ("IONS", 1, "#221133", "#A855F7", "#A855F7"),
        ("COSMIC RAYS", 2, "#1E293B", "#334155", "#94A3B8"),
        ion_cards
    )
    costumes["comp_ions"] = make_svg_asset(p6, "comp_ions", 220, 125)

    return costumes


# --- 8. Live Feedback Status Strips (Human-Friendly Messages) ---
def generate_telemetry_assets():
    costumes = {}
    messages = [
        ("telem_ready", "#10B981", "Chamber ready • Drag and merge atoms to synthesize new molecules"),
        ("telem_react", "#38BDF8", "Chemical Reaction: Synthesized new molecular bond"),
        ("telem_exo", "#F97316", "Exothermic Reaction: Thermal energy burst and photon emitted"),
        ("telem_uv_req", "#C084FC", "UV Radiation Required: Turn on UV lamp to trigger photolysis"),
        ("telem_cosmic", "#38BDF8", "Cosmic Ray Impact: High-energy particle ionized an atom"),
        ("telem_inert", "#94A3B8", "Inert Collision: No reactive pathway under current conditions"),
        ("telem_discover", "#F59E0B", "★ New Discovery: Novel compound cataloged in the laboratory archive!"),
        ("telem_frozen", "#7DD3FC", "❄ Time Frozen: Thermal velocities and reaction clocks paused"),
        ("telem_save", "#38BDF8", "Save Complete: Discovery snapshot recorded to register"),
        ("telem_load", "#818CF8", "Load Complete: Chemical discoveries restored from snapshot"),
        ("telem_purge", "#F87171", "Chamber Cleared: Vacuum flushed • All particles evacuated")
    ]

    for name, col, text in messages:
        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="460" height="22" viewBox="0 0 460 22">
  <rect width="460" height="22" rx="4" fill="#131D31" stroke="#1E293B" stroke-width="1"/>
  <circle cx="12" cy="11" r="3.5" fill="{col}"/>
  <text x="22" y="14.5" font-family="system-ui, -apple-system, sans-serif" font-size="8" font-weight="bold" fill="{col}">{text[:75]}</text>
</svg>'''
        costumes[name] = make_svg_asset(svg, name, 230, 11)

    return costumes


# --- 9. Particle Effects & Visual Assets ---
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
  <line x1="2" y1="7" x2="60" y2="7" stroke="url(#cosmic_streak)" stroke-width="3" stroke-linecap="round"/>
  <circle cx="58" cy="7" r="3.5" fill="#FFFFFF"/>
</svg>'''
    costumes["cosmic_ray"] = make_svg_asset(cosmic_svg, "cosmic_ray", 32, 7)

    # Photon Wave-packet (26x26, center 13, 13)
    photon_svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="26" height="26" viewBox="0 0 26 26">
  <circle cx="13" cy="13" r="8" fill="#FACC15" fill-opacity="0.25"/>
  <circle cx="13" cy="13" r="4.5" fill="#FACC15" fill-opacity="0.7"/>
  <circle cx="13" cy="13" r="2" fill="#FFFFFF"/>
  <path d="M 6 13 Q 9.5 7, 13 13 T 20 13" fill="none" stroke="#FEF08A" stroke-width="1.8"/>
</svg>'''
    costumes["photon_wave"] = make_svg_asset(photon_svg, "photon_wave", 13, 13)

    # Exothermic plasma shockwave (3 frames)
    for frame, r, col in [(1, 16, "#F97316"), (2, 28, "#EF4444"), (3, 38, "#DC2626")]:
        fx_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="84" height="84" viewBox="0 0 84 84">
  <circle cx="42" cy="42" r="{r}" fill="{col}" fill-opacity="0.35" stroke="#FEF08A" stroke-width="2"/>
  <circle cx="42" cy="42" r="{max(4, r-8)}" fill="#FFFFFF" fill-opacity="0.25"/>
</svg>'''
        costumes[f"fx_exo_{frame}"] = make_svg_asset(fx_svg, f"fx_exo_{frame}", 42, 42)

    # Bond sparkle (2 frames)
    for frame, r in [(1, 14), (2, 24)]:
        fx_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="60" height="60" viewBox="0 0 60 60">
  <circle cx="30" cy="30" r="{r}" fill="none" stroke="#38BDF8" stroke-width="2" stroke-dasharray="3,3"/>
  <circle cx="30" cy="30" r="{r-5}" fill="#38BDF8" fill-opacity="0.25"/>
  <circle cx="30" cy="30" r="2.5" fill="#FFFFFF"/>
</svg>'''
        costumes[f"fx_bond_{frame}"] = make_svg_asset(fx_svg, f"fx_bond_{frame}", 30, 30)

    # Ionization electric zap (2 frames)
    for frame, pts in [(1, "30,8 22,26 34,24 26,52"), (2, "30,8 36,26 24,24 32,52")]:
        fx_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="60" height="60" viewBox="0 0 60 60">
  <circle cx="30" cy="30" r="18" fill="#38BDF8" fill-opacity="0.15"/>
  <polyline points="{pts}" fill="none" stroke="#67E8F9" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
</svg>'''
        costumes[f"fx_zap_{frame}"] = make_svg_asset(fx_svg, f"fx_zap_{frame}", 30, 30)

    # Annihilation poof (2 frames)
    for frame, r in [(1, 12), (2, 22)]:
        fx_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="60" height="60" viewBox="0 0 60 60">
  <circle cx="30" cy="30" r="{r}" fill="#A855F7" fill-opacity="0.3" stroke="#C084FC" stroke-width="1.8"/>
  <circle cx="30" cy="30" r="{max(2, r-6)}" fill="none" stroke="#FFFFFF" stroke-width="1" stroke-dasharray="2,2"/>
</svg>'''
        costumes[f"fx_poof_{frame}"] = make_svg_asset(fx_svg, f"fx_poof_{frame}", 30, 30)

    # Toast Banner (240x36, center 120, 18)
    toast_svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="240" height="36" viewBox="0 0 240 36">
  <rect width="240" height="36" rx="6" fill="#131D31" stroke="#38BDF8" stroke-width="1.5"/>
  <circle cx="20" cy="18" r="9" fill="#38BDF8"/>
  <text x="20" y="21.5" font-family="system-ui, -apple-system, sans-serif" font-size="10" font-weight="bold" fill="#0F172A" text-anchor="middle">★</text>
  <text x="36" y="16" font-family="system-ui, -apple-system, sans-serif" font-size="8.5" font-weight="bold" fill="#38BDF8">Discovery Cataloged</text>
  <text x="36" y="27" font-family="system-ui, -apple-system, sans-serif" font-size="7.5" fill="#E2E8F0">New species added to laboratory archive</text>
</svg>'''
    costumes["toast_banner"] = make_svg_asset(toast_svg, "toast_banner", 120, 18)

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
        ("add", "Add", "#10B981"),
        ("del", "Delete", "#EF4444"),
        ("insp", "Inspect", "#F59E0B"),
        ("uv", "UV Light", "#8B5CF6"),
        ("freeze", "Freeze", "#0284C7"),
        ("catalog", "Catalog", "#6366F1"),
        ("audio", "Audio", "#14B8A6"),
        ("save", "Save", "#3B82F6"),
        ("help", "Help", "#8B5CF6"),
        ("purge", "Clear", "#DC2626")
    ]
    for tool_name, label, act_col in tools:
        svg_norm = generate_vector_button(tool_name, label, active=False)
        svg_act = generate_vector_button(tool_name, label, active=True, custom_active_col=act_col)
        costumes[f"btn_{tool_name}"] = make_svg_asset(svg_norm, f"btn_{tool_name}", 22, 14)
        costumes[f"btn_{tool_name}_active"] = make_svg_asset(svg_act, f"btn_{tool_name}_active", 22, 14)

    # Special audio muted costume
    svg_mut = generate_vector_button("audio_muted", "Muted", active=True, custom_active_col="#64748B")
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
