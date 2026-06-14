#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
DEEP SYMBOLIC HZ + AURA SCANNER

Creative / symbolic use only.
Not real aura detection.
Not real medical, scientific, or satellite analysis.
"""

import math
import datetime

def aura_color(magnitude):
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

def deep_scan(freq, magnitude):

    aura, rgb, meaning = aura_color(magnitude)

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

    report = {
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

    return report

def print_report(report):

    print("=" * 60)
    print("DEEP SYMBOLIC AURA SCAN")
    print("=" * 60)

    for k, v in report.items():
        print(f"{k:20} : {v}")

    print("=" * 60)

# Example
if __name__ == "__main__":

    frequency = 7.77
    magnitude = 4289

    result = deep_scan(frequency, magnitude)
    print_report(result)