from django.shortcuts import redirect, render
from django.urls import reverse
from django.conf import settings
from django.http import HttpResponse
from django.utils.text import slugify
import random
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter, ImageFormatter
from django.contrib.auth import logout, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import requests
from .models import SnippetModel, UpvoteModel
import logging
import traceback
from django.contrib import messages
from django.db.models import Q
import io
from django.core.files.images import ImageFile


def index(request):
    template_name = "snip/index.html"
    template_data = dict()
    recent_snippets = SnippetModel.objects.all().order_by('-created_date')[:10]
    template_data['recent_snippets'] = recent_snippets

    top_rated_snippets = SnippetModel.objects.all().order_by('-upvotes')[:10]
    template_data['top_rated_snippets'] = top_rated_snippets

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
    # create 404 page here

    lexer = get_lexer_by_name("python", stripall=True)

    # if image does not exists in snippet instance, create one, save it
    if not snippet.image:
        img_formatter = ImageFormatter(
            image_format="PNG",
            cssclass="highlight",
            style="fruity",
            noclasses=True,
            linenos=False,
        )
        img_result = highlight(snippet.code, lexer, img_formatter)
        # img_result is - bytes
        # https://stackoverflow.com/a/62624236/2291289
        filename = slugify(snippet.title) + ".png"
        image = ImageFile(io.BytesIO(img_result), name=filename)
        snippet.image = image
        snippet.save()

    # HTML formatter
    formatter = HtmlFormatter(
        linenos='table',
        cssclass="highlight",
        style="fruity",
        noclasses=True,
        prestyles="padding-left:10px"  # for gap between line number and code
    )

    result = highlight(snippet.code, lexer, formatter)
    # print(result)

    already_upvoted = False
    if not request.user.is_anonymous:
        already_upvoted = UpvoteModel.objects.filter(Q(snippet=snippet) & Q(user=request.user)).exists()
    template_data['already_upvoted'] = already_upvoted
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
    filename = slugify(snippet.title) + ".png"
    response = HttpResponse(snippet.image.read(), content_type='image/png')
    response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)
    return response


def archive(request):
    template_data = dict()
    template_name = 'snip/archive.html'
    template_data['all_snippets'] = SnippetModel.objects.all()
    return render(request, template_name, template_data)


def mylogin(request):
    template_name = 'snip/login.html'
    return render(request, template_name, {})


@login_required
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
    python_version = post_data.get('python_version')

    if not all([title, code, python_version]):
        # TODO: use messaging here
        return render(request, template_name, template_data)

    snippet = SnippetModel()
    snippet.title = title
    snippet.description = description
    snippet.code = code
    snippet.author = request.user
    # create the author name
    author = None
    if request.user.first_name:
        author = request.user.first_name
    if author and request.user.last_name:
        author = author + " " + request.user.last_name
    if not author:
        author = request.user.username

    snippet.author_name = author
    snippet.python_version = python_version
    snippet.save()

    return redirect(reverse("snip:snippet", args=(snippet.sid,), kwargs={}))


def login_github(request):
    client_id = settings.GITHUB_CLIENT_ID
    scope = 'read:user'
    state = 'somerandomstring123'  # to prevent csrf
    return redirect(
        'https://github.com/login/oauth/authorize?client_id={}&scope={}&state={}'.format(client_id,
                                                                                         scope, state,
                                                                                         ))


def login_github_callback(request):
    # verify the state variable value for csrf
    code = request.GET.get('code', None)

    if not code:
        messages.error(request, "Invalid Code received from Github Auth API");
        logging.getLogger('error').error('code not present in request {}'.format(request.GET))
        return redirect(reverse("snip:index", args=(), kwargs={}))

    # first redirect
    params = {
        'client_id': settings.GITHUB_CLIENT_ID,
        'client_secret': settings.GITHUB_SECRET,
        'code': code,
        'Content-Type': 'application/json'
    }

    headers = {
        'Accept': 'application/json'
    }

    result = requests.post('https://github.com/login/oauth/access_token', data=params, headers=headers)
    # print(result)
    # print(result.text)
    # print(result.json())
    token = result.json().get('access_token')
    logging.getLogger('info').info('token received in response from github')
    # after getting the token, access the user api to get user details
    user_api_url = 'https://api.github.com/user'
    headers = {
        'Authorization': 'token ' + token,
        'Accept': 'application/json'
    }
    result = requests.get(user_api_url, headers=headers)
    # print(result.json())
    user_data = result.json()
    logging.getLogger('info').info('user data from github {}'.format(user_data))
    email = user_data.get('email', None)
    if not email:
        messages.error(request, "Invalid data received from GitHub");
        logging.getLogger('error').error('email not present in data received from github {}'.format(user_data))
        return redirect(reverse("snip:index", args=(), kwargs={}))

    # get the user details, now login this user.

    try:
        user = User.objects.get(email=email)
        logging.getLogger('info').info('user already exists in db')
    except User.DoesNotExist as e:
        # if user does not exists in db, create a user and save it.
        name = user_data.get('name', None)
        username = user_data.get('username', None)
        if name:
            splitted_name = name.split(' ')
            first_name = splitted_name[0]
            if len(splitted_name) > 1:
                last_name = splitted_name[1]
            else:
                last_name = ''
        else:
            first_name = ''
            last_name = ''

        # create user
        user = User()
        user.username = username
        user.email = email
        user.first_name = first_name
        user.last_name = last_name
        user.is_admin = False
        user.is_active = True
        user.is_superuser = False

        user.save()
        logging.getLogger('info').info('user created in db')

    except Exception as e:
        messages.error(request, "Some error occurred while logging. Please let us know.")
        logging.getLogger('error').error(traceback.format_exc())

    login(request, user)
    messages.success(request, "Login Successful");
    return redirect(reverse("snip:index", args=(), kwargs={}))


def author_page(request, author_username):
    template_data = dict()
    template_name = 'snip/author.html'
    template_data['author'] = author_instance = User.objects.get(username=author_username)
    template_data['all_snippets'] = SnippetModel.objects.filter(author_id=author_instance.id)

    author_name = ''
    if author_instance.first_name:
        author_name = author_instance.first_name
    else:
        author_name = author_instance.username
    template_data['author_name'] = author_name

    # if author_username is the current user logged in i.e. if logged in user wants to see his/her details
    # fetch those details here and do it.
    # add conditions on HTML if required.
    template_data['logged_in_user_data'] = 'GET DATA HERE'

    return render(request, template_name, template_data)


@login_required
def upvote_snippet(request, snippet_id):
    snippet = None
    try:
        snippet = SnippetModel.objects.get(sid=snippet_id)
    except SnippetModel.DoesNotExist as e:
        logging.getLogger('error').error('Snippet does not exists {}'.format(snippet_id))
        return redirect(reverse("snip:index", args=(), kwargs={}))

    # add the upvote to Upvotes Table
    upvote_instance = UpvoteModel()
    upvote_instance.user = request.user
    upvote_instance.snippet = snippet
    try:
        upvote_instance.save()
        # exception if this combination already exists
    except Exception as e:
        logging.getLogger('error').error(traceback.format_exc())
        messages.success(request, 'Can not upvote')
        return redirect(reverse("snip:snippet", args=(snippet.sid,), kwargs={}))

    # get total upvotes for this snippet
    snippet_upvote_count = UpvoteModel.objects.filter(snippet=snippet).count()
    # update the snippet count in snippet table.
    # store once. use multiple times when snippet is read.
    snippet.upvotes = snippet_upvote_count
    snippet.save()

    messages.success(request, 'Upvoted')
    return redirect(reverse("snip:snippet", args=(snippet.sid,), kwargs={}))


@login_required
def downvote_snippet(request, snippet_id):
    snippet = None
    try:
        snippet = SnippetModel.objects.get(sid=snippet_id)
    except SnippetModel.DoesNotExist as e:
        logging.getLogger('error').error('Snippet does not exists {}'.format(snippet_id))
        return redirect(reverse("snip:index", args=(), kwargs={}))

    # try to delete a record
    UpvoteModel.objects.filter(Q(snippet=snippet) & Q(user=request.user)).delete()

    # get total upvotes for this snippet
    snippet_upvote_count = UpvoteModel.objects.filter(snippet=snippet).count()
    # update the snippet count in snippet table.
    # store once. use multiple times when snippet is read.
    snippet.upvotes = snippet_upvote_count
    snippet.save()

    messages.warning(request, 'Downvoted')
    return redirect(reverse("snip:snippet", args=(snippet.sid,), kwargs={}))


@login_required
def report_snippet(request, snippet_id):
    snippet = SnippetModel.objects.get(sid=snippet_id)
    messages.error(request, 'Please drop a mail at code108labs@gmail.com to report this.')
    return redirect(reverse("snip:snippet", args=(snippet.sid,), kwargs={}))
