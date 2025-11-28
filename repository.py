# repository.py
from db_connection import get_conn
from models import Satellite, Zone, Assignment, LogEntry
from typing import List, Optional
import json
from datetime import datetime

# ---------- SATELLITES ----------
def create_satellite(name: str, status: str='operativo', orbit_params: Optional[dict]=None, available: bool=True) -> int:
    conn = get_conn()
    try:
        cur = conn.cursor()
        orbit_json = json.dumps(orbit_params) if orbit_params is not None else None
        cur.execute("""
            INSERT INTO satellites (name, status, orbit_params, available)
            VALUES (%s,%s,%s,%s)
        """, (name, status, orbit_json, available))
        conn.commit()
        return cur.lastrowid
    finally:
        conn.close()

def get_all_satellites() -> List[Satellite]:
    conn = get_conn()
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM satellites ORDER BY id;")
        rows = cur.fetchall()
        res = []
        for r in rows:
            res.append(Satellite(r['id'], r['name'], r['status'], r['last_telemetry'], r.get('orbit_params'), bool(r['available'])))
        return res
    finally:
        conn.close()

def update_satellite(sat_id:int, **fields) -> None:
    if not fields:
        return
    conn = get_conn()
    try:
        cur = conn.cursor()
        parts = []
        vals = []
        for k,v in fields.items():
            parts.append(f"{k}=%s")
            vals.append(v)
        vals.append(sat_id)
        sql = "UPDATE satellites SET " + ", ".join(parts) + " WHERE id=%s"
        cur.execute(sql, tuple(vals))
        conn.commit()
    finally:
        conn.close()

def delete_satellite(sat_id:int) -> None:
    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM satellites WHERE id=%s", (sat_id,))
        conn.commit()
    finally:
        conn.close()

# ---------- ZONES ----------
def create_zone(name:str, polygon_geo:Optional[str]=None, priority:str='MEDIO', restricted:bool=False) -> int:
    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO zones (name, polygon_geo, priority, restricted)
            VALUES (%s,%s,%s,%s)
        """, (name, polygon_geo, priority, restricted))
        conn.commit()
        return cur.lastrowid
    finally:
        conn.close()

def get_all_zones() -> List[Zone]:
    conn = get_conn()
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM zones ORDER BY id;")
        rows = cur.fetchall()
        res = []
        for r in rows:
            res.append(Zone(r['id'], r['name'], r['polygon_geo'], r['priority'], bool(r['restricted'])))
        return res
    finally:
        conn.close()

def update_zone(zone_id:int, **fields) -> None:
    if not fields:
        return
    conn = get_conn()
    try:
        cur = conn.cursor()
        parts = []
        vals = []
        for k,v in fields.items():
            parts.append(f"{k}=%s")
            vals.append(v)
        vals.append(zone_id)
        sql = "UPDATE zones SET " + ", ".join(parts) + " WHERE id=%s"
        cur.execute(sql, tuple(vals))
        conn.commit()
    finally:
        conn.close()

def delete_zone(zone_id:int) -> None:
    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM zones WHERE id=%s", (zone_id,))
        conn.commit()
    finally:
        conn.close()

# ---------- ASSIGNMENTS ----------
def create_assignment(satellite_id:int, zone_id:int, frequency_minutes:int=60, assigned_by:Optional[int]=None) -> int:
    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO assignments (satellite_id, zone_id, frequency_minutes, assigned_by)
            VALUES (%s,%s,%s,%s)
        """, (satellite_id, zone_id, frequency_minutes, assigned_by))
        conn.commit()
        return cur.lastrowid
    finally:
        conn.close()

def get_all_assignments() -> List[Assignment]:
    conn = get_conn()
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM assignments ORDER BY id;")
        rows = cur.fetchall()
        res = []
        for r in rows:
            res.append(Assignment(r['id'], r['satellite_id'], r['zone_id'], r['frequency_minutes'], r['status'], r['assigned_by'], r['assigned_at']))
        return res
    finally:
        conn.close()

def update_assignment(assign_id:int, **fields) -> None:
    if not fields:
        return
    conn = get_conn()
    try:
        cur = conn.cursor()
        parts = []
        vals = []
        for k,v in fields.items():
            parts.append(f"{k}=%s")
            vals.append(v)
        vals.append(assign_id)
        sql = "UPDATE assignments SET " + ", ".join(parts) + " WHERE id=%s"
        cur.execute(sql, tuple(vals))
        conn.commit()
    finally:
        conn.close()

def delete_assignment(assign_id:int) -> None:
    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM assignments WHERE id=%s", (assign_id,))
        conn.commit()
    finally:
        conn.close()

# ---------- LOGS ----------
def create_log(event_type:str, details:str, created_by:Optional[int]=None) -> int:
    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO logs (event_type, details, created_by) VALUES (%s,%s,%s)",
                    (event_type, details, created_by))
        conn.commit()
        return cur.lastrowid
    finally:
        conn.close()

def get_logs(limit:int=100):
    conn = get_conn()
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM logs ORDER BY created_at DESC LIMIT %s", (limit,))
        return cur.fetchall()
    finally:
        conn.close()