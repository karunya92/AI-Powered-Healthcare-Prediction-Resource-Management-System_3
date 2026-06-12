from dataclasses import dataclass


@dataclass
class Resource:
    resource_id: int = None
    resource_name: str = ""
    quantity: int = 0
    available: int = 0

    def to_dict(self):
        return {
            "resource_id": self.resource_id,
            "resource_name": self.resource_name,
            "quantity": self.quantity,
            "available": self.available
        }


@dataclass
class Bed:
    bed_id: int = None
    ward_name: str = ""
    bed_number: str = ""
    status: str = "Available"

    def to_dict(self):
        return {
            "bed_id": self.bed_id,
            "ward_name": self.ward_name,
            "bed_number": self.bed_number,
            "status": self.status
        }


@dataclass
class Staff:
    staff_id: int = None
    name: str = ""
    role: str = ""
    shift: str = ""

    def to_dict(self):
        return {
            "staff_id": self.staff_id,
            "name": self.name,
            "role": self.role,
            "shift": self.shift
        }