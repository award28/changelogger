from dataclasses import dataclass


@dataclass
class ContentRequest:
    version: str


def content(
    version: str,
) -> None:
    """Retrieves the changelog content for the specified version.
    """
    req = ContentRequest(
        version=version,
    )
    _content(req)

def _content(req: ContentRequest) -> None:
    print(req)
