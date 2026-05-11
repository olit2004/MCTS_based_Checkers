from dataclasses import dataclass, field


@dataclass
class Move:
    start: tuple
    end: tuple
    captures: list = field(default_factory=list)

    def to_dict(self):
        return {
            "from": self.start,
            "to": self.end,
            "captures": self.captures
        }