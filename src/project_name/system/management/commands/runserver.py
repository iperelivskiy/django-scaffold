"""
A tiny correction to how django serves media files in development server.
Can save you some CPU time in development.

This command utilizes a tiny wsgi handler for serving media files.
Just like contrib.staticfiles do. So middleware processing is omitted etc.
"""
from django.conf import settings
from django.views.static import serve
from django.contrib.staticfiles.handlers import StaticFilesHandler
from django.contrib.staticfiles.management.commands.runserver import \
    Command as StaticFilesRunserverCommand


class Command(StaticFilesRunserverCommand):
    def get_handler(self, *args, **options):
        """
        Returns the static and media files serving handler wrapping
        the default handler.
        """
        handler = super(Command, self).get_handler(*args, **options)
        insecure_serving = options.get('insecure_serving', False)
        if settings.DEBUG or insecure_serving:
            return _MediaFilesHandler(handler)
        return handler


class _MediaFilesHandler(StaticFilesHandler):
    """
    Handler for serving the media files.
    """
    def get_base_dir(self):
        return settings.MEDIA_ROOT

    def get_base_url(self):
        return settings.MEDIA_URL

    def serve(self, request):
        relative_url = request.path[len(self.base_url[2]):]
        return serve(request, relative_url, document_root=self.get_base_dir())
