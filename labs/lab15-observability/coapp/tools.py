"""
Read-only tools over the Harbor PSA SQLite extract (Ch. 6 agents: tools).

TOOLS is the list of OpenAI tool schemas the model sees; call_tool(name, args)
runs one and returns a JSON string (or "ERROR: ..."), which goes back to the
model as the tool result. Every query is read-only, and all tools except
run_sql are parameterized.

These are not the five tools you built in Lab 9 (lookup_ticket, search_tickets,
get_client, list_assets, sla_target). Either set works with answer(). This set
adds broader lookups and run_sql, one read-only SELECT for counts and joins the
fixed tools can't do. That is a trade-off worth noticing: a general tool is more
flexible, but the model can misuse it more easily and it is harder to keep safe,
so run_sql accepts a single SELECT on a read-only connection and returns at
most 50 rows.
"""
import json
import sqlite3

from . import config

TOOLS = [
    {"type": "function", "function": {
        "name": "lookup_client",
        "description": "Find a Larkspur client by 3-letter code or part of its name. Returns tier, users, sites, contacts.",
        "parameters": {"type": "object", "properties": {
            "client": {"type": "string", "description": "Client code like EMS, or part of the name"}},
            "required": ["client"]}}},
    {"type": "function", "function": {
        "name": "list_clients",
        "description": "List clients, optionally only one service tier. Returns the count and codes/names.",
        "parameters": {"type": "object", "properties": {
            "tier": {"type": "string", "enum": ["Essentials", "Professional", "Premier"]}}}}},
    {"type": "function", "function": {
        "name": "query_tickets",
        "description": "Count and list support tickets with optional filters. Dates are YYYY-MM-DD.",
        "parameters": {"type": "object", "properties": {
            "client_code": {"type": "string"},
            "status": {"type": "string", "enum": ["open", "in_progress", "waiting_on_client", "closed", "not_closed"]},
            "category": {"type": "string", "description": "e.g. Hardware, Email/M365, Account/Access"},
            "priority": {"type": "string", "enum": ["P1", "P2", "P3", "P4"]},
            "created_after": {"type": "string"},
            "created_before": {"type": "string"},
            "limit": {"type": "integer", "minimum": 1, "maximum": 20}}}}},
    {"type": "function", "function": {
        "name": "query_assets",
        "description": "Count and list managed assets (laptops, servers, firewalls, ...) with optional filters.",
        "parameters": {"type": "object", "properties": {
            "client_code": {"type": "string"},
            "type": {"type": "string", "enum": ["laptop", "desktop", "server", "firewall", "switch",
                                                "access_point", "printer", "phone", "nas"]},
            "status": {"type": "string", "enum": ["active", "retired", "in_repair", "not_retired"]},
            "os_contains": {"type": "string", "description": "e.g. 'Windows 10'"},
            "limit": {"type": "integer", "minimum": 1, "maximum": 20}}}}},
    {"type": "function", "function": {
        "name": "list_technicians",
        "description": "List Larkspur technicians with role and tier level.",
        "parameters": {"type": "object", "properties": {
            "active_only": {"type": "boolean"}}}}},
    {"type": "function", "function": {
        "name": "run_sql",
        "description": (
            "Run ONE read-only SQLite SELECT on the Harbor PSA extract, for counts, averages, rankings and joins "
            "the other tools can't do. Tables: clients(code, name, tier, users, backup_included, has_voip, ...), "
            "contacts(contact_id, client_code, first_name, last_name, title, phone, is_authorized_contact, is_vip), "
            "technicians(tech_id, name, role, tier_level, active), "
            "assets(asset_tag, client_code, hostname, type, make, model, ram_gb, os, purchase_date, warranty_end, status), "
            "tickets(ticket_id, created_at, client_code, contact_id, channel, subject, category, subcategory, priority, "
            "status, assigned_tech_id, first_response_at, resolved_at, sla_response_met, csat, onsite, labor_minutes, asset_tag), "
            "sla_targets(tier, priority, response_minutes, resolution_business_minutes). Returns at most 50 rows."),
        "parameters": {"type": "object", "properties": {
            "query": {"type": "string", "description": "A single SELECT statement"}},
            "required": ["query"]}}},
]


def _con():
    con = sqlite3.connect(f"file:{config.db_path()}?mode=ro", uri=True, check_same_thread=False)
    con.row_factory = sqlite3.Row
    return con


def _rows(sql, params=()):
    with _con() as con:
        return [dict(r) for r in con.execute(sql, params).fetchall()]


def lookup_client(client: str = "") -> dict:
    c = (client or "").strip()
    rows = _rows("SELECT code, name, industry, city, tier, users, sites, client_since, backup_included, has_voip "
                 "FROM clients WHERE upper(code)=upper(?) OR lower(name) LIKE lower(?) LIMIT 5", (c, f"%{c}%"))
    for r in rows:
        r["contacts"] = _rows("SELECT first_name || ' ' || last_name AS name, title, is_authorized_contact "
                              "FROM contacts WHERE client_code=?", (r["code"],))
    return {"matches": len(rows), "clients": rows}


def list_clients(tier: str | None = None) -> dict:
    if tier:
        rows = _rows("SELECT code, name, tier FROM clients WHERE lower(tier)=lower(?) ORDER BY code", (tier,))
    else:
        rows = _rows("SELECT code, name, tier FROM clients ORDER BY code")
    return {"count": len(rows), "clients": rows}


def _where(filters):
    sql, params = [], []
    for clause, value in filters:
        if value not in (None, ""):
            sql.append(clause)
            params.append(value)
    return (" WHERE " + " AND ".join(sql)) if sql else "", params


def query_tickets(client_code=None, status=None, category=None, priority=None,
                  created_after=None, created_before=None, limit=10) -> dict:
    filters = [("upper(client_code)=upper(?)", client_code), ("lower(category)=lower(?)", category),
               ("priority=?", priority), ("created_at>=?", created_after), ("created_at<?", created_before)]
    where, params = _where(filters)
    if status == "not_closed":
        where += (" AND " if where else " WHERE ") + "status!='closed'"
    elif status:
        where += (" AND " if where else " WHERE ") + "status=?"
        params.append(status)
    count = _rows(f"SELECT count(*) AS n FROM tickets{where}", params)[0]["n"]
    rows = _rows(f"SELECT ticket_id, created_at, client_code, subject, category, priority, status "
                 f"FROM tickets{where} ORDER BY created_at DESC LIMIT ?", [*params, int(limit or 10)])
    return {"count": count, "tickets": rows}


def query_assets(client_code=None, type=None, status=None, os_contains=None, limit=10) -> dict:
    filters = [("upper(client_code)=upper(?)", client_code), ("type=?", type),
               ("os LIKE ?", f"%{os_contains}%" if os_contains else None)]
    where, params = _where(filters)
    if status == "not_retired":
        where += (" AND " if where else " WHERE ") + "status!='retired'"
    elif status:
        where += (" AND " if where else " WHERE ") + "status=?"
        params.append(status)
    count = _rows(f"SELECT count(*) AS n FROM assets{where}", params)[0]["n"]
    rows = _rows(f"SELECT asset_tag, client_code, hostname, type, model, os, status, warranty_end "
                 f"FROM assets{where} ORDER BY asset_tag LIMIT ?", [*params, int(limit or 10)])
    return {"count": count, "assets": rows}


def list_technicians(active_only: bool = True) -> dict:
    sql = "SELECT tech_id, name, role, tier_level, active FROM technicians"
    rows = _rows(sql + (" WHERE active=1" if active_only else "") + " ORDER BY tech_id")
    return {"count": len(rows), "technicians": rows}


def run_sql(query: str = "") -> dict:
    """One read-only SELECT (the connection is opened read-only too). At most 50 rows."""
    q = (query or "").strip().rstrip(";")
    if not q.lower().startswith(("select", "with")) or ";" in q:
        raise ValueError("only a single SELECT statement is allowed")
    with _con() as con:
        cur = con.execute(q)
        cols = [d[0] for d in cur.description or []]
        rows = [dict(zip(cols, r)) for r in cur.fetchmany(50)]
    return {"columns": cols, "rows": rows, "row_count_returned": len(rows)}


_FUNCS = {"lookup_client": lookup_client, "list_clients": list_clients, "query_tickets": query_tickets,
          "query_assets": query_assets, "list_technicians": list_technicians, "run_sql": run_sql}


def call_tool(name: str, args: dict) -> str:
    """Run a tool by name. Always returns a string (JSON result or 'ERROR: ...')."""
    fn = _FUNCS.get(name)
    if fn is None:
        return f"ERROR: unknown tool {name!r}. Available: {sorted(_FUNCS)}"
    try:
        return json.dumps(fn(**(args or {})), default=str)[:6000]
    except TypeError as e:
        return f"ERROR: bad arguments for {name}: {e}"
    except Exception as e:
        return f"ERROR: {type(e).__name__}: {e}"
