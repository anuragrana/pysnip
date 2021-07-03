from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
from django.utils.text import slugify

from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter, ImageFormatter

from .models import SnippetModel

code = """# METHOD 1
import datetime
start = datetime.datetime.now()
# code
print(datetime.datetime.now()-start)

# METHOD 2
import time
start_time = time.time()
main()
print(f"Total Time To Execute The Code is {(time.time() - start_time)}" )

# METHOD 3
import timeit
code = '''
## Code snippet whose execution time is to be measured
[2,6,3,6,7,1,5,72,1].sort()
'''
print(timeit.timeit(stmy = code,number = 1000))"""


def index(request):
    template_name = "snip/index.html"
    template_data = dict()
    recent_snippets = SnippetModel.objects.all().order_by('-created_date')[:10]
    template_data['recent_snippets'] = recent_snippets

    # since on snippet page, seo data is populated by snippet model instance attributes.
    # to re-use the variables in template, we are assigning home page seo data in snippet variable
    seo_data = dict()
    seo_data['title'] = settings.PROJECT_NAME_SPACED
    seo_data['description'] = settings.SITE_DESC
    template_data['snippet'] = seo_data

    return render(request, template_name, template_data)


def get_snippet(request, snippet_id):
    template_name = "snip/snippet.html"
    template_data = dict()

    lexer = get_lexer_by_name("python", stripall=True)
    formatter = HtmlFormatter(
        linenos='table',
        cssclass="highlight",
        style="fruity",
        noclasses=True,
        prestyles="padding-left:10px"  # for gap between line number and code
    )

    snippet = SnippetModel.objects.get(sid=snippet_id)
    # create 404 page

    code = snippet.code

    result = highlight(code, lexer, formatter)
    print(result)

    # TODO: store the highlighted code in DB once and reuse it
    template_data['highlighted_code'] = result
    template_data['snippet'] = snippet
    return render(request, template_name, template_data)


def download_code_as_file(request, snippet_id):
    snippet = SnippetModel.objects.get(sid=snippet_id)
    filename = slugify(snippet.title) + ".py"
    response = HttpResponse(snippet.code, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)
    return response


def download_code_as_image(request, snippet_id):
    snippet = SnippetModel.objects.get(sid=snippet_id)

    # TODO: Return the already stored image file of this snippet

    filename = slugify(snippet.title) + ".png"

    lexer = get_lexer_by_name("python", stripall=True)
    formatter = ImageFormatter(
        image_format="PNG",
        cssclass="highlight",
        style="fruity",
        noclasses=True,
        linenos=False,
    )
    result = highlight(snippet.code, lexer, formatter)
    # print(result)
    print(type(result))
    response = HttpResponse(result, content_type='image/png')
    response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)
    return response


def archive(request):
    template_data = dict()
    template_name = 'snip/archive.html'
    template_data['all_snippets'] = SnippetModel.objects.all()
    return render(request, template_name, template_data)
