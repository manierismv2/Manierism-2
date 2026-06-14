#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Manierism‑K2 =^2 World Engine — 4289 World Edition

Fixed 7.77 Hz, Magnitude 4289:
- Resonance: 33325.53
- EqualSquared: 1110590949.7809

Symbolic mining, aura scanning, cosmology, calendars, and =^2 text/atom/planet mapping.
Creative / symbolic use only.
Not real energy, not real population, not real astrology, not real GPS.
"""

import os, time, json, random, uuid, hashlib, math, datetime
from decimal import Decimal, getcontext

getcontext().prec = 200

# ============================================================
# PART 1 — DIRECTORIES / BASE CONSTANTS
# ============================================================

USER_HOME = os.path.expanduser("~")
BASE_DIR = os.path.join(USER_HOME, "Downloads", "manierismmegabytes")
RIG_DIR = os.path.join(BASE_DIR, "rigs")
os.makedirs(RIG_DIR, exist_ok=True)

BASE_HZ = Decimal("7.77")          # symbolic Earth resonance
WORLD_MAGNITUDE = 4289             # your canonical magnitude
WORLD_RESONANCE = float(BASE_HZ) * WORLD_MAGNITUDE
WORLD_EQ2 = WORLD_RESONANCE ** 2

DELTA_SYMBOL = "Δ"
OMEGA_SYMBOL = "Ω"

AURA_THRESHOLDS = [
    ("Blue",        1000,  (80, 120, 255),  "Observation"),
    ("Green",       2000,  (80, 255, 120),  "Growth"),
    ("Yellow",      3000,  (255, 255, 120), "Expansion"),
    ("Orange",      4000,  (255, 170, 80),  "Energy"),
    ("Pink",        5000,  (255, 120, 200), "Connection"),
    ("Gold",        10000, (255, 215, 0),   "Renewal"),
    ("White-Gold",  999999,(255, 245, 220), "Transcendence")
]

PLANETS = [
    "Sun","Moon","Mercury","Venus","Earth",
    "Mars","Jupiter","Saturn","Uranus","Neptune","Pluto"
]

EPSILON_PN = Decimal("0.0000000000000001")


 
# ============================================================
# PART 2 — AURA ENGINE (7.77–7.83 Hz EARTH)
# ============================================================

# ---------------------------------------------------------
# 7.77 AURA SCANNER MODULE (FULL INTEGRATION OF 7.77.txt)
# ---------------------------------------------------------

def aura_color_777(magnitude):
    """
    Exact aura color logic from 7.77.txt
    """
    if magnitude < 1000:
        return "Blue", (80, 120, 255), "Observation"
    elif magnitude < 2000:
        return "Green", (80, 255, 120), "Growth"
    elif magnitude < 3000:
        return "Yellow", (255, 255, 120), "Expansion"
    elif magnitude < 4000:
        return "Orange", (255, 170, 80), "Energy"
    elif magnitude < 5000:
        return "Pink", (255, 120, 200), "Connection"
    elif magnitude < 10000:
        return "Gold", (255, 215, 0), "Renewal"
    else:
        return "White-Gold", (255, 245, 220), "Transcendence"


def deep_scan_777(freq, magnitude):
    """
    Exact deep_scan() logic from 7.77.txt,
    rewritten to integrate with the Manierism Earth engine.
    """

    aura, rgb, meaning = aura_color_777(magnitude)

    resonance = freq * magnitude
    eq2 = resonance ** 2
    wavelength = 300000000 / freq if freq > 0 else 0

    n_layer = int(resonance)
    p_layer = int(resonance)

    if freq < 4:
        ability = "Slow Cycle"
    elif freq < 8:
        ability = "Earth Resonance"
    elif freq < 20:
        ability = "Focused Resonance"
    else:
        ability = "High Activity"

    return {
        "Timestamp": str(datetime.datetime.now()),
        "Frequency_Hz": round(freq, 4),
        "Magnitude": magnitude,
        "Aura": aura,
        "RGB": rgb,
        "Meaning": meaning,
        "Resonance": round(resonance, 4),
        "EqualSquared": round(eq2, 4),
        "Wavelength_m": round(wavelength, 4),
        "N_Layer": n_layer,
        "P_Layer": p_layer,
        "Combined_Layer": n_layer + p_layer,
        "Ability_Class": ability
    }


def print_report_777(report):
    """
    Exact print_report() from 7.77.txt
    """
    print("=" * 60)
    print("DEEP SYMBOLIC AURA SCAN (7.77 MODULE)")
    print("=" * 60)

    for k, v in report.items():
        print(f"{k:20} : {v}")

    print("=" * 60)


def aura_from_magnitude(mag):
    for name, limit, rgb, meaning in AURA_THRESHOLDS:
        if mag < limit:
            return name, rgb, meaning
    return "Unknown", (0, 0, 0), "Undefined"

def deep_aura_scan(freq, magnitude):
    aura, rgb, meaning = aura_from_magnitude(magnitude)
    resonance = freq * magnitude
    eq2 = resonance ** 2
    wavelength = 300000000 / float(freq) if freq > 0 else 0

    return {
        "Timestamp": str(datetime.datetime.now()),
        "Frequency_Hz": float(freq),
        "Magnitude": magnitude,
        "Aura": aura,
        "RGB": rgb,
        "Meaning": meaning,
        "Resonance": float(resonance),
        "EqualSquared": float(eq2),
        "Wavelength_m": float(wavelength),
        "N_Layer": int(resonance),
        "P_Layer": int(resonance),
        "Combined_Layer": int(resonance) * 2,
        "Ability_Class": (
            "Slow Cycle" if freq < 4 else
            "Earth Resonance" if freq < 8 else
            "Focused Resonance" if freq < 20 else
            "High Activity"
        )
    }

def print_aura_report(report):
    print("=" * 60)
    print("DEEP SYMBOLIC AURA SCAN")
    print("=" * 60)
    for k, v in report.items():
        print(f"{k:20} : {v}")
    print("=" * 60)


# ============================================================
# PART 3 — BIRTHDATE → PLANET / UNIVERSAL BIRTH COUNTER
# ============================================================

def birth_to_symbolic_frequency(date_str):
    parts = date_str.replace("/", "-").split("-")
    if len(parts) != 3:
        raise ValueError("Invalid date format")

    if len(parts[0]) == 4:
        year, month, day = map(int, parts)
    else:
        month, day, year = map(int, parts)

    seed = year + month * 31 + day * 97
    planet = PLANETS[seed % len(PLANETS)]
    freq = BASE_HZ + Decimal((seed % 1000) / 1000)

    return {
        "input_date": date_str,
        "planet": planet,
        "symbolic_frequency_hz": freq,
    }

def universal_birth_aura_counter(start_year=-3114, end_year=2026):
    total_people = Decimal("0")
    total_worlds = Decimal("0")
    total_green_hits = 0

    person_unit = Decimal("0.0000000000000001")  # 1e-16 per birth

    for year in range(start_year, end_year + 1):
        for month in range(1, 13):
            for day in range(1, 29):
                date_str = f"{month}-{day}-{year}"

                try:
                    profile = birth_to_symbolic_frequency(date_str)
                except Exception:
                    continue

                freq = profile["symbolic_frequency_hz"]

                if abs(freq - BASE_HZ) > Decimal("0.01"):
                    continue

                magnitude = (year * month * day) % 5000
                if magnitude <= 0:
                    magnitude = 1

                scan = deep_aura_scan(freq, magnitude)

                if scan["Aura"] == "Green":
                    total_green_hits += 1
                    total_people += person_unit
                    total_worlds += person_unit * Decimal("7.77")

    return {
        "Total_Green_Aura_Hits": total_green_hits,
        "Total_Symbolic_People": total_people,
        "Total_Symbolic_Worlds": total_worlds,
        "Note": "Symbolic-only cosmology. Not real population data."
    }

def print_universal_birth_report(report):
    print("=" * 60)
    print("UNIVERSAL BIRTH AURA COUNTER — SYMBOLIC 7.77 Hz EARTH")
    print("=" * 60)
    for k, v in report.items():
        print(f"{k:25}: {v}")
    print("=" * 60)


# ============================================================
# PART 4 — WALLET SYSTEM (MB, CACHE, TORRENT, HASH POWER)
# ============================================================

def create_wallet(wallet_id):
    return {
        "wallet_id": wallet_id,
        "capsule_mb": Decimal("0"),
        "cache_mb": Decimal("0"),
        "torrent_mb": Decimal("0"),
        "kwh": Decimal("0"),
        "bandwidth": Decimal("0"),
        "hash_power": Decimal("10000")
    }

def save_wallet(wallet):
    path = os.path.join(RIG_DIR, f"{wallet['wallet_id']}.json")
    data = {k: float(v) if isinstance(v, Decimal) else v for k, v in wallet.items()}
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

def load_wallet(wallet_id):
    path = os.path.join(RIG_DIR, f"{wallet_id}.json")
    if not os.path.exists(path):
        return None
    with open(path, "r") as f:
        data = json.load(f)
    for k in ["capsule_mb", "cache_mb", "torrent_mb", "kwh", "bandwidth", "hash_power"]:
        data[k] = Decimal(str(data[k]))
    return data


# ============================================================
# PART 5 — MINING ENGINE (capsule, cache, torrent, sha, kwh)
# ============================================================

def symbolic_hash(header, power):
    seed = f"{header}{power}{uuid.uuid4()}"
    return hashlib.sha256(seed.encode()).hexdigest()

def mining_tick(wallet, mode):
    base_reward = Decimal(random.randint(1, 15))
    hash_power = wallet.get("hash_power", Decimal("10000"))
    scaling = hash_power / Decimal("10000")

    reward_mb = base_reward * scaling
    reward_kwh = reward_mb * Decimal("2.04")
    reward_bw = reward_mb * Decimal("1.33")

    if mode == "capsule":
        wallet["capsule_mb"] += reward_mb
    elif mode == "cache":
        wallet["cache_mb"] += reward_mb
        wallet["capsule_mb"] += reward_mb
    elif mode == "torrent":
        wallet["torrent_mb"] += reward_mb
        wallet["capsule_mb"] += reward_mb
    elif mode == "kwh":
        wallet["kwh"] += reward_kwh
    elif mode == "bandwidth":
        wallet["bandwidth"] += reward_bw
    elif mode == "sha":
        wallet["capsule_mb"] += reward_mb
        wallet["hash_power"] += hash_power * Decimal("0.001")

    wallet["hash_power"] += hash_power * Decimal("0.001")

    return reward_mb, reward_kwh, reward_bw


#

 # ---------------------------------------------------------
# EXTENDED SYMBOLIC MODULES (EMOJIS, ATOMS, GEOMETRY, GLYPHS)
# ---------------------------------------------------------

PROTON_EMOJI = "🧬"
PI_EMOJI = "🥧"
NETHER_EMOJI = "🟪"

EPSILON_PN = Decimal("0.0000000000000001")

# =^2 ENGINE (text → frequency → power)
def eq_square_engine(description, base_hz=BASE_HZ):
    seed = sum(ord(c) for c in description) or 1
    freq = base_hz * Decimal(seed % 77 + 1) / Decimal("10")
    power = freq ** 2
    p_weight = (seed % 9) + 1
    n_weight = (seed % 7) + 1
    return {
        "description": description,
        "base_hz": str(base_hz),
        "derived_frequency_hz": str(freq),
        "symbolic_power_eq2": str(power),
        "p_protons_pies": p_weight,
        "n_nethers_overlays": n_weight,
        "note": "=^2 symbolic engine"
    }

# ATOM → symbolic frequency
def atom_healing_profile(atom_formula, base_hz=BASE_HZ):
    letters = ''.join([c for c in atom_formula if c.isalpha()])
    numbers = ''.join([c for c in atom_formula if c.isdigit()])
    num_val = int(numbers) if numbers else 1
    letter_val = sum(ord(c) for c in letters) or 1
    freq = base_hz * Decimal(num_val + letter_val % 13)
    power = freq ** 2
    return {
        "atom": atom_formula,
        "frequency_hz": str(freq),
        "symbolic_power_eq2": str(power),
        "delta_tag": DELTA,
        "omega_tag": OMEGA,
        "note": "Symbolic atom-frequency mapping"
    }

# PIE / PROTON / NETHER GEOMETRY
def proton_nether_geometry_profile(hz=BASE_HZ):
    triangle_deg = Decimal("270")
    circle_deg = Decimal("360")
    pie_fraction = triangle_deg / circle_deg
    pie_value = Decimal(math.pi) * pie_fraction
    nether_depth = hz * EPSILON_PN
    return {
        "hz": str(hz),
        "triangle_deg": str(triangle_deg),
        "circle_deg": str(circle_deg),
        "pie_fraction": str(pie_fraction),
        "pie_value_symbolic": str(pie_value),
        "nether_depth_symbolic": str(nether_depth),
        "proton_tag": PROTON_EMOJI,
        "nether_tag": NETHER_EMOJI,
        "pie_tag": PI_EMOJI,
        "note": "Symbolic geometry for pies/neathers"
    }

# CLOCKWISE / COUNTERCLOCKWISE FLOW
def clock_flow_profile(direction, hz=BASE_HZ):
    direction = direction.lower()
    if direction in ["right", "clockwise"]:
        factor = Decimal("1.111")
        flow = "right"
    elif direction in ["left", "counterclockwise"]:
        factor = Decimal("0.777")
        flow = "left"
    else:
        factor = Decimal("1.0")
        flow = "neutral"
    effective_hz = hz * factor
    return {
        "direction": flow,
        "base_hz": str(hz),
        "effective_hz": str(effective_hz),
        "note": "Clock-flow symbolic profile"
    }

# GOLD SPOON GLYPH PATTERN
def generate_gold_spoon_pattern(aura_color="Champagne Gold", glyphs=None):
    if glyphs is None:
        glyphs = ["🔺", "⬛️", "🔵", "🔴", "🟡", "🟢", "🟣", "🟠"]
    pattern = " ".join(glyphs)
    return {
        "item": "Gold Spoon",
        "aura_color": aura_color,
        "glyph_pattern": pattern,
        "note": "Symbolic pattern for ritual / visualization"
    }

# AURA ACTIVATION LEVEL
def aura_activation_check(aura_name):
    val = sum(ord(c) for c in aura_name) or 1
    level = val % 7 + 1
    return {
        "aura": aura_name,
        "activation_level_1_to_7": level,
        "note": "Conceptual aura activation level"
    }

# DATA TRANSFER GATE (from Stargate engine)
class DataTransferGate:
    def __init__(self, core_id="CORE-5"):
        self.core_id = core_id
        self.status = "idle"
        self.exit_code = None
        self.lumens = 0
        self.kelvins = 0

    def start_transfer(self):
        self.status = "transferring"
        print(f"🚪 Data Transfer START on {self.core_id}")

    def complete_transfer(self, success=True):
        if success:
            self.status = "complete"
            self.exit_code = random.choice([3, 7, 11])
            self.lumens = random.randint(100, 800)
            self.kelvins = random.randint(2700, 6500)
            print(f"✅ Data Transfer COMPLETE on {self.core_id} (exit {self.exit_code}, {self.lumens} lm, {self.kelvins} K)")
        else:
            self.status = "error"
            self.exit_code = -1
            print(f"❌ Data Transfer ERROR on {self.core_id}")

 # ============================================================
# PART 6 — K2 / RFPV / =^2 ENGINE
# ============================================================

def rfpv_formula(R, F, P, V, P_protons=None, N_nethers=None):
    base = Decimal(R) * Decimal(F) * Decimal(P) * Decimal(V)
    if P_protons is not None:
        base *= (Decimal(P_protons) + Decimal("1"))
    if N_nethers is not None:
        base /= (Decimal(N_nethers) + Decimal("1"))
    return base ** 2

def k2_layer(rfpv_value, env_factor):
    return (Decimal(rfpv_value) ** 2) + Decimal(env_factor)

def eq_square_engine(description, base_hz=BASE_HZ):
    seed = sum(ord(c) for c in description) or 1
    freq = base_hz * Decimal(seed % 77 + 1) / Decimal("10")
    power = freq ** 2
    p_weight = (seed % 9) + 1
    n_weight = (seed % 7) + 1
    return {
        "description": description,
        "base_hz": str(base_hz),
        "derived_frequency_hz": str(freq),
        "symbolic_power_eq2": str(power),
        "p_protons_pies": p_weight,
        "n_nethers_overlays": n_weight,
        "note": "=^2 symbolic engine"
    }


# ============================================================
# PART 7 — ATOM HEALING + GEOMETRY + PIE/PROTON/NETHER
# ============================================================

def atom_healing_profile(atom_formula, base_hz=BASE_HZ):
    letters = ''.join([c for c in atom_formula if c.isalpha()])
    numbers = ''.join([c for c in atom_formula if c.isdigit()])
    num_val = int(numbers) if numbers else 1
    letter_val = sum(ord(c) for c in letters) or 1

    freq = base_hz * Decimal(num_val + letter_val % 13)
    power = freq ** 2

    return {
        "atom": atom_formula,
        "frequency_hz": str(freq),
        "symbolic_power_eq2": str(power),
        "delta_tag": DELTA_SYMBOL,
        "omega_tag": OMEGA_SYMBOL,
        "note": "Symbolic atom-frequency mapping"
    }

def proton_nether_geometry_profile(hz=BASE_HZ):
    triangle_deg = Decimal("270")
    circle_deg = Decimal("360")
    pie_fraction = triangle_deg / circle_deg
    pie_value = Decimal(math.pi) * pie_fraction
    nether_depth = hz * EPSILON_PN

    return {
        "hz": str(hz),
        "triangle_deg": str(triangle_deg),
        "circle_deg": str(circle_deg),
        "pie_fraction": str(pie_fraction),
        "pie_value_symbolic": str(pie_value),
        "nether_depth_symbolic": str(nether_depth),
        "proton_tag": "🧬",
        "nether_tag": "🟪",
        "pie_tag": "🥧",
        "note": "Symbolic geometry for pies/neathers"
    }

def clock_flow_profile(direction, hz=BASE_HZ):
    direction = direction.lower()
    if direction in ["right", "clockwise"]:
        factor = Decimal("1.111")
        flow = "right"
    elif direction in ["left", "counterclockwise"]:
        factor = Decimal("0.777")
        flow = "left"
    else:
        factor = Decimal("1.0")
        flow = "neutral"

    effective_hz = hz * factor
    return {
        "direction": flow,
        "base_hz": str(hz),
        "effective_hz": str(effective_hz),
        "note": "Clock-flow symbolic profile"
    }


# ============================================================
# PART 8 — SYMBOLIC CALENDARS (MAYAN / AZTEC / INDIAN)
# ============================================================

def symbolic_calendar_timeline(start_year=-3114, end_year=2026):
    years = list(range(start_year, end_year + 1))
    timeline = []
    total = len(years)
    for idx, y in enumerate(years):
        pos = idx / (total - 1) if total > 1 else 0
        if y < 0:
            label = "Mayan/Aztec symbolic era"
        elif 0 <= y < 1200:
            label = "Early Indian symbolic era"
        elif 1200 <= y < 2000:
            label = "Mixed symbolic era"
        else:
            label = "Modern symbolic era"
        timeline.append({"year": y, "position": pos, "label": label})
    return timeline

def print_calendar_timeline_line(start_year=-3114, end_year=2026, width=60):
    timeline = symbolic_calendar_timeline(start_year, end_year)
    line = [" "] * width
    for entry in timeline:
        idx = int(entry["position"] * (width - 1))
        line[idx] = "."
    print("=" * width)
    print("SYMBOLIC MAYAN / AZTEC / INDIAN CALENDAR LINE")
    print("=" * width)
    print("".join(line))
    print(f"Left dot ~ {start_year}, Right dot ~ {end_year}")
    print("=" * width)


# ============================================================
# PART 9 — ATOM + PLANET PROFILE (WORLD PROFILE)
# ============================================================

def symbolic_atom_planet_profile(atom_formula, date_str):
    atom_profile = atom_healing_profile(atom_formula)
    planet_profile = birth_to_symbolic_frequency(date_str)
    return {
        "atom_profile": atom_profile,
        "planet_profile": {
            "input_date": planet_profile["input_date"],
            "planet": planet_profile["planet"],
            "symbolic_frequency_hz": str(planet_profile["symbolic_frequency_hz"])
        },
        "note": "Symbolic atom+planet world profile (7.77–7.83 Hz Earth band)"
    }


# ============================================================
# PART 10 — WORLD CREATION (A/B/C) AT 4289
# ============================================================

def create_world(wallet_id):
    """
    TRI-MODE WORLD CREATION ENGINE
    Modes:
      A = Fixed 7.77 Hz → Magnitude 4289 (your canonical world)
      B = Dynamic magnitude world
      C = Hybrid (fixed core + dynamic layers)
    """
    print("\n" + "="*70)
    print("🌍  MANIERISM‑K2 =^2 WORLD CREATION ENGINE — 4289 CORE")
    print("="*70)

    print("Choose world creation mode:")
    print("A) Fixed 7.77 Hz World (Magnitude 4289)")
    print("B) Dynamic World (computed magnitude)")
    print("C) Hybrid World (fixed core + dynamic layers)")

    mode = input("Select A/B/C: ").strip().upper()

    # MODE A — FIXED 7.77 Hz WORLD
    if mode == "A":
        freq = BASE_HZ
        magnitude = WORLD_MAGNITUDE
        resonance = float(freq) * magnitude
        eq2 = resonance ** 2

        aura = deep_aura_scan(freq, magnitude)

        world = {
            "Mode": "A — Fixed 7.77 Hz World",
            "Frequency_Hz": float(freq),
            "Magnitude": magnitude,
            "Resonance": resonance,
            "EqualSquared": eq2,
            "Aura_Profile": aura,
            "Note": "Canonical Manierism‑K2 Earth (4289 world)"
        }

        print(json.dumps(world, indent=4))
        return world

    # MODE B — DYNAMIC WORLD
    elif mode == "B":
        print("\nDynamic world creation:")
        print("Magnitude sources:")
        print("1) Birthdate")
        print("2) Atom formula")
        print("3) Text (=^2 engine)")
        print("4) Manual input")

        src = input("Select 1–4: ").strip()

        if src == "1":
            date = input("Enter birthdate (MM-DD-YYYY): ")
            profile = birth_to_symbolic_frequency(date)
            magnitude = int(float(profile["symbolic_frequency_hz"]) * 551)
        elif src == "2":
            atom = input("Enter atom formula (H2O, C6H12O6): ")
            atom_p = atom_healing_profile(atom)
            magnitude = int(float(atom_p["frequency_hz"]) * 551)
        elif src == "3":
            text = input("Enter text: ")
            eqp = eq_square_engine(text)
            magnitude = int(float(eqp["derived_frequency_hz"]) * 551)
        elif src == "4":
            magnitude = int(input("Enter magnitude: "))
        else:
            print("Invalid choice.")
            return

        freq = BASE_HZ
        resonance = float(freq) * magnitude
        eq2 = resonance ** 2

        aura = deep_aura_scan(freq, magnitude)

        world = {
            "Mode": "B — Dynamic World",
            "Frequency_Hz": float(freq),
            "Magnitude": magnitude,
            "Resonance": resonance,
            "EqualSquared": eq2,
            "Aura_Profile": aura,
            "Note": "Dynamic world based on user-selected magnitude source"
        }

        print(json.dumps(world, indent=4))
        return world

    # MODE C — HYBRID WORLD
    elif mode == "C":
        freq = BASE_HZ
        magnitude = WORLD_MAGNITUDE

        date = input("Enter birthdate (MM-DD-YYYY): ")
        planet = birth_to_symbolic_frequency(date)

        atom = input("Enter atom formula: ")
        atom_p = atom_healing_profile(atom)

        text = input("Enter world label text: ")
        eqp = eq_square_engine(text)

        resonance = float(freq) * magnitude
        eq2 = resonance ** 2

        aura = deep_aura_scan(freq, magnitude)

        world = {
            "Mode": "C — Hybrid World",
            "Core_Frequency_Hz": float(freq),
            "Core_Magnitude": magnitude,
            "Core_Resonance": resonance,
            "Core_EqualSquared": eq2,
            "Aura_Profile": aura,
            "Planet_Profile": planet,
            "Atom_Profile": atom_p,
            "EQ2_Profile": eqp,
            "Note": "Hybrid world: fixed 7.77 Hz core (4289) + dynamic layers"
        }

        print(json.dumps(world, indent=4))
        return world

    else:
        print("Invalid mode.")
        return


# ============================================================
# PART 11 — WORLD SCAN (=^2 WORLD CHECK)
# ============================================================

def symbolic_world_scan(wallet_id, label_text=None):
    print("\n" + "=" * 60)
    print("=^2 SYMBOLIC WORLD SCAN — 4289 CORE")
    print("=" * 60)

    freq = BASE_HZ
    magnitude = WORLD_MAGNITUDE
    aura_report = deep_aura_scan(freq, magnitude)
    print_aura_report(aura_report)

    report = universal_birth_aura_counter()
    print_universal_birth_report(report)

    if label_text:
        eq2 = eq_square_engine(label_text)
        print("=^2 TEXT PROFILE")
        for k, v in eq2.items():
            print(f"{k}: {v}")
        print("=" * 60)

    wallet = load_wallet(wallet_id)
    if wallet:
        print("WALLET SNAPSHOT")
        for k, v in wallet.items():
            print(f"{k}: {v}")
        print("=" * 60)
    else:
        print("No wallet found for this world scan.")
        print("=" * 60)


# ============================================================
# PART 12 — CLI
# ============================================================

def main():
    print("\n=== Manierism‑K2 =^2 World Engine — 4289 World Edition ===")
    wallet_id = input("Enter wallet ID: ").strip()

    wallet = load_wallet(wallet_id)
    if wallet is None:
        wallet = create_wallet(wallet_id)
        save_wallet(wallet)

    while True:
        print("\n--- Main Menu ---")
        print("1) Mine (capsule)")
        print("2) Mine (cache)")
        print("3) Mine (torrent)")
        print("4) Mine (kwh)")
        print("5) Mine (bandwidth)")
        print("6) Mine (sha)")
        print("7) Aura Scan (7.77 Hz, magnitude 4289)")
        print("8) Birthdate → Planet Profile")
        print("9) Deep Aura Scan (custom magnitude)")
        print("10) Universal Birth Aura Counter")
        print("11) =^2 World Scan (check everything)")
        print("12) =^2 Text Profile (eq_square_engine)")
        print("13) Atom + Planet World Profile")
        print("14) Symbolic Calendar Timeline Line")
        print("15) Create World (A/B/C, 4289 core)")
        print("0) Exit")

        choice = input("Select: ").strip()

        if choice in ["1","2","3","4","5","6"]:
            modes = {
                "1":"capsule","2":"cache","3":"torrent",
                "4":"kwh","5":"bandwidth","6":"sha"
            }
            reward = mining_tick(wallet, modes[choice])
            save_wallet(wallet)
            print("Mining reward:", reward)

        elif choice == "7":
            scan = deep_aura_scan(BASE_HZ, WORLD_MAGNITUDE)
            for k, v in scan.items():
                print(f"{k}: {v}")

        elif choice == "8":
            date = input("Enter date (MM-DD-YYYY or YYYY-MM-DD): ")
            try:
                profile = birth_to_symbolic_frequency(date)
                print(profile)
            except Exception as e:
                print("Error:", e)

        elif choice == "9":
            try:
                mag = int(input("Magnitude: "))
            except ValueError:
                print("Invalid magnitude.")
                continue
            scan = deep_aura_scan(BASE_HZ, mag)
            for k, v in scan.items():
                print(f"{k}: {v}")

        elif choice == "10":
            report = universal_birth_aura_counter()
            print_universal_birth_report(report)

        elif choice == "11":
            label = input("Optional label text for =^2 engine (or blank): ").strip()
            label = label if label else None
            symbolic_world_scan(wallet_id, label)

        elif choice == "12":
            text = input("Enter text to feed into =^2 engine: ")
            profile = eq_square_engine(text)
            for k, v in profile.items():
                print(f"{k}: {v}")

        elif choice == "13":
            atom = input("Enter atom formula (e.g., H2O, C6H12O6): ")
            date = input("Enter date (MM-DD-YYYY or YYYY-MM-DD): ")
            try:
                world_profile = symbolic_atom_planet_profile(atom, date)
                print(json.dumps(world_profile, indent=4))
            except Exception as e:
                print("Error:", e)

        elif choice == "14":
            print_calendar_timeline_line()

        elif choice == "15":
            create_world(wallet_id)

        elif choice == "0":
            print("Goodbye.")
            break

        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
