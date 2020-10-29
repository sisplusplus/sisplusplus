import requests
from bs4 import BeautifulSoup
from sis.models import Faculty, Program


class Scraper:
    def __init__(self):
        pass

    def scrape_faculty(self):
        # Gets and parses faculty codes.
        # Updates faculty name if it was changed.
        # Attention: Does not delete faculties that don't exist anymore

        soup = get_soup("http://www.sis.itu.edu.tr/eng/curriculums/")

        select_box = soup.find("select", {"name":"fakulte"})
        for option in select_box.findChildren("option"):
            if option['value'] == '':
                continue
            code = option['value']
            full_name = option.text.strip()

            try:
                faculty_obj = Faculty.objects.get(code=code)
            except Faculty.DoesNotExist:
                faculty_obj = None
                
            if not faculty_obj:
                print("Adding faculty " + code + " - " + full_name)
                Faculty.objects.create(code=code, full_name=full_name)
            else:
                if full_name != faculty_obj.full_name:
                    print("Updating full_name of the faculty with code \'" + code +
                           "\' from \'" + faculty_obj.full_name + "\' to \'" + full_name + "\'")
                    faculty_obj.full_name = full_name
                    faculty_obj.save()
                else:
                    print(faculty_obj.code + " - " + faculty_obj.full_name + " already exists.")

    def scrape_program(self):
        for faculty in Faculty.objects.all():
            soup = get_soup("http://www.sis.itu.edu.tr/eng/curriculums/index.php?fakulte=" + faculty.code)
            selection = soup.find("select", {"name":"subj"})
            for option in selection.findChildren("option"):
                if option['value'] == '':
                    continue
                code = option['value']
                full_name = option.text.strip()
                
                try:
                    program_obj = Program.objects.get(code=code)
                except:
                    program_obj = None

                if not program_obj:
                    print("Adding program " + code + " - " + full_name + " of " + faculty.code)
                    Program.objects.create(code=code, full_name=full_name, faculty=faculty)
                else:
                    if faculty != program_obj.faculty or full_name != program_obj.full_name:
                        print("Updating program \'" + code + " - " + program_obj.full_name
                              + " of " + program_obj.faculty.code + "\' to \'" +
                              code + " - " + full_name + " of " + faculty.code + "\'")
                        program_obj.full_name = full_name
                        program_obj.faculty = faculty
                        program_obj.save()
                    else:
                        print("Program " + program_obj.code + " needs no update.")

    def scrape_curriculum(self):
        pass

    def scrape_course(self):
        pass

    def scrape_semester(self):
        pass
    
def get_soup(url):
    return BeautifulSoup(requests.get(url).content, "lxml")
