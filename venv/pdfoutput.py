import os
import time
import urllib.request
import json
import threading
from queue import Queue

class PDFOutput:
    # Constructor for the class. Takes university_id as an argument and an optional delay argument
    # which is by default set to 0.2 seconds.
    def __init__(self, university_id, delay=0.2):
        self.university_id = university_id  # University ID for the university of interest
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
        majors = []
        for agreement in agreements:
            time.sleep(self.delay)  # Delay to prevent spamming the server with requests
            university_id = agreement['institutionParentId']
            school_year = agreement['receivingYearIds'][-1]  # Get the last year in 'receivingYearIds'
            # Requesting the major data from the API
            with urllib.request.urlopen(f'https://assist.org/api/agreements?receivingInstitutionId={university_id}&sendingInstitutionId={self.community_college_id}&academicYearId={school_year}&categoryCode=major') as url:
                reports = json.loads(url.read().decode())['reports']
            for report in reports:
                majors.append(report['label'])  # Appending the major to the list of majors
        return majors

    # This function returns the URL of the PDF for the given major
    def get_pdf_url(self, major_name):
        agreements = self.get_agreements()
        for agreement in agreements:
            time.sleep(self.delay)  # Delay to prevent spamming the server with requests
            university_id = agreement['institutionParentId']
            school_year = agreement['receivingYearIds'][-1]  # Get the last year in 'receivingYearIds'
            # Requesting the major data from the API
            with urllib.request.urlopen(f'https://assist.org/api/agreements?receivingInstitutionId={university_id}&sendingInstitutionId={self.community_college_id}&academicYearId={school_year}&categoryCode=major') as url:
                reports = json.loads(url.read().decode())['reports']
            for report in reports:
                # Checking if the major name matches the user input
                if report['label'] == major_name:
                    # Return the URL of the PDF for the major
                    return f"https://assist.org/transfer/report/{report['key']}"
        # If no matching major is found, return None
        return None
