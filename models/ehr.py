from dataclasses import dataclass


@dataclass
class EHR:
    record_id: int = None
    patient_id: int = None
    diagnosis: str = ""
    treatment: str = ""
    prescription: str = ""
    report_date: str = ""

    def to_dict(self):
        return {
            "record_id": self.record_id,
            "patient_id": self.patient_id,
            "diagnosis": self.diagnosis,
            "treatment": self.treatment,
            "prescription": self.prescription,
            "report_date": self.report_date
        }