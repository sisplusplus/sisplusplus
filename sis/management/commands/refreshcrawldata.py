from django.core.management.base import BaseCommand, CommandError
from sis.crawler.base import Crawler
#from sis.models import Faculty, Program, Curriculum, Course, Semester

class Command(BaseCommand):
    help = 'Refreshes the crawled data like Program, Curriculum, Course etc.'

    def handle(self, *args, **options):
        myCrawler = Crawler()
        myCrawler.crawlFaculty()
        myCrawler.crawlProgram()
        myCrawler.crawlCurriculum()
        myCrawler.crawlCourse()
        myCrawler.crawlSemester()
