from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel

# --------------------------
# Enums
# --------------------------
class BikeType(Enum):
    ROUTE = "ROUTE"
    VILLE = "VILLE"
    ELECTRIQUE = "ELECTRIQUE"
    VTT = "VTT"

class StatusLabel(Enum):
    DEVIS = "DEVIS"
    RENOVATION = "RENOVATION"
    ANNONCE = "ANNONCE"
    VENDU = "VENDU"

# --------------------------
# Classes
# --------------------------
class Prix(BaseModel):
    achat: float
    potentiel: Optional[float] = None
    annonce: Optional[float] = None
    vendu: Optional[float] = None

class BikeStatus(BaseModel):
    status: StatusLabel
    date: datetime

class Service(BaseModel):
    category: str
    label: str
    temps_estim: int
    temps_reel: Optional[int] = None

class Piece(BaseModel):
    label: str
    prix_estim: float
    qt_estim: int
    prix_reel: Optional[float] = None
    qt_reel: Optional[int] = None

class Bike(BaseModel):
    id: str
    type: BikeType
    label: str
    prix: Prix
    status: List[BikeStatus] = field(default_factory=list)
    services: List[Service] = field(default_factory=list)
    pieces: List[Piece] = field(default_factory=list)

    def print(self):
        print(f"Bike {self.id}: '{self.label}' {self.type} - {self.prix}")

# --------------------------
# Helper to create datetime like Kotlin calendar
# --------------------------
def make_date(year, month, day, hour=0, minute=0, second=0):
    # Note: month in Python is 1-based (Jan=1), Kotlin Calendar.APRIL=3
    return datetime(year, month, day, hour, minute, second)

# --------------------------
# 5 Bike instances
# --------------------------
bikes = [
    Bike(
        id="0",
        type=BikeType.ROUTE,
        label="Bike label 0",
        prix=Prix(achat=1000.0, potentiel=1200.0),
        status=[BikeStatus(status=StatusLabel.DEVIS, date=make_date(2024, 4, 26))],
        services=[
            Service(category="Démontage", label="Complet", temps_estim=60),
            Service(category="Nettoyage", label="Complet", temps_estim=360),
            Service(category="Montage", label="Complet", temps_estim=60),
            Service(category="Réglage", label="Complet", temps_estim=60),
        ],
        pieces=[
            Piece(label="Guidoline", prix_estim=15.0, qt_estim=1),
            Piece(label="Patins", prix_estim=10.0, qt_estim=2),
        ],
    ),
    Bike(
        id="1",
        type=BikeType.VILLE,
        label="Bike label 1",
        prix=Prix(achat=100.0, potentiel=200.0),
        status=[
            BikeStatus(status=StatusLabel.DEVIS, date=make_date(2024, 4, 26)),
            BikeStatus(status=StatusLabel.RENOVATION, date=make_date(2024, 4, 27)),
        ],
        services=[
            Service(category="Démontage", label="Complet", temps_estim=60, temps_reel=30),
            Service(category="Nettoyage", label="Complet", temps_estim=360, temps_reel=460),
            Service(category="Montage", label="Complet", temps_estim=60, temps_reel=60),
            Service(category="Réglage", label="Complet", temps_estim=60, temps_reel=90),
        ],
        pieces=[
            Piece(label="Guidoline", prix_estim=15.0, qt_estim=1, prix_reel=30.0, qt_reel=1),
            Piece(label="Patins", prix_estim=10.0, qt_estim=2),
        ],
    ),
    Bike(
        id="2",
        type=BikeType.ELECTRIQUE,
        label="Bike label 2",
        prix=Prix(achat=100.0, potentiel=200.0, annonce=250.0, vendu=220.0),
        status=[
            BikeStatus(status=StatusLabel.DEVIS, date=make_date(2024, 4, 26)),
            BikeStatus(status=StatusLabel.RENOVATION, date=make_date(2024, 4, 27)),
            BikeStatus(status=StatusLabel.ANNONCE, date=make_date(2024, 4, 28, 11, 6)),
            BikeStatus(status=StatusLabel.VENDU, date=make_date(2024, 4, 29, 10, 3, 6)),
        ],
        services=[
            Service(category="Démontage", label="Complet", temps_estim=60, temps_reel=10),
            Service(category="Nettoyage", label="Complet", temps_estim=360, temps_reel=10),
            Service(category="Montage", label="Complet", temps_estim=60, temps_reel=10),
            Service(category="Réglage", label="Complet", temps_estim=60, temps_reel=10),
        ],
        pieces=[
            Piece(label="Guidoline", prix_estim=15.0, qt_estim=1, prix_reel=30.0, qt_reel=1),
            Piece(label="Patins", prix_estim=10.0, qt_estim=2),
        ],
    ),
    Bike(
        id="3",
        type=BikeType.VTT,
        label="Bike label 3",
        prix=Prix(achat=100.0, potentiel=200.0, annonce=250.0, vendu=220.0),
        status=[
            BikeStatus(status=StatusLabel.DEVIS, date=make_date(2024, 4, 26)),
            BikeStatus(status=StatusLabel.RENOVATION, date=make_date(2024, 4, 27)),
            BikeStatus(status=StatusLabel.ANNONCE, date=make_date(2024, 4, 28, 11, 6)),
            BikeStatus(status=StatusLabel.VENDU, date=make_date(2024, 4, 29, 10, 3, 6)),
        ],
        services=[
            Service(category="Démontage", label="Complet", temps_estim=60, temps_reel=10),
            Service(category="Nettoyage", label="Complet", temps_estim=360, temps_reel=10),
            Service(category="Montage", label="Complet", temps_estim=60, temps_reel=10),
            Service(category="Réglage", label="Complet", temps_estim=60, temps_reel=10),
        ],
        pieces=[
            Piece(label="Guidoline", prix_estim=15.0, qt_estim=1, prix_reel=30.0, qt_reel=1),
            Piece(label="Patins", prix_estim=10.0, qt_estim=2),
        ],
    ),
    Bike(
        id="4",
        type=BikeType.VTT,
        label="Bike label 4",
        prix=Prix(achat=100.0, potentiel=200.0, annonce=250.0),
        status=[
            BikeStatus(status=StatusLabel.DEVIS, date=make_date(2024, 4, 26)),
            BikeStatus(status=StatusLabel.RENOVATION, date=make_date(2024, 4, 27)),
            BikeStatus(status=StatusLabel.ANNONCE, date=make_date(2024, 4, 28, 11, 6)),
        ],
        services=[
            Service(category="Démontage", label="Complet", temps_estim=60, temps_reel=30),
            Service(category="Nettoyage", label="Complet", temps_estim=360, temps_reel=460),
            Service(category="Montage", label="Complet", temps_estim=60, temps_reel=60),
            Service(category="Montage", label="Guidoline", temps_estim=15, temps_reel=20),
            Service(category="Réglage", label="Complet", temps_estim=60, temps_reel=90),
        ],
        pieces=[
            Piece(label="Guidoline", prix_estim=15.0, qt_estim=1, prix_reel=30.0, qt_reel=1),
            Piece(label="Patins", prix_estim=10.0, qt_estim=2),
        ],
    ),
]