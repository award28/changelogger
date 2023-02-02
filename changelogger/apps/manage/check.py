from dataclasses import dataclass

@dataclass
class CheckRequest:
    ...


def check() -> None:
    """Validates the specified versioned files are parsable and updatable.
    """
    req = CheckRequest()
    _check(req)

def _check(req: CheckRequest) -> None:
    print(req)
