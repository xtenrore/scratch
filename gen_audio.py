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
    dur = 6.0
    n = int(RATE * dur)
    samples = []
    
    # Pre-generate smooth cyclic noise buffer (6.0s seamless loop)
    random.seed(1337)
    raw_noise = [random.random() * 2.0 - 1.0 for _ in range(n)]
    # 2-pass moving average for smooth low-pass filtered vacuum chamber air tone
    filt_noise = [0.0] * n
    k = 80
    window_sum = sum(raw_noise[:k])
    for i in range(n):
        window_sum += raw_noise[(i + k) % n] - raw_noise[i]
        filt_noise[i] = (window_sum / k) * 0.08

    for i in range(n):
        t = i / RATE
        # Cyclic LFOs (exact integer periods over 6s)
        # LFO 1: 0.3333 Hz (period 3.0s, exactly 2 cycles over 6s)
        lfo1 = 0.5 + 0.5 * math.cos(2 * math.pi * (2.0 / dur) * t)
        # LFO 2: 0.1666 Hz (period 6.0s, exactly 1 cycle over 6s)
        lfo2 = 0.5 + 0.5 * math.sin(2 * math.pi * (1.0 / dur) * t)

        # 1. Fundamental sub drone (A1 = 55 Hz, 330 cycles over 6s)
        sub = math.sin(2 * math.pi * 55.0 * t) * 0.32
        
        # 2. Detuned binaural vacuum hum (329 and 331 cycles over 6s -> 0.333 Hz beat)
        beat1 = math.sin(2 * math.pi * (329.0 / dur) * t) * 0.14
        beat2 = math.sin(2 * math.pi * (331.0 / dur) * t) * 0.14

        # 3. Sub-octave deep warmth (27.5 Hz, 165 cycles over 6s)
        deep = math.sin(2 * math.pi * 27.5 * t) * 0.22

        # 4. Fifth harmonic warmth (82.5 Hz, 495 cycles over 6s)
        fifth = math.sin(2 * math.pi * 82.5 * t) * 0.14

        # 5. Octave harmonic with subtle breathing (110 Hz, 660 cycles over 6s)
        octave = math.sin(2 * math.pi * 110.0 * t) * (0.09 + 0.06 * lfo1)

        # 6. Ethereal atmospheric fifth (165 Hz, 990 cycles over 6s)
        air1 = math.sin(2 * math.pi * 165.0 * t) * (0.05 * lfo2)

        # 7. Sci-fi crystalline shimmer resonance (330 Hz, 1980 cycles over 6s)
        shimmer = math.sin(2 * math.pi * 330.0 * t) * (0.02 + 0.015 * lfo1)

        # 8. Vacuum chamber low-pass ambient air tone
        hiss = filt_noise[i]

        val = (sub + beat1 + beat2 + deep + fifth + octave + air1 + shimmer + hiss) * 19000
        samples.append(val)

    # 10ms smooth crossfade at loop boundaries to ensure 100% zero-pop seamless looping
    fade_len = int(RATE * 0.01)  # 220 samples
    for j in range(fade_len):
        w = 0.5 * (1.0 - math.cos(math.pi * j / fade_len))
        # blend head and tail
        tail_val = samples[n - fade_len + j]
        head_val = samples[j]
        blended = tail_val * (1.0 - w) + head_val * w
        samples[j] = blended
        samples[n - fade_len + j] = blended

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
