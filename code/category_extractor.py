from data_store import DataStore


class CategoryExtractionStrategy:
    def __init__(self):
        self.tei_namespaces = {"tei": "http://www.tei-c.org/ns/1.0"}
        self.Datastore = DataStore()

    def find_relevant_paragraphs(self, body):
        raise NotImplementedError

    def extract(self, body):
        relevant_divs = self.find_relevant_paragraphs(body)
        if not relevant_divs:
            return
        return self.extract_from_divs(relevant_divs)
    
    def extract_from_divs(self, relevant_divs):
        categories = []
        regulations = []
        for p in relevant_divs:
            for s in p:
                if s.text is None:
                    continue
                for key, value in self.Datastore.get_categories('2015/2283').items():
                    if key in s.text.lower():
                        regulations.append('2015/2283')
                        categories.append(value)
                for key, value in self.Datastore.get_categories('97/618').items():
                    if key in s.text.lower():
                        regulations.append('97/618/EC')
                        categories.append(value)
                for key, value in self.Datastore.get_categories('258/97').items():
                    if key in s.text.lower():
                        regulations.append('258/97')
                        categories.append(value)
        
        categories_str = ", ".join(list(set(categories)))
        regulations_str = ", ".join(list(set(regulations)))
        return categories_str, regulations_str
        
    
class OpinionAExtraction(CategoryExtractionStrategy):
    def find_relevant_paragraphs(self, body):
        relevant_divs = []
        queries = ['Introduction', 'Data', 'Methodologies', 'Data and Methodologies']
        for query in queries:
            div = body.findall(f'.//tei:div[tei:head="{query}"]', self.tei_namespaces)
            for d in div:
                relevant_divs.append(d)
        if len(relevant_divs) == 0:
            return
        relevant_paragraphs = []
        for relevant_div in relevant_divs:
            ps = relevant_div.findall('.//tei:p', self.tei_namespaces)
            for p in ps:
                relevant_paragraphs.append(p)
        return relevant_paragraphs

    def extract(self, body):
        return super().extract(body)

class OpinionBExtraction(CategoryExtractionStrategy):
    def find_relevant_paragraphs(self, body):
        assessment_div = body.xpath('.//tei:div[tei:head="ASSESSMENT"]', namespaces=self.tei_namespaces)
        if not assessment_div:
            return
        return assessment_div[0].xpath('.//tei:p', namespaces=self.tei_namespaces)

    def extract(self, body):
        return super().extract(body)
    
class OpinionCExtraction(CategoryExtractionStrategy):

    def find_relevant_paragraphs(self, body):
        # The divs are called either "ASSESSMENT"
        assessment_div = body.xpath('.//tei:div[tei:head="ASSESSMENT"]', namespaces=self.tei_namespaces)
        if assessment_div is None:
            return
        return assessment_div[0].xpath('.//tei:p', namespaces=self.tei_namespaces)

    def extract(self, body):
        return super().extract(body)

class OpinionDExtraction(CategoryExtractionStrategy):

    def find_relevant_paragraphs(self, body):
        # The divs are called either "ASSESSMENT" or "ASSESSMENT Introduction"
        assessment_div = body.xpath('.//tei:div[tei:head="ASSESSMENT" or tei:head="ASSESSMENT Introduction"]', namespaces=self.tei_namespaces)
        if not assessment_div:
            return
        # Return all paragraphs in the div
        return assessment_div[0].xpath('.//tei:p', namespaces=self.tei_namespaces)

    def extract(self, body):
        return super().extract(body)
    
class OpinionEExtraction(CategoryExtractionStrategy):
    def find_relevant_paragraphs(self, body):
        assessment_div = body.xpath('.//tei:div[tei:head="| Introduction"]', namespaces=self.tei_namespaces)
        if not assessment_div:
            return
        return assessment_div[0].xpath('.//tei:p', namespaces=self.tei_namespaces)

    def extract(self, body):
        return super().extract(body)
