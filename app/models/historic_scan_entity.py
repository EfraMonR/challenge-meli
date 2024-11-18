import json
from datetime import datetime

class HistoricScanEntity:
    def __init__(self, date_scan: str, classification: str, id_database: int, deleted: int, user_id: int, id: int = None):
        self.id = id
        
        if isinstance(date_scan, str):
            self.date_scan = datetime.strptime(date_scan, '%Y-%m-%d %H:%M:%S')
        elif isinstance(date_scan, datetime):
            self.date_scan = date_scan
        else:
            raise ValueError("date_scan must be a string or datetime object")
        
        if isinstance(classification, str):
            self.classification = classification
        else:
            self.classification = json.dumps(classification)
            
        self.id_database = id_database
        self.deleted = deleted
        self.user_id = user_id
        