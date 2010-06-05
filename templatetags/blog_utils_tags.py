import re

from django.template import Library, Node, Template, Context
from django.template.defaultfilters import stringfilter
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

from django.conf import settings

register = Library()
def get_image(image):
	from photologue.models import Photo
	if Photo.objects.filter(title = image).count():
		return Photo.objects.get(title=image)
	if Photo.objects.filter(title_slug = image).count():
		return Photo.objects.get(title_slug=image)
	return False 

def get_photologue_html(size,image):
	image = get_image(image)
	if not image:
		return "Bad image name" 
	if size.lower() == "thumb":
		template = "photologue/thumb_snippet.html"
	else:
		template = "photologue/image_snippet.html"

	return render_to_string(template,{'image': image })

pattern = re.compile(r'\[\[([^:]+):(.+)\]\]')

@register.filter
@stringfilter
def photologue(content):
	content = pattern.sub(lambda match: get_photologue_html(match.group(1),match.group(2)),content)
	if '[[COLUMN]]' in content:
		column_content = []
		for i in content.split('[[COLUMN]]'):
			column_content.append('<div class="column">%s</div>' % (str(i)))
		return mark_safe("".join(column_content))
	return mark_safe(content)

@register.filter
@stringfilter
def private(content):
	pattern = re.compile(r'\(\(.*?\)\)')
	return mark_safe(pattern.sub('...',content))

@register.inclusion_tag('blog_utils/FB.html')
def FB():
	return {'key': settings.FACEBOOK_API_KEY }

@register.inclusion_tag('blog_utils/GA.html')
def GA():
	return {'GA': settings.GA }

@register.inclusion_tag('add_this.html')
def add_this(url,title):
	from django.contrib.sites.models import Site
	site = Site.objects.get_current()
	if hasattr(settings,'ADD_THIS_USERNAME'):
		username = settings.ADD_THIS_USERNAME
		return {'url': url, 'title': title, 'username': username, 'site': site }
