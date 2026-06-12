from dataclasses import dataclass


@dataclass
class Doctor:
    doctor_id: int = None
    doctor_name: str = ""
    specialization: str = ""
    experience: int = 0
    phone: str = ""
    email: str = ""

    def to_dict(self):
        return {
            "doctor_id": self.doctor_id,
            "doctor_name": self.doctor_name,
            "specialization": self.specialization,
            "experience": self.experience,
            "phone": self.phone,
            "email": self.email
        }