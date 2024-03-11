from dataclasses import dataclass

@dataclass
class ProcDTO:
    pid: int
    cam_name: str
    type_: str