import time
import urllib.request
import json

class PDFOutput:
    # Constructor for the class. Takes university_id as an argument and an optional delay argument
    # which is by default set to 0.2 seconds.
    def __init__(self, university_id, school_year_id=None, delay=0.2):
        self.university_id = university_id  # University ID for the university of interest
        self.school_year_id = school_year_id  # School Year ID chosen by the user
        self.community_college_id = 150  # Community college ID. Here it is set to 150
        self.delay = delay  # Delay between subsequent requests

    # This function fetches the agreements made by the university of interest from the ASSIST API
    def get_agreements(self):
        # Requesting the agreements data from the API
        with urllib.request.urlopen(f'https://assist.org/api/institutions/{self.community_college_id}/agreements') as url:
            agreements = json.loads(url.read().decode())
        # Filtering out the most recent agreements
        recent_agreements = [agreement for agreement in agreements if 'receivingYearIds' in agreement and agreement['institutionParentId'] == self.university_id]
        return recent_agreements

 # This function fetches all the majors available for the university of interest from the ASSIST API
    def get_majors(self, agreements):
        majors = set()  # Use a set instead of a list
        for agreement in agreements:
            time.sleep(self.delay)  # Delay to prevent spamming the server with requests
            university_id = agreement['institutionParentId']
            school_year_id = agreement['receivingYearIds'][-1]
            if school_year_id == 74:
                school_year_id = 73
            # Requesting the major data from the API
            print(school_year_id)
            with urllib.request.urlopen(f'https://assist.org/api/agreements?receivingInstitutionId={university_id}&sendingInstitutionId={self.community_college_id}&academicYearId={school_year_id}&categoryCode=major') as url:
                reports = json.loads(url.read().decode())['reports']
            for report in reports:
                majors.add(report['label'])  # Add the major to the set of majors
        return sorted(majors) # Return the list of majors in alphabetical order

    def get_school_years(self):
    # Requesting the agreements data from the API
        with urllib.request.urlopen(f'https://assist.org/api/institutions/{self.community_college_id}/agreements') as url:
            agreements = json.loads(url.read().decode())
        # Filtering out the agreements for the university
        university_agreements = [agreement for agreement in agreements if agreement['institutionParentId'] == self.university_id]
        # Extract all receivingYearIds across all agreements
        all_years = [agreement['receivingYearIds'] for agreement in university_agreements]
        # Flatten the list and remove duplicates
        unique_years = sorted(set(year for years in all_years for year in years))
        return unique_years

    # This function returns the URL of the PDF for the given major
    def get_pdf_url(self, major_name, school_year_id=None):
        agreements = self.get_agreements()
        for agreement in agreements:
            time.sleep(self.delay)  # Delay to prevent spamming the server with requests
            university_id = agreement['institutionParentId']
            school_year_id = agreement['receivingYearIds'][-1]
            if school_year_id == 74:
                school_year_id = 73
            # Requesting the major data from the API
            url = f'https://assist.org/api/agreements?receivingInstitutionId={university_id}&sendingInstitutionId={self.community_college_id}&academicYearId={school_year_id}&categoryCode=major'
            print(url)
            with urllib.request.urlopen(f'https://assist.org/api/agreements?receivingInstitutionId={university_id}&sendingInstitutionId={self.community_college_id}&academicYearId={school_year_id}&categoryCode=major') as url:
                reports = json.loads(url.read().decode())['reports']
            for report in reports:
                # Checking if the major name matches the user input
                if report['label'] == major_name:
                    # Return the URL of the PDF for the major
                    return f"https://assist.org/transfer/report/{report['key']}"
        # If no matching major is found, return None
        return None