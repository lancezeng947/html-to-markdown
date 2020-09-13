from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegisterForm

# Types of messages:
# messages.debug
# messages.info
# messages.success
# messages.warning
# messages.error

# Create your views here.
def register(request):


	if request.method == 'POST':	
		form = UserRegisterForm(request.POST)

		print(form.is_valid())

		if form.is_valid():
			form.save()

			return redirect('/')

	else:
		form = UserRegisterForm()

	return render(request, 'register.html', {'form': form})

