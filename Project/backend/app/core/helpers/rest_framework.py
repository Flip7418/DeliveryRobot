DEFAULT_REST_FRAMEWORK_SETTINGS = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'authorization.backends.JWTAuthentication',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend'
    ]
}
