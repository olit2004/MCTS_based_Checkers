from dataclasses import dataclass, field

@dataclass
class Move:
    start: tuple
    end: tuple
    captures: list = field(default_factory=list)

    def to_dict(self):
        return {
            "from": list(self.start),
            "to": list(self.end),
            "captures": [list(c) for c in self.captures]

}