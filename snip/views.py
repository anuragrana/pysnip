from django.shortcuts import redirect, render
from django.urls import reverse
from django.conf import settings
from django.http import HttpResponse
from django.utils.text import slugify
import random
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter, ImageFormatter
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

from .models import SnippetModel


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

    snippet = SnippetModel.objects.get(sid=snippet_id)
    # create 404 page

    lexer = get_lexer_by_name("python", stripall=True)
    formatter = HtmlFormatter(
        linenos='table',
        cssclass="highlight",
        style="fruity",
        noclasses=True,
        prestyles="padding-left:10px"  # for gap between line number and code
    )

    print(snippet)
    code = snippet.code

    result = highlight(code, lexer, formatter)
    # print(result)

    # TODO: store the highlighted code in DB once and reuse it
    template_data['highlighted_code'] = result
    template_data['snippet'] = snippet
    return render(request, template_name, template_data)


def get_next_snippet(request, snippet_id):
    # get the snippets with sid greater than current snippet_id ,
    # order by sid in increasing order and then get first result
    snippets = SnippetModel.objects.filter(sid__gt=snippet_id).order_by('sid')[:1]
    if not snippets:
        snippet = SnippetModel.objects.order_by('sid').first()
    else:
        snippet = snippets[0]

    return redirect(reverse("snip:snippet", args=(snippet.sid,), kwargs={}))


def get_previous_snippet(request, snippet_id):
    # get the snippets with sid less than current snippet_id ,
    # order by sid in decreasing order and then get first result
    snippets = SnippetModel.objects.filter(sid__lt=snippet_id).order_by('-sid')[:1]
    if not snippets:
        snippet = SnippetModel.objects.order_by('sid').last()
    else:
        snippet = snippets[0]

    return redirect(reverse("snip:snippet", args=(snippet.sid,), kwargs={}))


def get_random_snippet(request, snippet_id):
    total_count = SnippetModel.objects.all().count()
    # get a random number less than total_count and then get the record after that offset
    n = random.randint(0, total_count - 1)
    print(n)
    snippets = SnippetModel.objects.all()[n:n + 1]
    snippet = snippets[0]

    return redirect(reverse("snip:snippet", args=(snippet.sid,), kwargs={}))


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


# Github after login send the request to callback URL which is set in application.
# From there the request goes to LOGIN_REDIRECT_URL in settings.py
def mylogin(request):
    return redirect(reverse("snip:index", args=(), kwargs={}))


def mylogout(request):
    logout(request)
    return redirect(reverse("snip:index", args=(), kwargs={}))


@login_required
def add_snippet(request):
    template_name = "snip/add_snippet.html"
    template_data = dict()
    if request.method == "GET":
        return render(request, template_name, template_data)

    # if post request
    post_data = request.POST.copy()

    # add all elements from post data to template data
    template_data.update(post_data)

    title = post_data.get('title')
    description = post_data.get('description')
    code = post_data.get('code')
    author = post_data.get('author')
    python_version = post_data.get('python_version')

    if not all([title, code, author, python_version]):
        # TODO: use messaging here
        return render(request, template_name, template_data)

    snippet = SnippetModel()
    snippet.title = title
    snippet.description = description
    snippet.code = code
    snippet.author = author
    snippet.python_version = python_version
    snippet.save()

    return redirect(reverse("snip:snippet", args=(snippet.sid,), kwargs={}))
