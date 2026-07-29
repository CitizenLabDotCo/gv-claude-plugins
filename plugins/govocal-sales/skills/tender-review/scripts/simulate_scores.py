#!/usr/bin/env python3
"""
Tender scoring + price-to-win simulator (verification engine).

Use this to VERIFY the arithmetic behind the HTML simulator and the price-to-win recommendation.
Don't do procurement price algebra by hand — feed a tender_map-style config in and check the numbers.

It implements the price-formula patterns in references/price_formulas.md, combines price with quality
(additive or MEAT), sweeps our price, and finds the highest price at which we still win.

Usage:
    python3 simulate_scores.py config.json
    python3 simulate_scores.py            # runs the built-in Mechelen-style demo

Config shape (minimal):
{
  "price_weight_points": 50,
  "price_pattern": "lowest_proportional",   # see PRICE_PATTERNS below
  "price_reference": "P_min",               # P_min | P_max | P_avg | a number (fixed ceiling/ref)
  "award_type": "additive",                 # additive | meat
  "cost_floor": 22000,
  "our_quality_points": 38,                 # our non-price points (sum of quality criteria)
  "quality_points_max": 50,                 # max non-price points
  "bidders": [                              # competitors (price = assumed bid; quality = est. points)
      {"name": "TreeCompany", "price": 28000, "quality_points": 33},
      {"name": "Hoplr",       "price": 35000, "quality_points": 30}
  ],
  "sweep": {"low": 20000, "high": 45000, "step": 250}
}
"""
import json, sys

PRICE_PATTERNS = (
    "lowest_proportional", "linear_interpolation", "relative_reference",
    "relative_average", "proportional_difference", "threshold", "meat_ratio",
)


def price_score(p, pattern, max_pts, ref_value, all_prices, caps=None):
    """Return price points for price `p`. `ref_value` may be a number or a token resolved by caller."""
    pmin = min(all_prices)
    pmax = max(all_prices)
    pavg = sum(all_prices) / len(all_prices)

    def resolve(ref):
        if isinstance(ref, (int, float)):
            return float(ref)
        return {"P_min": pmin, "P_max": pmax, "P_avg": pavg}.get(ref, pmin)

    if pattern == "lowest_proportional":
        s = (pmin / p) * max_pts
    elif pattern == "linear_interpolation":
        hi = resolve(ref_value) if ref_value not in (None, "P_min") else pmax
        s = 0.0 if hi == pmin else max_pts * (hi - p) / (hi - pmin)
    elif pattern == "relative_reference":
        ref = resolve(ref_value)
        s = max_pts * (ref - p) / ref
    elif pattern == "relative_average":
        s = (pavg / p) * max_pts
    elif pattern == "proportional_difference":
        s = max_pts * (1 - (p - pmin) / pmin)
    elif pattern == "threshold":
        ceiling = resolve(ref_value)
        s = 0.0 if p > ceiling else (pmin / p) * max_pts
    elif pattern == "meat_ratio":
        s = p  # handled in total() for MEAT; price not separately scored
    else:
        raise ValueError(f"unknown price pattern: {pattern}")

    s = max(0.0, min(s, max_pts))
    if caps:
        s = max(caps.get("floor", 0.0), min(s, caps.get("cap", max_pts)))
    return s


def total_for(price, quality_points, cfg, all_prices):
    """Total award score for a bidder at a given price."""
    if cfg["award_type"] == "meat":
        # value = quality / price (higher = better). Return as-is; compare directly.
        return quality_points / price if price else 0.0
    ps = price_score(price, cfg["price_pattern"], cfg["price_weight_points"],
                     cfg.get("price_reference", "P_min"), all_prices, cfg.get("caps"))
    return quality_points + ps


def evaluate(cfg, our_price):
    """All bidders' totals at a given own-price. Returns (our_total, best_competitor, table)."""
    prices = [our_price] + [b["price"] for b in cfg["bidders"]]
    table = []
    our_total = total_for(our_price, cfg["our_quality_points"], cfg, prices)
    table.append({"name": "Go Vocal", "price": our_price,
                  "quality": cfg["our_quality_points"], "total": round(our_total, 2)})
    best_comp = None
    for b in cfg["bidders"]:
        t = total_for(b["price"], b["quality_points"], cfg, prices)
        table.append({"name": b["name"], "price": b["price"],
                      "quality": b["quality_points"], "total": round(t, 2)})
        if best_comp is None or t > best_comp["total"]:
            best_comp = {"name": b["name"], "total": t}
    return our_total, best_comp, table


def price_to_win(cfg):
    """Highest own-price >= cost_floor at which we beat the strongest competitor."""
    sw = cfg["sweep"]
    p = sw["low"]
    winning = []
    while p <= sw["high"]:
        our_total, best_comp, _ = evaluate(cfg, p)
        wins = best_comp is None or our_total >= best_comp["total"]
        if wins and p >= cfg.get("cost_floor", sw["low"]):
            winning.append(p)
        p += sw["step"]
    if not winning:
        return None
    return max(winning)  # most margin retained while still winning


def main():
    if len(sys.argv) > 1:
        cfg = json.load(open(sys.argv[1]))
    else:
        cfg = {  # Mechelen-style demo: price 50 / quality 40 / MVOO 10, lowest-proportional price
            "price_weight_points": 50, "price_pattern": "lowest_proportional",
            "price_reference": "P_min", "award_type": "additive", "cost_floor": 22000,
            "our_quality_points": 44, "quality_points_max": 50,
            "bidders": [
                {"name": "TreeCompany", "price": 28000, "quality_points": 36},
                {"name": "Hoplr", "price": 33000, "quality_points": 31},
            ],
            "sweep": {"low": 20000, "high": 45000, "step": 250},
        }

    ptw = price_to_win(cfg)
    print("=== Price-to-win ===")
    if ptw is None:
        print("No winning price at/above cost floor under these assumptions.")
    else:
        our_total, best_comp, table = evaluate(cfg, ptw)
        print(f"Recommended max price (still winning): {ptw:,.0f} {''}")
        print(f"  Our total: {our_total:.2f}  vs strongest competitor "
              f"{best_comp['name']} {best_comp['total']:.2f}")
        print("\n=== Scoreboard at recommended price ===")
        for r in sorted(table, key=lambda x: -x["total"]):
            print(f"  {r['name']:<14} price {r['price']:>9,.0f}  quality {r['quality']:>5}  "
                  f"total {r['total']:>6.2f}")

    # Sensitivity across competitor-price scenarios
    print("\n=== Sensitivity (competitor prices ±10%) ===")
    for label, mult in (("low -10%", 0.9), ("expected", 1.0), ("high +10%", 1.1)):
        c2 = json.loads(json.dumps(cfg))
        for b in c2["bidders"]:
            b["price"] = round(b["price"] * mult)
        ptw2 = price_to_win(c2)
        print(f"  {label:<12}: price-to-win = "
              f"{('%.0f' % ptw2) if ptw2 else 'no win'}")


if __name__ == "__main__":
    main()
