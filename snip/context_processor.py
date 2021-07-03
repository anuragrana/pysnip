from django.conf import settings
import os


# context processor can be used to pass some parameter to all templates from one place
def site(request):
    data = dict()
    data["project_name"] = settings.PROJECT_NAME
    data["project_name_spaced"] = settings.PROJECT_NAME_SPACED
    data["site_url"] = settings.SITE_URL
    data["page_canonical_url"] = request.build_absolute_uri()
    data["seo_keywords"] = settings.SEO_KEYWORDS
    data['site_description'] = settings.SITE_DESC
    data['site_image'] = settings.SITE_URL + os.path.join(settings.STATIC_URL,  "snip/zen-of-python.png")
    # print(data)
    return data
