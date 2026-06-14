#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Manierism‑K2 Stargate Engine (Rewritten Edition)
Symbolic mining, aura scanning, and cosmological simulation.
Not scientific. Not real energy generation. Not real population tracking.
"""

import os, time, json, random, uuid, hashlib, math, datetime
from decimal import Decimal, getcontext

getcontext().prec = 200

# ---------------------------------------------------------
# Directories and basic setup
# ---------------------------------------------------------
USER_HOME = os.path.expanduser("~")
BASE_DIR = os.path.join(USER_HOME, "Downloads", "manierismmegabytes")
RIG_DIR = os.path.join(BASE_DIR, "rigs")
os.makedirs(RIG_DIR, exist_ok=True)

# ---------------------------------------------------------
# Symbolic constants
# ---------------------------------------------------------
BASE_HZ = Decimal("7.77")
DELTA = "Δ"
OMEGA = "Ω"

# Aura thresholds (symbolic)
AURA_THRESHOLDS = [
    ("Blue",       1000, (80, 120, 255), "Observation"),
    ("Green",      2000, (80, 255, 120), "Growth"),
    ("Yellow",     3000, (255, 255, 120), "Expansion"),
    ("Orange",     4000, (255, 170, 80), "Energy"),
    ("Pink",       5000, (255, 120, 200), "Connection"),
    ("Gold",      10000, (255, 215, 0), "Renewal"),
    ("White-Gold",999999, (255, 245, 220), "Transcendence")
]

PLANETS = [
    "Sun","Moon","Mercury","Venus","Earth",
    "Mars","Jupiter","Saturn","Uranus","Neptune","Pluto"
]

# ---------------------------------------------------------
# Utility functions
# ---------------------------------------------------------
def format_num(n):
    try:
        return f"{Decimal(n):,.6f}"
    except:
        return str(n)

def aura_from_magnitude(mag):
    for name, limit, rgb, meaning in AURA_THRESHOLDS:
        if mag < limit:
            return name, rgb, meaning
    return "Unknown", (0,0,0), "Undefined"

# ---------------------------------------------------------
# Aura scan engine
# ---------------------------------------------------------
def deep_aura_scan(freq, magnitude):
    aura, rgb, meaning = aura_from_magnitude(magnitude)
    resonance = freq * magnitude
    eq2 = resonance ** 2
    wavelength = 300000000 / freq if freq > 0 else 0

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

# ---------------------------------------------------------
# Birthdate → symbolic planet profile
# ---------------------------------------------------------
def birth_to_symbolic_frequency(date_str):
    parts = date_str.replace("/", "-").split("-")
    if len(parts) != 3:
        raise ValueError("Invalid date format")

    # Interpret formats flexibly
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
        "symbolic_frequency_hz": freq,   # you interpret this as people (e.g. billions)
    }

# ---------------------------------------------------------
# UNIVERSAL BIRTH AURA COUNTER (SYMBOLIC)
# ---------------------------------------------------------
def universal_birth_aura_counter(start_year=-3114, end_year=2026):
    """
    Symbolic-only population/world counter.
    Scans symbolic births across Mayan/Aztec/Inca/Gregorian-style years.
    Each qualifying birth contributes 1e-16 'people units'.
    Counts only GREEN aura births resonating at 7.77 Hz.
    """

    total_people = Decimal("0")
    total_worlds = Decimal("0")
    total_green_hits = 0

    person_unit = Decimal("0.0000000000000001")  # 1e-16 per birth

    for year in range(start_year, end_year + 1):
        for month in range(1, 13):
            for day in range(1, 29):  # symbolic uniform cycle
                date_str = f"{month}-{day}-{year}"

                try:
                    profile = birth_to_symbolic_frequency(date_str)
                except:
                    continue

                freq = profile["symbolic_frequency_hz"]

                # Only count 7.77 Hz births (this Earth)
                if abs(freq - BASE_HZ) > Decimal("0.01"):
                    continue

                # Symbolic magnitude seed (still used for aura)
                magnitude = (year * month * day) % 5000
                if magnitude <= 0:
                    magnitude = 1

                scan = deep_aura_scan(freq, magnitude)

                if scan["Aura"] == "Green":
                    total_green_hits += 1

                    # each qualifying birth = 1e-16 people
                    total_people += person_unit
                    # worlds scaled from people (your 7.77 factor)
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

# ---------------------------------------------------------
# Mining engine (rewritten but same behavior)
# ---------------------------------------------------------
def symbolic_hash(header, power):
    seed = f"{header}{power}{uuid.uuid4()}"
    return hashlib.sha256(seed.encode()).hexdigest()

def mining_tick(wallet, mode):
    """
    Rewritten symbolic mining tick.
    Behaves like your original engine but rewritten from scratch.
    """

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

# ---------------------------------------------------------
# Wallet system (rewritten)
# ---------------------------------------------------------
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
    data = {k: float(v) if isinstance(v, Decimal) else v for k,v in wallet.items()}
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

def load_wallet(wallet_id):
    path = os.path.join(RIG_DIR, f"{wallet_id}.json")
    if not os.path.exists(path):
        return None
    with open(path, "r") as f:
        data = json.load(f)
    for k in ["capsule_mb","cache_mb","torrent_mb","kwh","bandwidth","hash_power"]:
        data[k] = Decimal(str(data[k]))
    return data

# ---------------------------------------------------------
# CLI
# ---------------------------------------------------------
def main():
    print("\n=== Manierism‑K2 Stargate Engine (Rewritten Edition) ===")
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
        print("7) Aura Scan (7.77 Hz)")
        print("8) Birthdate → Planet Profile")
        print("9) Deep Aura Scan (custom magnitude)")
        print("10) Universal Birth Aura Counter")
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
            scan = deep_aura_scan(BASE_HZ, 4289)
            for k,v in scan.items():
                print(f"{k}: {v}")

        elif choice == "8":
            date = input("Enter date (MM-DD-YYYY): ")
            print(birth_to_symbolic_frequency(date))

        elif choice == "9":
            mag = int(input("Magnitude: "))
            scan = deep_aura_scan(BASE_HZ, mag)
            for k,v in scan.items():
                print(f"{k}: {v}")

        elif choice == "10":
            report = universal_birth_aura_counter()
            print_universal_birth_report(report)

        elif choice == "0":
            print("Goodbye.")
            break

        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
