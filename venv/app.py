from flask import Flask, render_template, request, jsonify
from pdfoutput import PDFOutput
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        university_id = int(request.form.get('university'))
        major = request.form.get('major')
        school_year = request.form.get('school_year')
        pdf_output = PDFOutput(university_id, school_year)
        pdf_url = pdf_output.get_pdf_url(major)
        if pdf_url:
            return jsonify(pdf_url=pdf_url)
        else:
            return "No PDF found"
    else:
        response = requests.get('https://assist.org/api/institutions/150/agreements')
        agreements = response.json()
        unique_universities = set()
        universities = []
        for agreement in agreements:
            id_name_tuple = (agreement['institutionParentId'], agreement['institutionName'])
            if id_name_tuple not in unique_universities:
                universities.append({'id': agreement['institutionParentId'], 'name': agreement['institutionName'], 'code': agreement['code'].strip()})
                unique_universities.add(id_name_tuple)
        universities.sort(key=lambda x: x['name'])
        return render_template('index.html', universities=universities)

@app.route('/majors', methods=['GET'])
def get_majors():
    university_id = int(request.args.get('university_id'))
    school_year_id = request.args.get('school_year')
    pdf_output = PDFOutput(university_id, school_year_id)
    agreements = pdf_output.get_agreements()
    majors = pdf_output.get_majors(agreements)
    return jsonify(list(majors))  # Convert the set of majors back into a list before returning

@app.route('/school_years', methods=['GET'])
def get_school_years():
    university_id = int(request.args.get('university_id'))
    pdf_output = PDFOutput(university_id)  # Do not pass school_year_id here
    agreements = pdf_output.get_agreements()
    def id_to_year(year_id):
        start_year = 2022 - (73 - year_id)
        if(year_id == 74):
            return "2022-2023"
        else:
            return f"{start_year}-{start_year+1}"
    school_years = [id_to_year(agreement['receivingYearIds'][-1]) for agreement in agreements]
    return jsonify(list(school_years))  # Remember to return the list of school years

if __name__ == '__main__':
    app.run(debug=True)
