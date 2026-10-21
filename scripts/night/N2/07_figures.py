"""N2 step 6: hand-off closures against the city's own promise date, and build/N2/figures.json.

Reads build/N2/closed_classed.parquet, headline.json, joins.json, register.json.
Writes build/N2/handoff_before_promise.csv and build/N2/figures.json
({id, value, unit, period, definition, label, source_sql_or_script, note}).
Run: .venv/bin/python -I scripts/night/N2/07_figures.py
"""
import json, pathlib
import duckdb

ROOT = pathlib.Path(__file__).resolve().parents[3]
B = ROOT / "build" / "N2"
H = json.loads((B / "headline.json").read_text())
J = json.loads((B / "joins.json").read_text())
REG = json.loads((B / "register.json").read_text())["rows"]
con = duckdb.connect()
con.execute(f"CREATE VIEW cc AS SELECT * FROM '{B/'closed_classed.parquet'}'")

con.execute(f"""COPY (
  SELECT PROBLEMCODE, resolution_text, class, count(*) AS n,
    round(median(days), 2) AS median_days_to_close,
    round(median(days) * 24 * 60) AS median_minutes_to_close,
    round(median(promise_days), 1) AS median_promise_days,
    round(avg((t_closed <= t_promise)::INT), 3) AS share_closed_before_promise,
    round(median(days_left_at_close), 1) AS median_days_left_on_promise_at_close,
    round(avg((days <= 1)::INT), 3) AS share_closed_within_1_day
  FROM cc WHERE class IN ('handed_off','converted') AND t_promise IS NOT NULL
  GROUP BY ALL HAVING count(*) >= 200 ORDER BY median_days_left_on_promise_at_close DESC
) TO '{B/'handoff_before_promise.csv'}' (HEADER)""")

def one(sql, *a):
    return con.execute(sql, list(a)).fetchone()

SCOPE = "requests filed 1 Jan 2025 to 12 Oct 2026, STATUS CLOSED, one row per REQUESTID"
S03 = "scripts/night/N2/03_measures.py (classes from scripts/night/N2/classes.py)"
F = []
def fig(id, value, unit, definition, label="observed", src=S03, note="", period=SCOPE):
    F.append(dict(id=id, value=value, unit=unit, period=period, definition=definition, label=label,
                  source_sql_or_script=src, note=note))

CLASS_NOTE = ("Classes come from a rule table over the city's closing text (PUBLICRESOLUTION), drafted by an AI model "
              "and open for review in research/chapters/N2-closure-classes.csv; the share is a count under those rules.")
m = H["mix_all"]
fig("n2_closed_requests", H["n_closed"], "requests", "Closed 311 requests in scope (deduplicated by REQUESTID).",
    note="Row counts are about 8% higher because the city's CSV repeats a request once per caller.")
fig("n2_share_closed_handoff", round(m["share_handoff_or_converted"], 3), "share of closures",
    "Share of closures whose closing text records a hand-off (scheduled, referred, queued, tagged, 'will be', in progress, "
    "sent to another agency, or a notice to the owner) or a work order, rather than finished work.", note=CLASS_NOTE)
fig("n2_share_closed_done", round(m["share_done"], 3), "share of closures",
    "Share of closures whose closing text says the work was performed (work completed, collection made, repairs made, ...).", note=CLASS_NOTE)
fig("n2_share_closed_no_action", round(m["share_no_action"], 3), "share of closures",
    "Share closed as nothing to do or could not act (no violation, gone on arrival, unable to locate, not city's).", note=CLASS_NOTE)
fig("n2_share_closed_blank", round(m["share_blank"], 3), "share of closures", "Share closed with no closing text at all.",
    note="Half of blank closures are 'Public Nuisance Rpt', which the city describes as logging only.")
fig("n2_share_closed_handoff_excl_notices", round(m["share_handoff_or_converted_excl_enforcement"], 3), "share of closures",
    "As n2_share_closed_handoff but counting enforcement notices to owners (notice of violation, already under notice, warning, "
    "ticket, summons, arrest) as neither hand-off nor done.", note="The conservative version of the headline. " + CLASS_NOTE)
fig("n2_handoff_share_of_outcome_closures", round(m["handoff_or_converted_share_of_done_handoff_converted"], 3), "share",
    "Among closures that say something about the work (done, hand-off, work order), the share that record a hand-off or work order.",
    note="About half. " + CLASS_NOTE)
fig("n2_share_closed_handoff_resident", round(H["mix_resident"]["share_handoff_or_converted"], 3), "share of closures",
    "As n2_share_closed_handoff, resident channels only (any caller row WEB, PHONE, EMAIL, CHAT, TWITTER, LETTER).", note=CLASS_NOTE)
ot = H["on_time_closures"]
fig("n2_on_time_closures_that_are_handoffs", round(ot["share_handoff_or_converted"], 3), "share of on-time closures",
    "Of closures made on or before the request's own promised date (PRJCOMPLETEDATE), the share that record a hand-off or work order.",
    note=f"Done: {ot['share_done']:.1%}; no action: {ot['share_no_action']:.1%}; n on time = {ot['n_on_time']:,}. "
         "A closed-by-promise rate counts these hand-offs as on time. " + CLASS_NOTE)
hb = H["handoff_before_promise"]
fig("n2_handoff_closed_before_promise", round(hb["share_closed_before_promise"], 3), "share of hand-off closures",
    "Share of hand-off or work-order closures that were closed before the promised date for the work.",
    note=f"Median {hb['median_days_to_close']:.1f} days to close with {hb['median_days_left_at_close']:.1f} days still left on the promise; n = {hb['n_handoff_with_promise']:,}.")

for pc, txt, idp in [("Weeds-Vacant Bldg", "on schedule to be cut, call CSB for details", "n2_weeds_vbldg_on_schedule"),
                     ("Weeds-Vacant Lot", "on schedule to be cut, call CSB for details", "n2_weeds_vlot_on_schedule"),
                     ("NOWATER", "scheduled for repair by water department", "n2_nowater_scheduled"),
                     ("WTR-COMING-UP", "scheduled for repair by water department", "n2_water_coming_up_scheduled"),
                     ("Cave-Ins", "referred to street maintenance for repair work to be scheduled", "n2_caveins_referred")]:
    r = one("""SELECT count(*), median(days)*24*60, median(promise_days), avg((t_closed<=t_promise)::INT), median(days_left_at_close)
               FROM cc WHERE PROBLEMCODE=? AND resolution_text=?""", pc, txt)
    tot = one("SELECT count(*) FROM cc WHERE PROBLEMCODE=?", pc)[0]
    fig(idp, round(r[1]), "minutes (median, filing to closure)",
        f"'{pc}' requests closed with the words '{txt}': median minutes from filing to closure.",
        note=f"n = {r[0]:,} of {tot:,} closed '{pc}' requests; the request's own promise date is a median {r[2]:g} days after filing; "
             f"{r[3]:.0%} closed before it, with a median {r[4]:.0f} days still to run.")

for pc, idp in [("Debris-alley/street", "n2_debris_alley_on_time_handoff"), ("Bulky items missed", "n2_bulky_on_time_handoff"),
                ("Vacnt Bldg Unsecured", "n2_vacant_unsecured_on_time_handoff")]:
    r = one("""SELECT avg((t_closed<=t_promise)::INT),
                      avg((class IN ('handed_off','converted'))::INT) FILTER (WHERE t_closed<=t_promise),
                      avg((class='done' AND t_closed<=t_promise)::INT), count(*), median(promise_days)
               FROM cc WHERE PROBLEMCODE=? AND t_promise IS NOT NULL""", pc)
    fig(idp, round(r[1], 3), "share of on-time closures",
        f"'{pc}': of closures made by the request's promise date, the share that record a hand-off rather than the work.",
        note=f"Closed by promise ({r[4]:g} days): {r[0]:.0%} of {r[3]:,}; closed by promise with text saying done: {r[2]:.0%}.")

bu = next(r for r in J["boardups"]["rows"] if r["label"].startswith("closed 'referred"))
na = next(r for r in J["boardups"]["rows"] if r["label"].startswith("closed no_action"))
P_BU = "311 'Vacnt Bldg Unsecured' filed 1 Jan 2024 to 14 Jul 2026 (90 days of follow-up)"
fig("n2_boardup_within_promise", bu["boarded_within_14d_promise"], "share of requests",
    "Vacant building unsecured, closed 'referred to board up crew': share with a board-up recorded at the same address within the 14-day promise.",
    src="scripts/night/N2/05_joins.py", period=P_BU,
    note=(f"n = {bu['n']:,}; median {bu['median_days_to_close_311']} days to close in 311; boarded within 30 days {bu['boarded_within_30d']:.0%}, "
          f"within 90 days {bu['boarded_within_90d']:.0%}; median {bu['median_days_to_boardup_if_any']} days to board-up where one exists. "
          f"Comparison: closures saying no violation etc. {na['boarded_within_90d']:.0%} within 90 days. Address match, board-up layer "
          "maps8_BUILDING_DIVISION_Boardups (DateBoardedUp). Chronic sites: 33% had a board-up 30 to 365 days before filing."))
fig("n2_boardup_within_90d", bu["boarded_within_90d"], "share of requests",
    "As n2_boardup_within_promise, within 90 days of filing.", src="scripts/night/N2/05_joins.py", period=P_BU)
lra = next(r for r in J["demolitions"]["rows"] if r["PROBLEMCODE"] == "LRA Demo Submission" and r["status_group"] == "open")
fig("n2_lra_demo_open_but_demolished", lra["n_completed_demolition_after_filing"], "requests",
    "LRA demolition submissions still open in 311 that have a completed demolition permit at the same address after filing.",
    src="scripts/night/N2/05_joins.py", period="311 'LRA Demo Submission' filed 1 Jan 2024 to 12 Oct 2026, open on 13 Oct 2026",
    note=f"{lra['completed_demolition_at_address_after_filing']:.0%} of {lra['n']} open; permit layer maps8_BUILDING_DIVISION_Demolitions (PermitStatus Completed, DateClosed). Open is not undone either.")
fig("n2_csv_rows_per_request", 349031, "rows",
    "Rows in the city's 2024-2026 311 CSVs; they hold 322,104 distinct REQUESTIDs (24,020 repeated, up to 21 times; 19,431 exact duplicate rows; the rest differ only in CALLERTYPE).",
    src="scripts/night/N2/01_load.py", period="311 CSVs 2024, 2025, 2026 (to 13 Oct 2026)",
    note="Count requests by distinct REQUESTID; row counts over-count by about 8%.")
reg_yes = sum(1 for r in REG if r["independent_completion_record"].startswith("yes"))
reg_part = sum(1 for r in REG if r["independent_completion_record"].startswith("partial"))
reg_no = sum(1 for r in REG if r["independent_completion_record"].startswith("no"))
fig("n2_register_services_with_record", reg_yes, "services",
    f"Services in the register (of {len(REG)}) with an independent completion record on disk that can be joined to requests.",
    src="scripts/night/N2/06_register.py", period="files on disk 13 Oct 2026",
    note=f"partial: {reg_part}; none: {reg_no}; not applicable: {len(REG)-reg_yes-reg_part-reg_no}. Yes = weeds (ledger), vacant buildings unsecured (board-ups), LRA demolition (permits).")
sw = next(r for r in REG if r["id"] == "sidewalks")
fig("n2_sidewalk_daterepair_filled", 0, "rows", "Rows of the city's sidewalk inventory (36,822) with the DateRepair field filled.",
    src="scripts/night/N2/04_probe_completion_files.py", period="maps8_Sidewalks layer as saved 13 Oct 2026",
    note=f"Curb ramps: 0 of 7,932. Sidewalk requests filed 2025-26: {sw['filed_2025_26']:,}, {sw['open']:,} open.")

# ---- register counts quoted in the README: open requests for three services, re-counted from the extract
P311 = B / "private" / "csb_2024_2026.parquet"
for idp, pc, what in [("n2_reg_lead_open", "Lead Insp", "lead-paint inspection"),
                      ("n2_reg_sirens_open", "Sirens Not Heard", "outdoor warning siren not heard"),
                      ("n2_reg_tornado_debris_open", "TDebris-alley/street", "tornado debris removal (alley/street)")]:
    n, n_open = con.execute(f"""SELECT count(DISTINCT REQUESTID),
        count(DISTINCT REQUESTID) FILTER (WHERE STATUS NOT IN ('CLOSED','CANCEL') OR STATUS IS NULL)
        FROM '{P311}' WHERE PROBLEMCODE = ? AND t_init >= TIMESTAMP '2025-01-01' AND t_init < TIMESTAMP '2026-10-13'""", [pc]).fetchone()
    fig(idp, n_open, "requests open",
        f"'{pc}' ({what}) requests filed 1 Jan 2025 to 12 Oct 2026 that were still open (status neither CLOSED nor CANCEL) in the city's file of 13 Oct 2026.",
        src="scripts/night/N2/07_figures.py (same count as build/N2/register.json, scripts/night/N2/06_register.py)",
        period="requests filed 1 Jan 2025 to 12 Oct 2026; status as of the 13 Oct 2026 file",
        note=f"{n_open} of {n} filed ({n_open/n:.0%}). Shown in the register as '{n_open} of {n} open'.")

# ---- derivations ("How we know"), one or two plain sentences per figure
BASE_311 = ("311 service requests (city open data, csb.zip yearly CSVs 2024-2026; invalid UTF-8 bytes dropped with iconv -c), "
            "reduced to one row per REQUESTID because the CSV repeats a request once per caller.")
CLASS_DERIV = (BASE_311 + " Each closure's closing text (PUBLICRESOLUTION) is given one class by a rule table that an AI model drafted "
               "and a person can review (research/chapters/N2-closure-classes.csv); the figure counts closures under those rules.")
PROMISE_DERIV = CLASS_DERIV + " The promise is the request's own PRJCOMPLETEDATE, which the city sets when the request is filed."
BU_DERIV = (BASE_311 + " 'Vacant building unsecured' requests joined to the Building Division's board-up layer (city ArcGIS maps8 "
            "BUILDING_DIVISION Boardups, DateBoardedUp) by normalised street address; the first board-up from one day before filing counts. "
            "Board-ups recur at the same buildings, so a later board-up need not answer this request.")
DERIV = {
    "n2_closed_requests": BASE_311 + " Counted requests with STATUS CLOSED filed 1 Jan 2025 to 12 Oct 2026.",
    "n2_on_time_closures_that_are_handoffs": PROMISE_DERIV,
    "n2_handoff_closed_before_promise": PROMISE_DERIV,
    "n2_debris_alley_on_time_handoff": PROMISE_DERIV,
    "n2_bulky_on_time_handoff": PROMISE_DERIV,
    "n2_vacant_unsecured_on_time_handoff": PROMISE_DERIV,
    "n2_boardup_within_promise": BU_DERIV,
    "n2_boardup_within_90d": BU_DERIV,
    "n2_lra_demo_open_but_demolished": (BASE_311 + " Open 'LRA Demo Submission' requests joined to the Building Division's demolition-permit "
        "layer (city ArcGIS maps8 BUILDING_DIVISION Demolitions) by normalised street address; counted when a permit there is Completed with "
        "DateClosed on or after the filing date. Owner and contractor fields were not used."),
    "n2_csv_rows_per_request": ("Counted rows and distinct REQUESTIDs in the city's 311 CSVs for 2024, 2025 and 2026 (csb.zip, invalid bytes "
        "dropped) and compared every column among repeated ids: only CALLERTYPE differs."),
    "n2_register_services_with_record": ("Each service's 311 request types checked against every city file on disk that could record the work "
        "(forestry ledger, Cityworks samples, board-up, demolition, sidewalk, street-light and signal layers, water outage page, towed-vehicle "
        "lookup); 'yes' needs dated work at an address that can be joined to the request."),
    "n2_sidewalk_daterepair_filled": ("Read every feature of the city's sidewalk and curb-ramp layers (city ArcGIS maps8 Sidewalks and "
        "CurbRamps, saved 13 Oct 2026) and counted non-empty DateRepair values."),
}
for k in ["n2_weeds_vbldg_on_schedule", "n2_weeds_vlot_on_schedule", "n2_nowater_scheduled", "n2_water_coming_up_scheduled", "n2_caveins_referred"]:
    DERIV[k] = (BASE_311 + " Median minutes from DATETIMEINIT to DATETIMECLOSED for closures with exactly these closing words; "
                "the promise is the request's PRJCOMPLETEDATE.")
for k in ["n2_reg_lead_open", "n2_reg_sirens_open", "n2_reg_tornado_debris_open"]:
    DERIV[k] = (BASE_311 + " Counted distinct requests of this type filed 1 Jan 2025 to 12 Oct 2026 whose STATUS in the 13 Oct 2026 file "
                "is neither CLOSED nor CANCEL; no other source is joined.")
for f in F:
    f["derivation"] = DERIV.get(f["id"], CLASS_DERIV)
    if f["id"] == "n2_register_services_with_record":
        f["note"] = f["note"].replace("Yes = weeds (ledger)", "Yes = weeds on vacant lots and at vacant buildings (forestry ledger)")
    if f["id"] in ("n2_weeds_vbldg_on_schedule", "n2_weeds_vlot_on_schedule"):
        f["note"] += " The speed suggests an automatic closing rule (inferred)."

(B / "figures.json").write_text(json.dumps(F, indent=2))
for f in F:
    print(f"{f['id']:42s} {f['value']!s:>10} {f['unit']}  | {f['note'][:150]}")
