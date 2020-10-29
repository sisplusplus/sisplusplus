import requests
from bs4 import BeautifulSoup
from sis.models import Faculty, Program

class Crawler:
    def __init__(self):
        pass

    def crawlFaculty(self):
        # Gets and parses faculty codes.
        # Updates faculty name if it was changed.
        # Attention: Does not delete faculties that don't exist anymore
        
        soup = getSoup("http://www.sis.itu.edu.tr/tr/sistem/fak_bol_kodlari.html")

        # Iterate over table rows with faculty information
        for htmlField in soup.find_all("span", {"class":"altbaslik"}):
            _code, _fullName = [ j.strip() for j in htmlField.text.split('-') ]

            try:
                facultyObj = Faculty.objects.get(code=_code)
            except Faculty.DoesNotExist:
                facultyObj = None
                
            if not facultyObj:
                print("Adding faculty " + _code + " - " + _fullName)
                Faculty.objects.create(code=_code, fullName=_fullName)
            else:
                if _fullName != facultyObj.fullName:
                    print("Updating fullName of the faculty with code \'" + _code +
                           "\' from \'" + facultyObj.fullName + "\' to \'" + _fullName + "\'")
                    facultyObj.fullName = _fullName
                    facultyObj.save()
                else:
                    print(facultyObj.code + " - " + facultyObj.fullName + " already exists.")

    def crawlProgram(self):
        soup = getSoup("http://www.sis.itu.edu.tr/tr/sistem/fak_bol_kodlari.html")

        # Iterate over table rows with faculty information
        for htmlFacultyField in soup.find_all("span", {"class":"altbaslik"}):
            facultyCode = htmlFacultyField.text.split('-')[0].strip()
            
            # Assigning htmlFacultyField to tableRow as the while loop start condition
            tableRow = htmlFacultyField

            # Iterates over the table rows that contain programs until whitespace
            while (tableRow := tableRow.find_next("tr")) and tableRow.text.strip() != '':
                _code = tableRow.find_next("td").text.strip()
                _fullName = tableRow.find_next("td").find_next("td").text.strip()
                
                try:
                    programObj = Program.objects.get(code=_code)
                except:
                    programObj = None

                if not programObj:
                    print("Adding program " + _code + " - " + _fullName + " of " + facultyCode)
                    Program.objects.create(code=_code, fullName=_fullName, faculty=Faculty.objects.get(code=facultyCode))
                else:
                    if facultyCode != programObj.faculty.code or _fullName != programObj.fullName:
                        print("Updating program \'" + _code + " - " + programObj.fullName
                              + " of " + programObj.faculty.code + "\' to \'" +
                              _code + " - " + _fullName + " of " + facultyCode + "\'")
                        programObj.fullName = _fullName
                        programObj.faculty = Faculty.objects.get(code=facultyCode)
                        programObj.save()
                    else:
                        print("Program " + programObj.code + " needs no update.")

    def crawlCurriculum(self):
        pass

    def crawlCourse(self):
        pass

    def crawlSemester(self):
        pass
    
def getSoup(url):
    return BeautifulSoup(requests.get(url).content, "html.parser")
