import requests
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
        pass

    def scrape_faculty(self):
        # Gets and parses faculty codes.
        # Updates faculty name if it was changed.
        # Attention: Does not delete faculties that don't exist anymore

        soup = get_soup("http://www.sis.itu.edu.tr/tr/dersplan/")

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
                if TEST_MODE_MINIMAL_SCRAPE:
                    break
            else:
                print(
                    f"Faculty exists : {faculty_obj.code : <3} - {faculty_obj.full_name}"
                )
                if TEST_MODE_MINIMAL_SCRAPE:
                    break

    def scrape_program(self):
        for faculty in Faculty.objects.all():
            soup = get_soup(
                f"http://www.sis.itu.edu.tr/tr/dersplan/index.php?fakulte={faculty.code}"
            )
            selection = soup.find("select", {"name": "subj"})
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
                    if TEST_MODE_MINIMAL_SCRAPE:
                        break
                else:
                    print(
                        f"Program exists : {program_obj.code : <4}- {full_name} of {faculty.full_name}"
                    )
                    if TEST_MODE_MINIMAL_SCRAPE:
                        break

    def scrape_curriculum(self):
        for program in Program.objects.all():
            base_url = f"http://www.sis.itu.edu.tr/tr/dersplan/plan/{program.code}/"
            try:
                soup = get_soup(base_url)
            except Exception as e:
                print(e)
                continue

            span = soup.find("span", {"class": "ustbaslik"})

            for a_tag in span.find_next_siblings("a"):
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

    def scrape_course(self):
        pass

    def scrape_semester(self):
        pass

    def scrape_semester_and_courses(self):
        for curriculum in Curriculum.objects.all():
            soup = get_soup(curriculum.url)
            for semester_num, table in enumerate(
                soup.findAll("table", {"class": "plan"}), start=1
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

                    # if it is not a special course set
                    if code_column.text.strip() != "":
                        course_codes_and_urls = [
                            (a_tag.text, a_tag["href"])
                            for a_tag in code_column.findChildren("a")
                        ]
                        courses = [
                            self._get_or_create_course_from_url(code, url)
                            for code, url in course_codes_and_urls
                        ]
                        defaults = {
                            "semester": semester,
                            "title": code_column.find_next("td").text.strip(),
                        }
                        (
                            semester_course_slot,
                            created,
                        ) = SemesterCourseSlot.objects.get_or_create(
                            code=f"{semester.code}_row{row_num}",
                            semester=semester,
                            title=code_column.find_next("td").text.strip(),
                        )
                        if created:
                            semester_course_slot.courses.add(*courses)
                            print(
                                f"Created semester course slot: {semester_course_slot.code} "
                                f"{semester_course_slot.title}"
                            )
                        else:
                            print(
                                f"Semester course slot exists: {semester_course_slot.code}"
                            )
                    else:
                        # TODO special course set
                        pass

    @staticmethod
    def _map_header_to_column_soup(header_translations, header, row):
        # Sanitize header and row since there are breaks in between
        header = header.findChildren("td")
        row = row.findChildren("td")

        header = [td.text.strip() for td in header]
        header = [header_translations.get(i, i.lower()) for i in header]

        d = dict(zip(header, row))
        return {key: value for key, value in d.items() if value not in ("-", "")}

    @staticmethod
    def _map_header_to_column_text(header_translations, header, row):
        # Sanitize header and row since there are breaks in between
        header = header.findChildren("td")
        row = row.findChildren("td")

        header = [td.text.strip() for td in header]
        header = [header_translations.get(i, i.lower()) for i in header]
        row = [td.text.strip() for td in row]

        d = dict(zip(header, row))
        return {key: value for key, value in d.items() if value not in ("-", "")}

    @staticmethod
    def _get_or_create_course_from_url(code, url):
        try:
            return Course.objects.get(code=code)
        except Exception:
            pass

        soup = get_soup(url)

        # Course Catalog page is made out of different tables
        # containing information about specified course

        # Table 1
        table = soup.find("table", {"class": "plan"})
        header = table.find("tr")

        row = header.find_next_siblings("tr")[0]
        header_translations = {
            "Kod (Code)": "code",
            "Ders Adı (Course Name)": "title",
            "Türü (Type)": "type",
            "Dili (Language)": "language",
        }
        header_to_column = Scraper._map_header_to_column_soup(
            header_translations, header, row
        )
        code = header_to_column["code"].text.strip()
        title = header_to_column["title"].contents[0].strip()
        is_compulsary = header_to_column["type"].text == "Zorunlu (Compulsory)"

        # Table 2
        table = table.find_next("table", {"class": "plan"})
        header = table.find("tr")
        row = header.find_next_siblings("tr")[0]
        header_translations = {
            "Kredi (Local Credits)": "credit",
            "AKTS (ECTS)": "ects",
            "Ders (Theoretical)": "theoretical",
            "Uygulama (Tutorial)": "tutorial",
            "Labaratuvar (Laboratory)": "lab",
        }
        table_two_data = Scraper._map_header_to_column_text(
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


def get_soup(url):
    retry = 1
    while retry:
        try:
            response = requests.get(url)
            retry = 0
        except requests.exceptions.ConnectionError:
            print(f"Couldn't connect url: {url} - trying again")
            retry = 1

    if response.status_code != 200:
        raise Exception(f"{url} returned {response.status_code} instead of 200")
    return BeautifulSoup(response.content, "lxml")
