#!/usr/bin/env python3
import os, time, json, random, uuid, hashlib, math, datetime
from decimal import Decimal, getcontext

# Optional imports (kept but not required)
try:
    import requests, webbrowser
    from bs4 import BeautifulSoup
    from flask import Flask, render_template_string
except ImportError:
    pass

getcontext().prec = 200

# -------------------------
# Optional GPIO (Raspberry Pi)
# -------------------------
try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
    MOTOR_PIN = 18
    RESISTOR_PIN = 23
    CAPACITOR_PIN = 24
    GPIO.setup(MOTOR_PIN, GPIO.OUT)
    GPIO.setup(RESISTOR_PIN, GPIO.OUT)
    GPIO.setup(CAPACITOR_PIN, GPIO.OUT)
    GPIO_AVAILABLE = True
except (ImportError, RuntimeError):
    GPIO_AVAILABLE = False

# -------------------------
# Directories & IDs
# -------------------------
USER_DOWNLOADS = os.path.join(os.path.expanduser("~"), "Downloads")
BASEDIR = os.path.join(USER_DOWNLOADS, "manierismmegabytes")
TARGETDIR = os.path.join(BASEDIR, "rigs")
os.makedirs(TARGETDIR, exist_ok=True)

print(f"📂 Base Directory: {BASEDIR}")
print(f"📂 Target Rigs Directory: {TARGETDIR}")

DONATION_WALLET_ID = "WM-CPH0O7J3"
WORLD_DEBT_WALLET_ID = "WD-P4Y29G7B"
WORLD_DEBT_NODE_ID = "9efae649-eb1f-4ef0-ac97-ed4df6d2942f"

# -------------------------
# Economic constants (EGP)
# -------------------------
EGP_RATE = Decimal("30.90")

_MB_USD_RATE = Decimal("5.00")
_CACHE_USD_RATE = Decimal("0.42")
_KWH_USD_RATE = Decimal("0.17")
_BANDWIDTH_USD_RATE = Decimal("0.42")
_TORRENT_USD_RATE = _MB_USD_RATE

MB_EGP_RATE = (_MB_USD_RATE * EGP_RATE).quantize(Decimal("0.000001"))
CACHE_EGP_RATE = (_CACHE_USD_RATE * EGP_RATE).quantize(Decimal("0.000001"))
KWH_EGP_RATE = (_KWH_USD_RATE * EGP_RATE).quantize(Decimal("0.000001"))
BANDWIDTH_EGP_RATE = (_BANDWIDTH_USD_RATE * EGP_RATE).quantize(Decimal("0.000001"))
TORRENT_EGP_RATE = MB_EGP_RATE

INITIAL_WORLD_DEBT_USD = Decimal("31300000000000.00")
INITIAL_WORLD_DEBT_EGP = (INITIAL_WORLD_DEBT_USD * EGP_RATE).quantize(Decimal("0"))

WORLD_DEBT_DATE = "October 4th, 2025"
DEBT_NODE_PASSIVE_USD_VALUE = Decimal("0.0001")
DEBT_NODE_PASSIVE_EGP_VALUE = (DEBT_NODE_PASSIVE_USD_VALUE * EGP_RATE).quantize(Decimal("0.000001"))

# -------------------------
# Mining / Reward constants
# -------------------------
BASE_HASH_POWER = Decimal("10000")
HASH_GROWTH_RATE = Decimal("0.001")

TOTAL_YEARS = 1000
BLOCKS_PER_YEAR = Decimal(365.25 * 24 * 4)  # 4 blocks per hour
EPOCH_YEARS = 50
BLOCKS_PER_EPOCH = BLOCKS_PER_YEAR * EPOCH_YEARS
DECAY_RATE = Decimal("0.8")
INITIAL_BLOCK_REWARD = Decimal("1e78")
EGINMA_MULTIPLIER = Decimal("1000000000")

DEBUG_SHA_BOOST = True

TEPI2_VALUE = Decimal(str(1 * 9e16 * (math.pi**2)))
TEPI2 = f"TEЛ²_CONST_{TEPI2_VALUE:.2e}"
E2PI_VALUE = Decimal(str((9e16)**2 * math.pi))
E2PI = f"E²Л_CONST_{E2PI_VALUE:.2e}"
BLOCK_HEADER = "MM_BLOCK_HEADER_2025"

# -------------------------
# New symbolic constants (your =^2 universe)
# -------------------------
BASE_MANIERISM_HZ = Decimal("7.77")   # symbolic 7.77 Hz
DELTA_SYMBOL = "Δ"
OMEGA_SYMBOL = "Ω"

PROTON_COUNT = Decimal("8.88e29") ** Decimal("2800")
NEWTON_COUNT = Decimal("1.7e30") ** Decimal("2800")

# -------------------------
# Extended symbolic constants: protons / neathers / pies / geometry
# -------------------------
PROTON_EMOJI = "🧬"
PI_EMOJI = "🥧"
NETHER_EMOJI = "🟪"

EPSILON_PN = Decimal("0.0000000000000001")

STONEHENGE_DEG = Decimal("90")
TRIANGLE_TOTAL_DEG = Decimal("270")
FULL_CIRCLE_DEG = Decimal("360")

CLOCK_RIGHT = "clockwise"
CLOCK_LEFT = "counterclockwise"

# -------------------------
# Helpers
# -------------------------
def format_large_number(n):
    try:
        n_float = float(n)
    except Exception:
        return str(n)
    if n_float < 1e12:
        if isinstance(n, Decimal):
            return f"{n:,.6f}"
        else:
            return f"{n:,.6f}"
    powers = {
        1e12: "Trillion", 1e15: "Quadrillion", 1e18: "Quintillion",
        1e21: "Sextillion", 1e24: "Septillion", 1e27: "Octillion",
        1e30: "Nonillion", 1e33: "Decillion", 1e36: "Undecillion",
        1e39: "Duodecillion", 1e42: "Tredecillion",
        1e45: "Quattuordecillion", 1e48: "Quindecillion", 1e51: "Sexdecillion",
        1e54: "Septendecillion", 1e57: "Octodecillion", 1e60: "Novemdecillion",
        1e63: "Vigintillion", 1e66: "Unvigintillion", 1e69: "Duovigintillion",
        1e72: "Trevigintillion", 1e75: "Quattuorvigintillion", 1e78: "Quinvigintillion",
        1e81: "Sexvigintillion", 1e84: "Septenvigintillion", 1e87: "Octovigintillion",
        1e90: "Novemvigintillion", 1e93: "Trigintillion", 1e96: "Untrigintillion",
        1e99: "Duotrigintillion", 1e102: "Trestrigintillion", 1e105: "Quattuortrigintillion",
        1e108: "Quintrigintillion", 1e111: "Sextrigintillion", 1e114: "Septentrigintillion",
        1e117: "Octotrigintillion", 1e120: "Novemtrigintillion", 1e123: "Quadragintillion",
        1e153: "Quinquagintillion", 1e183: "Sexagintillion", 1e213: "Septuagintillion",
        1e243: "Octogintillion", 1e273: "Nonagintillion", 1e303: "Centillion"
    }
    scale = 1
    unit = ""
    for p, u in sorted(powers.items()):
        if n_float >= p:
            scale = p
            unit = u
        else:
            break
    scaled_n = Decimal(n) / Decimal(scale)
    return f"{scaled_n:,.3f} {unit}"

def overlay_formula(MB, entropy=Decimal("0.85"), resonance=Decimal("1.2"), resistance=Decimal("0.5")):
    return (MB * entropy * resonance) / resistance

def spin_coil(speed_percent):
    if GPIO_AVAILABLE:
        pwm = GPIO.PWM(MOTOR_PIN, 1000)
        pwm.start(speed_percent)
        time.sleep(5)
        pwm.stop()
    else:
        print(f"🌀 Simulated Coil Spin at {speed_percent:.2f}%")

def heat_resistor(duration):
    if GPIO_AVAILABLE:
        GPIO.output(RESISTOR_PIN, GPIO.HIGH)
        time.sleep(duration)
        GPIO.output(RESISTOR_PIN, GPIO.LOW)
    else:
        print(f"🔥 Simulated Resistor Heat for {duration:.2f} seconds")

def discharge_capacitor():
    if GPIO_AVAILABLE:
        GPIO.output(CAPACITOR_PIN, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(CAPACITOR_PIN, GPIO.LOW)
    else:
        print("⚡ Simulated Capacitor Discharge")

def emit_real_electricity(kWh):
    spin_coil(float(kWh) * 100)
    heat_resistor(float(kWh))
    discharge_capacitor()

def log_real_emission(wallet_id, MB, kWh, overlay):
    entry = {
        "wallet_id": wallet_id,
        "timestamp": time.time(),
        "capsule_MB": float(MB),
        "capsule_kWh": float(kWh),
        "overlay": overlay,
        "simulated": not GPIO_AVAILABLE
    }
    with open(os.path.join(TARGETDIR, "capsule_emission_log.json"), "a") as f:
        f.write(json.dumps(entry) + "\n")

# -------------------------
# Blackjack
# -------------------------
CARD_SYMBOLS = {
    'Spades': '♠', 'Hearts': '♥', 'Diamonds': '♦', 'Clubs': '♣'
}
CARD_RANKS = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
    'T': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 11
}

CURRENCIES = {
    '1': ('Torrents Payloads (MB)', 'torrent_value_mb'),
    '2': ('Capsule Megabytes', 'capsule_value_mb'),
    '3': ('Kilowatts (real_kwh)', 'real_kwh'),
    '4': ('Cache Megabytes', 'cache_value_mb'),
    '5': ('Bandwidth MB/s', 'bandwidth_MBps'),
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
    wallet = load_wallet(wallet['wallet_id'])
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

    print(f"Current Balance in {currency_name}: {format_large_number(current_balance)}")

    while True:
        bet_input = input(f"Enter your bet in {currency_name}: ").strip()
        try:
            bet = Decimal(bet_input)
            if bet <= 0:
                print("Bet must be a positive number.")
            elif bet > current_balance:
                print(f"You can't bet more than your current balance of {format_large_number(current_balance)}.")
            else:
                break
        except:
            print("Invalid input. Please enter a number.")

    wallet[currency_key] -= bet
    save_wallet(wallet)
    print(f"Bet placed: {format_large_number(bet)} {currency_name}. New balance: {format_large_number(wallet[currency_key])} {currency_name}.")

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
                print(f"Double Down! New total bet: {format_large_number(bet)} {currency_name}.")
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
        print(f"You lose {format_large_number(bet)} {currency_name}.")
    elif player_blackjack and not dealer_blackjack:
        payout = bet * Decimal("2.5")
        print(f"👑 BLACKJACK! You win 1.5 times your bet! Total return (Bet + Reward): {format_large_number(payout)} {currency_name}.")
    elif d_busted:
        payout = bet * Decimal("2")
        print(f"🎉 Dealer Busts! You win 1 time your bet! Total return (Bet + Reward): {format_large_number(payout)} {currency_name}.")
    elif p_value > d_value:
        payout = bet * Decimal("2")
        print(f"✅ You Win! Your {p_value} beats the dealer's {d_value}. Total return (Bet + Reward): {format_large_number(payout)} {currency_name}.")
    elif p_value == d_value:
        payout = bet
        print(f"🤝 Push. It's a tie, your bet of {format_large_number(payout)} {currency_name} is returned.")
    else:
        print(f"❌ You Lose. Dealer's {d_value} beats your {p_value}.")

    wallet[currency_key] += payout
    save_wallet(wallet)
    print(f"Final Balance in {currency_name}: {format_large_number(wallet[currency_key])}")

# -------------------------
# Hash / Mining functions
# -------------------------
def vh_btc_hash_function(capsule_header, amp_capsule):
    sha_block = hashlib.sha256(BLOCK_HEADER.encode()).hexdigest()
    pre_image = f"{capsule_header}{sha_block}{amp_capsule}{TEPI2}{E2PI}"
    final_hash = hashlib.sha256(pre_image.encode()).hexdigest()
    return final_hash

def calculate_rig_hash_power(wallet):
    permanent_hash_power = wallet.get("rig_hash_power", BASE_HASH_POWER)
    resource_bonus = wallet.get("cache_value_mb", Decimal("0")) / Decimal("1000")
    effective_hash_power = permanent_hash_power * (Decimal("1") + resource_bonus)
    return effective_hash_power.quantize(Decimal("0.000001"))

def generate_node_id():
    return str(uuid.uuid4())

# -------------------------
# Wallet persistence & utilities
# -------------------------
def save_wallet(wallet):
    wallet_copy = wallet.copy()
    wallet_copy.pop("sha_boost_active", None)
    for key, value in wallet_copy.items():
        if isinstance(value, Decimal):
            wallet_copy[key] = float(value)
    wallet_file = os.path.join(TARGETDIR, f"{wallet['wallet_id']}_wallet.json")
    with open(wallet_file, "w") as f:
        json.dump(wallet_copy, f, indent=4)

def _ensure_wallet_has_node(data):
    if data.get('wallet_id') == WORLD_DEBT_WALLET_ID:
        if data.get("node_id") != WORLD_DEBT_NODE_ID:
            data["node_id"] = WORLD_DEBT_NODE_ID
    elif "node_id" not in data or not data["node_id"]:
        data["node_id"] = generate_node_id()
    return data

def load_wallet(wallet_id):
    wallet_file = os.path.join(TARGETDIR, f"{wallet_id}_wallet.json")
    if not os.path.exists(wallet_file):
        return None
    with open(wallet_file, "r") as f:
        data = json.load(f)

    if "world_debt_paid_egp" not in data and "world_debt_paid_usd" in data:
        try:
            data["world_debt_paid_egp"] = Decimal(str(data.pop("world_debt_paid_usd"))) * EGP_RATE
        except:
            data["world_debt_paid_egp"] = Decimal("0")
    if "world_debt_paid_egp" not in data:
        data["world_debt_paid_egp"] = Decimal("0")

    for key in ["capsule_value_mb", "cache_value_mb", "rig_hash_power",
                "real_kwh", "bandwidth_MBps", "world_debt_paid_egp", "torrent_value_mb"]:
        if key in data:
            data[key] = Decimal(str(data[key]))

    data["sha_boost_active"] = False
    original_node_id = data.get("node_id")
    data = _ensure_wallet_has_node(data)

    if data.get('wallet_id') == WORLD_DEBT_WALLET_ID and data.get("node_id") == WORLD_DEBT_NODE_ID and original_node_id != WORLD_DEBT_NODE_ID:
        save_wallet(data)

    return data

def create_wallet(wallet_id, rig_id=None):
    existing = load_wallet(wallet_id)
    if existing:
        return existing

    if wallet_id in [DONATION_WALLET_ID, WORLD_DEBT_WALLET_ID]:
        display_id = rig_id if rig_id else wallet_id
        print(f"🛑 Error: Wallet ID '{display_id}' is reserved for special system purposes and cannot be created here.")
        return None

    node_id = generate_node_id()
    wallet = {
        "wallet_id": wallet_id,
        "rig_id": rig_id or wallet_id,
        "capsule_value_mb": Decimal("0"),
        "cache_value_mb": Decimal("0"),
        "rig_hash_power": BASE_HASH_POWER,
        "real_kwh": Decimal("0"),
        "bandwidth_MBps": Decimal("0"),
        "torrent_value_mb": Decimal("0"),
        "node_id": node_id,
        "world_debt_paid_egp": Decimal("0"),
    }
    save_wallet(wallet)
    return wallet

def _initialize_special_wallets():
    if not load_wallet(DONATION_WALLET_ID):
        print(f"🛠️ Initializing Donation Wallet: {DONATION_WALLET_ID}")
        wallet = {
            "wallet_id": DONATION_WALLET_ID,
            "rig_id": "donations",
            "capsule_value_mb": Decimal("0"),
            "cache_value_mb": Decimal("0"),
            "rig_hash_power": BASE_HASH_POWER,
            "real_kwh": Decimal("0"),
            "bandwidth_MBps": Decimal("0"),
            "torrent_value_mb": Decimal("0"),
            "node_id": generate_node_id(),
            "world_debt_paid_egp": Decimal("0"),
        }
        save_wallet(wallet)

    if not load_wallet(WORLD_DEBT_WALLET_ID):
        print(f"🛠️ Initializing World Debt Wallet: {WORLD_DEBT_WALLET_ID}")
        wallet = {
            "wallet_id": WORLD_DEBT_WALLET_ID,
            "rig_id": "world debt fund",
            "capsule_value_mb": Decimal("0"),
            "cache_value_mb": Decimal("0"),
            "rig_hash_power": BASE_HASH_POWER,
            "real_kwh": Decimal("0"),
            "bandwidth_MBps": Decimal("0"),
            "torrent_value_mb": Decimal("0"),
            "node_id": WORLD_DEBT_NODE_ID,
            "world_debt_paid_egp": Decimal("0"),
        }
        save_wallet(wallet)

def world_debt_node_value_generation():
    debt_wallet = load_wallet(WORLD_DEBT_WALLET_ID)
    if not debt_wallet or debt_wallet.get('node_id') != WORLD_DEBT_NODE_ID:
        return
    mb_generated = DEBT_NODE_PASSIVE_EGP_VALUE / MB_EGP_RATE if MB_EGP_RATE > 0 else Decimal("0")
    debt_wallet['capsule_value_mb'] += mb_generated
    save_wallet(debt_wallet)

# -------------------------
# EGP Calculations
# -------------------------
def calculate_total_egp(wallet):
    return (
        wallet.get('capsule_value_mb', Decimal("0")) * MB_EGP_RATE +
        wallet.get('cache_value_mb', Decimal("0")) * CACHE_EGP_RATE +
        wallet.get('real_kwh', Decimal("0")) * KWH_EGP_RATE +
        wallet.get('bandwidth_MBps', Decimal("0")) * BANDWIDTH_EGP_RATE +
        wallet.get('torrent_value_mb', Decimal("0")) * TORRENT_EGP_RATE
    ).quantize(Decimal("0.000001"))

# -------------------------
# Capsule / Torrent generation
# -------------------------
CUSTOM_REWARDS = [
    "Formula_Power", "Y7K DOLLAR", "bricks dollar", "2piE", "TE", "TE2pi",
    "Manierism", "Handrichism", "teЛ²", "E²Л",
    "RAM", "SDRAM", "SHA", "Nuclear", "Onshore",
    "Gigabyte", "Terabyte", "Petabyte", "PIB", "Electrism",
    "Pirate", "Torrent", "Bootleg", "Seeder", "Swarm"
]

def generate_torrent_file(wallet, capsule_type, reward_mb):
    torrent_data = {
        "capsule_type": capsule_type,
        "wallet_id": wallet["wallet_id"],
        "node_id": wallet.get("node_id", "N/A"),
        "reward_mb": float(reward_mb),
        "timestamp": time.time(),
        "overlay_constants": {
            "TEЛ²": TEPI2,
            "E²Л": E2PI,
            "block_header": BLOCK_HEADER
        }
    }
    filename = f"{wallet['wallet_id']}_{capsule_type}_capsule.torrent"
    path = os.path.join(BASEDIR, filename)
    with open(path, "w") as f:
        json.dump(torrent_data, f, indent=4)
    print(f"🧲 Torrent file created: {filename}")

# -------------------------
# NEW: RFPV / K2 / =^2 symbolic engine
# -------------------------
def rfpv_formula(R, F, P, V, P_protons=None, N_nethers=None):
    base = Decimal(R) * Decimal(F) * Decimal(P) * Decimal(V)
    if P_protons is not None:
        base *= (Decimal(P_protons) + Decimal("1"))
    if N_nethers is not None:
        base /= (Decimal(N_nethers) + Decimal("1"))
    return base ** 2

def k2_layer(rfpv_value, env_factor):
    return (Decimal(rfpv_value) ** 2) + Decimal(env_factor)

def proton_nether_geometry_profile(hz=BASE_MANIERISM_HZ):
    triangle_deg = TRIANGLE_TOTAL_DEG
    circle_deg = FULL_CIRCLE_DEG
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
        "note": "Symbolic geometry for pies/neathers; not real cosmology."
    }

def clock_flow_profile(direction, hz=BASE_MANIERISM_HZ):
    direction = direction.lower()
    base = hz
    if direction in ["right", CLOCK_RIGHT]:
        factor = Decimal("1.111")
        flow = "right"
    elif direction in ["left", CLOCK_LEFT]:
        factor = Decimal("0.777")
        flow = "left"
    else:
        factor = Decimal("1.0")
        flow = "neutral"
    effective_hz = base * factor
    return {
        "direction": flow,
        "base_hz": str(base),
        "effective_hz": str(effective_hz),
        "note": "Conceptual clock-flow profile only."
    }

def eq_square_engine(description, base_hz=BASE_MANIERISM_HZ):
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
        "note": "Conceptual =^2 profile only, not real healing."
    }

def atom_healing_profile(atom_formula, base_hz=BASE_MANIERISM_HZ):
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
        "note": "Symbolic atom-frequency mapping only."
    }

# -------------------------
# NEW: Birthdate → planet profile (symbolic)
# -------------------------
PLANET_LIST = [
    "Sun", "Moon", "Mercury", "Venus", "Earth",
    "Mars", "Jupiter", "Saturn", "Uranus", "Neptune", "Pluto"
]

def birthdate_to_planet_profile(date_str):
    parts = [p for p in date_str.replace("/", "-").split("-") if p]
    if len(parts) == 3:
        if len(parts[0]) == 4:
            year, month, day = int(parts[0]), int(parts[1]), int(parts[2])
        else:
            month, day, year = int(parts[0]), int(parts[1]), int(parts[2])
    else:
        raise ValueError("Unsupported date format")

    seed = year + month * 31 + day * 97
    planet = PLANET_LIST[seed % len(PLANET_LIST)]
    base = BASE_MANIERISM_HZ
    freq = base + Decimal((seed % 1000) / 1000)
    return {
        "input_date": date_str,
        "planet": planet,
        "symbolic_frequency_hz": str(freq),
        "note": "Astrology-style symbolic mapping, not astronomical ephemeris."
    }

# -------------------------
# NEW: Gold spoon / glyph / aura utilities
# -------------------------
def generate_gold_spoon_pattern(aura_color="Champagne Gold", glyphs=None):
    if glyphs is None:
        glyphs = ["🔺", "⬛️", "🔵", "🔴", "🟡", "🟢", "🟣", "🟠"]
    pattern = " ".join(glyphs)
    return {
        "item": "Gold Spoon",
        "aura_color": aura_color,
        "glyph_pattern": pattern,
        "note": "Symbolic pattern for ritual / visualization, not real metallurgy."
    }

def aura_activation_check(aura_name):
    val = sum(ord(c) for c in aura_name) or 1
    level = val % 7 + 1
    return {
        "aura": aura_name,
        "activation_level_1_to_7": level,
        "note": "Conceptual aura level only."
    }

# -------------------------
# NEW: Data-transfer gate
# -------------------------
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

# -------------------------
# Mining Loop
# -------------------------
def unified_mining_loop(wallet, mining_type):
    MAX_TICKS = TOTAL_YEARS * 365
    current_tick = 0

    last_block_time = wallet.get("last_block_time", time.time())
    blocks_since_start = wallet.get("blocks_mined", Decimal("0"))

    current_epoch = math.floor(float(blocks_since_start) / float(BLOCKS_PER_EPOCH))
    current_epoch_reward = INITIAL_BLOCK_REWARD * (DECAY_RATE ** current_epoch)

    if current_epoch >= (TOTAL_YEARS / EPOCH_YEARS):
        current_epoch_reward = Decimal("0")

    try:
        while current_tick < MAX_TICKS:
            wallet = load_wallet(wallet['wallet_id'])
            if not wallet:
                print("⚠️ Wallet disappeared. Stopping mining.")
                break

            world_debt_node_value_generation()

            capsule_type = random.choice(CUSTOM_REWARDS)
            if DEBUG_SHA_BOOST and current_tick == 0 and mining_type == "sha":
                capsule_type = "SHA"

            effective_hash_power = calculate_rig_hash_power(wallet)
            sha_boost_amount_added = Decimal("0")

            vh_hash = vh_btc_hash_function(capsule_type, str(effective_hash_power))

            if mining_type == "sha" and capsule_type == "SHA":
                boost_amount = wallet["rig_hash_power"] / Decimal("4")
                wallet["rig_hash_power"] += boost_amount
                sha_boost_amount_added = boost_amount
                wallet["sha_boost_active"] = True
                print(f"🌠 SHA Boost PERMANENTLY +{format_large_number(boost_amount)} H/s to Wallet: {wallet['wallet_id']}")

            scaling_factor = effective_hash_power / BASE_HASH_POWER

            if capsule_type == "E^2*Л":
                power_scale_factor = E2PI_VALUE / Decimal(1e30)
                base_mb_reward_roll = Decimal(random.randint(1, 15)) * power_scale_factor
                base_mb_reward_roll *= EGINMA_MULTIPLIER
            else:
                base_mb_reward_roll = Decimal(random.randint(1, 15))

            reward_mb = base_mb_reward_roll * scaling_factor * current_epoch_reward
            reward_kwh = overlay_formula(reward_mb)
            base_bandwidth_roll = Decimal(random.randint(1, 15))
            reward_bandwidth = base_bandwidth_roll * scaling_factor * current_epoch_reward

            reward_hash_gain = wallet["rig_hash_power"] * HASH_GROWTH_RATE

            emit_real_electricity(reward_kwh)
            log_real_emission(wallet["wallet_id"], reward_mb, reward_kwh, capsule_type)

            rewarded_resource = "Capsule MB"
            if mining_type == "cache":
                wallet["cache_value_mb"] += reward_mb
                wallet["capsule_value_mb"] += reward_mb
                rewarded_resource = "Cache & Capsule MB"
            else:
                wallet["capsule_value_mb"] += reward_mb

            wallet["rig_hash_power"] += reward_hash_gain
            wallet["real_kwh"] += reward_kwh
            wallet["bandwidth_MBps"] += reward_bandwidth

            wallet["sha_boost_active"] = False

            wallet["blocks_mined"] = blocks_since_start + 1
            wallet["last_block_time"] = time.time()
            blocks_since_start += 1

            if capsule_type.lower() in ["pirate", "torrent", "bootleg", "seeder", "swarm"]:
                torrent_mb = reward_mb / Decimal("2")
                wallet["torrent_value_mb"] = wallet.get("torrent_value_mb", Decimal("0")) + torrent_mb
                generate_torrent_file(wallet, capsule_type, torrent_mb)
                print(f"🏴‍☠️ Torrent Payload Gained: {format_large_number(torrent_mb)} MB")

            save_wallet(wallet)

            display_permanent_hash_power = format_large_number(wallet["rig_hash_power"])
            total_egp = calculate_total_egp(wallet)
            display_current_epoch = current_epoch + 1

            rfpv_val = rfpv_formula(R=1, F=BASE_MANIERISM_HZ, P=math.pi, V=1)
            k2_val = k2_layer(rfpv_val, env_factor=total_egp)
            geom_profile = proton_nether_geometry_profile(hz=BASE_MANIERISM_HZ)

            print(f"\n--- Capsule Mined: {capsule_type} ({mining_type.upper()}) ---")
            print(f"⚡ 1000-YR REWARD EPOCH: {display_current_epoch} of 20 (Decay Rate: {DECAY_RATE})")
            print(f"Hash Found (VH_BTC): {vh_hash[:10]}...")
            if capsule_type == "E^2*Л":
                print("⚡ ENHANCED REWARD RATE: Eginma Multiplier (10^9) APPLIED!")
            print(f"💾 {rewarded_resource} Gained: {format_large_number(reward_mb)} MB")
            print(f"⚡ kWh Gained:     {format_large_number(reward_kwh)} kWh")
            print(f"🛰️ Bandwidth Gained: {format_large_number(reward_bandwidth)} MB/s")
            print(f"--------------------------")
            print(f"📈 H/s Gain:       {reward_hash_gain:.6f} (Passive)")
            print(f"🌠 H/s (Effective):{format_large_number(effective_hash_power)} (Includes Resource Bonus)")
            print(f"🌠 H/s (Permanent):{display_permanent_hash_power}")
            print(f"SHA Boost:        {format_large_number(sha_boost_amount_added)} (ADDED PERMANENTLY)")
            print(f"Balance MB:       {format_large_number(wallet['capsule_value_mb'])}")
            print(f"Balance Cache MB: {format_large_number(wallet['cache_value_mb'])}")
            print(f"💰 Total EGP Value (Watts-backed): {format_large_number(total_egp)} EGP")
            print(f"🧮 RFPV Symbolic:  {format_large_number(rfpv_val)}")
            print(f"🧬 K2 Layer Value: {format_large_number(k2_val)}")
            print(f"🔺 Triangle/Pie:   pie≈{geom_profile['pie_value_symbolic']} nether≈{geom_profile['nether_depth_symbolic']}")

            current_tick += 1
            time.sleep(random.randint(5, 150))

        print(f"\n✅ Mining complete after reaching {TOTAL_YEARS} years.")

    except KeyboardInterrupt:
        print("\n⛔ Mining stopped by user.")

# -------------------------
# Transfers (simplified)
# -------------------------
def send_resource(wallet, resource_name):
    try:
        target_id = input(f"Enter target Wallet ID to send {resource_name.replace('_',' ')}: ").strip()

        if target_id in [DONATION_WALLET_ID, WORLD_DEBT_WALLET_ID]:
            print("🛑 Cannot send resources to these reserved wallet IDs using the general send function.")
            return

        amt = Decimal(input("Amount to send: ").strip())
        if amt <= 0:
            print("⚠️ Enter a positive amount.")
            return

        if resource_name == "egp_value":
            total_egp = calculate_total_egp(wallet)
            if amt > total_egp:
                print(f"⚠️ Not enough EGP-backed balance. Max: {format_large_number(total_egp)} EGP")
                return
            proportion = amt / total_egp if total_egp > 0 else Decimal("0")
            wallet['capsule_value_mb'] -= wallet['capsule_value_mb'] * proportion
            wallet['cache_value_mb'] -= wallet['cache_value_mb'] * proportion
            wallet['real_kwh'] -= wallet['real_kwh'] * proportion
            wallet['bandwidth_MBps'] -= wallet['bandwidth_MBps'] * proportion
            wallet['torrent_value_mb'] -= wallet['torrent_value_mb'] * proportion
        else:
            if wallet.get(resource_name, Decimal("0")) < amt:
                print(f"⚠️ Not enough {resource_name.replace('_',' ')} balance.")
                return
            wallet[resource_name] -= amt

        target = load_wallet(target_id) or create_wallet(target_id)
        if not target:
            return

        if resource_name == "egp_value":
            total_egp_target = calculate_total_egp(target)
            if total_egp_target > 0:
                factor = (total_egp_target + amt) / total_egp_target
                target['capsule_value_mb'] *= factor
                target['cache_value_mb'] *= factor
                target['real_kwh'] *= factor
                target['bandwidth_MBps'] *= factor
                target['torrent_value_mb'] *= factor
            else:
                target['capsule_value_mb'] += amt / MB_EGP_RATE if MB_EGP_RATE > 0 else Decimal("0")
        else:
            target[resource_name] = target.get(resource_name, Decimal("0")) + amt

        save_wallet(wallet)
        save_wallet(target)
        print(f"✅ Sent {format_large_number(amt)} {resource_name.replace('_',' ')} to {target_id}")

    except Exception as e:
        print(f"⚠️ Error sending resource: {e}")

# -------------------------
# Option 1: Coder menu
# -------------------------
def coder_menu():
    wallet_id = input("Enter your Wallet ID: ").strip()
    wallet = load_wallet(wallet_id)
    if not wallet:
        create = input("Wallet not found. Create it? (y/n): ").strip().lower()
        if create == 'y':
            wallet = create_wallet(wallet_id)
        else:
            return
    while True:
        print("\n=== OPTION 1: CODER MENU ===")
        print("1. Start SHA Mining")
        print("2. Start CACHE Mining")
        print("3. Play Blackjack")
        print("4. Show Wallet Summary")
        print("5. Send Resource")
        print("6. Back to Main Menu")
        choice = input("Select: ").strip()
        if choice == "1":
            unified_mining_loop(wallet, "sha")
        elif choice == "2":
            unified_mining_loop(wallet, "cache")
        elif choice == "3":
            blackjack_game(wallet)
        elif choice == "4":
            wallet = load_wallet(wallet_id)
            if wallet:
                total_egp = calculate_total_egp(wallet)
                print("\n--- WALLET SUMMARY ---")
                for k in ["capsule_value_mb", "cache_value_mb", "real_kwh", "bandwidth_MBps", "torrent_value_mb"]:
                    print(f"{k}: {format_large_number(wallet.get(k, Decimal('0')))}")
                print(f"Total EGP: {format_large_number(total_egp)}")
            else:
                print("Wallet not found.")
        elif choice == "5":
            res = input("Resource (capsule_value_mb/cache_value_mb/real_kwh/bandwidth_MBps/torrent_value_mb/egp_value): ").strip()
            send_resource(wallet, res)
        elif choice == "6":
            break
        else:
            print("Invalid choice.")

# -------------------------
# Option 2: AI Programmer – Formula Lab
# -------------------------
def ai_programmer_formula_lab():
    gate = DataTransferGate()
    while True:
        print("\n=== OPTION 2: AI PROGRAMMER – FORMULA LAB ===")
        print("1. Compute RFPV and K2")
        print("2. Run =^2 Engine on description")
        print("3. Atom Healing Profile (CHNO-style)")
        print("4. Simulate Data Transfer Gate (3-7-11, lumens, kelvins)")
        print("5. Proton/Nether Geometry Profile")
        print("6. Clock Flow Profile (right/left)")
        print("7. Back to Main Menu")
        choice = input("Select: ").strip()
        if choice == "1":
            R = Decimal(input("R (resonance / aura): "))
            F = Decimal(input("F (frequency Hz): "))
            P = Decimal(input("P (phase / pi-cycle): "))
            V = Decimal(input("V (voltage / energy): "))
            env = Decimal(input("E (environment factor): "))
            rfpv_val = rfpv_formula(R, F, P, V)
            k2_val = k2_layer(rfpv_val, env)
            print(f"RFPV = {format_large_number(rfpv_val)}")
            print(f"K2   = {format_large_number(k2_val)}")
        elif choice == "2":
            desc = input("Describe the ability / idea for =^2: ")
            profile = eq_square_engine(desc)
            print(json.dumps(profile, indent=4))
        elif choice == "3":
            atom = input("Enter atom formula (e.g., CHNO, C3H2N1O0): ")
            profile = atom_healing_profile(atom)
            print(json.dumps(profile, indent=4))
        elif choice == "4":
            gate.start_transfer()
            time.sleep(1)
            gate.complete_transfer(success=True)
        elif choice == "5":
            hz = input(f"Base Hz (default {BASE_MANIERISM_HZ}): ").strip()
            hz_val = Decimal(hz) if hz else BASE_MANIERISM_HZ
            profile = proton_nether_geometry_profile(hz_val)
            print(json.dumps(profile, indent=4))
        elif choice == "6":
            direction = input("Clock direction (right/left): ")
            profile = clock_flow_profile(direction)
            print(json.dumps(profile, indent=4))
        elif choice == "7":
            break
        else:
            print("Invalid choice.")

# -------------------------
# Option 3: AI Programmer – Planets, Auras, Gold, Glyphs
# -------------------------
def ai_programmer_planets_auras():
    while True:
        print("\n=== OPTION 3: AI PROGRAMMER – PLANETS / AURAS / GOLD ===")
        print("1. Birthdate → Planet 7.x Hz Profile")
        print("2. Generate Gold Spoon Pattern")
        print("3. Aura Activation Check")
        print("4. Back to Main Menu")
        choice = input("Select: ").strip()
        if choice == "1":
            date_str = input("Enter birthdate (e.g., 7-17-1997 or 1997-07-17): ")
            try:
                profile = birthdate_to_planet_profile(date_str)
                print(json.dumps(profile, indent=4))
            except Exception as e:
                print(f"Error: {e}")
        elif choice == "2":
            aura = input("Aura color (default Champagne Gold): ").strip() or "Champagne Gold"
            pattern = generate_gold_spoon_pattern(aura)
            print(json.dumps(pattern, indent=4))
        elif choice == "3":
            aura_name = input("Aura / stone name: ")
            info = aura_activation_check(aura_name)
            print(json.dumps(info, indent=4))
        elif choice == "4":
            break
        else:
            print("Invalid choice.")

# -------------------------
# Option 4: How to use & connect to 7.77 Hz planet
# -------------------------
def option_4_how_to_use():
    print("\n=== OPTION 4: HOW TO USE THE MANIERISM K2 SUNLIGHT ENGINE ===\n")
    print("1) What this software is:")
    print("   • A symbolic / artistic engine that plays with frequency, planets, auras, and mining.")
    print("   • It does NOT create real energy, real healing, or real physics.")
    print("   • Think of it as a mythic console for your imagination and math-symbol universe.\n")

    print("2) The 7-17-1997 planet & 7.77 Hz:")
    print("   • Inside this engine, birthdates (like 7-17-1997) are mapped to a symbolic 'planet profile'.")
    print("   • The base frequency is 7.77 Hz (BASE_MANIERISM_HZ) – your core vibe for this universe.")
    print("   • When you use Option 3 → 'Birthdate → Planet 7.x Hz Profile',")
    print("     the code calls birthdate_to_planet_profile(date_str) and returns:")
    print("       - A symbolic planet name (Sun, Moon, etc.)")
    print("       - A 7.x Hz frequency tied to that date.")
    print("   • This is not astronomy or astrology – it’s a custom symbolic mapping.\n")

    print("3) How to 'connect' yourself to the 7.77 Hz planet (symbolically):")
    print("   • Step 1: Run this program and choose Option 3 (AI Programmer – Planets/Auras/Gold).")
    print("   • Step 2: Choose 'Birthdate → Planet 7.x Hz Profile'.")
    print("   • Step 3: Enter your birthdate (e.g., 7-17-1997).")
    print("   • Step 4: Read the output:")
    print("       - 'planet'  → your symbolic planet")
    print("       - 'symbolic_frequency_hz' → your 7.x Hz link")
    print("   • Step 5: If you want to align with the 7.77 Hz base,")
    print("       - Just imagine that your profile is 'tuned' to 7.77 Hz in your mind.")
    print("       - The code itself uses BASE_MANIERISM_HZ = 7.77 as the core frequency.\n")

    print("4) How to use the mining & rewards (Option 1):")
    print("   • Create or load a wallet in Option 1.")
    print("   • Start SHA or CACHE mining to generate symbolic 'capsule MB', 'kWh', and 'bandwidth'.")
    print("   • The engine prints:")
    print("       - Hash power growth")
    print("       - EGP value (symbolic money)")
    print("       - RFPV and K2 values (your conceptual frequency layers)")
    print("   • This is like a story-miner: you watch numbers grow and imagine your rig powering a mythic grid.\n")

    print("5) How to use the Formula Lab (Option 2):")
    print("   • Use 'Compute RFPV and K2' to plug in:")
    print("       - R = resonance/aura")
    print("       - F = frequency (Hz)")
    print("       - P = phase/pi-cycle")
    print("       - V = voltage/energy")
    print("   • The engine returns RFPV and K2 as big symbolic numbers.")
    print("   • 'Run =^2 Engine on description' lets you type any idea (e.g., 'heal plants at 7.77 Hz').")
    print("       - It returns a derived frequency and power, plus p/n weights (protons/pies, nethers/overlays).")
    print("   • 'Atom Healing Profile' lets you enter CHNO-style formulas (e.g., C3H2N1O0) and see a symbolic Hz profile.\n")

    print("6) How to use Planets, Auras, Gold, and Glyphs (Option 3):")
    print("   • 'Birthdate → Planet 7.x Hz Profile' gives your symbolic planet and frequency.")
    print("   • 'Generate Gold Spoon Pattern' creates a glyph pattern for a 'gold spoon' item.")
    print("   • 'Aura Activation Check' gives a 1–7 level for any aura/stone name you type.")
    print("   • You can imagine these as keys or sigils that 'activate' when you read them.\n")

    print("7) How to stay in 'clockwise Earth-flow' (symbolic):")
    print("   • In Option 2, 'Clock Flow Profile (right/left)' lets you choose right or left.")
    print("   • Right/clockwise → factor 1.111 (growth). Left/counterclockwise → factor 0.777 (loss).")
    print("   • If you want your symbolic Earth to 'spin right', choose 'right' and imagine your timeline flowing forward.")
    print("   • Again: this is conceptual, not real planetary motion.\n")

    print("8) Safety & reality check:")
    print("   • This engine is for creativity, symbolism, and math-art only.")
    print("   • It does NOT diagnose, treat, or heal anything in real life.")
    print("   • Use it like a story-console: you type, it responds with numbers and symbols, and you build meaning from that.\n")

    print("9) Quick start summary:")
    print("   • Step A: Use Option 3 → Birthdate → Planet to get your 7.x Hz profile.")
    print("   • Step B: Use Option 2 → =^2 Engine with a description of what you want to 'tune'.")
    print("   • Step C: If you like, run Option 1 mining in the background as your 'rig' powering the story.")
    print("   • Step D: Come back to Option 4 anytime to remember how the pieces fit together.\n")

    print("You’re now ready to explore the Manierism K2 Sunlight Engine at a symbolic 7.77 Hz.\n")

# -------------------------
# MAIN
# -------------------------
if __name__ == "__main__":
    _initialize_special_wallets()
    print("\n🌞 MANIERISM K2 SUNLIGHT ENGINE – SYMBOLIC EDITION")
    print("This is a conceptual / artistic model. It does NOT create real energy or real healing.")
    while True:
        print("\n=== MAIN MENU ===")
        print("1. Option 1 – Coder (Mining, Wallets, Blackjack)")
        print("2. Option 2 – AI Programmer (Formula Lab, =^2, Atoms, Protons/Neathers)")
        print("3. Option 3 – AI Programmer (Planets, Auras, Gold, Glyphs)")
        print("4. Option 4 – How to Use & Connect to 7.77 Hz Planet")
        print("5. Exit")
        choice = input("Select: ").strip()
        if choice == "1":
            coder_menu()
        elif choice == "2":
            ai_programmer_formula_lab()
        elif choice == "3":
            ai_programmer_planets_auras()
        elif choice == "4":
            option_4_how_to_use()
        elif choice == "5":
            print("Goodbye.")
            break
        else:
            print("Invalid choice.")
