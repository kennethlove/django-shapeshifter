from pytest_djangoapp import configure_djangoapp_plugin

pytest_plugins = configure_djangoapp_plugin(
    extend_INSTALLED_APPS=[
        'django.contrib.sessions',
        'django.contrib.messages',
    ],
    extend_MIDDLEWARE=[
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
    ]
)
