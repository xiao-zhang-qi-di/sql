from django.test import TestCase

# Create your tests here.
import os
import sys
import django
sys.path.insert(0, '/Users/zhangqidi/代码/sql_project')
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sql_project.settings")
django.setup()

import time

from django.conf import settings
def function():
    # print(getattr(settings, 'INCEPTION_HOST'))
    print(settings.INCEPTION_HOST)
    print(time.localtime())

if __name__ == '__main__':
    function()