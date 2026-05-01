from dataclasses import dataclass, asdict


@dataclass
class AnalysisResult:
    key: str
    bpm: int
    chords: dict[str, list[str]]  # categories: major, minor, diminished, seventh, sus

    def to_dict(self) -> dict:
        return asdict(self)
