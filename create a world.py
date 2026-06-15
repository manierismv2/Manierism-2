#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Manierism‑K2 =^2 World Engine — 4289 World Edition (C-Blend)

- Fixed Earth core: 7.77 Hz, Magnitude 4289
- Personal worlds: birthday → symbolic Hz (1–1400+) → magnitude synced to 4289 core
- Includes:
  * Aura engine (7.77–7.83 Hz)
  * Birthdate → planet + universal birth counter
  * Wallet + mining (capsule/cache/torrent/kwh/bandwidth/sha)
  * =^2 text/atom/planet geometry
  * Symbolic calendars
  * World creation (A/B/C + D: personal birth-frequency worlds)
  * Blackjack menu using MB/kWh/bandwidth balances

Creative / symbolic use only.
Not real energy, not real population, not real astrology, not real GPS.
"""

import os, time, json, random, uuid, hashlib, math, datetime
from decimal import Decimal, getcontext

getcontext().prec = 200


def convert_decimals(obj):
    if isinstance(obj, Decimal):
        return str(obj)
    if isinstance(obj, dict):
        return {k: convert_decimals(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [convert_decimals(i) for i in obj]
    return obj


# ============================================================
# PART 1 — DIRECTORIES / BASE CONSTANTS
# ============================================================

USER_HOME = os.path.expanduser("~")
BASE_DIR = os.path.join(USER_HOME, "Downloads", "manierismmegabytes")
RIG_DIR = os.path.join(BASE_DIR, "rigs")
os.makedirs(RIG_DIR, exist_ok=True)

BASE_HZ = Decimal("7.77")          # symbolic Earth resonance
WORLD_MAGNITUDE = 4289             # canonical magnitude core
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

PROTON_EMOJI = "🧬"
PI_EMOJI = "🥧"
NETHER_EMOJI = "🟪"


# ============================================================
# PART 2 — AURA ENGINE (7.77–7.83 Hz EARTH)
# ============================================================

def aura_color_777(magnitude):
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
        "year": year,
        "month": month,
        "day": day,
        "planet": planet,
        "symbolic_frequency_hz": freq,
    }


def personal_birth_hz(date_str):
    """
    Simple symbolic Hz from birthday:
    e.g. 12-30-2001 → 1230 Hz (MMDD).
    """
    parts = date_str.replace("/", "-").split("-")
    if len(parts) != 3:
        raise ValueError("Invalid date format")

    if len(parts[0]) == 4:
        year, month, day = map(int, parts)
    else:
        month, day, year = map(int, parts)

    hz_val = int(f"{month:02d}{day:02d}")  # 1–1400+ band
    return hz_val, year


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
        "proton_tag": PROTON_EMOJI,
        "nether_tag": NETHER_EMOJI,
        "pie_tag": PI_EMOJI,
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
# PART 10 — WORLD CREATION (A/B/C/D) AT 4289
# ============================================================

def create_world(wallet_id):
    """
    TRI+1 MODE WORLD CREATION ENGINE
    Modes:
      A = Fixed 7.77 Hz → Magnitude 4289 (canonical world)
      B = Dynamic magnitude world
      C = Hybrid (fixed core + dynamic layers)
      D = Personal Birth-Frequency World (Hz from birthday, magnitude synced to 4289)
    """
    print("\n" + "="*70)
    print("🌍  MANIERISM‑K2 =^2 WORLD CREATION ENGINE — 4289 CORE")
    print("="*70)

    print("Choose world creation mode:")
    print("A) Fixed 7.77 Hz World (Magnitude 4289)")
    print("B) Dynamic World (computed magnitude)")
    print("C) Hybrid World (fixed core + dynamic layers)")
    print("D) Personal Birth-Frequency World")

    mode = input("Select A/B/C/D: ").strip().upper()

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

        print(json.dumps(convert_decimals(world), indent=4))
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

        print(json.dumps(convert_decimals(world), indent=4))
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

        print(json.dumps(convert_decimals(world), indent=4))
        return world

    # MODE D — PERSONAL BIRTH-FREQUENCY WORLD
    elif mode == "D":
        date = input("Enter birthdate (MM-DD-YYYY or YYYY-MM-DD): ")
        try:
            hz_val, year = personal_birth_hz(date)
            planet_profile = birth_to_symbolic_frequency(date)
        except Exception as e:
            print("Error:", e)
            return

        # Sync magnitude to 4289 core + personal Hz
        magnitude = WORLD_MAGNITUDE + hz_val

        freq_core = BASE_HZ
        resonance_core = float(freq_core) * WORLD_MAGNITUDE
        eq2_core = resonance_core ** 2

        resonance_personal = float(hz_val)
        eq2_personal = resonance_personal ** 2

        aura_core = deep_aura_scan(freq_core, WORLD_MAGNITUDE)
        aura_personal = deep_aura_scan(Decimal(hz_val), magnitude)

        world = {
            "Mode": "D — Personal Birth-Frequency World",
            "Birthdate": date,
            "Birth_Hz": hz_val,
            "Birth_Year": year,
            "Birth_Planet": planet_profile["planet"],
            "Core_Frequency_Hz": float(freq_core),
            "Core_Magnitude": WORLD_MAGNITUDE,
            "Core_Resonance": resonance_core,
            "Core_EqualSquared": eq2_core,
            "Personal_Magnitude": magnitude,
            "Personal_Resonance": resonance_personal,
            "Personal_EqualSquared": eq2_personal,
            "Core_Aura_Profile": aura_core,
            "Personal_Aura_Profile": aura_personal,
            "Note": "Personal world synced to 4289 core using birthday Hz band (1–1400+)."
        }

        print(json.dumps(convert_decimals(world), indent=4))
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
# PART 12 — BLACKJACK (MB / KWH / BANDWIDTH CURRENCIES)
# ============================================================

CARD_SYMBOLS = {
    'Spades': '♠', 'Hearts': '♥', 'Diamonds': '♦', 'Clubs': '♣'
}
CARD_RANKS = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
    'T': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 11
}

CURRENCIES = {
    '1': ('Torrents Payloads (MB)', 'torrent_mb'),
    '2': ('Capsule Megabytes', 'capsule_mb'),
    '3': ('Kilowatts (kwh)', 'kwh'),
    '4': ('Cache Megabytes', 'cache_mb'),
    '5': ('Bandwidth MB/s', 'bandwidth'),
}


def create_deck():
    deck = []
    suits = list(CARD_SYMBOLS.keys())
    ranks = list(CARD_RANKS.keys())
    for suit in suits:
        for rank in ranks:
            deck.append((rank, suit))
    random.shuffle(deck)
    return deck


def get_hand_value(hand):
    value = sum(CARD_RANKS[card[0]] for card in hand)
    num_aces = sum(1 for card in hand if card[0] == 'A')
    while value > 21 and num_aces > 0:
        value -= 10
        num_aces -= 1
    return value


def get_card_art(card, face_down=False):
    rank, suit_name = card
    suit_symbol = CARD_SYMBOLS.get(suit_name, ' ')
    if face_down:
        lines = [
            "┌───────┐",
            "│░░░░░░░│",
            "│░░░░░░░│",
            "│░░░░░░░│",
            "│░░░░░░░│",
            "│░░░░░░░│",
            "└───────┘"
        ]
    else:
        lines = [
            "┌───────┐",
            f"│ {rank:<2}    │",
            "│       │",
            f"│   {suit_symbol}   │",
            "│       │",
            f"│    {rank:>2} │",
            "└───────┘"
        ]
    return lines


def display_hands(player_hand, dealer_hand, hide_dealer_card=True):
    if hide_dealer_card:
        dealer_cards = [dealer_hand[0], ('?', 'Down')] + dealer_hand[2:]
    else:
        dealer_cards = dealer_hand

    player_art = [get_card_art(c, False) for c in player_hand]
    dealer_art = [get_card_art(c, c[0] == '?') for c in dealer_cards]

    print("\n" + "="*50)
    print("DEALER'S HAND:")
    for i in range(len(dealer_art[0])):
        line = "    ".join(card[i] for card in dealer_art)
        print(line)
    if not hide_dealer_card:
        print(f"Value: {get_hand_value(dealer_hand)}")
    print("\n" + "-"*50)
    print("YOUR HAND:")
    for i in range(len(player_art[0])):
        line = "    ".join(card[i] for card in player_art)
        print(line)
    print(f"Value: {get_hand_value(player_hand)}")
    print("="*50)


def blackjack_game(wallet):
    print(f"\n⚡ Blackjack - Choose Your Betting Currency ⚡")
    for k, (name, _) in CURRENCIES.items():
        print(f"{k}. {name}")

    while True:
        choice = input("Enter choice (1-5): ").strip()
        if choice in CURRENCIES:
            currency_name, currency_key = CURRENCIES[choice]
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, 4, or 5.")

    current_balance = wallet.get(currency_key, Decimal("0"))
    if current_balance <= 0:
        print(f"❌ You have no {currency_name} to bet! Go mining to earn some.")
        return

    print(f"Current Balance in {currency_name}: {current_balance}")

    while True:
        bet_input = input(f"Enter your bet in {currency_name}: ").strip()
        try:
            bet = Decimal(bet_input)
            if bet <= 0:
                print("Bet must be a positive number.")
            elif bet > current_balance:
                print(f"You can't bet more than your current balance of {current_balance}.")
            else:
                break
        except:
            print("Invalid input. Please enter a number.")

    wallet[currency_key] -= bet
    save_wallet(wallet)
    print(f"Bet placed: {bet} {currency_name}. New balance: {wallet[currency_key]} {currency_name}.")

    deck = create_deck()
    player_hand = [deck.pop(), deck.pop()]
    dealer_hand = [deck.pop(), deck.pop()]

    player_blackjack = get_hand_value(player_hand) == 21
    player_busted = False
    if not player_blackjack:
        while True:
            display_hands(player_hand, dealer_hand, hide_dealer_card=True)
            p_value = get_hand_value(player_hand)
            has_enough_for_double = bet <= wallet.get(currency_key, Decimal("0"))
            if len(player_hand) == 2 and has_enough_for_double:
                action = input("Action (H)it, (S)tand, (D)ouble Down: ").strip().lower()
            else:
                action = input("Action (H)it or (S)tand: ").strip().lower()

            if action == 'h':
                player_hand.append(deck.pop())
                p_value = get_hand_value(player_hand)
                if p_value > 21:
                    player_busted = True
                    display_hands(player_hand, dealer_hand, hide_dealer_card=True)
                    print("BUST! You went over 21. Funds were already deducted.")
                    break
            elif action == 's':
                break
            elif action == 'd' and len(player_hand) == 2 and has_enough_for_double:
                wallet[currency_key] -= bet
                bet *= 2
                save_wallet(wallet)
                print(f"Double Down! New total bet: {bet} {currency_name}.")
                player_hand.append(deck.pop())
                p_value = get_hand_value(player_hand)
                if p_value > 21:
                    player_busted = True
                    display_hands(player_hand, dealer_hand, hide_dealer_card=True)
                    print("BUST on Double Down! Funds were already deducted.")
                break
            else:
                print("Invalid action.")

    d_value = get_hand_value(dealer_hand)
    dealer_blackjack = d_value == 21 and len(dealer_hand) == 2
    d_busted = False

    if not player_busted and not (player_blackjack and dealer_blackjack):
        print("\n--- Dealer's Turn ---")
        display_hands(player_hand, dealer_hand, hide_dealer_card=False)
        while d_value < 17:
            print("Dealer hits...")
            time.sleep(1)
            dealer_hand.append(deck.pop())
            d_value = get_hand_value(dealer_hand)
            display_hands(player_hand, dealer_hand, hide_dealer_card=False)
        if d_value > 21:
            print("DEALER BUSTS!")
            d_busted = True
        else:
            print("Dealer stands.")

    print("\n=== Game Result ===")
    display_hands(player_hand, dealer_hand, hide_dealer_card=False)

    p_value = get_hand_value(player_hand)
    d_value = get_hand_value(dealer_hand)

    payout = Decimal("0")

    if player_busted:
        print(f"You lose {bet} {currency_name}.")
    elif player_blackjack and not dealer_blackjack:
        payout = bet * Decimal("2.5")
        print(f"👑 BLACKJACK! You win 1.5 times your bet! Total return (Bet + Reward): {payout} {currency_name}.")
    elif d_busted:
        payout = bet * Decimal("2")
        print(f"🎉 Dealer Busts! You win 1 time your bet! Total return (Bet + Reward): {payout} {currency_name}.")
    elif p_value > d_value:
        payout = bet * Decimal("2")
        print(f"✅ You Win! Your {p_value} beats the dealer's {d_value}. Total return (Bet + Reward): {payout} {currency_name}.")
    elif p_value == d_value:
        payout = bet
        print(f"🤝 Push. It's a tie, your bet of {payout} {currency_name} is returned.")
    else:
        print(f"❌ You Lose. Dealer's {d_value} beats your {p_value}.")

    wallet[currency_key] += payout
    save_wallet(wallet)
    print(f"Final Balance in {currency_name}: {wallet[currency_key]}")


# ============================================================
# PART 13 — CLI (ALL MENUS MERGED)
# ============================================================

def main():
    print("\n=== Manierism‑K2 =^2 World Engine — 4289 World Edition (C-Blend) ===")
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
        print("15) Create World (A/B/C/D, 4289 core + personal)")
        print("16) Blackjack (MB/kWh/bandwidth wallet game)")
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
                print(convert_decimals(profile))
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
                print(json.dumps(convert_decimals(world_profile), indent=4))
            except Exception as e:
                print("Error:", e)

        elif choice == "14":
            print_calendar_timeline_line()

        elif choice == "15":
            create_world(wallet_id)

        elif choice == "16":
            blackjack_game(wallet)

        elif choice == "0":
            print("Goodbye.")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
