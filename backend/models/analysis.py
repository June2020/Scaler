from dataclasses import dataclass, asdict


@dataclass
class AnalysisResult:
    key: str
    bpm: int
    chords: list[str]

    def to_dict(self) -> dict:
        return asdict(self)
