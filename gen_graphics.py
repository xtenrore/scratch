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
    svg.append(f'    <radialGradient id="{grad_id}" cx="32%" cy="28%" r="68%">')
    svg.append(f'      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.65"/>')
    svg.append(f'      <stop offset="40%" stop-color="{color}" stop-opacity="1.0"/>')
    svg.append(f'      <stop offset="100%" stop-color="{border}" stop-opacity="1.0"/>')
    svg.append('    </radialGradient>')
    svg.append('  </defs>')

    text_color = "#0A0D14" if color in ["#E2E8F0", "#FACC15", "#A3E635", "#67E8F9", "#FFFFFF"] else "#FFFFFF"

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

        # Valence electron orbital indicator
        svg.append(f'  <circle cx="32" cy="32" r="{r+2.5}" fill="none" stroke="{border}" stroke-width="0.75" stroke-dasharray="2,2" opacity="0.45"/>')
        # Core atom sphere
        svg.append(f'  <circle cx="32" cy="32" r="{r}" fill="url(#{grad_id})" stroke="{border}" stroke-width="1.6"/>')
        # Atomic number badge in top-left
        svg.append(f'  <rect x="{32-r}" y="{32-r}" width="12" height="9" rx="1.5" fill="#0C0E14" stroke="{border}" stroke-width="0.75"/>')
        svg.append(f'  <text x="{32-r+6}" y="{32-r+7}" font-family="system-ui, -apple-system, sans-serif" font-size="6.5" font-weight="bold" fill="#38BDF8" text-anchor="middle">{z}</text>')
        # Chemical symbol
        svg.append(f'  <text x="32" y="37" font-family="system-ui, -apple-system, sans-serif" font-size="{font_size}" font-weight="bold" fill="{text_color}" text-anchor="middle">{disp_text}</text>')

    elif is_ion:
        # Structured Ions: distinct electric ionization halo and signed charge badge
        halo_color = "#38BDF8" if charge > 0 else "#FB7185"
        # Ionization boundary halo
        svg.append(f'  <circle cx="32" cy="32" r="26" fill="none" stroke="{halo_color}" stroke-width="1.6" stroke-dasharray="3,2" opacity="0.85"/>')
        # Core sphere
        svg.append(f'  <circle cx="32" cy="32" r="21" fill="url(#{grad_id})" stroke="{border}" stroke-width="1.6"/>')
        # Formula text
        svg.append(f'  <text x="32" y="37" font-family="system-ui, -apple-system, sans-serif" font-size="{font_size}" font-weight="bold" fill="{text_color}" text-anchor="middle">{disp_text}</text>')
        # Signed charge pill in upper right
        ch_text = "+" if charge == 1 else ("-" if charge == -1 else (f"{charge}+" if charge > 0 else f"{abs(charge)}-"))
        svg.append(f'  <circle cx="48" cy="16" r="7.5" fill="#0C0E14" stroke="{halo_color}" stroke-width="1.3"/>')
        svg.append(f'  <text x="48" y="19.5" font-family="system-ui, -apple-system, sans-serif" font-size="8" font-weight="bold" fill="{halo_color}" text-anchor="middle">{ch_text}</text>')

    else:
        # Covalent Molecules & Radicals
        is_diatomic = any(sym.endswith("2") and len(sym) <= 3 for _ in [0]) or sym in ["CO", "NO•", "NH•", "HCl", "HF", "HBr", "HI", "NaCl", "KCl", "CaO", "SiO", "PN", "NaF", "KF", "NaBr", "KBr", "NaI", "KI", "CN"]
        if is_diatomic:
            # Overlapping covalent dual-sphere dumbbell
            svg.append(f'  <rect x="9" y="17" width="46" height="30" rx="15" fill="url(#{grad_id})" stroke="{border}" stroke-width="1.6"/>')
            svg.append(f'  <line x1="20" y1="32" x2="44" y2="32" stroke="#FFFFFF" stroke-width="0.8" stroke-opacity="0.35" stroke-dasharray="2,2"/>')
        else:
            # Polyatomic molecular cluster capsule
            svg.append(f'  <rect x="6" y="16" width="52" height="32" rx="10" fill="url(#{grad_id})" stroke="{border}" stroke-width="1.6"/>')
            svg.append(f'  <line x1="14" y1="27" x2="50" y2="27" stroke="#FFFFFF" stroke-width="0.75" stroke-opacity="0.25" stroke-dasharray="2,2"/>')
            svg.append(f'  <line x1="14" y1="37" x2="50" y2="37" stroke="#FFFFFF" stroke-width="0.75" stroke-opacity="0.25" stroke-dasharray="2,2"/>')

        # Formula text
        svg.append(f'  <text x="32" y="37" font-family="system-ui, -apple-system, sans-serif" font-size="{font_size}" font-weight="bold" fill="{text_color}" text-anchor="middle">{disp_text}</text>')

        # Distinct radical dot indicator
        if is_radical:
            svg.append(f'  <circle cx="50" cy="16" r="4" fill="#EF4444" stroke="#FFFFFF" stroke-width="1"/>')
            svg.append(f'  <circle cx="50" cy="16" r="1.5" fill="#FFFFFF"/>')

    svg.append('</svg>')
    return "\n".join(svg)


# --- 2. Stage Backdrops: Precision Laboratory Vacuum Chamber ---
def generate_backdrops():
    def base_stage_canvas():
        return '''
  <!-- Main Stage Vacuum Field Canvas (480x360) -->
  <rect width="480" height="360" fill="#0C0E14"/>
  
  <!-- Precision Header Bar (Y: 0 to 24) -->
  <rect x="0" y="0" width="480" height="24" fill="#141722"/>
  <line x1="0" y1="24" x2="480" y2="24" stroke="#252B3C" stroke-width="1"/>
  
  <!-- Header Title & Instrument Indicators -->
  <circle cx="16" cy="12" r="4.5" fill="#38BDF8"/>
  <circle cx="16" cy="12" r="2" fill="#FFFFFF"/>
  <text x="28" y="16" font-family="system-ui, -apple-system, sans-serif" font-size="10.5" font-weight="bold" fill="#F8FAFC">MOLECULAR SYNTHESIS CHAMBER</text>
  <text x="240" y="16" font-family="system-ui, -apple-system, sans-serif" font-size="8" fill="#94A3B8" text-anchor="middle">HIGH-VACUUM CHEMISTRY SIMULATOR • 129 TARGET SPECIES</text>
  <text x="466" y="16" font-family="system-ui, -apple-system, sans-serif" font-size="8.5" font-weight="bold" fill="#F59E0B" text-anchor="end">P: 1.2 × 10⁻⁷ TORR</text>
  
  <!-- Tool Rail Tray (Y: 24 to 58) -->
  <rect x="0" y="24" width="480" height="34" fill="#10131B"/>
  <line x1="0" y1="58" x2="480" y2="58" stroke="#1E2433" stroke-width="1"/>

  <!-- Main Reaction Chamber (Y: 58 to 328, width 468, x: 6 to 474) -->
  <rect x="6" y="58" width="468" height="270" rx="3" fill="#08090D" stroke="#202636" stroke-width="1.2"/>
  
  <!-- Chamber Precision Optical Crosshairs -->
  <line x1="235" y1="193" x2="245" y2="193" stroke="#22293A" stroke-width="1"/>
  <line x1="240" y1="188" x2="240" y2="198" stroke="#22293A" stroke-width="1"/>
  <line x1="115" y1="193" x2="125" y2="193" stroke="#1A202E" stroke-width="0.8"/>
  <line x1="120" y1="188" x2="120" y2="198" stroke="#1A202E" stroke-width="0.8"/>
  <line x1="355" y1="193" x2="365" y2="193" stroke="#1A202E" stroke-width="0.8"/>
  <line x1="360" y1="188" x2="360" y2="198" stroke="#1A202E" stroke-width="0.8"/>
  
  <!-- Chamber Corner Brackets -->
  <path d="M 12 70 L 12 64 L 18 64" fill="none" stroke="#283144" stroke-width="1"/>
  <path d="M 468 70 L 468 64 L 462 64" fill="none" stroke="#283144" stroke-width="1"/>
  <path d="M 12 316 L 12 322 L 18 322" fill="none" stroke="#283144" stroke-width="1"/>
  <path d="M 468 316 L 468 322 L 462 322" fill="none" stroke="#283144" stroke-width="1"/>

  <!-- Bottom Telemetry Console Strip (Y: 328 to 360) -->
  <rect x="0" y="328" width="480" height="32" fill="#141722"/>
  <line x1="0" y1="328" x2="480" y2="328" stroke="#252B3C" stroke-width="1"/>
'''

    # 1. Standard Dark Vacuum Chamber
    bg_std = f'''<svg xmlns="http://www.w3.org/2000/svg" width="480" height="360" viewBox="0 0 480 360">
{base_stage_canvas()}
</svg>'''

    # 2. Ultraviolet Actinic Illumination Mode (254 nm)
    bg_uv = f'''<svg xmlns="http://www.w3.org/2000/svg" width="480" height="360" viewBox="0 0 480 360">
{base_stage_canvas()}
  <!-- Actinic UV Perimeter Accent -->
  <rect x="6" y="58" width="468" height="270" rx="3" fill="none" stroke="#8B5CF6" stroke-width="1.5" opacity="0.85"/>
  <line x1="8" y1="62" x2="472" y2="62" stroke="#8B5CF6" stroke-width="1" stroke-dasharray="6,4" opacity="0.6"/>
  <line x1="8" y1="324" x2="472" y2="324" stroke="#8B5CF6" stroke-width="1" stroke-dasharray="6,4" opacity="0.6"/>
  
  <!-- UV Actinic Status Tag -->
  <rect x="140" y="65" width="200" height="18" rx="2" fill="#191228" stroke="#8B5CF6" stroke-width="1"/>
  <circle cx="150" cy="74" r="3" fill="#A855F7"/>
  <text x="242" y="77.5" font-family="system-ui, -apple-system, sans-serif" font-size="8" font-weight="bold" fill="#C084FC" text-anchor="middle">ACTINIC UV-C IRRADIATION (254 nm) • ACTIVE</text>
</svg>'''

    # 3. Cryostatic Freeze Mode (2.7 K)
    bg_freeze = f'''<svg xmlns="http://www.w3.org/2000/svg" width="480" height="360" viewBox="0 0 480 360">
{base_stage_canvas()}
  <!-- Cryogenic Thermal Perimeter Accent -->
  <rect x="6" y="58" width="468" height="270" rx="3" fill="none" stroke="#0EA5E9" stroke-width="1.5" opacity="0.85"/>
  <line x1="8" y1="62" x2="472" y2="62" stroke="#0EA5E9" stroke-width="1" stroke-dasharray="4,4" opacity="0.6"/>
  <line x1="8" y1="324" x2="472" y2="324" stroke="#0EA5E9" stroke-width="1" stroke-dasharray="4,4" opacity="0.6"/>
  
  <!-- Cryostat Status Tag -->
  <rect x="140" y="65" width="200" height="18" rx="2" fill="#0C1B2A" stroke="#0EA5E9" stroke-width="1"/>
  <circle cx="150" cy="74" r="3" fill="#38BDF8"/>
  <text x="242" y="77.5" font-family="system-ui, -apple-system, sans-serif" font-size="8" font-weight="bold" fill="#7DD3FC" text-anchor="middle">CRYOSTAT TEMPERATURE: 2.7 K • TIME FROZEN</text>
</svg>'''

    return bg_std, bg_uv, bg_freeze


# --- 3. Tactile Laboratory Instrument Buttons ---
def generate_vector_button(tool_name, label, active=False, custom_active_col=None):
    # Geometry: 44x28, center 22, 14
    act_col = custom_active_col or "#38BDF8"
    bg = "#151924" if not active else "#0E243A"
    border = "#262E40" if not active else act_col
    fg = "#CBD5E1" if not active else act_col
    sub_fg = "#94A3B8" if not active else act_col
    highlight = "#30394D" if not active else act_col

    icons = {
        "add": '''
          <circle cx="22" cy="10" r="6" fill="none" stroke="{fg}" stroke-width="1.2"/>
          <line x1="22" y1="6.5" x2="22" y2="13.5" stroke="{fg}" stroke-width="1.6" stroke-linecap="round"/>
          <line x1="18.5" y1="10" x2="25.5" y2="10" stroke="{fg}" stroke-width="1.6" stroke-linecap="round"/>
        ''',
        "del": '''
          <rect x="17" y="7" width="10" height="7" rx="1" fill="none" stroke="{fg}" stroke-width="1.2"/>
          <line x1="15" y1="7" x2="29" y2="7" stroke="{fg}" stroke-width="1.4" stroke-linecap="round"/>
          <line x1="20" y1="5" x2="24" y2="5" stroke="{fg}" stroke-width="1.2" stroke-linecap="round"/>
        ''',
        "insp": '''
          <circle cx="21" cy="9" r="4.5" fill="none" stroke="{fg}" stroke-width="1.3"/>
          <line x1="24.5" y1="12.5" x2="28" y2="16" stroke="{fg}" stroke-width="1.6" stroke-linecap="round"/>
          <circle cx="21" cy="9" r="1.5" fill="{fg}"/>
        ''',
        "uv": '''
          <circle cx="22" cy="10" r="3.5" fill="none" stroke="{fg}" stroke-width="1.2"/>
          <line x1="22" y1="3.5" x2="22" y2="5.5" stroke="{fg}" stroke-width="1.2" stroke-linecap="round"/>
          <line x1="22" y1="14.5" x2="22" y2="16.5" stroke="{fg}" stroke-width="1.2" stroke-linecap="round"/>
          <line x1="15.5" y1="10" x2="17.5" y2="10" stroke="{fg}" stroke-width="1.2" stroke-linecap="round"/>
          <line x1="26.5" y1="10" x2="28.5" y2="10" stroke="{fg}" stroke-width="1.2" stroke-linecap="round"/>
        ''',
        "freeze": '''
          <line x1="22" y1="4" x2="22" y2="16" stroke="{fg}" stroke-width="1.2" stroke-linecap="round"/>
          <line x1="16.5" y1="7.2" x2="27.5" y2="12.8" stroke="{fg}" stroke-width="1.2" stroke-linecap="round"/>
          <line x1="16.5" y1="12.8" x2="27.5" y2="7.2" stroke="{fg}" stroke-width="1.2" stroke-linecap="round"/>
          <circle cx="22" cy="10" r="1.2" fill="{fg}"/>
        ''',
        "catalog": '''
          <rect x="16" y="5" width="12" height="10" rx="1" fill="none" stroke="{fg}" stroke-width="1.2"/>
          <line x1="22" y1="5" x2="22" y2="15" stroke="{fg}" stroke-width="1"/>
          <line x1="16" y1="10" x2="28" y2="10" stroke="{fg}" stroke-width="0.8"/>
        ''',
        "audio": '''
          <polygon points="16,8 19,8 23,5 23,15 19,12 16,12" fill="{fg}"/>
          <path d="M 25 7 Q 27 10 25 13" fill="none" stroke="{fg}" stroke-width="1.2" stroke-linecap="round"/>
          <path d="M 27 5 Q 30 10 27 15" fill="none" stroke="{fg}" stroke-width="1.2" stroke-linecap="round"/>
        ''',
        "audio_muted": '''
          <polygon points="16,8 19,8 23,5 23,15 19,12 16,12" fill="{fg}"/>
          <line x1="15" y1="15" x2="29" y2="5" stroke="#EF4444" stroke-width="1.6" stroke-linecap="round"/>
        ''',
        "save": '''
          <rect x="17" y="5" width="10" height="9" rx="1" fill="none" stroke="{fg}" stroke-width="1.2"/>
          <rect x="19" y="5" width="6" height="3.5" fill="{fg}"/>
          <line x1="18" y1="11" x2="26" y2="11" stroke="{fg}" stroke-width="1"/>
        ''',
        "help": '''
          <circle cx="22" cy="10" r="6" fill="none" stroke="{fg}" stroke-width="1.2"/>
          <text x="22" y="13.5" font-family="system-ui, -apple-system, sans-serif" font-size="8.5" font-weight="bold" fill="{fg}" text-anchor="middle">?</text>
        ''',
        "purge": '''
          <path d="M 22 5 A 5 5 0 1 1 17 12" fill="none" stroke="{fg}" stroke-width="1.3" stroke-linecap="round"/>
          <polyline points="20,4 23,5 22,8" fill="none" stroke="{fg}" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"/>
        '''
    }

    icon_svg = icons.get(tool_name, "").replace("{fg}", fg)
    pip_svg = f'<circle cx="39" cy="5" r="1.5" fill="{act_col}"/>' if active else ''

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="44" height="28" viewBox="0 0 44 28">
  <rect x="1" y="1" width="42" height="26" rx="2" fill="{bg}" stroke="{border}" stroke-width="1"/>
  <line x1="2" y1="2" x2="42" y2="2" stroke="{highlight}" stroke-width="1"/>
  {pip_svg}
  {icon_svg}
  <text x="22" y="24" font-family="system-ui, -apple-system, sans-serif" font-size="6.5" font-weight="bold" fill="{sub_fg}" text-anchor="middle">{label}</text>
</svg>'''
    return svg


# --- 4. Periodic Element Palette Drawer & Tiles ---
def generate_palette_drawer():
    # 460x105 drawer, center 230, 52
    svg = ['<svg xmlns="http://www.w3.org/2000/svg" width="460" height="105" viewBox="0 0 460 105">']
    svg.append('  <!-- Drawer Surface -->')
    svg.append('  <rect width="460" height="105" rx="3" fill="#11141C" stroke="#252D3E" stroke-width="1.2"/>')
    svg.append('  <!-- Header Title -->')
    svg.append('  <rect x="0" y="0" width="460" height="22" rx="3" fill="#181D2A"/>')
    svg.append('  <line x1="0" y1="22" x2="460" y2="22" stroke="#252D3E" stroke-width="1"/>')
    svg.append('  <circle cx="12" cy="11" r="3.5" fill="#38BDF8"/>')
    svg.append('  <text x="22" y="15" font-family="system-ui, -apple-system, sans-serif" font-size="9" font-weight="bold" fill="#38BDF8">PERIODIC ELEMENT INJECTOR</text>')
    svg.append('  <text x="444" y="15" font-family="system-ui, -apple-system, sans-serif" font-size="8" fill="#94A3B8" text-anchor="end">[A] TOGGLE DOCK • SELECT ATOM TO SPAWN</text>')
    svg.append('</svg>')
    return "\n".join(svg)


def generate_palette_frame():
    return make_svg_asset(generate_palette_drawer(), "palette_drawer_frame", 230, 52)


def generate_palette_item_costumes():
    assets = {}
    for s in db_chemistry.SPECIES[:19]:
        color = s["color"]
        border = s["border"]
        fg = "#0A0D14" if color in ["#E2E8F0", "#FACC15", "#A3E635", "#67E8F9", "#FFFFFF"] else "#FFFFFF"
        z = s.get("z", 1)
        name_trunc = s["name"][:5].upper()
        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="40" height="34" viewBox="0 0 40 34">
  <rect x="0.5" y="0.5" width="39" height="33" rx="2" fill="#161924" stroke="{border}" stroke-width="1"/>
  <rect x="2" y="2" width="10" height="7" rx="1" fill="#0C0E14"/>
  <text x="7" y="7.5" font-family="system-ui, -apple-system, sans-serif" font-size="6" font-weight="bold" fill="#38BDF8" text-anchor="middle">{z}</text>
  <circle cx="20" cy="15" r="9" fill="{color}" stroke="{border}" stroke-width="0.8"/>
  <text x="20" y="18.5" font-family="system-ui, -apple-system, sans-serif" font-size="8.5" font-weight="bold" fill="{fg}" text-anchor="middle">{s["symbol"]}</text>
  <text x="20" y="30.5" font-family="system-ui, -apple-system, sans-serif" font-size="5.5" font-weight="bold" fill="#94A3B8" text-anchor="middle">{name_trunc}</text>
</svg>'''
        assets[f"pal_card_{s['id']}"] = make_svg_asset(svg, f"pal_card_{s['id']}", 20, 17)
    return assets


# --- 5. Spectrometer Compound Inspector HUD (129 HUD Cards) ---
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
    text_color = "#0A0D14" if color in ["#E2E8F0", "#FACC15", "#A3E635", "#67E8F9", "#FFFFFF"] else "#FFFFFF"

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="180" height="155" viewBox="0 0 180 155">
  <!-- Card Base Surface -->
  <rect width="180" height="155" rx="3" fill="#121622" stroke="#2B3448" stroke-width="1.2"/>
  
  <!-- Header Bar -->
  <rect x="0" y="0" width="180" height="22" rx="3" fill="#191E2D"/>
  <line x1="0" y1="22" x2="180" y2="22" stroke="#2B3448" stroke-width="1"/>
  <circle cx="12" cy="11" r="3.5" fill="#38BDF8"/>
  <text x="20" y="15" font-family="system-ui, -apple-system, sans-serif" font-size="8.5" font-weight="bold" fill="#38BDF8">SPECTROMETER ANALYSIS</text>
  <text x="168" y="15" font-family="system-ui, -apple-system, sans-serif" font-size="8" font-weight="bold" fill="#64748B" text-anchor="end">#{sid}</text>

  <!-- Visual Formula Box -->
  <rect x="12" y="28" width="46" height="34" rx="2" fill="{color}" stroke="{border}" stroke-width="1.2"/>
  <text x="35" y="50" font-family="system-ui, -apple-system, sans-serif" font-size="13" font-weight="bold" fill="{text_color}" text-anchor="middle">{format_subscripts(sym)}</text>

  <!-- Species Name & Classification -->
  <text x="66" y="39" font-family="system-ui, -apple-system, sans-serif" font-size="9.5" font-weight="bold" fill="#F8FAFC">{name[:16]}</text>
  <text x="66" y="50" font-family="system-ui, -apple-system, sans-serif" font-size="7" fill="#94A3B8">{stype[:20]}</text>
  <text x="66" y="60" font-family="system-ui, -apple-system, sans-serif" font-size="7" font-weight="bold" fill="{ch_col}">{ch_str}</text>

  <line x1="12" y1="68" x2="168" y2="68" stroke="#1F2636" stroke-width="1"/>

  <!-- Properties Grid -->
  <text x="14" y="80" font-family="system-ui, -apple-system, sans-serif" font-size="7" fill="#64748B">Composition:</text>
  <text x="76" y="80" font-family="system-ui, -apple-system, sans-serif" font-size="7.5" font-weight="bold" fill="#F1F5F9">{atoms[:20]}</text>

  <text x="14" y="93" font-family="system-ui, -apple-system, sans-serif" font-size="7" fill="#64748B">Formula:</text>
  <text x="76" y="93" font-family="system-ui, -apple-system, sans-serif" font-size="7.5" font-weight="bold" fill="#38BDF8">{formula[:18]}</text>

  <text x="14" y="106" font-family="system-ui, -apple-system, sans-serif" font-size="7" fill="#64748B">Catalog Status:</text>
  <text x="76" y="106" font-family="system-ui, -apple-system, sans-serif" font-size="7.5" font-weight="bold" fill="#10B981">Discovered ★</text>

  <!-- Description Box -->
  <rect x="10" y="114" width="160" height="34" rx="2" fill="#0A0C13" stroke="#1E2534" stroke-width="1"/>
  <text x="14" y="126" font-family="system-ui, -apple-system, sans-serif" font-size="6.5" fill="#94A3B8">{desc[:34]}</text>
  <text x="14" y="138" font-family="system-ui, -apple-system, sans-serif" font-size="6.5" fill="#94A3B8">{desc[34:68]}</text>
</svg>'''
    return svg


# --- 6. First-Run Scientific Quickstart Guide ---
def generate_onboarding_card():
    # 420x220, center 210, 110
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="420" height="220" viewBox="0 0 420 220">
  <rect width="420" height="220" rx="3" fill="#11141D" stroke="#2E374C" stroke-width="1.5"/>
  <rect x="0" y="0" width="420" height="26" rx="3" fill="#181D2A"/>
  <line x1="0" y1="26" x2="420" y2="26" stroke="#2E374C" stroke-width="1"/>
  <circle cx="16" cy="13" r="4.5" fill="#38BDF8"/>
  <text x="28" y="17" font-family="system-ui, -apple-system, sans-serif" font-size="10" font-weight="bold" fill="#F8FAFC">LABORATORY EXPERIMENTATION PROTOCOL</text>
  <text x="406" y="17" font-family="system-ui, -apple-system, sans-serif" font-size="8" fill="#94A3B8" text-anchor="end">VACUUM CHAMBER v3.0</text>

  <!-- Instructions Grid -->
  <rect x="16" y="36" width="388" height="34" rx="2" fill="#161A26" stroke="#252D3E" stroke-width="1"/>
  <text x="26" y="49" font-family="system-ui, -apple-system, sans-serif" font-size="8" font-weight="bold" fill="#38BDF8">1. INJECT ELEMENTS</text>
  <text x="26" y="61" font-family="system-ui, -apple-system, sans-serif" font-size="7.5" fill="#CBD5E1">Click [ADD] or press [A] to open the periodic dock and inject base atoms into the vacuum.</text>

  <rect x="16" y="76" width="388" height="34" rx="2" fill="#161A26" stroke="#252D3E" stroke-width="1"/>
  <text x="26" y="89" font-family="system-ui, -apple-system, sans-serif" font-size="8" font-weight="bold" fill="#10B981">2. SYNTHESIZE MOLECULES</text>
  <text x="26" y="101" font-family="system-ui, -apple-system, sans-serif" font-size="7.5" fill="#CBD5E1">Drag atoms into proximity. Exothermic reactions emit orange plasma bursts and photons.</text>

  <rect x="16" y="116" width="388" height="34" rx="2" fill="#161A26" stroke="#252D3E" stroke-width="1"/>
  <text x="26" y="129" font-family="system-ui, -apple-system, sans-serif" font-size="8" font-weight="bold" fill="#C084FC">3. PHOTOLYSIS &amp; COSMIC IONIZATION</text>
  <text x="26" y="141" font-family="system-ui, -apple-system, sans-serif" font-size="7.5" fill="#CBD5E1">Toggle [UV] for actinic photolysis into free radicals. Cosmic rays ionize atoms into charged ions.</text>

  <!-- Dismiss Action Button -->
  <rect x="120" y="164" width="180" height="34" rx="2" fill="#0C253D" stroke="#38BDF8" stroke-width="1.2"/>
  <text x="210" y="184" font-family="system-ui, -apple-system, sans-serif" font-size="9.5" font-weight="bold" fill="#38BDF8" text-anchor="middle">START EXPERIMENT [CLICK]</text>
  <text x="210" y="209" font-family="system-ui, -apple-system, sans-serif" font-size="7" fill="#64748B" text-anchor="middle">Press any key or click to dismiss this protocol guide</text>
</svg>'''
    return svg


# --- 7. Chemical Discovery Compendium (Catalog Modal) Assets ---
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
            bg = "#181D2A" if is_active else "#10131B"
            border = tcol if is_active else "#22293A"
            fg = tcol if is_active else "#64748B"
            weight = "bold" if is_active else "normal"
            tab_svg.append(f'<rect x="{tx}" y="28" width="{tw}" height="18" rx="2" fill="{bg}" stroke="{border}" stroke-width="1"/>')
            tab_svg.append(f'<text x="{tx + tw/2}" y="40.5" font-family="system-ui, -apple-system, sans-serif" font-size="7.5" font-weight="{weight}" fill="{fg}" text-anchor="middle">{tname}</text>')
            if is_active:
                tab_svg.append(f'<line x1="{tx+4}" y1="46" x2="{tx+tw-4}" y2="46" stroke="{tcol}" stroke-width="2"/>')

        tabs_str = "\n  ".join(tab_svg)

        return f'''
  <!-- Chassis Frame (440x250) -->
  <rect width="440" height="250" rx="3" fill="#11141C" stroke="#2B3448" stroke-width="1.5"/>
  
  <!-- Header Bar -->
  <rect x="0" y="0" width="440" height="26" rx="3" fill="#181D2A"/>
  <line x1="0" y1="26" x2="440" y2="26" stroke="#2B3448" stroke-width="1"/>
  <circle cx="14" cy="13" r="4" fill="#38BDF8"/>
  <text x="26" y="17" font-family="system-ui, -apple-system, sans-serif" font-size="9.5" font-weight="bold" fill="#F8FAFC">{title}</text>
  <text x="390" y="17" font-family="system-ui, -apple-system, sans-serif" font-size="8" fill="#94A3B8" text-anchor="end">{subtitle}</text>
  
  <!-- Close Button Bay in Upper Right -->
  <rect x="406" y="5" width="22" height="16" rx="2" fill="#1C1418" stroke="#EF4444" stroke-width="1"/>
  <text x="417" y="16.5" font-family="system-ui, -apple-system, sans-serif" font-size="11" font-weight="bold" fill="#EF4444" text-anchor="middle">×</text>

  <!-- Navigation Tabs -->
  {tabs_str}

  <!-- Bottom Action Bar -->
  <rect x="0" y="222" width="440" height="28" rx="3" fill="#181D2A"/>
  <line x1="0" y1="222" x2="440" y2="222" stroke="#2B3448" stroke-width="1"/>
  
  <!-- Reset Button [D] -->
  <rect x="14" y="226" width="110" height="20" rx="2" fill="#241318" stroke="#EF4444" stroke-width="1"/>
  <text x="69" y="239" font-family="system-ui, -apple-system, sans-serif" font-size="7.5" font-weight="bold" fill="#F87171" text-anchor="middle">Reset Archive [D]</text>
  
  <!-- Center Hint -->
  <text x="220" y="239" font-family="system-ui, -apple-system, sans-serif" font-size="7.5" fill="#94A3B8" text-anchor="middle">Click species to inject or inspect • [×] to close</text>
  
  <!-- Close Catalog Button -->
  <rect x="316" y="226" width="110" height="20" rx="2" fill="#0C253D" stroke="#38BDF8" stroke-width="1"/>
  <text x="371" y="239" font-family="system-ui, -apple-system, sans-serif" font-size="8" font-weight="bold" fill="#38BDF8" text-anchor="middle">Close Catalog [×]</text>
'''

    # Clean inner shelf background for card tabs (does NOT draw duplicate cards!)
    def render_clean_shelf_tab(tab_idx, title, sub_title, left_btn, right_btn):
        svg = ['<svg xmlns="http://www.w3.org/2000/svg" width="440" height="250" viewBox="0 0 440 250">']
        svg.append(base_comp_modal(tab_idx, title, sub_title))
        # Inner shelf frame
        svg.append('  <rect x="10" y="50" width="420" height="168" rx="2" fill="#0B0E15" stroke="#1D2433" stroke-width="1"/>')
        svg.append('  <rect x="14" y="54" width="220" height="16" rx="1" fill="#131722"/>')
        svg.append('  <text x="22" y="65" font-family="system-ui, -apple-system, sans-serif" font-size="7" fill="#94A3B8">SELECT ANY SPECIES CARD BELOW TO INJECT INTO CHAMBER</text>')
        # Page controls on right
        if left_btn:
            svg.append(f'  <rect x="270" y="54" width="70" height="16" rx="2" fill="{left_btn[2]}" stroke="{left_btn[3]}" stroke-width="0.8"/>')
            svg.append(f'  <text x="305" y="65" font-family="system-ui, -apple-system, sans-serif" font-size="6.5" font-weight="bold" fill="{left_btn[4]}" text-anchor="middle">{left_btn[0]}</text>')
        if right_btn:
            svg.append(f'  <rect x="348" y="54" width="70" height="16" rx="2" fill="{right_btn[2]}" stroke="{right_btn[3]}" stroke-width="0.8"/>')
            svg.append(f'  <text x="383" y="65" font-family="system-ui, -apple-system, sans-serif" font-size="6.5" font-weight="bold" fill="{right_btn[4]}" text-anchor="middle">{right_btn[0]}</text>')
        svg.append('</svg>')
        return "\n".join(svg)

    # 1. comp_summary (Overview Page)
    p1 = f'''<svg xmlns="http://www.w3.org/2000/svg" width="440" height="250" viewBox="0 0 440 250">
{base_comp_modal(1, "Discovery Compendium", "129 Total Species")}
  <!-- Progress Overview -->
  <rect x="14" y="52" width="412" height="32" rx="2" fill="#161B26" stroke="#2B3448" stroke-width="1"/>
  <text x="26" y="65" font-family="system-ui, -apple-system, sans-serif" font-size="8" fill="#94A3B8">LABORATORY DISCOVERY PROGRESS</text>
  <text x="414" y="65" font-family="system-ui, -apple-system, sans-serif" font-size="8" font-weight="bold" fill="#38BDF8" text-anchor="end">129 TARGET SPECIES</text>
  <rect x="26" y="71" width="388" height="6" rx="1" fill="#0A0C12"/>
  <rect x="26" y="71" width="110" height="6" rx="1" fill="#38BDF8"/>
</svg>'''
    costumes["comp_summary"] = make_svg_asset(p1, "comp_summary", 220, 125)

    # 2. comp_elements (Clean Shelf Background - cards are sprites!)
    p2 = render_clean_shelf_tab(
        2, "Base Chemical Elements", "19 Available Elements",
        None, ("19 Elements", 0, "#0E281C", "#10B981", "#10B981")
    )
    costumes["comp_elements"] = make_svg_asset(p2, "comp_elements", 220, 125)

    # 3. comp_molecules_1
    p3 = render_clean_shelf_tab(
        3, "Neutral Molecules", "Part 1 of 2",
        ("&lt; Page 1", 1, "#181D2A", "#2E374C", "#94A3B8"),
        ("Page 2 &gt;", 2, "#0C253D", "#38BDF8", "#38BDF8")
    )
    costumes["comp_molecules_1"] = make_svg_asset(p3, "comp_molecules_1", 220, 125)

    # 4. comp_molecules_2
    p4 = render_clean_shelf_tab(
        3, "Neutral Molecules", "Part 2 of 2",
        ("&lt; Page 1", 1, "#0C253D", "#38BDF8", "#38BDF8"),
        ("Page 2 &gt;", 2, "#181D2A", "#2E374C", "#94A3B8")
    )
    costumes["comp_molecules_2"] = make_svg_asset(p4, "comp_molecules_2", 220, 125)

    # 5. comp_radicals
    p5 = render_clean_shelf_tab(
        4, "Free Radical Species", "UV Photolysis Required",
        ("RADICALS", 1, "#261318", "#EF4444", "#EF4444"),
        ("UV ACTIVE", 2, "#181D2A", "#2E374C", "#94A3B8")
    )
    costumes["comp_radicals"] = make_svg_asset(p5, "comp_radicals", 220, 125)

    # 6. comp_ions
    p6 = render_clean_shelf_tab(
        5, "Structured Ion Species", "Cosmic Ray Ionization",
        ("IONS", 1, "#221133", "#A855F7", "#A855F7"),
        ("COSMIC RAYS", 2, "#181D2A", "#2E374C", "#94A3B8")
    )
    costumes["comp_ions"] = make_svg_asset(p6, "comp_ions", 220, 125)

    return costumes


# --- 8. Dynamic Telemetry Banner Assets ---
def generate_telemetry_assets():
    costumes = {}
    messages = [
        ("telem_ready", "#10B981", "CHAMBER READY • DRAG ATOMS TO MERGE • [A] ADD  [X] DEL  [I] INSPECT  [U] UV  [F] FREEZE  [C] CATALOG"),
        ("telem_idle", "#10B981", "CHAMBER READY • DRAG ATOMS TO MERGE • [A] ADD  [X] DEL  [I] INSPECT  [U] UV  [F] FREEZE  [C] CATALOG"),
        ("telem_react", "#38BDF8", "CHEMICAL SYNTHESIS • MOLECULAR BOND FORMED SUCCESSFULLY"),
        ("telem_exo", "#F59E0B", "EXOTHERMIC REACTION • THERMAL ENERGY RELEASED • PHOTON EMITTED"),
        ("telem_uv_req", "#C084FC", "ACTINIC UV REQUIRED • TURN ON UV LAMP [U] TO TRIGGER PHOTOLYSIS"),
        ("telem_cosmic", "#38BDF8", "COSMIC RAY IMPACT • HIGH-ENERGY RELATIVISTIC PARTICLE IONIZED ATOM"),
        ("telem_inert", "#94A3B8", "INERT COLLISION • NO REACTIVE PATHWAY UNDER CURRENT CONDITIONS"),
        ("telem_discover", "#F59E0B", "★ NOVEL SPECIES DISCOVERED! RECORDED IN LABORATORY ARCHIVE [C]"),
        ("telem_frozen", "#7DD3FC", "❄ CRYOSTATIC FREEZE ACTIVE • THERMAL VELOCITIES AND CLOCKS PAUSED"),
        ("telem_save", "#38BDF8", "RECORD SAVED • DISCOVERY SNAPSHOT STORED TO LOCAL REGISTER"),
        ("telem_load", "#818CF8", "RECORD LOADED • DISCOVERY SNAPSHOT RESTORED SUCCESSFULLY"),
        ("telem_purge", "#EF4444", "CHAMBER EVACUATED • VACUUM PURGED • ALL ACTIVE PARTICLES CLEARED")
    ]

    for name, col, text in messages:
        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="460" height="22" viewBox="0 0 460 22">
  <rect width="460" height="22" rx="2" fill="#10131B" stroke="#22293A" stroke-width="1"/>
  <circle cx="12" cy="11" r="3" fill="{col}"/>
  <text x="22" y="14.5" font-family="system-ui, -apple-system, sans-serif" font-size="7.5" font-weight="bold" fill="{col}">{text[:85]}</text>
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
  <line x1="2" y1="7" x2="60" y2="7" stroke="url(#cosmic_streak)" stroke-width="2.5" stroke-linecap="round"/>
  <circle cx="58" cy="7" r="3" fill="#FFFFFF"/>
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
  <circle cx="30" cy="30" r="{r}" fill="none" stroke="#38BDF8" stroke-width="1.8" stroke-dasharray="3,3"/>
  <circle cx="30" cy="30" r="{r-5}" fill="#38BDF8" fill-opacity="0.25"/>
  <circle cx="30" cy="30" r="2" fill="#FFFFFF"/>
</svg>'''
        costumes[f"fx_bond_{frame}"] = make_svg_asset(fx_svg, f"fx_bond_{frame}", 30, 30)

    # Ionization electric zap (2 frames)
    for frame, pts in [(1, "30,8 22,26 34,24 26,52"), (2, "30,8 36,26 24,24 32,52")]:
        fx_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="60" height="60" viewBox="0 0 60 60">
  <circle cx="30" cy="30" r="18" fill="#38BDF8" fill-opacity="0.15"/>
  <polyline points="{pts}" fill="none" stroke="#67E8F9" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
</svg>'''
        costumes[f"fx_zap_{frame}"] = make_svg_asset(fx_svg, f"fx_zap_{frame}", 30, 30)

    # Annihilation poof (2 frames)
    for frame, r in [(1, 12), (2, 22)]:
        fx_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="60" height="60" viewBox="0 0 60 60">
  <circle cx="30" cy="30" r="{r}" fill="#A855F7" fill-opacity="0.3" stroke="#C084FC" stroke-width="1.6"/>
  <circle cx="30" cy="30" r="{max(2, r-6)}" fill="none" stroke="#FFFFFF" stroke-width="0.8" stroke-dasharray="2,2"/>
</svg>'''
        costumes[f"fx_poof_{frame}"] = make_svg_asset(fx_svg, f"fx_poof_{frame}", 30, 30)

    # Toast Banner (240x36, center 120, 18)
    toast_svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="240" height="36" viewBox="0 0 240 36">
  <rect width="240" height="36" rx="3" fill="#121622" stroke="#38BDF8" stroke-width="1.2"/>
  <circle cx="20" cy="18" r="8" fill="#38BDF8"/>
  <text x="20" y="21.5" font-family="system-ui, -apple-system, sans-serif" font-size="9" font-weight="bold" fill="#0C0E14" text-anchor="middle">★</text>
  <text x="36" y="16" font-family="system-ui, -apple-system, sans-serif" font-size="8" font-weight="bold" fill="#38BDF8">Discovery Cataloged</text>
  <text x="36" y="27" font-family="system-ui, -apple-system, sans-serif" font-size="7" fill="#E2E8F0">New species added to laboratory archive</text>
</svg>'''
    costumes["toast_banner"] = make_svg_asset(toast_svg, "toast_banner", 120, 18)

    return costumes


# --- 10. Individual Clickable Element Asset Generators (md.md compliance) ---

def generate_tool_rail_bar():
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="460" height="28" viewBox="0 0 460 28">
  <rect width="460" height="28" rx="2" fill="#0E1118" stroke="#1E2536" stroke-width="1"/>
</svg>'''
    return make_svg_asset(svg, "tool_rail_bar", 230, 14)


def generate_comp_tab_costumes():
    tabs = [
        ("overview", "Overview", 78, "#6366F1"),
        ("elements", "Elements", 78, "#10B981"),
        ("molecules", "Molecules", 86, "#38BDF8"),
        ("radicals", "Radicals", 80, "#EF4444"),
        ("ions", "Ions", 74, "#A855F7")
    ]
    assets = {}
    for key, title, w, col in tabs:
        svg_inact = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="18" viewBox="0 0 {w} 18">
  <rect width="{w}" height="18" rx="2" fill="#10131B" stroke="#22293A" stroke-width="1"/>
  <text x="{w/2}" y="12.5" font-family="system-ui, -apple-system, sans-serif" font-size="7.5" fill="#64748B" text-anchor="middle">{title}</text>
</svg>'''
        svg_act = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="18" viewBox="0 0 {w} 18">
  <rect width="{w}" height="18" rx="2" fill="#181D2A" stroke="{col}" stroke-width="1"/>
  <text x="{w/2}" y="12.5" font-family="system-ui, -apple-system, sans-serif" font-size="7.5" font-weight="bold" fill="{col}" text-anchor="middle">{title}</text>
  <line x1="4" y1="18" x2="{w-4}" y2="18" stroke="{col}" stroke-width="2"/>
</svg>'''
        assets[f"tab_{key}_inactive"] = make_svg_asset(svg_inact, f"tab_{key}_inactive", w // 2, 9)
        assets[f"tab_{key}_active"] = make_svg_asset(svg_act, f"tab_{key}_active", w // 2, 9)
    return assets


def generate_comp_button_costumes():
    assets = {}
    svg_close_x = '''<svg xmlns="http://www.w3.org/2000/svg" width="22" height="16" viewBox="0 0 22 16">
  <rect width="22" height="16" rx="2" fill="#1C1418" stroke="#EF4444" stroke-width="1"/>
  <text x="11" y="12" font-family="system-ui, -apple-system, sans-serif" font-size="11" font-weight="bold" fill="#EF4444" text-anchor="middle">×</text>
</svg>'''
    assets["comp_btn_close_x"] = make_svg_asset(svg_close_x, "comp_btn_close_x", 11, 8)

    svg_close_bot = '''<svg xmlns="http://www.w3.org/2000/svg" width="110" height="20" viewBox="0 0 110 20">
  <rect width="110" height="20" rx="2" fill="#0C253D" stroke="#38BDF8" stroke-width="1"/>
  <text x="55" y="13" font-family="system-ui, -apple-system, sans-serif" font-size="8" font-weight="bold" fill="#38BDF8" text-anchor="middle">Close Catalog [×]</text>
</svg>'''
    assets["comp_btn_close_bottom"] = make_svg_asset(svg_close_bot, "comp_btn_close_bottom", 55, 10)

    svg_reset = '''<svg xmlns="http://www.w3.org/2000/svg" width="110" height="20" viewBox="0 0 110 20">
  <rect width="110" height="20" rx="2" fill="#241318" stroke="#EF4444" stroke-width="1"/>
  <text x="55" y="13" font-family="system-ui, -apple-system, sans-serif" font-size="7.5" font-weight="bold" fill="#F87171" text-anchor="middle">Reset Archive [D]</text>
</svg>'''
    assets["comp_btn_reset"] = make_svg_asset(svg_reset, "comp_btn_reset", 55, 10)

    svg_next = '''<svg xmlns="http://www.w3.org/2000/svg" width="70" height="14" viewBox="0 0 70 14">
  <rect width="70" height="14" rx="2" fill="#181D2A" stroke="#2E374C" stroke-width="0.8"/>
  <text x="35" y="10" font-family="system-ui, -apple-system, sans-serif" font-size="6.5" font-weight="bold" fill="#94A3B8" text-anchor="middle">Page 2 &gt;</text>
</svg>'''
    assets["comp_btn_next"] = make_svg_asset(svg_next, "comp_btn_next", 35, 7)

    svg_prev = '''<svg xmlns="http://www.w3.org/2000/svg" width="70" height="14" viewBox="0 0 70 14">
  <rect width="70" height="14" rx="2" fill="#0E281C" stroke="#10B981" stroke-width="0.8"/>
  <text x="35" y="10" font-family="system-ui, -apple-system, sans-serif" font-size="6.5" font-weight="bold" fill="#10B981" text-anchor="middle">&lt; Page 1</text>
</svg>'''
    assets["comp_btn_prev"] = make_svg_asset(svg_prev, "comp_btn_prev", 35, 7)

    return assets


def generate_comp_category_cards():
    cards = [
        ("atoms", "Base Elements", "19", "Available", "H through I", "Browse [2]", "#10B981", "#0E281C"),
        ("molecules", "Molecules", "69", "Synthesizable", "Covalent &amp; Salts", "Browse [3]", "#38BDF8", "#0C253D"),
        ("radicals", "Radicals", "19", "UV Photolysis", "Unpaired Electrons", "Browse [4]", "#EF4444", "#261318"),
        ("ions", "Ions", "22", "Cosmic Ionization", "Charged Particles", "Browse [5]", "#A855F7", "#221133")
    ]
    assets = {}
    for key, title, count, sub1, sub2, btn_text, col, btn_bg in cards:
        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="98" height="124" viewBox="0 0 98 124">
  <rect width="98" height="124" rx="2" fill="#141824" stroke="{col}" stroke-width="1"/>
  <text x="49" y="16" font-family="system-ui, -apple-system, sans-serif" font-size="8.5" font-weight="bold" fill="{col}" text-anchor="middle">{title}</text>
  <text x="49" y="46" font-family="system-ui, -apple-system, sans-serif" font-size="22" font-weight="bold" fill="#FFFFFF" text-anchor="middle">{count}</text>
  <text x="49" y="64" font-family="system-ui, -apple-system, sans-serif" font-size="7.5" fill="{col}" text-anchor="middle">{sub1}</text>
  <text x="49" y="78" font-family="system-ui, -apple-system, sans-serif" font-size="7" fill="#94A3B8" text-anchor="middle">{sub2}</text>
  <rect x="8" y="96" width="82" height="18" rx="2" fill="{btn_bg}" stroke="{col}" stroke-width="0.8"/>
  <text x="49" y="108" font-family="system-ui, -apple-system, sans-serif" font-size="7.5" font-weight="bold" fill="{col}" text-anchor="middle">{btn_text}</text>
</svg>'''
        assets[f"comp_cat_{key}"] = make_svg_asset(svg, f"comp_cat_{key}", 49, 62)
    return assets


def generate_comp_elem_cards():
    assets = {}
    for s in db_chemistry.SPECIES[:19]:
        color = s["color"]
        border = s["border"]
        fg = "#0A0D14" if color in ["#E2E8F0", "#FACC15", "#A3E635", "#67E8F9", "#FFFFFF"] else "#FFFFFF"
        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="38" height="56" viewBox="0 0 38 56">
  <rect width="38" height="56" rx="2" fill="#141824" stroke="{color}" stroke-width="1"/>
  <text x="19" y="11" font-family="system-ui, -apple-system, sans-serif" font-size="6.5" fill="#94A3B8" text-anchor="middle">Z={s["z"]}</text>
  <circle cx="19" cy="24" r="8.5" fill="{color}" stroke="{border}" stroke-width="0.8"/>
  <text x="19" y="27" font-family="system-ui, -apple-system, sans-serif" font-size="8.5" font-weight="bold" fill="{fg}" text-anchor="middle">{s["symbol"]}</text>
  <text x="19" y="41" font-family="system-ui, -apple-system, sans-serif" font-size="6" font-weight="bold" fill="#F8FAFC" text-anchor="middle">{s["name"][:5]}</text>
  <rect x="5" y="45" width="28" height="8" rx="1" fill="#0E281C" stroke="{color}" stroke-width="0.5"/>
  <text x="19" y="51" font-family="system-ui, -apple-system, sans-serif" font-size="5" font-weight="bold" fill="{color}" text-anchor="middle">[ADD]</text>
</svg>'''
        assets[f"comp_elem_card_{s['id']}"] = make_svg_asset(svg, f"comp_elem_card_{s['id']}", 19, 28)
    return assets


def generate_comp_species_cards():
    assets = {}
    sp_map = {s["id"]: s for s in db_chemistry.SPECIES}
    tab_configs = [
        ("mol1", [20, 21, 22, 25, 39, 40, 44, 47], "#38BDF8", "INJECT"),
        ("mol2", [30, 32, 57, 58, 60, 71, 85, 106], "#38BDF8", "INJECT"),
        ("rad", [41, 42, 43, 28, 46, 29, 27, 56], "#EF4444", "PHOTOLYSIS"),
        ("ion", [109, 111, 118, 117, 123, 124, 119, 129], "#A855F7", "IONIZE")
    ]
    for prefix, ids, accent, tag in tab_configs:
        for sid in ids:
            s = sp_map[sid]
            form = format_subscripts(s["formula"])
            name = s["name"][:14]
            desc = s.get("desc", "")[:20]
            svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="98" height="68" viewBox="0 0 98 68">
  <rect width="98" height="68" rx="2" fill="#141824" stroke="{accent}" stroke-width="1"/>
  <rect x="6" y="6" width="86" height="24" rx="2" fill="#0A0C13"/>
  <text x="49" y="23" font-family="system-ui, -apple-system, sans-serif" font-size="13" font-weight="bold" fill="{accent}" text-anchor="middle">{form}</text>
  <text x="49" y="41" font-family="system-ui, -apple-system, sans-serif" font-size="7.5" font-weight="bold" fill="#F8FAFC" text-anchor="middle">{name}</text>
  <text x="49" y="51" font-family="system-ui, -apple-system, sans-serif" font-size="6.5" fill="#94A3B8" text-anchor="middle">{desc}</text>
  <rect x="24" y="56" width="50" height="9" rx="1.5" fill="#0C253D" stroke="{accent}" stroke-width="0.6"/>
  <text x="49" y="63.5" font-family="system-ui, -apple-system, sans-serif" font-size="6" font-weight="bold" fill="{accent}" text-anchor="middle">{tag}</text>
</svg>'''
            assets[f"comp_{prefix}_card_{sid}"] = make_svg_asset(svg, f"comp_{prefix}_card_{sid}", 49, 34)
    return assets


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
        ("freeze", "Freeze", "#0EA5E9"),
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

    # 10. Individual Clickable Element Costumes (md.md compliance)
    costumes["tool_rail_bar"] = generate_tool_rail_bar()
    costumes["palette_drawer_frame"] = generate_palette_frame()
    costumes.update(generate_palette_item_costumes())
    costumes.update(generate_comp_tab_costumes())
    costumes.update(generate_comp_button_costumes())
    costumes.update(generate_comp_category_cards())
    costumes.update(generate_comp_elem_cards())
    costumes.update(generate_comp_species_cards())

    print(f"SUCCESS: Generated {len(costumes)} verified vector graphic assets!")
    return costumes

if __name__ == "__main__":
    generate_all_assets()
