import lxml.etree as ET
import pandas as pd
import re 
import datetime
from name_extractor import NameExtractor
from data_store import DataStore
from unidecode import unidecode
from category_extractor import CategoryExtractionStrategy

class Opinion():
    def __init__(self, xml_filepath : str, grobid_filepath : str, category_extractor : CategoryExtractionStrategy): 
        # Split into body and front
        self._tree = ET.parse(xml_filepath).getroot() #Jats file
        self._body = self._tree.find('.//body')
        self._front = self._tree.find('.//front')
        self.article_meta = self._front.find('article-meta')

        self.Datastore = DataStore()
        self.category_extractor = category_extractor

        self.tei_namespaces = {"tei": "http://www.tei-c.org/ns/1.0"}
        self.tei_file = ET.parse(grobid_filepath).getroot()

        # Initialize empty
        self.extracted_information = {
            'EFSA Q number' : '',
            'DOI' : '',
            'title' : '',
            'publication date' : '', 
            'adoption date' : '',
            'EFSA panels' : '',
            'applicant': '',
            'mandate': '',
            'nf_name': '',
            'scientific officers': '',
            'categories': '',
            'regulations' : '',
        }

        self.extract_information()

    def extract_information(self):
        self.extract_title()
        self.extract_question_number()
        self.extract_panels()
        self.extract_doi()
        self.extract_adoption_date()
        self.extract_publication_date()
        self.extract_applicant()
        self.extract_mandate()
        self.extract_nf_name()
        self.extract_scientific_officers()
        self.extract_categories()

    def extract_question_number(self):
        footnotes = self._front.find('notes').find('fn-group')
        for fn in footnotes:
            for child in fn:
                combined_text = "".join(child.itertext()) #to ignore <bold> tag etc.
                efsa_question_pattern = r'EFSA[-‐–—]Q[-‐–—]\S+'
                efsa_q_numbers = re.findall(efsa_question_pattern, combined_text)
                if len(efsa_q_numbers) > 0: # One opinion can have multiple question numbers
                    for q_number in efsa_q_numbers:
                        self.extracted_information['EFSA Q number'] += q_number.replace(';', '').replace('‐', '-')
                    return

        if self.extracted_information['EFSA Q number'] == '': # For type B opinions, where the first approach fails
            if self._body:
                # Find all sections with the title "QUESTION NUMBER"
                sections = self._body.findall('.//sec[title="QUESTION NUMBER"]')
                for section in sections:
                    self.extracted_information['EFSA Q number'] = section.find('p').text.replace(';', '').replace('‐', '-') #replace efsas weird dash
                    return
                
    def extract_panels(self):
        collab = self.article_meta.find('.//collab')
        if collab is not None: # Try to find panels in the <collab>
            if 'NDA' in collab.text:
                self.extracted_information['EFSA panels'] += ' NDA'
            elif 'EFSA' in collab.text:
                self.extracted_information['EFSA panels'] += ' EFSA'

        title_lower = self.extracted_information['title'].lower() # Find panels in the title
        if 'panel' in title_lower:
            if 'dietetic' in self.extracted_information['title'].lower() and 'nutrition' in self.extracted_information['title'].lower():
                self.extracted_information['EFSA panels'] += ' NDA'
            if 'genetic' in self.extracted_information['title'].lower():
                self.extracted_information['EFSA panels'] += ' GMO'
    
    def extract_title(self):
        title_tag = self.article_meta.find('.//article-title')
        self.extracted_information['title'] = "".join(title_tag.itertext())

    def extract_adoption_date(self):
        footnotes = self._front.find('notes').find('fn-group')
        for fn in footnotes:
            for child in fn:
                if 'adopt' in "".join(child.itertext()).lower():
                    self.extracted_information['adoption date'] = "".join(child.itertext()).split(':')[1].strip() #TODO Mozna taky datum
                    break

    def extract_publication_date(self):        
        pub_date = self.article_meta.find('pub-date')
        date_obj = datetime.date(int(pub_date.find('year').text), int(pub_date.find('month').text), int(pub_date.find('day').text))
        self.extracted_information['publication date'] = date_obj.strftime('%d-%m-%Y')

    def extract_doi(self):
        for id in self.article_meta.findall('article-id'):
            if id.attrib['pub-id-type'] == 'doi':
                self.extracted_information['DOI'] = id.text

    def extract_applicant(self):
        if self._body is None:
            return
        text = "".join(self._body.itertext())
        # Attempt to extract applicant using the first approach
        try:
            applicant = text.split('company')[1].split('submitted')[0]
            if len(applicant) < 150: # Applicant is usually a company name, so it should not be too long
                self.extracted_information['applicant'] = applicant
        except (IndexError, AttributeError):
            pass

        # If no applicant was found, attempt to extract using the second approach
        if self.extracted_information['applicant'] == '':
            try:
                applicant = text.split('submitted')[0].split(',')[-1]
                if len(applicant) < 150:
                    self.extracted_information['applicant'] = applicant
            except (IndexError, AttributeError):
                pass

    def extract_mandate(self):
        if 'traditional' in self.extracted_information['title'].lower():
            self.extracted_information['mandate'] = 'traditional food'
        elif 'extension' in self.extracted_information['title'].lower() or 'extended' in self.extracted_information['title'].lower():
            self.extracted_information['mandate'] = 'extension of use'
        elif 'source' in self.extracted_information['title'].lower():
            self.extracted_information['mandate'] = 'new dossier, nutrient source'
        else:
            self.extracted_information['mandate'] = 'new dossier'


    def extract_nf_name(self):
        name_extractor = NameExtractor(self.extracted_information['title'], self.extracted_information['mandate'])
        self.extracted_information['nf_name'] = name_extractor.extract_nf_name()

    def extract_scientific_officers(self):
        source_description = self.tei_file.find('.//tei:sourceDesc', self.tei_namespaces)
        authors = source_description.findall('.//tei:persName', self.tei_namespaces) # Find all authors in the <sourceDesc>
        officers_list = []
        for author in authors:
            forenames = author.findall('.//tei:forename', self.tei_namespaces)
            surname = author.find('.//tei:surname', self.tei_namespaces)
            if len(forenames) != 0 and surname is not None: # Author may be e.g. 'EFSA', which is not relevant
                forenames = [unidecode(f.text.lower()) for f in forenames] # Unidecode as some names contain special characters
                forename_text = ' '.join(forenames) # Some authors have multiple forenames
                surname_text = unidecode(surname.text.lower()).replace('-', ' ')

                for f, s in self.Datastore.get_officers(): # Check if the author is in the list of scientific officers
                    if unidecode(f.lower()) in forename_text and unidecode(s.lower()) in surname_text:
                        officers_list.append(f + ' ' + s)

        if len(officers_list) > 0: # If there are any scientific officers, join them together
            officers_string = ', '.join(officers_list)
            self.extracted_information['scientific officers'] = officers_string


    def extract_categories(self):
        body = self.tei_file.find('.//tei:body', self.tei_namespaces)  
        print('extract categories was called')
        print(self.category_extractor.extract(body))
        if self.category_extractor.extract(body) is not None:
            categories, regulations = self.category_extractor.extract(body)
            self.extracted_information['categories'] = categories
            self.extracted_information['regulations'] = regulations

    def into_df(self): #Create pandas dataframe from the article information
        return pd.DataFrame(self.extracted_information, index=[0])
    
    