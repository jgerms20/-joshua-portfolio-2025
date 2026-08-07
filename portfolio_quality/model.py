from dataclasses import asdict, dataclass


@dataclass(frozen=True, slots=True)
class Finding:
    severity: str
    code: str
    page: str
    target: str
    message: str


@dataclass(slots=True)
class HealthReport:
    findings: list[Finding]

    @property
    def has_critical(self) -> bool:
        return any(item.severity == "broken" for item in self.findings)

    def exit_code(self) -> int:
        return int(self.has_critical)

    def to_dict(self) -> dict[str, object]:
        return {
            "ok": not self.has_critical,
            "findings": [asdict(item) for item in self.findings],
        }
