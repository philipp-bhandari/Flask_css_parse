import re
import urllib
import cssutils
import logging
cssutils.log.setLevel(logging.CRITICAL)


class CSSParser:
    def __init__(self, path):

        with open('file.css', 'w', encoding='utf-8') as file:
            text = urllib.request.urlopen(path).read().decode('utf-8')
            file.write(text)
        path = 'file.css'

        self.parser = cssutils.CSSParser()
        self.stylesheet = self.parser.parseFile(path)

        self.STYLE = 'STYLE_RULE'
        self.MEDIA = 'MEDIA_RULE'
        self.UNKNOWN = 'UNKNOWN_RULE'
        self.OTHER = 'OTHER_RULE'

        self.all_rules_dict = self.parcelling(self.stylesheet)
        try:
            self.media_selectors = self.get_media_selectors(self.all_rules_dict[self.MEDIA])
            self.media_rules_dict = self.create_media_rules_dict(self.media_selectors)
        except KeyError:
            self.media_selectors = []
            self.media_rules_dict = {}

    def parse_help(self, rule, rule_type, rule_dict):
        if rule_type not in [self.STYLE, self.MEDIA, self.UNKNOWN]:
            rule_type = self.OTHER
        try:
            rule_dict[rule_type].append(rule)
        except KeyError:
            rule_dict[rule_type] = []
            rule_dict[rule_type].append(rule)
        return rule_dict

    def parcelling(self, sheet):
        # spreading css rules

        rule_dict = {}
        for rule in sheet.cssRules:
            rule_type = rule.typeString
            rule_dict = self.parse_help(rule, rule_type, rule_dict)
        return rule_dict

    def get_media_selectors(self, media_rules):
        # get a list of uniq media selectors

        media_selectors = []
        for rule in media_rules:
            media_selectors.append(rule.media.mediaText)
        media_selectors = list(set(media_selectors))
        return media_selectors

    def create_media_rules_dict(self, media_selectors):
        # make a dict with keys - media-rules, values - lists with rules

        media_rules_dict = {}
        media_rules = self.all_rules_dict[self.MEDIA]
        for selector in media_selectors:
            for rule in media_rules:
                if selector == rule.media.mediaText:
                    try:
                        for item in rule:
                            media_rules_dict[selector].append(item)
                    except KeyError:
                        media_rules_dict[selector] = []
                        for item in rule:
                            media_rules_dict[selector].append(item)
        return media_rules_dict

    def search_selector(self, selector):
        style_rules = self.all_rules_dict[self.STYLE]
        find_style_rules = []
        find_media_rules = {}
        for rule in style_rules:
            result = re.search(selector, rule.selectorText)
            if result:
                find_style_rules.append(rule)
        for rule_name in self.media_rules_dict:
            for rule in self.media_rules_dict[rule_name]:
                result = re.search(selector, rule.selectorText)
                if result:
                    try:
                        find_media_rules[rule_name].append(rule)
                    except KeyError:
                        find_media_rules[rule_name] = []
                        find_media_rules[rule_name].append(rule)

        return find_style_rules, find_media_rules


if __name__ == '__main__':
    pass
    # test = CSSParser('https://get-x.ru/css/style.css')
    # styles = test.search_selector('.wr1 .block .content')
    #




