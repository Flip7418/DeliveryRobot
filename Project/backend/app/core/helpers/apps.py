DEFAULT_APPS = (
   'django.contrib.admin',
   'django.contrib.auth',
   'django.contrib.contenttypes',
   'django.contrib.sessions',
   'django.contrib.messages',
   'django.contrib.staticfiles',
)

THIRD_APPS = (
   'rest_framework',
   'django_filters',
   'corsheaders',
   'drf_yasg',
   'channels'
)

PROJECT_APPS = (
   'authorization',
   'blog',
   'doctor',
   'order',
   'pill',
   'student',
   'user',
   'robot'
)

APPS = DEFAULT_APPS + THIRD_APPS + PROJECT_APPS
