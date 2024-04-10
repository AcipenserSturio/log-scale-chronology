import csv
from dataclasses import dataclass, field
from pathlib import Path

from .date import Date


class Taxonomy:
    def __init__(self):
        self.taxa = {}

    def register(self, path: Path):
        with open(path) as f:
            data = csv.reader(f)
            colloq, _ = next(data)
            prev_taxon, prev_mya = next(data)
            self.add_taxon(prev_taxon, Date(f"{prev_mya} mya"), None)
            for taxon, mya in data:
                self.add_taxon(taxon, Date(f"{mya} mya"), prev_taxon)
                prev_taxon, prev_mya = taxon, mya
            self.add_taxon(colloq, Date(f"0.8 mya"), prev_taxon)

    def add_taxon(self, name: str, date: Date, parent: str | None):
        if name in self.taxa:
            return
        taxon = Taxon(name=name, date=date)
        self.taxa[name] = taxon
        if parent:
            self.taxa[parent].children.append(taxon)


@dataclass
class Taxon:
    name: str
    date: Date
    children: list = field(default_factory=list)

    @property
    def size(self) -> int:
        if self.children:
            return sum([child.size for child in self.children])
        return 1

    @property
    def branches(self):
        return list(sorted(self.children, key=lambda child: child.size, reverse=True))
