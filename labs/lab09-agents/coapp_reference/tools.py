"""
Read-only tools over the Harbor PSA SQLite extract (Ch. 6, "Agents": tools, function calling).

    from coapp.tools import TOOLS, call_tool
    call_tool("get_client", {"code": "KVA"})         # -> JSON string
    call_tool("lookup_ticket", '{"ticket_id": "x"}')  # -> '{"error": "..."}' (sent back to the model)

TOOLS is the list of OpenAI tool schemas the model sees. call_tool(name, args) validates
the arguments, runs the tool, and ALWAYS returns a string: the JSON result, or a JSON
object with an "error" key that tells the model what to fix. Every query is parameterized
and runs on a read-only SQLite connection, so a tool can never change the data.
"""
import json
import re
import sqlite3

from . import config

CATEGORIES = ["Account/Access", "Email/M365", "Hardware", "Printing/Scanning", "Network/Internet",
              "Software", "Backup/Restore", "Onboarding/Offboarding", "Phone/VoIP", "Security Report",
              "Server/Infrastructure", "General Request"]
ASSET_TYPES = ["laptop", "desktop", "server", "firewall", "switch", "access_point", "printer", "phone", "nas"]
STATUSES = ["open", "in_progress", "waiting_on_client", "closed", "not_closed"]
MAX_ROWS = 20


def _fn(name, description, properties, required):
    return {"type": "function", "function": {
        "name": name, "description": description,
        "parameters": {"type": "object", "properties": properties, "required": required,
                       "additionalProperties": False}}}


TOOLS = [
    _fn("lookup_ticket",
        "Get one support ticket by its ID: status, priority, category, client (name and tier), "
        "assigned technician, timestamps, and a short description and resolution note.",
        {"ticket_id": {"type": "string", "pattern": r"^TCK-\d{6}$",
                       "description": "Ticket ID like TCK-119947 (TCK- plus 6 digits)."}},
        ["ticket_id"]),
    _fn("search_tickets",
        "Search tickets with filters. Returns the total number of matches and up to 20 tickets "
        "(newest first). Use status='not_closed' for tickets that are still open in any way "
        "(open, in_progress or waiting_on_client).",
        {"client_code": {"type": "string", "pattern": r"^[A-Za-z]{3}$",
                         "description": "3-letter client code like KVA. Use get_client to find a code from a name."},
         "status": {"type": "string", "enum": STATUSES},
         "category": {"type": "string", "enum": CATEGORIES},
         "since": {"type": "string", "pattern": r"^\d{4}-\d{2}-\d{2}$",
                   "description": "Only tickets created on or after this date (YYYY-MM-DD)."}},
        []),
    _fn("get_client",
        "Get a client's profile: code, name, service tier (Essentials/Professional/Premier), users, "
        "sites, backup and VoIP flags, and contacts. Accepts the 3-letter code or part of the name.",
        {"code": {"type": "string", "minLength": 2,
                  "description": "Client code like KVA, or part of the client name like 'Kaw Valley'."}},
        ["code"]),
    _fn("list_assets",
        "List a client's managed assets (computers, servers, network gear, printers, phones). "
        "Returns the total count and up to 20 assets. Retired assets are excluded unless include_retired is true.",
        {"client_code": {"type": "string", "pattern": r"^[A-Za-z]{3}$",
                         "description": "3-letter client code like EMS."},
         "type": {"type": "string", "enum": ASSET_TYPES},
         "os_contains": {"type": "string", "description": "Filter on operating system text, e.g. 'Windows 10'."},
         "include_retired": {"type": "boolean"}},
        ["client_code"]),
    _fn("sla_target",
        "Get the CURRENT contractual SLA targets for a service tier and ticket priority: first-response "
        "target and resolution target, and whether the clock is business hours or 24x7.",
        {"tier": {"type": "string", "enum": ["Essentials", "Professional", "Premier"]},
         "priority": {"type": "string", "enum": ["P1", "P2", "P3", "P4"]}},
        ["tier", "priority"]),
]
TOOL_NAMES = [t["function"]["name"] for t in TOOLS]


class ToolError(Exception):
    """A problem the model can fix (not found, bad value). Sent back as {"error": ...}."""


def _con():
    con = sqlite3.connect(f"file:{config.db_path()}?mode=ro", uri=True, check_same_thread=False)
    con.row_factory = sqlite3.Row
    return con


def _rows(sql, params=()):
    con = _con()
    try:
        return [dict(r) for r in con.execute(sql, params).fetchall()]
    finally:
        con.close()


def _short(text, n=400):
    text = (text or "").strip()
    return text if len(text) <= n else text[:n] + "..."


def describe_minutes(minutes: int, clock: str) -> str:
    """240, 'business' -> '4 business hours'; 15, '24x7' -> '15 minutes (24x7)'."""
    if clock == "business":
        if minutes % 660 == 0:
            d = minutes // 660
            return f"{d} business day{'s' if d > 1 else ''}"
        if minutes % 60 == 0:
            h = minutes // 60
            return f"{h} business hour{'s' if h > 1 else ''}"
        return f"{minutes} business minutes"
    if minutes % 60 == 0:
        h = minutes // 60
        return f"{h} hour{'s' if h > 1 else ''} (24x7)"
    return f"{minutes} minutes (24x7)"


def _client_code(code: str) -> str:
    code = (code or "").strip().upper()
    if not _rows("SELECT 1 FROM clients WHERE code=?", (code,)):
        raise ToolError(f"No client with code {code!r}. Call get_client with the client's name to find its code.")
    return code


def lookup_ticket(ticket_id: str) -> dict:
    rows = _rows(
        "SELECT t.ticket_id, t.created_at, t.client_code, c.name AS client_name, c.tier AS client_tier, "
        "t.subject, t.description, t.category, t.subcategory, t.priority, t.status, "
        "tech.name AS assigned_technician, t.first_response_at, t.resolved_at, t.resolution_notes, "
        "t.runbook_ref, t.sla_response_met, t.onsite, t.asset_tag "
        "FROM tickets t JOIN clients c ON c.code = t.client_code "
        "LEFT JOIN technicians tech ON tech.tech_id = t.assigned_tech_id WHERE t.ticket_id = ?",
        (ticket_id.strip().upper(),))
    if not rows:
        raise ToolError(f"Ticket {ticket_id} was not found. Check the ID, or use search_tickets.")
    r = rows[0]
    r["description"] = _short(r["description"])
    r["resolution_notes"] = _short(r["resolution_notes"])
    return r


def search_tickets(client_code: str | None = None, status: str | None = None,
                   category: str | None = None, since: str | None = None) -> dict:
    where, params = [], []
    if client_code:
        where.append("client_code = ?")
        params.append(_client_code(client_code))
    if status == "not_closed":
        where.append("status != 'closed'")
    elif status:
        where.append("status = ?")
        params.append(status)
    if category:
        where.append("category = ?")
        params.append(category)
    if since:
        where.append("created_at >= ?")
        params.append(since)
    sql_where = (" WHERE " + " AND ".join(where)) if where else ""
    total = _rows(f"SELECT count(*) AS n FROM tickets{sql_where}", params)[0]["n"]
    rows = _rows(f"SELECT ticket_id, created_at, client_code, status, priority, category, subject "
                 f"FROM tickets{sql_where} ORDER BY created_at DESC LIMIT {MAX_ROWS}", params)
    return {"total_matches": total, "returned": len(rows), "tickets": rows}


def get_client(code: str) -> dict:
    code = code.strip()
    rows = _rows("SELECT code, name, industry, city, state, users, tier, client_since, sites, "
                 "backup_included, has_voip, primary_contact_id, authorized_contact_id "
                 "FROM clients WHERE upper(code) = upper(?)", (code,))
    if not rows:
        rows = _rows("SELECT code, name, industry, city, state, users, tier, client_since, sites, "
                     "backup_included, has_voip, primary_contact_id, authorized_contact_id "
                     "FROM clients WHERE lower(name) LIKE lower(?) ORDER BY name", (f"%{code}%",))
    if not rows:
        raise ToolError(f"No client matches {code!r}. Try a shorter part of the name.")
    if len(rows) > 1:
        return {"matches": [{"code": r["code"], "name": r["name"]} for r in rows],
                "note": "More than one client matched; call get_client again with the exact code."}
    r = rows[0]
    names = {c["contact_id"]: f"{c['first_name']} {c['last_name']} ({c['title']})"
             for c in _rows("SELECT * FROM contacts WHERE client_code = ?", (r["code"],))}
    r["primary_contact"] = names.get(r.pop("primary_contact_id"))
    r["authorized_contact"] = names.get(r.pop("authorized_contact_id"))
    return r


def list_assets(client_code: str, type: str | None = None, os_contains: str | None = None,
                include_retired: bool = False) -> dict:
    where, params = ["client_code = ?"], [_client_code(client_code)]
    if type:
        where.append("type = ?")
        params.append(type)
    if os_contains:
        where.append("lower(os) LIKE lower(?)")
        params.append(f"%{os_contains}%")
    if not include_retired:
        where.append("status != 'retired'")
    sql_where = " WHERE " + " AND ".join(where)
    total = _rows(f"SELECT count(*) AS n FROM assets{sql_where}", params)[0]["n"]
    rows = _rows(f"SELECT asset_tag, hostname, type, make, model, os, status, warranty_end, notes "
                 f"FROM assets{sql_where} ORDER BY asset_tag LIMIT {MAX_ROWS}", params)
    return {"total_matches": total, "returned": len(rows), "assets": rows}


def sla_target(tier: str, priority: str) -> dict:
    rows = _rows("SELECT * FROM sla_targets WHERE tier = ? AND priority = ?", (tier, priority))
    if not rows:
        raise ToolError(f"No SLA row for tier={tier!r}, priority={priority!r}.")
    r = rows[0]
    return {"tier": tier, "priority": priority,
            "response_minutes": r["response_minutes"], "response_clock": r["response_clock"],
            "response_target": describe_minutes(r["response_minutes"], r["response_clock"]),
            "resolution_minutes": r["resolution_business_minutes"], "resolution_clock": r["resolution_clock"],
            "resolution_target": describe_minutes(r["resolution_business_minutes"], r["resolution_clock"])}


FUNCTIONS = {"lookup_ticket": lookup_ticket, "search_tickets": search_tickets, "get_client": get_client,
             "list_assets": list_assets, "sla_target": sla_target}
_SCHEMAS = {t["function"]["name"]: t["function"]["parameters"] for t in TOOLS}


def validate_args(name: str, args: dict) -> list:
    """Return a list of readable problems with the arguments (empty list = valid)."""
    schema = _SCHEMAS[name]
    try:
        from jsonschema import Draft202012Validator
        problems = []
        for e in sorted(Draft202012Validator(schema).iter_errors(args), key=str):
            where = "/".join(map(str, e.path)) or "arguments"
            if e.validator == "pattern":  # regexes confuse models; repeat the human description instead
                desc = schema["properties"].get(where, {}).get("description", "")
                problems.append(f"{where}: {e.instance!r} is not in the right format. {desc}".strip())
            else:
                problems.append(f"{where}: {e.message}")
        return problems
    except ImportError:  # minimal fallback when jsonschema is not installed
        problems = [f"missing required argument {k!r}" for k in schema["required"] if k not in args]
        problems += [f"unknown argument {k!r}" for k in args if k not in schema["properties"]]
        for k, spec in schema["properties"].items():
            if k in args and "enum" in spec and args[k] not in spec["enum"]:
                problems.append(f"{k}: {args[k]!r} is not one of {spec['enum']}")
            if k in args and "pattern" in spec and not re.match(spec["pattern"], str(args[k])):
                problems.append(f"{k}: {args[k]!r} does not match {spec['pattern']}")
        return problems


def call_tool(name: str, args) -> str:
    """Validate and run one tool. Always returns a string for the tool message."""
    if name not in FUNCTIONS:
        return json.dumps({"error": f"Unknown tool {name!r}. Available tools: {TOOL_NAMES}"})
    if isinstance(args, str):
        try:
            args = json.loads(args or "{}")
        except json.JSONDecodeError:
            return json.dumps({"error": "The arguments were not valid JSON. Send a JSON object."})
    args = {k: v for k, v in (args or {}).items() if v is not None}
    problems = validate_args(name, args)
    if problems:
        return json.dumps({"error": f"Invalid arguments for {name}: " + "; ".join(problems)})
    try:
        return json.dumps(FUNCTIONS[name](**args), default=str)[:6000]
    except ToolError as e:
        return json.dumps({"error": str(e)})
    except Exception as e:  # unexpected bug: still tell the model something useful
        return json.dumps({"error": f"{type(e).__name__}: {e}"})
