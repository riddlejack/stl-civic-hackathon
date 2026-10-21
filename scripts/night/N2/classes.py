"""Closure classes for St. Louis 311 PUBLICRESOLUTION texts.

This is the reviewable rule table. Every distinct closing text seen on closed
requests 2024-2026 is listed once in TEXT_RULES with its class and a rule id.
TYPE_OVERRIDES changes the class for a (PROBLEMCODE, text) pair where the same
words mean something different for that request type. Anything not listed
falls to 'info_other' with rule 'unlisted' so it is visible, not hidden.

Classes (exactly one per text):
  done        the closing words say the city performed the requested work
  handed_off  scheduled, referred, queued, tagged, "will be", in progress,
              sent to another agency, or an enforcement step that passes the
              fix to the owner (notice, warning, ticket, fine, summons, arrest);
              the rule id says which (handed_off:enforcement is separable)
  converted   a work order or work ticket was created
  no_action   nothing to do or could not act: no violation, no problem found,
              gone/abated on arrival, unable to locate or access, not the
              city's responsibility, declined
  info_other  call for details, contacted, need more info, advice, other
  blank       no closing text at all

The classes were assigned by Claude (an AI model) reading every text with its
top request types; a person should review them. Matching is on the text after
trimming, collapsing internal whitespace and lower-casing (see norm()).
"""
import re

def norm(s):
    if s is None:
        return ""
    return re.sub(r"\s+", " ", str(s)).strip().lower()

# text (normalised) -> (class, rule id)
_R = {}
def _add(cls, rule, *texts):
    for t in texts:
        _R[norm(t)] = (cls, f"{cls}:{rule}")

# ---- done: the words say the work was performed
_add("done", "work_stated",
     "work completed", "complete", "repairs made", "repairs completed", "Services completed",
     "Street maintenance work completed", "asphalted", "Park maintenance complete",
     "removed and made safe", "grass cut", "Meter Repaired", "hydrant cap replaced",
     "hydrant maintenance complete", "work has complied with requested change",
     "building was secured by city", "building was re-secured by city",
     "teehead shut - owner to be billed", "stop box shut", "destroy tap/service")
_add("done", "collection_made",
     "collection made", "bulk/debris items have been collected",
     "trash/debris was cleaned in area and collection made",
     "container was overloaded and had to be collected by special truck",
     "trash/litter/debris removed")
_add("done", "container_work",
     "container(s) replaced with new", "container maintenance completed", "container moved",
     "container(s) placed", "uprighted container", "container removed")
_add("done", "graffiti_removed",
     "Graffiti removed  painted", "Graffiti removed  power washed",
     "Graffiti removed  painted and power washed", "graffiti removed")
_add("done", "animal_handled",
     "animal(s) picked up", "animal picked up", "apprehended animal",
     "Education and TNR Completed")
_add("done", "vehicle_towed", "vehicle towed")
_add("done", "treated",
     "treated with rodentcide", "treated with larvicide", "treated with adulticide",
     "added to no spray list")
_add("done", "inspection_service",
     "lead inspection completed", "no lead hazards found")
_add("done", "permit_decided", "permit approved", "permit issued")

# ---- converted: a work order / work ticket exists
_add("converted", "work_order",
     "removal work order created", "trim work order created", "Work order created",
     "work ticket issued to crew")

# ---- handed_off: scheduled / future tense / queued
_add("handed_off", "scheduled",
     "on schedule to be cut, call CSB for details", "on schedule to be cut, call Forestry for details",
     "Grass on schedule to be cut", "scheduled for repair by water department",
     "repair work scheduled", "repairs scheduled", "teehead leaking - scheduled for repair",
     "Trash on schedule for pickup", "bulk will be picked up in correct week")
_add("handed_off", "future_tense",
     "Collection will be made next scheduled day",
     "Due to employee shortage, the routes will be completed in order, as soon possible",
     "matter will be investigated and appropriate action taken",
     "Matter is being investigated and appropriate action will be taken",
     "collection will be made;problem items removed from container",
     "Your street painting request has been evaluated and will be included in our seasonal striping plan.",
     "will adjust timing", "timing is under study")
_add("handed_off", "queued_program",
     "added to rotation", "approved for next available planting",
     "added to sewer lateral repair program", "Sent to sewer lateral program for inspection",
     "Already on sidewalk program", "location added to sidewalk program",
     "Major Capital Improvement Project")
_add("handed_off", "in_progress",
     "work in progress", "Work still in process", "parts on order", "sign on order",
     "Waiting for parts")
_add("handed_off", "tagged", "vehicle tagged for tow")
_add("handed_off", "internal_referral",
     "referred to street maintenance for repair work to be scheduled",
     "Sent to street maintenance for repair", "refer to street inspector for evaluation",
     "referred to board up crew", "supervisor notified", "Maintenance supervisor notified",
     "sent to field", "Referred to Forestry", "referred to Forestry",
     "referred to proper department", "referred to Water Division", "referred to Building Division",
     "referred to Parks", "referred to Traffic Division", "referred to Refuse Division",
     "referred to Trash Task Force", "referred to community sanitation",
     "Sent to Parking Enforcement",
     "no leaks detected - referred to street division for repair",
     "vehicle not derelict, refer to Treasurer for ticketing")
_add("handed_off", "external_agency",
     "report to MODOT", "reported to MODOT", "referred  to MODOT", "reported to MSD", "referred to MSD",
     "referred to msd", "referred to Laclede Gas", "ameren signal outage",
     "on-going project, under construction by others",
     "contractor responsible has been notified to make repairs",
     "Work being performed by Board of Public Service", "Work being performed by MSD",
     "Work being performed by Water Dept", "Work being performed by MODOT",
     "Work being performed by Laclede Gas", "telecom responsible has been notified",
     "turned over to insurance company",
     "accident report has been forwarded to city counselor's office",
     "Stolen/Police notified", "building was occupied, will need police")
_add("handed_off", "funding_pending",
     "not funded by traffic division, seeking outside funding support",
     "Aldermanic funding support", "aldermanic approval needed")
_add("handed_off", "enforcement",
     "issued notice of violation", "Building already under notice", "already under notice",
     "confirmed violation, owner notified", "owner notified", "owner sent notice to repair",
     "secure notice sent", "summons issued", "Issued Fine", "Referred to Court", "referred to court",
     "stop work order issued", "violation notice under appeal",
     "Re-Instructional/ Warning Letter Sent", "Verbal Re-Instructional/ Warning Given",
     "instructional letter issued as a warning", "verbal advice given", "given verbal advice",
     "vehicle ticketed", "violation issued to private hauler/owner",
     "Extension Given", "working with property owner - extension given",
     "Cleared by arrest - Illegal Dumping", "Cleared by arrest - Container Violation",
     "Cleared by arrest - Illegal Dumping & Container Violation",
     "Cleared by arrest - No Commercial Container", "cleared by arrest",
     "Cleared by arrest - Accumulation of Rubbish")

# ---- no_action
_add("no_action", "not_found_or_gone",
     "vehicle gone upon inspection", "vehicle gone upon reinspection", "no vehicle found",
     "no problem found", "patrolled area, no strays observed", "animal not found",
     "abated before inspection", "abated at time of inspection", "secured at time of inspection",
     "vehicle repaired upon reinspection", "No graffiti found", "no leaks detected",
     "no water surfacing at time of inspection",
     "chased stray, unable to apprehend, will continue to monitor area", "Completed by owner",
     "collection made by private hauler", "Work being performed by property owner")
_add("no_action", "no_violation",
     "no evidence of violation", "no forestry violations", "unable to confirm violation",
     "no violation found", "no cause for complaint", "complaint unfounded",
     "meets minimum standards", "permit found and current", "no permit required",
     "vehicle not derelict, no cause for complaint", "animal(s) appear healthy",
     "animal(s) current on vaccination/registration", "container sits in the proper space",
     "proper number of containers in alley", "container not blocking", "vendor is legal",
     "Not enough evidence to lead to arrest", "No evidence to lead to an arrest", "no witness(es)",
     "Caller is not the witness", "Witness(es) refuses to assist in prosecution")
_add("no_action", "no_service_needed",
     "no service necessary", "no service to tree(s) necessary", "No response required at this time",
     "no appropriate planting site", "Block is on a \"no mosquito spraying\" list")
_add("no_action", "no_access_or_location",
     "inspector unable to gain access", "no response at premise", "inspection not permitted by owner/occupant",
     "lead inspection not permitted", "No access to Roll-out Container", "no such address",
     "no such address/incorrect address", "wrong address", "Incorrect information provided",
     "vacant property", "Unable to remove, too high, no access or too dangerous")
_add("no_action", "not_city_responsibility",
     "not city property", "no jurisdiction", "owner's responsibility",
     "Citizen's responsibility to clean up trash", "citizen will need plumber to make repairs",
     "Not responsibility of Parks Department", "responsibility of Ameren UE")
_add("no_action", "declined",
     "shelter full, unable to accept animals", "property not eligible for sidewalk program",
     "permit denied", "need permit", "Alderman did not provide funds",
     "yard waste now on winter schedule")

# ---- info_other
_add("info_other", "call_for_details",
     "Please call CSB for details", "Request investigated, please call NSO for details",
     "Request investigated, please call for details", "See LRA comments", "see SR comments",
     "Investigations Complete / Resolved, call 314-552-7626 for details", "Contact SLMPD")
_add("info_other", "need_info",
     "need more info", "Need More Info", "Need customer to provide exact address",
     "See corrected address")
_add("info_other", "contacted_or_advised",
     "citizen contacted", "citizen contacted - no response, left message", "unable to contact citizen",
     "instructions issued to customer", "recycling info sent", "sent Holiday schedule",
     "disseminated air pollution guidelines", "citizen contacted - appeal denied",
     "letter sent to resident to verify status")
_add("info_other", "outcome_unstated",
     "investigation complete", "canceled", "Camera request")
_add("done", "work_stated", "siren repaired")
_add("no_action", "no_violation", "unable to substantiate this claim",
     "siren inspected and found operational, citizen may not hear siren when indoors")
_add("no_action", "declined", "staff is unable to fulfill this request at this time")
_add("handed_off", "external_agency", "reported to Ameren", "referred to Charter Communications")
_add("handed_off", "internal_referral", "refer to street division for repair")
_add("info_other", "call_for_details", "other - call CSB for details",
     "staff is addressing this concern, please call for details", "MORE INFORMATION NEEDED")
_add("info_other", "facility_status",
     "Restrooms closed", "Fountains closed", "Restrooms open", "Irrigation off")

TEXT_RULES = dict(_R)

# Prefix rules for texts that carry staff contact details (we never write those out)
PREFIX_RULES = [
    (norm("More information is needed."), ("info_other", "info_other:need_info")),
]

# (PROBLEMCODE, normalised text) -> (class, judgement note)
TYPE_OVERRIDES = {
    ("Foreman cntct citizn", norm("citizen contacted")):
        ("done", "judgement: the request type is 'foreman contact citizen'; contacting is the service"),
    ("Instructn hshld/blky", norm("instructions issued to customer")):
        ("done", "judgement: the request type asks for instructions; issuing them is the service"),
}

CLASSES = ["done", "handed_off", "converted", "no_action", "info_other", "blank"]


def classify(problemcode, text):
    """Return (class, rule_or_judgement) for one closed request."""
    t = norm(text)
    if t == "":
        return "blank", "blank:no_text"
    key = (problemcode, t)
    if key in TYPE_OVERRIDES:
        return TYPE_OVERRIDES[key]
    if t in TEXT_RULES:
        return TEXT_RULES[t]
    for p, v in PREFIX_RULES:
        if t.startswith(p):
            return v
    return "info_other", "info_other:unlisted (not yet reviewed)"


def redact(text):
    """Drop staff e-mail addresses from a closing text before writing it out."""
    if text is None:
        return ""
    return re.sub(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+", "[staff e-mail removed]", str(text))
