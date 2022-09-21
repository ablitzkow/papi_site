import xml.etree.ElementTree as ET

tree = ET.parse('sitemap.xml')
root = tree.getroot()

a = root.find('url')
b = ET.SubElement(a, 'loc')

print(b.text)


