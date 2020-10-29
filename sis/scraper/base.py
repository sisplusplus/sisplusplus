import requests
from bs4 import BeautifulSoup
from sis.models import Faculty, Program, Curriculum, Course, Semester


class Scraper:
    def __init__(self):
        pass

    def scrape_faculty(self):
        # Gets and parses faculty codes.
        # Updates faculty name if it was changed.
        # Attention: Does not delete faculties that don't exist anymore

        soup = get_soup("http://www.sis.itu.edu.tr/tr/dersplan/")

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
                break
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
            soup = get_soup(f"http://www.sis.itu.edu.tr/tr/dersplan/index.php?fakulte={faculty.code}")
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
                    break
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
        for program in Program.objects.all():
            base_url = f"http://www.sis.itu.edu.tr/tr/dersplan/plan/{program.code}/"
            try:
                soup = get_soup(base_url)
            except Exception as e:
                print(e)
                continue
                
            span = soup.find("span", {"class":"ustbaslik"})

            for a_tag in span.find_next_siblings("a"):
                # Getting rid of redundant information
                # Student's Catalog Term: Before 2001-2002 Fall Semester
                full_name = a_tag.text.strip().split(':')[-1].strip()
                if not full_name:
                    continue
                url = base_url + a_tag['href']
                code = f"{program.code}{a_tag['href'].split('.')[0]}"
                curriculum, created = Curriculum.objects.get_or_create(program=program, full_name=full_name, url=url, code=code)
                if created:
                    print(f"Created {program.code} - {full_name} code: {curriculum.code}")
                else:
                   print(f"{program.code} - {full_name} already exists")

    def scrape_course(self):
        pass

    def scrape_semester(self):
        pass

    def scrape_semester_and_courses(self):
        for curriculum in Curriculum.objects.all():
            soup = get_soup(curriculum.url)
            for semester_num, table in enumerate(soup.findAll("table", {"class": "plan"}), start=1):
                semester, _ = Semester.objects.get_or_create(code=f'{curriculum.code}_{semester_num}', defaults={'num': semester_num, 'curriculum':curriculum})

                header = table.find("tr")
                for row in header.find_next_siblings("tr"):
                    data = self._create_dict(header, row)
                    if 'code' in data:
                        if len(data['code']) > 8:
                            # another model is needed
                            continue
                        print(f"{semester_num}-{curriculum.code}:creating course with {data}")
                        code=data.pop('code')
                        course, _ = Course.objects.get_or_create(code=code, defaults=data)
                        semester.courses.add(course)
                        




    @staticmethod
    def _create_dict(header, row):
        header_translations = {'Course Code': "code", 'Course Title': "title",
                               'Lab.': "lab", 'Type': "type",
                               'Compulsory/Elective': "is_compulsary",} 
        header_translations_tr = {'Ders Kodu': "code", 'Ders Adı': "title",
                               'Lab.': "lab", 'Türü': "type",
                                  'Z/S': "is_compulsary", 'Kredi':'credit', 'AKTS':'ects',
                                  'Ders':'theoretical', 'Uyg.':'tutorial'} 
        header = [td.text.strip() for td in header]
        # We don't need to translate ECTS as its lowered version is enough
        header = [header_translations_tr.get(i, i.lower()) for i in header]
        row = [td.text.strip() for td in row]
        d = dict(zip(header, row))
        d['is_compulsary'] = d['is_compulsary'].lower() == 'z'
        d.pop('yarıyıl')
        return {key: value for key, value in d.items()
                if value not in ("-", "")}


    
def get_soup(url):
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Page returned {response.status_code} instead of 200")
    return BeautifulSoup(response.content, "lxml")
