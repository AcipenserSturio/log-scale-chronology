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
            self.rename_taxon(taxon, colloq)
            # self.add_taxon(colloq, Date(f"5 mya"), prev_taxon)

    def add_taxon(self, name: str, date: Date, parent: str | None):
        if name in self.taxa:
            return
        taxon = Taxon(name=name, date=date)
        self.taxa[name] = taxon
        if parent:
            self.taxa[parent].children.append(taxon)

    def rename_taxon(self, old_name: str, new_name: str):
        taxon = self.taxa[old_name]
        del self.taxa[old_name]
        taxon.name = new_name
        self.taxa[new_name] = taxon

    @property
    def root(self):
        return self.taxa["cellular_organisms"]

@dataclass
class Taxon:
    name: str
    date: Date
    children: list = field(default_factory=list)
    _x: int = field(init=False)

    @property
    def size(self) -> int:
        if self.children:
            return sum([child.size for child in self.children])
        return 1

    @property
    def branches(self):
        return list(sorted(self.children, key=lambda child: child.size, reverse=True))
        # return self.children

    @property
    def leaf(self) -> "Taxon":
        if self.children:
            return self.branches[0].leaf
        return self

    @property
    def is_leaf(self) -> bool:
        return not self.children

    # def count_leaves(self, leaves_found: int) -> int:
    #     if len(self.children) == 0:
    #         self._leaf_index = leaves_found
    #         print("Leaf", self._leaf_index, self.name, sep="\t")
    #         return 1
    #
    #     if len(self.children) == 1:
    #         leaves_found = self.children[0].count_leaves(leaves_found)
    #         print("Dot", leaves_found, self.name, sep="\t")
    #         return leaves_found
    #
    #     for child in self.branches:
    #         leaves_found += child.count_leaves(leaves_found)
    #     print("Branch", leaves_found, self.name, sep="\t")
    #     return leaves_found

    def set_leaf_x(self, x: int) -> int:
        if self.is_leaf:
            self._x = x
            return x + 1
        for child in self.branches:
            x = child.set_leaf_x(x)
        return x

    @property
    def x(self) -> int | float:
        if self.children:
            children_x = [child.x for child in self.children]
            return (children_x[0] + children_x[-1]) / 2
        return self._x
