from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from .models import Markdown


from django.core.files.storage import FileSystemStorage

#Import Converter Script
from . import script
from .script import html_to_markdown, get_md


# Create your views here.
def home(request):

	if request.method == 'POST':

		#Check if there's an uploaded file:
		try:
			uploaded_file = request.FILES['upload'] #request.FILES is a dictionary with keys = name of form input
		except:
			error = 'Please upload a .html file'
			return render(request, 'index.html', {'error': error})

		#Read uploaded HTML & Convert to txt

		styling_dict = {
		    'title': '#',
		    'author': "##",
		    'section' : "###",
		    'location' : "*",
		    'note' : ">"
		}
		
		title = get_md(request.POST.getlist('title_sel')[0])
		author = get_md(request.POST.getlist('author_sel')[0])
		section = get_md(request.POST.getlist('section_sel')[0])
		location = get_md(request.POST.getlist('location_sel')[0])




		styling_dict['title'] = title
		styling_dict['author'] = author
		styling_dict['section'] = section
		styling_dict['location'] = location


		file_name = uploaded_file.name
		file_name = file_name[:-5] #Remove .html from name

		data = uploaded_file.read() #data is the .html file
		try: 
			markdown_txt = html_to_markdown(data, styling_dict) #markdown_txt is the converted markdown txt

		except:
			error = 'Incorrect HTML format'
			return render(request, 'index.html', {'error': error})

		md = Markdown(name=file_name, content=markdown_txt)

		Markdown.objects.all().delete()
		md.save()

		# response = HttpResponse(txt_file, content_type = 'application/text charset = utf-8')
		# response['Content-Disposition'] = 'attachment; filename="test.txt"'
		# return response
		
		return redirect('/download/{}'.format(file_name))

	return render(request, 'index.html', {})


def download(request, file_name):

	if request.method == 'POST':

		md_txt = Markdown.objects.all()
		md_txt = md_txt[0]

		#Convert object to .txt file
		response = HttpResponse(md_txt.content, content_type = 'application/text charset = utf-8')
		response['Content-Disposition'] = 'attachment; filename="{}.md"'.format(md_txt.name)

		#Remove object from DB
		md_txt.delete()

		return response

		#return render(request, 'download.html', {})


	return render(request, 'download.html', {'file_name': file_name})


def about(request):

	return render(request, 'about.html', {})


