
from django_assets import Bundle, register


register('main_js', Bundle(
    'libs/jquery-1.8.2.min.js',
    'libs/underscore-min.js',
    'plugins/plugins.js',
    'js/main.js',
    output='compress_/js/main.js'))


register('main_css', Bundle(
         'css/main.css',
         filters='cssrewrite',
         output='compress_/css/main.css'))
