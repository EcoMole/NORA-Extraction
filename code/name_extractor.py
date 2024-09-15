import re

class NameExtractor:

    def __init__(self, title, mandate):
        self.title = title
        self.mandate = mandate
        self.nf_name = ''

    def extract_nf_name(self):
        title = self.title
        mandate = self.mandate

        # Convert specific words to lowercase
        title = self._lowercase_specific_words(title)

        # Extract NF name based on mandate
        nf_name = ''
        if mandate == "extension of use":
            nf_name = self._extract_for_extension_of_use(title)
        elif mandate == "traditional food":
            nf_name = self._extract_for_traditional_food(title)
        else:
            nf_name = self._extract_for_other_mandates(title)

        # Store the result in the dossier
        self.nf_name = nf_name.strip()
        return self.nf_name

    def _lowercase_specific_words(self, title):
        to_lower = ['Novel', 'Food', 'Notification', 'Safety', 'Extension', 'Opinion']
        for word in to_lower:
            title = title.replace(word, word.lower())
        return title.replace(' a ', ' ')

    def _extract_for_extension_of_use(self, title):
        patterns = [
            r"extension of use of (.*?) as novel",
            r"safety of (.*?) for extended use.*? as novel",
            r"safety of (.*?) as novel"
        ]
        return self._regex_match(title, patterns)

    def _extract_for_traditional_food(self, title):
        pattern = r"notification of (.*?) as traditional"
        return self._regex_match(title, [pattern])

    def _extract_for_other_mandates(self, title):
        patterns = [
            r"safety of (.*?) for its use",
            r"safety of (.*?) ‐ Scientific Opinion",
            r"safety of (.*?) as food",
            r"safety of (.*?) for use in food",
            r"safety of (.*?) as novel",
            r"opinion on (.*?) as novel"
        ]
        return self._regex_match(title, patterns)

    def _regex_match(self, text, patterns):
        """
        Tries to match a list of regex patterns on the given text and returns
        the first match found, or an empty string if no match is found.
        """
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1)
        return ""