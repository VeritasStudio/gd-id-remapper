# modules/xml.py
import xml.etree.ElementTree as eTree


def xml_parse_level(string: str) -> str:
    tree = eTree.fromstring(string)
    level = tree.findall('./s')

    return level[2].text
