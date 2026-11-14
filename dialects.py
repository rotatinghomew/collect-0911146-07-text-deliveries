from dataclasses import dataclass


@dataclass(frozen=True)
class SourceProfile:
    source: str
    encoding: str
    delimiter: str
    version: int


PROFILES = {
    'east': SourceProfile('east', 'utf-8-sig', ',', 1),
    'west': SourceProfile('west', 'gb18030', ';', 2),
}


def profile(source):
    if source not in PROFILES:
        raise ValueError('来源尚无确认规则')
    return PROFILES[source]
