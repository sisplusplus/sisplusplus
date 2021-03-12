import requests
from collections import defaultdict
from bs4 import BeautifulSoup
from sis.models import (
    Faculty,
    Program,
    Curriculum,
    Course,
    Semester,
    SemesterCourseSlot,
)


TEST_MODE_MINIMAL_SCRAPE = False


class Scraper:
    def __init__(self):
        self.curriculum_url = "https://www.sis.itu.edu.tr/TR/ogrenci/lisans/ders-planlari/ders-planlari.php"
        self.program_url = "https://www.sis.itu.edu.tr/TR/ogrenci/lisans/ders-planlari/plan/{program.code}/"


    def scrape_faculty(self):
        # Gets and parses faculty codes.
        # Updates faculty name if it was changed.
        # Attention: Does not delete faculties that don't exist anymore
        soup = get_soup(self.curriculum_url)

        select_box = soup.find("select", {"name": "fakulte"})
        for option in select_box.findChildren("option"):
            if option["value"] == "":
                continue
            code = option["value"]
            full_name = option.text.strip()

            defaults = {"full_name": full_name}
            faculty_obj, created = Faculty.objects.update_or_create(
                code=code, defaults=defaults
            )

            if created:
                print(f"Created faculty: {code : <3}-{full_name}")
            else:
                print(f"Faculty exists : {faculty_obj.code : <3} - {faculty_obj.full_name}")
            if TEST_MODE_MINIMAL_SCRAPE:
                break

    def scrape_program(self):
        for faculty in Faculty.objects.all():
            payload = {"fakulte": faculty.code}
            soup = get_soup(self.curriculum_url, payload)
            selection = soup.find("select", {"name": "program"})
            for option in selection.findChildren("option"):
                if option["value"] == "":
                    continue
                code = option["value"]
                full_name = option.text.strip()

                defaults = {"full_name": full_name, "faculty": faculty}
                program_obj, created = Program.objects.update_or_create(
                    code=code, defaults=defaults
                )

                if created:
                    print(
                        f"Created program: {code : <4}- {full_name} of {faculty.full_name}"
                    )
                else:
                    print(
                        f"Program exists : {program_obj.code : <4}- {full_name} of {faculty.full_name}"
                    )
                if TEST_MODE_MINIMAL_SCRAPE:
                    break

    def scrape_curriculum(self):

        for program in Program.objects.all():
            try:
                base_url = self.program_url.format(program=program)
                soup = get_soup(base_url)
            except Exception as e:
                print(e)
                continue

            div = soup.find("div", {"class": "content-area"})

            for a_tag in div.findChildren("a"):
                # Getting rid of redundant information
                # Student's Catalog Term: Before 2001-2002 Fall Semester
                full_name = a_tag.text.strip().split(":")[-1].strip()
                if not full_name:
                    continue
                url = base_url + a_tag["href"]
                code = f"{program.code}{a_tag['href'].split('.')[0]}"
                defaults = {
                    "program": program,
                    "full_name": full_name,
                    "url": url,
                }
                curriculum, created = Curriculum.objects.update_or_create(
                    code=code, defaults=defaults
                )
                if created:
                    print(
                        f"Created curriculum: {program.code : <4}- {full_name :<55} code: {curriculum.code}"
                    )
                else:
                    print(
                        f"Curriculum exists : {program.code : <4}- {full_name :<55} code: {curriculum.code}"
                    )
                # if TEST_MODE_MINIMAL_SCRAPE:
                    # break
            # if TEST_MODE_MINIMAL_SCRAPE:
                # break

    def scrape_course(self):
        pass

    def scrape_semester(self):
        pass

    def scrape_semester_and_courses(self):
        for curriculum in Curriculum.objects.all():
            soup = get_soup(curriculum.url)
            for semester_num, table in enumerate(
                    soup.findAll("table", {"class": "table-responsive"}), start=1
                ):
                    defaults = {"num": semester_num, "curriculum": curriculum}
                    semester, created_semester = Semester.objects.update_or_create(
                        code=f"{curriculum.code}_{semester_num}", defaults=defaults
                    )

                    if created_semester:
                        print(f"Created semester: {semester.code}")

                    header = table.find("tr")
                    for row_num, row in enumerate(header.find_next_siblings("tr"), start=1):
                        code_column = row.find("td")
                        defaults = {
                            "semester": semester,
                            "title": code_column.find_next("td").text.strip(),
                        }
                        semester_course_slot, created, = SemesterCourseSlot.objects.get_or_create(
                            code=f"{semester.code}_row{row_num}",
                            defaults=defaults,
                        )
                        if created:
                            print(
                                f"Created semester course slot: {semester_course_slot.code} "
                                f"{semester_course_slot.title}"
                            )
                        else:
                            print(
                                f"Semester course slot exists: {semester_course_slot.code}"
                            )
                        # if created: # we are already skipping parsed curriculums.
                                      # This needs to be run in order to make sure
                                      # that we are still adding courses even if the
                                      # execution is interrupted before
                        # if it is not a special course set
                        if code_column.text.strip() != "":
                            courses = self._get_courses(code_column, defaults)
                            semester_course_slot.courses.add(*courses)
                        else:
                            url = curriculum.url.rsplit('/', 1)
                            url[1] = row.findAll('td')[1].a['href']
                            url = '/'.join(url)
                            soup = get_soup(url)
                            table = soup.find("table", {"class": "table-responsive"})
                            if table is None:
                                with open('errors', 'a') as f:
                                    f.write(f'{url} page has some problems\n')
                                    continue


                            header = table.find('tr')

                            for row in header.find_next_siblings("tr"):
                                code_column = row.find("td")
                                courses = self._get_courses(code_column, defaults)
                                semester_course_slot.courses.add(*courses)
                        

    @staticmethod
    def _map_header_to_column(header_translations, header, row):
        # Sanitize header and row since there are breaks in between
        header = header.findChildren("td")
        row = row.findChildren("td")

        header = [td.text.strip() for td in header]
        header = [header_translations.get(i, i.lower()) for i in header]
        row = [td.text.strip() for td in row]

        # return dict(zip(header, row))
        d = dict(zip(header, row))
        return defaultdict(str, {key: value for key, value in d.items() if value not in ("-", "")})

    def _get_courses(self, code_column, defaults=None):
        course_codes_and_urls = [
            (a_tag.text, a_tag["href"])
            for a_tag in code_column.findChildren("a")
        ]
        courses = [
            self._get_or_create_course_from_url(code, url)
            for code, url in course_codes_and_urls
        ]
        if defaults:
            for course in courses:
                if not course.title:
                    course.title = defaults["title"]
                    course.save()
        return courses

    @staticmethod
    def _get_or_create_course_from_url(code, url):
        try:
            return Course.objects.get(code=code)
        except Course.DoesNotExist:
            pass

        soup = get_soup(url)

        # Course Catalog page is made out of different tables
        # containing information about specified course

        # Table 1
        table = soup.find("table", {"class": "table-bordered"})
        if table is None:
            return Course.objects.update_or_create(code='DNE999', is_compulsary=False, defaults={'title': 'Course cannot be found'})[0]
        table = table.find("table", {"class": "table-bordered"})
        header = table.find("tr")

        row = header.find_next_siblings("tr")[0]
        header_translations = {
            "Kod": "code",
            "Ders Adı": "title",
            "Türü": "type",
            "Dili": "language",
        }
        header_to_column = Scraper._map_header_to_column(
            header_translations, header, row
        )
        code = header_to_column["code"]
        title = header_to_column["title"]
        is_compulsary = header_to_column["type"] == "Zorunlu"

        # Table 2
        table = table.find_next("table", {"class": "table-bordered"})
        header = table.find("tr")
        row = header.find_next_siblings("tr")[0]
        header_translations = {
            "Kredi": "credit",
            "AKTS": "ects",
            "Ders": "theoretical",
            "Uygulama": "tutorial",
            "Laboratuvar": "lab",
        }
        table_two_data = Scraper._map_header_to_column(
            header_translations, header, row
        )

        # TODO Table 3 - Prerequisites

        print(f"Created course: {code}")
        return Course.objects.create(
            code=code,
            title=title,
            is_compulsary=is_compulsary,
            **table_two_data,
        )


def get_soup(url, payload=None):
    retry = 1
    while retry:
        try:
            response = requests.get(url, params=payload)
            retry = 0
        except requests.exceptions.ConnectionError:
            print(f"Couldn't connect url: {url} - trying again")
            retry = 1

    if response.status_code != 200:
        raise Exception(f"{url} returned {response.status_code} instead of 200")
    return BeautifulSoup(response.content, "lxml")
