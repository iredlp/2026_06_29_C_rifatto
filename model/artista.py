from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Set

@dataclass
class Artista:
    ArtistId: int
    Name: str


    list_brani: list = field(default_factory=list)
    list_playlist: list = field(default_factory=list)
    #popolarita: int=0

    def __hash__(self):
        return hash(self. ArtistId)

    def __eq__(self, other):
        if isinstance(other, Artista):
            return self. ArtistId == other. ArtistId
        return False

    def __repr__(self):
        return (f"{self.Name}  ({self. ArtistId if self. ArtistId is not None else 'N/D'})")