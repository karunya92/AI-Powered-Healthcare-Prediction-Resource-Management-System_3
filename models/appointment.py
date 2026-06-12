from dataclasses import dataclass


@dataclass
class Appointment:
    appointment_id: int = None
    patient_id: int = None
    doctor_id: int = None
    appointment_date: str = ""
    status: str = "Pending"

    def to_dict(self):
        return {
            "appointment_id": self.appointment_id,
            "patient_id": self.patient_id,
            "doctor_id": self.doctor_id,
            "appointment_date": self.appointment_date,
            "status": self.status
        }