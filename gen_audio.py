import wave, struct, math, random, os, io, hashlib

RATE = 22050

def make_wav(samples):
    buf = io.BytesIO()
    with wave.open(buf, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(RATE)
        data = bytearray()
        for s in samples:
            # clamp to -32767 .. 32767
            val = int(max(-32767, min(32767, s)))
            data.extend(struct.pack("<h", val))
        w.writeframes(data)
    raw = buf.getvalue()
    md5 = hashlib.md5(raw).hexdigest()
    return raw, md5, len(samples)

def gen_click():
    dur = 0.03
    n = int(RATE * dur)
    samples = []
    for i in range(n):
        t = i / RATE
        env = (1.0 - t / dur) ** 2
        freq = 1400.0 - 600.0 * (t / dur)
        val = math.sin(2 * math.pi * freq * t) * 26000 * env
        samples.append(val)
    return make_wav(samples)

def gen_bond():
    dur = 0.18
    n = int(RATE * dur)
    samples = []
    for i in range(n):
        t = i / RATE
        env = math.sin(math.pi * (t / dur) ** 0.5) * (1.0 - t / dur)
        # Two harmonic tones: 587.33 Hz (D5) + 880 Hz (A5)
        s1 = math.sin(2 * math.pi * 587.33 * t)
        s2 = math.sin(2 * math.pi * 880.0 * t) * 0.6
        val = (s1 + s2) * 22000 * env
        samples.append(val)
    return make_wav(samples)

def gen_exothermic():
    dur = 0.35
    n = int(RATE * dur)
    samples = []
    random.seed(42)
    for i in range(n):
        t = i / RATE
        env = (1.0 - t / dur) ** 1.5
        # Pitch sweep: 150 Hz down to 45 Hz
        freq = 150.0 - 105.0 * (t / dur)
        bass = math.sin(2 * math.pi * freq * t)
        noise = (random.random() * 2.0 - 1.0) * (0.5 * (1.0 - t / dur))
        val = (bass * 0.7 + noise * 0.5) * 28000 * env
        samples.append(val)
    return make_wav(samples)

def gen_photon():
    dur = 0.12
    n = int(RATE * dur)
    samples = []
    for i in range(n):
        t = i / RATE
        env = (1.0 - t / dur) ** 1.2
        vibrato = math.sin(2 * math.pi * 35.0 * t) * 40.0
        freq = 2000.0 - 300.0 * (t / dur) + vibrato
        s1 = math.sin(2 * math.pi * freq * t)
        s2 = math.sin(2 * math.pi * (freq * 1.5) * t) * 0.3
        val = (s1 + s2) * 18000 * env
        samples.append(val)
    return make_wav(samples)

def gen_cosmic():
    dur = 0.22
    n = int(RATE * dur)
    samples = []
    for i in range(n):
        t = i / RATE
        env = (1.0 - t / dur) ** 0.8
        # Fast downward exponential chirp from 2400 to 180 Hz
        freq = 180.0 + 2220.0 * math.exp(-12.0 * t)
        s1 = math.sin(2 * math.pi * freq * t)
        # slight square distortion
        s_dist = 1.0 if s1 > 0 else -1.0
        val = (s1 * 0.6 + s_dist * 0.4) * 25000 * env
        samples.append(val)
    return make_wav(samples)

def gen_delete():
    dur = 0.12
    n = int(RATE * dur)
    samples = []
    for i in range(n):
        t = i / RATE
        env = (1.0 - t / dur) ** 2
        freq = 360.0 - 280.0 * (t / dur)
        val = math.sin(2 * math.pi * freq * t) * 22000 * env
        samples.append(val)
    return make_wav(samples)

def gen_freeze():
    dur = 0.28
    n = int(RATE * dur)
    samples = []
    for i in range(n):
        t = i / RATE
        env = math.sin(math.pi * (t / dur) ** 0.3) * (1.0 - t / dur)
        # Crystalline chime: 1318 Hz + 1975 Hz + 2637 Hz
        s1 = math.sin(2 * math.pi * 1318.5 * t)
        s2 = math.sin(2 * math.pi * 1975.5 * t) * 0.6
        s3 = math.sin(2 * math.pi * 2637.0 * t) * 0.3
        val = (s1 + s2 + s3) * 18000 * env
        samples.append(val)
    return make_wav(samples)

def gen_discover():
    dur = 0.45
    n = int(RATE * dur)
    samples = []
    # Arpeggio: C5 (523), E5 (659), G5 (784), C6 (1046)
    notes = [523.25, 659.25, 783.99, 1046.50]
    sub_dur = dur / 4.0
    for i in range(n):
        t = i / RATE
        note_idx = min(3, int(t / sub_dur))
        freq = notes[note_idx]
        note_t = t - note_idx * sub_dur
        note_env = math.exp(-4.0 * note_t)
        master_env = (1.0 - t / dur) ** 0.5
        s1 = math.sin(2 * math.pi * freq * t)
        s2 = math.sin(2 * math.pi * freq * 2.0 * t) * 0.25
        val = (s1 + s2) * 20000 * note_env * master_env
        samples.append(val)
    return make_wav(samples)

def gen_ambient():
    dur = 24.0
    n = int(RATE * dur)
    samples = [0.0] * n

    # 1. Four 6-second chord progressions (Dmaj7 -> Gmaj7 -> Bm9 -> Asus4/A)
    chords = [
        (0.0, 6.0, 73.42, [146.83, 220.00, 277.18, 369.99]),
        (6.0, 6.0, 98.00, [196.00, 246.94, 293.66, 369.99]),
        (12.0, 6.0, 61.74, [185.00, 220.00, 277.18, 293.66]),
        (18.0, 6.0, 55.00, [164.81, 220.00, 293.66, 369.99])
    ]

    for chord_start, chord_dur, bass_f, pad_fs in chords:
        i_start = int(chord_start * RATE)
        i_end = int((chord_start + chord_dur) * RATE)
        for i in range(i_start, min(n, i_end)):
            t = (i - i_start) / RATE
            env = (math.sin(math.pi * t / chord_dur) ** 1.2)
            bass = math.sin(2 * math.pi * bass_f * (i / RATE)) * 0.28
            pad = 0.0
            for pf in pad_fs:
                p1 = math.sin(2 * math.pi * pf * (i / RATE))
                p2 = math.sin(2 * math.pi * (pf * 1.0025) * (i / RATE))
                pad += (p1 + p2) * 0.075
            samples[i] += (bass + pad) * env

    # 2. Crystalline bell melody (sparkling science motif)
    bells = [
        (0.6, 3.5, 739.99, 0.42),   # F#5
        (2.1, 3.0, 880.00, 0.36),   # A5
        (3.6, 3.5, 1108.73, 0.32),  # C#6
        (6.6, 3.5, 987.77, 0.42),   # B5
        (8.1, 3.0, 739.99, 0.36),   # F#5
        (9.6, 3.5, 587.33, 0.38),   # D5
        (12.6, 3.5, 880.00, 0.42),  # A5
        (14.1, 3.0, 1108.73, 0.36), # C#6
        (15.6, 3.5, 1318.51, 0.32), # E6
        (18.6, 3.5, 1174.66, 0.42), # D6
        (20.1, 3.0, 880.00, 0.36),  # A5
        (21.6, 3.5, 739.99, 0.36),  # F#5
    ]

    for b_start, b_dur, freq, amp in bells:
        i_start = int(b_start * RATE)
        i_dur = int(b_dur * RATE)
        for k in range(i_dur):
            idx = (i_start + k) % n
            t = k / RATE
            env = math.exp(-2.2 * t) * (1.0 - k / i_dur)
            b1 = math.sin(2 * math.pi * freq * t)
            b2 = math.sin(2 * math.pi * (freq * 2.756) * t) * 0.22
            b3 = math.sin(2 * math.pi * (freq * 5.404) * t) * 0.08
            samples[idx] += (b1 + b2 + b3) * amp * env * 0.35

    # 3. Soft low-pass vacuum chamber ambience
    random.seed(1337)
    raw_noise = [random.random() * 2.0 - 1.0 for _ in range(n)]
    k_win = 80
    window_sum = sum(raw_noise[:k_win])
    for i in range(n):
        window_sum += raw_noise[(i + k_win) % n] - raw_noise[i]
        samples[i] += (window_sum / k_win) * 0.04

    # 4. Soft analog saturation and scaling
    max_v = max(abs(s) for s in samples) or 1.0
    for i in range(n):
        x = (samples[i] / max_v) * 1.5
        sat = math.tanh(x) * 26000
        samples[i] = sat

    # 5. Seamless loop crossfade (150ms)
    fade_len = int(RATE * 0.15)
    for j in range(fade_len):
        w = 0.5 * (1.0 - math.cos(math.pi * j / fade_len))
        tail_idx = n - fade_len + j
        head_idx = j
        blended = samples[tail_idx] * (1.0 - w) + samples[head_idx] * w
        samples[head_idx] = blended
        samples[tail_idx] = blended

    return make_wav(samples)

SOUNDS_GENERATORS = {
    "snd_click": gen_click,
    "snd_bond": gen_bond,
    "snd_exothermic": gen_exothermic,
    "snd_photon": gen_photon,
    "snd_cosmic": gen_cosmic,
    "snd_delete": gen_delete,
    "snd_freeze": gen_freeze,
    "snd_discover": gen_discover,
    "snd_ambient": gen_ambient
}

def generate_all_sounds():
    os.makedirs("/workspaces/scratch/assets", exist_ok=True)
    sound_meta = {}
    for name, gen in SOUNDS_GENERATORS.items():
        raw, md5, samples_count = gen()
        filepath = f"/workspaces/scratch/assets/{md5}.wav"
        with open(filepath, "wb") as f:
            f.write(raw)
        sound_meta[name] = {
            "name": name,
            "assetId": md5,
            "dataFormat": "wav",
            "format": "",
            "rate": RATE,
            "sampleCount": samples_count,
            "md5ext": f"{md5}.wav",
            "raw": raw
        }
        print(f"Generated {name}: {len(raw)} bytes, md5={md5}")
    return sound_meta

if __name__ == "__main__":
    generate_all_sounds()
