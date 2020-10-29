from django.core.management.base import BaseCommand, CommandError
from sis.scraper.base import Scraper
#from sis.models import Faculty, Program, Curriculum, Course, Semester

class Command(BaseCommand):
    help = 'Refreshes the scraped data like Program, Curriculum, Course etc.'

    def handle(self, *args, **options):
        scraper = Scraper()
        scraper.scrape_faculty()
        scraper.scrape_program()
        scraper.scrape_curriculum()
        scraper.scrape_semester_and_courses()
