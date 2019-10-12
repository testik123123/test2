from lxml import etree


class Parser():
    def __init__(self):
        self.parser = etree.XMLParser(remove_comments=True)

    def parse_clothes(self):
        clothes = {"boy": {}, "girl": {}}
        for filename in ["boyClothes.xml", "girlClothes.xml"]:
            if filename == "boyClothes.xml":
                gender = "boy"
            else:
                gender = "girl"
            doc = etree.parse("config_all_ru/inventory/"+filename,
                              parser=self.parser)
            root = doc.getroot()
            for category in root.findall(".//category[@logCategory2]"):
                name = gender+category.attrib["logCategory2"][1:]
                clothes[gender][name] = self.parse_clothes_category(category)
        return clothes

    def parse_clothes_category(self, category):
        tmp = {}
        for item in category:
            if item.tag == "category":
                tmp.update(self.parse_clothes_category(item))
                continue
            name = item.attrib["id"]
            tmp[name] = {}
            for attr in ["gold", "rating", "silver"]:
                if attr in item.attrib:
                    tmp[name][attr] = int(item.attrib[attr])
                else:
                    tmp[name][attr] = 0
        return tmp

    def parse_furniture(self):
        furniture = {}
        for filename in ["furniture.xml", "kitchen.xml", "bathroom.xml",
                         "decor.xml", "present.xml", "roomLayout.xml"]:
            doc = etree.parse(f"config_all_ru/inventory/{filename}",
                              parser=self.parser)
            root = doc.getroot()
            for item in root.findall(".//item"):
                name = item.attrib["id"]
                furniture[name] = {}
                for attr in ["gold", "rating", "silver"]:
                    if attr in item.attrib:
                        furniture[name][attr] = int(item.attrib[attr])
                    else:
                        furniture[name][attr] = 0
        return furniture

    def parse_conflicts(self):
        doc = etree.parse("config_all_ru/inventory/extend/clothesRules.xml",
                          parser=self.parser)
        root = doc.getroot()
        conflicts = []
        for rule in root.findall(".//rule"):
            conflicts.append([rule.attrib["category1"],
                              rule.attrib["category2"]])
        return conflicts
