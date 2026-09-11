import os, hashlib, db_chemistry

def make_svg_asset(svg_text, name, cx, cy):
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
    # Convert numbers to unicode subscripts for formulas
    sub_map = {'0': '₀', '1': '₁', '2': '₂', '3': '₃', '4': '₄', '5': '₅', '6': '₆', '7': '₇', '8': '₈', '9': '₉', '+': '⁺', '-': '⁻'}
    res = ""
    for ch in formula:
        res += sub_map.get(ch, ch)
    return res

def generate_species_svg(s):
    # Dimensions: 64x64, center 32, 32
    sym = s["symbol"]
    charge = s["charge"]
    color = s["color"]
    border = s["border"]
    stype = s["type"]

    is_ion = charge != 0
    is_radical = "•" in sym
    is_element = s["id"] <= 19

    # Clean display text
    disp_text = format_subscripts(sym)
    if len(disp_text) > 6:
        font_size = "11"
    elif len(disp_text) > 4:
        font_size = "12"
    elif len(disp_text) > 2:
        font_size = "14"
    else:
        font_size = "17"

    # SVG styling
    svg = ['<svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 64 64">']

    # Defs: Radial gradient for 3D sphere look
    grad_id = f"g_{s['id']}"
    svg.append('  <defs>')
    svg.append(f'    <radialGradient id="{grad_id}" cx="35%" cy="35%" r="65%">')
    svg.append(f'      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.85"/>')
    svg.append(f'      <stop offset="35%" stop-color="{color}" stop-opacity="0.95"/>')
    svg.append(f'      <stop offset="100%" stop-color="{border}" stop-opacity="1.0"/>')
    svg.append('    </radialGradient>')
    if is_ion:
        halo_color = "#38BDF8" if charge > 0 else "#FACC15"
        svg.append(f'    <filter id="glow_{s["id"]}" x="-30%" y="-30%" width="160%" height="160%">')
        svg.append(f'      <feDropShadow dx="0" dy="0" stdDeviation="3" flood-color="{halo_color}" flood-opacity="0.9"/>')
        svg.append('    </filter>')
    svg.append('  </defs>')

    # Background / Shape
    if is_element:
        # Atomic circle
        r = 24 if s["z"] > 10 else 22
        svg.append(f'  <circle cx="32" cy="32" r="{r}" fill="url(#{grad_id})" stroke="{border}" stroke-width="2.5"/>')
        # Atomic number badge
        svg.append(f'  <text x="18" y="21" font-family="sans-serif" font-size="8" font-weight="bold" fill="#ffffff" opacity="0.8">{s["z"]}</text>')
    elif is_ion:
        # Ion with glowing ring
        halo_color = "#38BDF8" if charge > 0 else "#FACC15"
        svg.append(f'  <circle cx="32" cy="32" r="26" fill="none" stroke="{halo_color}" stroke-width="2" stroke-dasharray="3,2" filter="url(#glow_{s["id"]})"/>')
        svg.append(f'  <circle cx="32" cy="32" r="22" fill="url(#{grad_id})" stroke="{border}" stroke-width="2"/>')
        # Charge badge in upper-right
        ch_text = "+" if charge == 1 else ("-" if charge == -1 else f"{abs(charge)}{'+' if charge > 0 else '-'}")
        svg.append(f'  <circle cx="48" cy="16" r="9" fill="{halo_color}" stroke="#0F172A" stroke-width="1.5"/>')
        svg.append(f'  <text x="48" y="20" font-family="sans-serif" font-size="10" font-weight="bold" fill="#0F172A" text-anchor="middle">{ch_text}</text>')
    else:
        # Molecular compound: rounded pill / bonded atom
        svg.append(f'  <rect x="6" y="14" width="52" height="36" rx="18" fill="url(#{grad_id})" stroke="{border}" stroke-width="2.5"/>')
        # Subtle bond line decoration
        svg.append(f'  <line x1="12" y1="32" x2="52" y2="32" stroke="#ffffff" stroke-width="1" stroke-opacity="0.3" stroke-dasharray="2,2"/>')

    # Formula text
    text_color = "#0F172A" if color in ["#E2E8F0", "#FACC15", "#A3E635", "#67E8F9"] else "#FFFFFF"
    y_offset = "37" if is_element or is_ion else "37"
    svg.append(f'  <text x="32" y="{y_offset}" font-family="sans-serif" font-size="{font_size}" font-weight="bold" fill="{text_color}" text-anchor="middle" filter="drop-shadow(0px 1px 1px rgba(0,0,0,0.5))">{disp_text}</text>')

    # Radical indicator
    if is_radical:
        svg.append(f'  <circle cx="52" cy="18" r="4" fill="#F43F5E" stroke="#ffffff" stroke-width="1"/>')

    svg.append('</svg>')
    return "\n".join(svg)

def generate_backdrops():
    # 480x360, center 240, 180
    def base_frame():
        return '''
  <!-- Vacuum Chamber Outer Hull -->
  <rect width="480" height="360" fill="#070A12"/>
  
  <!-- Starfield / Cosmic Vacuum Dust -->
  <circle cx="50" cy="80" r="1" fill="#475569" opacity="0.6"/>
  <circle cx="120" cy="220" r="1.5" fill="#38BDF8" opacity="0.5"/>
  <circle cx="210" cy="130" r="1" fill="#ffffff" opacity="0.7"/>
  <circle cx="340" cy="95" r="1.5" fill="#FACC15" opacity="0.4"/>
  <circle cx="420" cy="260" r="1" fill="#A855F7" opacity="0.6"/>
  <circle cx="80" cy="290" r="1" fill="#ffffff" opacity="0.5"/>
  <circle cx="280" cy="270" r="1.5" fill="#38BDF8" opacity="0.6"/>
  <circle cx="390" cy="160" r="1" fill="#475569" opacity="0.7"/>

  <!-- Chamber Boundary Frame -->
  <rect x="10" y="44" width="460" height="268" rx="8" fill="#0B1120" stroke="#1E293B" stroke-width="2"/>
  
  <!-- Subtle Chamber Grid Lines -->
  <line x1="10" y1="111" x2="470" y2="111" stroke="#131C2E" stroke-width="1" stroke-dasharray="4,4"/>
  <line x1="10" y1="178" x2="470" y2="178" stroke="#131C2E" stroke-width="1" stroke-dasharray="4,4"/>
  <line x1="10" y1="245" x2="470" y2="245" stroke="#131C2E" stroke-width="1" stroke-dasharray="4,4"/>
  <line x1="125" y1="44" x2="125" y2="312" stroke="#131C2E" stroke-width="1" stroke-dasharray="4,4"/>
  <line x1="240" y1="44" x2="240" y2="312" stroke="#131C2E" stroke-width="1" stroke-dasharray="4,4"/>
  <line x1="355" y1="44" x2="355" y2="312" stroke="#131C2E" stroke-width="1" stroke-dasharray="4,4"/>

  <!-- Top Control Bar Panel -->
  <rect x="0" y="0" width="480" height="42" fill="#0F172A" stroke="#334155" stroke-width="1.5"/>
  
  <!-- Bottom Status Strip -->
  <rect x="0" y="314" width="480" height="46" fill="#0F172A" stroke="#334155" stroke-width="1.5"/>
  <text x="16" y="336" font-family="sans-serif" font-size="11" font-weight="bold" fill="#38BDF8">VACUUM CHAMBER</text>
  <text x="16" y="349" font-family="sans-serif" font-size="9" fill="#94A3B8">Drag &amp; drop to react • Click atom to inspect • UV &amp; Cosmic rays active</text>
  <text x="464" y="340" font-family="sans-serif" font-size="10" font-weight="bold" fill="#64748B" text-anchor="end">PRESSURE: 10⁻¹⁰ TORR</text>
'''

    # Standard Vacuum
    bg_std = f'''<svg xmlns="http://www.w3.org/2000/svg" width="480" height="360" viewBox="0 0 480 360">
{base_frame()}
</svg>'''

    # UV Active
    bg_uv = f'''<svg xmlns="http://www.w3.org/2000/svg" width="480" height="360" viewBox="0 0 480 360">
  <defs>
    <linearGradient id="uv_glow" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#A855F7" stop-opacity="0.4"/>
      <stop offset="35%" stop-color="#A855F7" stop-opacity="0.15"/>
      <stop offset="100%" stop-color="#A855F7" stop-opacity="0.0"/>
    </linearGradient>
  </defs>
{base_frame()}
  <!-- Top UV Radiation Lamp Bar -->
  <rect x="10" y="44" width="460" height="6" fill="#C084FC" filter="drop-shadow(0 0 8px #A855F7)"/>
  <!-- UV Radiation Beam Cascade -->
  <rect x="10" y="50" width="460" height="262" fill="url(#uv_glow)"/>
  <text x="240" y="70" font-family="sans-serif" font-size="12" font-weight="bold" fill="#E9D5FF" text-anchor="middle" letter-spacing="3" opacity="0.8">⚡ ULTRAVIOLET RADIATION ACTIVE ⚡</text>
</svg>'''

    # Frozen Time
    bg_freeze = f'''<svg xmlns="http://www.w3.org/2000/svg" width="480" height="360" viewBox="0 0 480 360">
  <defs>
    <radialGradient id="frost_corner" cx="0%" cy="0%" r="100%">
      <stop offset="0%" stop-color="#38BDF8" stop-opacity="0.5"/>
      <stop offset="60%" stop-color="#38BDF8" stop-opacity="0.1"/>
      <stop offset="100%" stop-color="#38BDF8" stop-opacity="0.0"/>
    </radialGradient>
  </defs>
{base_frame()}
  <!-- Frost Overlay Vignettes -->
  <rect x="10" y="44" width="100" height="100" fill="url(#frost_corner)"/>
  <!-- Icy Chamber Border Highlight -->
  <rect x="10" y="44" width="460" height="268" rx="8" fill="none" stroke="#38BDF8" stroke-width="2.5" opacity="0.8"/>
  <text x="240" y="70" font-family="sans-serif" font-size="12" font-weight="bold" fill="#7DD3FC" text-anchor="middle" letter-spacing="3" opacity="0.9">❄ TIME FROZEN ❄</text>
</svg>'''

    return bg_std, bg_uv, bg_freeze

def generate_button_svg(label, icon, active=False, active_color="#38BDF8"):
    # Size: 44x32, center 22, 16
    bg = active_color if active else "#1E293B"
    border = "#F8FAFC" if active else "#475569"
    fg = "#0F172A" if active else "#F1F5F9"
    sub_fg = "#0F172A" if active else "#94A3B8"

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="44" height="32" viewBox="0 0 44 32">
  <rect x="1" y="1" width="42" height="30" rx="6" fill="{bg}" stroke="{border}" stroke-width="1.5"/>
  <text x="22" y="14" font-family="sans-serif" font-size="11" font-weight="bold" fill="{fg}" text-anchor="middle">{icon}</text>
  <text x="22" y="26" font-family="sans-serif" font-size="7" font-weight="bold" fill="{sub_fg}" text-anchor="middle">{label}</text>
</svg>'''

def generate_palette_elements_svg():
    # Drawer bar showing elements
    # 480x80, center 240, 40
    svg = ['<svg xmlns="http://www.w3.org/2000/svg" width="480" height="80" viewBox="0 0 480 80">']
    svg.append('  <rect width="480" height="80" fill="#0B1120" stroke="#334155" stroke-width="2" rx="8"/>')
    svg.append('  <text x="240" y="14" font-family="sans-serif" font-size="9" font-weight="bold" fill="#38BDF8" text-anchor="middle">ELEMENT SPAWNER PALETTE • CLICK TO SPAWN</text>')
    
    # 19 elements in 2 rows
    row1 = db_chemistry.SPECIES[:10]
    row2 = db_chemistry.SPECIES[10:19]
    
    for i, el in enumerate(row1):
        x = 24 + i * 48
        y = 22
        svg.append(f'  <circle cx="{x+16}" cy="{y+16}" r="14" fill="{el["color"]}" stroke="{el["border"]}" stroke-width="1.5"/>')
        fg = "#0F172A" if el["color"] in ["#E2E8F0", "#FACC15", "#A3E635", "#67E8F9"] else "#FFFFFF"
        svg.append(f'  <text x="{x+16}" y="{y+20}" font-family="sans-serif" font-size="10" font-weight="bold" fill="{fg}" text-anchor="middle">{el["symbol"]}</text>')

    for i, el in enumerate(row2):
        x = 48 + i * 48
        y = 52
        svg.append(f'  <circle cx="{x+16}" cy="{y+12}" r="12" fill="{el["color"]}" stroke="{el["border"]}" stroke-width="1.5"/>')
        fg = "#0F172A" if el["color"] in ["#E2E8F0", "#FACC15", "#A3E635", "#67E8F9"] else "#FFFFFF"
        svg.append(f'  <text x="{x+16}" y="{y+16}" font-family="sans-serif" font-size="9" font-weight="bold" fill="{fg}" text-anchor="middle">{el["symbol"]}</text>')

    svg.append('</svg>')
    return "\n".join(svg)

def generate_all_assets():
    os.makedirs("/workspaces/scratch/assets", exist_ok=True)
    costumes = {}

    # 1. Generate 129 Species Costumes
    for s in db_chemistry.SPECIES:
        svg_text = generate_species_svg(s)
        asset = make_svg_asset(svg_text, f"species_{s['id']}", 32, 32)
        costumes[f"species_{s['id']}"] = asset

    # 2. Backdrops
    bg_std, bg_uv, bg_freeze = generate_backdrops()
    costumes["backdrop_vacuum"] = make_svg_asset(bg_std, "backdrop_vacuum", 240, 180)
    costumes["backdrop_uv"] = make_svg_asset(bg_uv, "backdrop_uv", 240, 180)
    costumes["backdrop_frozen"] = make_svg_asset(bg_freeze, "backdrop_frozen", 240, 180)

    # 3. UI Buttons
    buttons = [
        ("btn_add", "ADD", "+", False, "#10B981"),
        ("btn_add_active", "ADD", "+", True, "#10B981"),
        ("btn_del", "DEL", "-", False, "#EF4444"),
        ("btn_del_active", "DEL", "-", True, "#EF4444"),
        ("btn_uv", "UV", "☀️", False, "#A855F7"),
        ("btn_uv_active", "UV", "☀️", True, "#A855F7"),
        ("btn_freeze", "FREEZE", "❄", False, "#38BDF8"),
        ("btn_freeze_active", "FREEZE", "❄", True, "#38BDF8"),
        ("btn_info", "INFO", "ℹ", False, "#F59E0B"),
        ("btn_info_active", "INFO", "ℹ", True, "#F59E0B"),
        ("btn_discover", "BOOK", "📖", False, "#6366F1"),
        ("btn_sound", "SOUND", "🔊", False, "#14B8A6"),
        ("btn_sound_muted", "MUTE", "🔇", True, "#64748B"),
        ("btn_save", "SAVE", "💾", False, "#3B82F6"),
        ("btn_load", "LOAD", "📂", False, "#8B5CF6"),
        ("btn_clear", "CLEAR", "🗑", False, "#DC2626")
    ]
    for bname, label, icon, act, act_col in buttons:
        svg_b = generate_button_svg(label, icon, act, act_col)
        costumes[bname] = make_svg_asset(svg_b, bname, 22, 16)

    # 4. Spawner Palette Drawer
    pal_svg = generate_palette_elements_svg()
    costumes["palette_drawer"] = make_svg_asset(pal_svg, "palette_drawer", 240, 40)

    # 5. Cosmic Ray Particle
    cosmic_svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="60" height="12" viewBox="0 0 60 12">
  <defs>
    <linearGradient id="ray_g" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#EC4899" stop-opacity="0.1"/>
      <stop offset="70%" stop-color="#38BDF8" stop-opacity="0.8"/>
      <stop offset="100%" stop-color="#ffffff" stop-opacity="1.0"/>
    </linearGradient>
  </defs>
  <line x1="2" y1="6" x2="58" y2="6" stroke="url(#ray_g)" stroke-width="4" stroke-linecap="round"/>
  <circle cx="56" cy="6" r="3" fill="#ffffff" filter="drop-shadow(0 0 3px #38BDF8)"/>
</svg>'''
    costumes["cosmic_ray"] = make_svg_asset(cosmic_svg, "cosmic_ray", 30, 6)

    # 6. Photon Particle
    photon_svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">
  <circle cx="12" cy="12" r="9" fill="#FACC15" fill-opacity="0.3"/>
  <circle cx="12" cy="12" r="6" fill="#FACC15" fill-opacity="0.7"/>
  <circle cx="12" cy="12" r="3" fill="#ffffff"/>
  <path d="M 6 12 Q 9 6, 12 12 T 18 12" fill="none" stroke="#FEF08A" stroke-width="1.5"/>
</svg>'''
    costumes["photon_wave"] = make_svg_asset(photon_svg, "photon_wave", 12, 12)

    # 7. Visual Effects
    # Exothermic burst (3 frames)
    for frame, r, col in [(1, 16, "#F97316"), (2, 28, "#EF4444"), (3, 38, "#DC2626")]:
        fx_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="80" height="80" viewBox="0 0 80 80">
  <circle cx="40" cy="40" r="{r}" fill="{col}" fill-opacity="0.5" stroke="#FEF08A" stroke-width="3"/>
  <line x1="40" y1="{40-r-4}" x2="40" y2="{40-r+4}" stroke="#ffffff" stroke-width="2"/>
  <line x1="40" y1="{40+r-4}" x2="40" y2="{40+r+4}" stroke="#ffffff" stroke-width="2"/>
  <line x1="{40-r-4}" y1="40" x2="{40-r+4}" y2="40" stroke="#ffffff" stroke-width="2"/>
  <line x1="{40+r-4}" y1="40" x2="{40+r+4}" y2="40" stroke="#ffffff" stroke-width="2"/>
</svg>'''
        costumes[f"fx_exo_{frame}"] = make_svg_asset(fx_svg, f"fx_exo_{frame}", 40, 40)

    # Bond sparkle (2 frames)
    for frame, r in [(1, 14), (2, 24)]:
        fx_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="60" height="60" viewBox="0 0 60 60">
  <circle cx="30" cy="30" r="{r}" fill="none" stroke="#38BDF8" stroke-width="2.5" stroke-dasharray="3,3"/>
  <circle cx="30" cy="30" r="{r-4}" fill="#38BDF8" fill-opacity="0.3"/>
</svg>'''
        costumes[f"fx_bond_{frame}"] = make_svg_asset(fx_svg, f"fx_bond_{frame}", 30, 30)

    # Ionization zap (2 frames)
    for frame, pts in [(1, "30,10 24,28 34,26 28,50"), (2, "30,10 36,28 26,26 32,50")]:
        fx_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="60" height="60" viewBox="0 0 60 60">
  <polyline points="{pts}" fill="none" stroke="#38BDF8" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
  <circle cx="30" cy="30" r="18" fill="#06B6D4" fill-opacity="0.2"/>
</svg>'''
        costumes[f"fx_zap_{frame}"] = make_svg_asset(fx_svg, f"fx_zap_{frame}", 30, 30)

    # Delete poof (2 frames)
    for frame, r in [(1, 12), (2, 22)]:
        fx_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="60" height="60" viewBox="0 0 60 60">
  <circle cx="30" cy="30" r="{r}" fill="#A855F7" fill-opacity="0.4" stroke="#C084FC" stroke-width="2"/>
</svg>'''
        costumes[f"fx_poof_{frame}"] = make_svg_asset(fx_svg, f"fx_poof_{frame}", 30, 30)

    # 8. Discovery Toast Banner
    toast_svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="240" height="40" viewBox="0 0 240 40">
  <rect x="2" y="2" width="236" height="36" rx="18" fill="#0F172A" stroke="#38BDF8" stroke-width="2"/>
  <circle cx="22" cy="20" r="12" fill="#38BDF8"/>
  <text x="22" y="24" font-family="sans-serif" font-size="12" font-weight="bold" fill="#0F172A" text-anchor="middle">★</text>
  <text x="44" y="18" font-family="sans-serif" font-size="9" font-weight="bold" fill="#38BDF8">NEW COMPOUND DISCOVERED!</text>
  <text x="44" y="30" font-family="sans-serif" font-size="10" font-weight="bold" fill="#FFFFFF">Added to Compendium</text>
</svg>'''
    costumes["toast_banner"] = make_svg_asset(toast_svg, "toast_banner", 120, 20)

    print(f"Generated {len(costumes)} vector graphic assets successfully!")
    return costumes

if __name__ == "__main__":
    generate_all_assets()
