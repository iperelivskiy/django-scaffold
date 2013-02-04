
from django_assets import Bundle, register


register('main_js', Bundle(
    'libs/jquery-1.8.3.js',
    'libs/underscore-1.4.4.js',
    'plugins/plugins.js',
    'js/main.js',
    output='_compress/js/main.js'))


register('main_css', Bundle(
         'css/main.css',
         filters='cssrewrite',
         output='_compress/css/main.css'))
