from dataclasses import dataclass, field

from jinja2 import Template


@dataclass
class SlackMessage:
    query: str
    place_holder: dict = field(default_factory=dict)

    def format(self):
        return Template(self.query).render(self.place_holder)

    @classmethod
    def from_file(cls, query_path, place_holder={}):
        with open(query_path) as fin:
            query = fin.read()

        return cls(query=query, place_holder=place_holder)
