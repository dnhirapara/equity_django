from .base import INSTALLED_APPS, BASE_DIR
import os

INSTALLED_APPS += [
    'daily_data.apps.DailyDataConfig',
]

CSV_FOLDER = os.path.join(BASE_DIR, 'csv_files')
ZIP_FOLDER = os.path.join(BASE_DIR, 'zips')

MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
MEDIA_URL = '/media/'

STATIC_ROOT = '/home/app/web/static/'
STATIC_URL = '/static/'
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, 'static/')
# ]
