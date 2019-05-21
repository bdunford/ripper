import re


class Helpers(object):

    @staticmethod
    def find_with_regex(source,patterns):
        references = []
        for p in patterns:
            matches = re.findall(p,source)
            if matches and len(matches):
                references += matches
        return list(references)
