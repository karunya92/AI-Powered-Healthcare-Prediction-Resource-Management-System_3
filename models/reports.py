from dataclasses import dataclass


@dataclass
class MedicalReport:
    report_id: int = None
    patient_id: int = None
    report_type: str = ""
    report_file: str = ""
    upload_date: str = ""

    def to_dict(self):
        return {
            "report_id": self.report_id,
            "patient_id": self.patient_id,
            "report_type": self.report_type,
            "report_file": self.report_file,
            "upload_date": self.upload_date
        }


@dataclass
class DiseasePrediction:
    prediction_id: int = None
    patient_id: int = None
    disease: str = ""
    prediction_result: str = ""
    probability: float = 0.0

    def to_dict(self):
        return {
            "prediction_id": self.prediction_id,
            "patient_id": self.patient_id,
            "disease": self.disease,
            "prediction_result": self.prediction_result,
            "probability": self.probability
        }