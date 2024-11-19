import json
from datetime import datetime
from app.models.historic_scan_entity import HistoricScanEntity

class ResponseGetClassification:
    def __init__(self, id: int, date_scan: datetime, classification: dict, id_database: int, deleted: int):
        self.id = id
        self.date_scan = date_scan
        self.classification = classification
        self.id_database = id_database
        self.deleted = deleted
        
    @classmethod
    def from_entity(cls, entity: HistoricScanEntity):
        classification = json.loads(entity.classification) if entity.classification else {}
        
        return cls(
            id_database = entity.id_database,
            id = entity.id,
            date_scan = entity.date_scan,
            classification = classification,
            deleted = entity.deleted
        )