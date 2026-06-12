from dataclasses import dataclass


@dataclass
class Patient:
    patient_id: int = None
    full_name: str = ""
    age: int = 0
    gender: str = ""
    blood_group: str = ""
    phone: str = ""
    address: str = ""
    insurance_id: str = ""

    def to_dict(self):
        return {
            "patient_id": self.patient_id,
            "full_name": self.full_name,
            "age": self.age,
            "gender": self.gender,
            "blood_group": self.blood_group,
            "phone": self.phone,
            "address": self.address,
            "insurance_id": self.insurance_id
        }