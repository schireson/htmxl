import importlib
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass(frozen=True)
class TokenStream:
    node: Any
    name: str
    attrs: Dict[str, str] = field(default_factory=dict)
    classes: Optional[List[str]] = None
    text: str = ""

    @classmethod
    def from_node(cls, node):
        """Produce a `TokenStream` node from a tree node produced by the specific parser."""

    @classmethod
    def parse_str(cls, data: str):
        """Parse a raw string representing a template into a `TokenStream`."""

    def content(self):
        """Yield the next token."""

    def get(self, name: str, default: Any):
        """Get a `TokenStream`'s HTML attribute."""
        return self.attrs.get(name, default)


@dataclass(frozen=True)
class Bs4Stream(TokenStream):
    @classmethod
    def parse_str(cls, data: str):
        import bs4

        node = bs4.BeautifulSoup(data, features="html.parser")
        return cls.from_node(node)

    @classmethod
    def from_node(cls, node):

        if node.name == "[document]":
            return cls(node=node, name="body")

        classes = node.attrs.get("class", [])

        return cls(
            node=node,
            name=node.name,
            attrs=node.attrs,
            text=node.text,
            classes=classes,
        )

    def content(self):
        import bs4.element

        for node in self.node:
            if isinstance(node, bs4.element.NavigableString):
                text = node.strip()
                if text:
                    yield self.__class__(None, "string", text=text)
            else:
                yield self.from_node(node)


@dataclass(frozen=True)
class LxmlStream(TokenStream):
    @classmethod
    def parse_str(cls, data: str):
        from lxml import etree

        parser = etree.XMLParser(remove_blank_text=True)

        # Lxml requires a single top-level node.
        data = f"<root>{data}</root>"
        node = etree.XML(data, parser)
        return cls.from_node(node)

    @classmethod
    def from_node(cls, node):
        classes = node.attrib.get("class")
        if classes:
            # lxml represents classes as a string. We need a list.
            # eg <div class="some-class some-other-class">
            #  node.attrib.get("class") = "some-class some-other-class"
            classes = classes.strip().split(" ")

        return cls(node=node, name=node.tag, attrs=node.attrib, text=node.text, classes=classes)

    def content(self):
        for node in self.node.iterchildren():
            if node.text:
                text = node.text.strip()
                yield self.__class__(None, "string", text=text)

            yield self.__class__.from_node(node)

            if node.tail:
                text = node.tail.strip()
                yield self.__class__(None, "string", text=text)


_parsers_by_name = {
    "lxml": LxmlStream,
    "beautifulsoup": Bs4Stream,
}

_parser_fallback = [("bs4", "beautifulsoup"), ("lxml", "lxml")]


def get_parser(name: Optional[str]) -> TokenStream:
    if name is None:
        for import_name, parser_name in _parser_fallback:
            try:
                importlib.import_module(import_name)
            except ImportError:
                pass
            else:
                name = parser_name
                break
        else:
            parser_options = ", ".join(_parsers_by_name)
            raise RuntimeError(
                "Failed to find an available parser library. Please use one of the"
                f"provided package extras to install supported parser: {parser_options}."
            )

    return _parsers_by_name[name]
