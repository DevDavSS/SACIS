# models.py
from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class User:
    id: Optional[int]
    username: str
    password_hash: str
    role: str
    created_at: Optional[datetime] = None

@dataclass
class Satellite:
    id: Optional[int]
    name: str
    status: str
    last_telemetry: Optional[datetime]
    orbit_params: Optional[str]
    available: bool

@dataclass
class Zone:
    id: Optional[int]
    name: str
    polygon_geo: Optional[str]
    priority: str
    restricted: bool

@dataclass
class Assignment:
    id: Optional[int]
    satellite_id: int
    zone_id: int
    frequency_minutes: int
    status: str
    assigned_by: Optional[int]
    assigned_at: Optional[datetime] = None

@dataclass
class LogEntry:
    id: Optional[int]
    event_type: str
    details: str
    created_by: Optional[int]
    created_at: Optional[datetime] = None