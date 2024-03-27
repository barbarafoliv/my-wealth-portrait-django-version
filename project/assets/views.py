from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Asset

# Create Assets page
@login_required(login_url='/login/')
def assets(request):
	if request.method == 'POST':
		data = request.POST
		name = data.get('name')
		amount = int(data.get('amount', 0))

		Asset.objects.create(
			name=name,
			amount=amount,
		)
		return redirect('/')

	queryset = Asset.objects.all()
	if request.GET.get('search'):
		queryset = queryset.filter(
			name__icontains=request.GET.get('search'))

	# Calculate the total sum
	total_sum = sum(asset.amount for asset in queryset)
	
	context = {'assets': queryset, 'total_sum': total_sum}
	return render(request, 'assets.html', context)

# Update an Asset data
@login_required(login_url='/login/')
def update_asset(request, id):
	queryset = Asset.objects.get(id=id)

	if request.method == 'POST':
		data = request.POST
		name = data.get('name')
		amount = int(data.get('amount', 0))

		queryset.name = name
		queryset.amount = amount
		queryset.save()
		return redirect('/')

	context = {'asset': queryset}
	return render(request, 'update_asset.html', context)

# Delete an Asset data
@login_required(login_url='/login/')
def delete_asset(request, id):
	queryset = Asset.objects.get(id=id)
	queryset.delete()
	return redirect('/')

# Login page for user
def login_page(request):
	if request.method == "POST":
		try:
			username = request.POST.get('username')
			password = request.POST.get('password')
			user_obj = User.objects.filter(username=username).first()
			if not user_obj:
				messages.error(request, "Username not found")
				return redirect('/login/')
			user_auth = authenticate(username=username, password=password)
			if user_auth:
				login(request, user_auth)
				return redirect('assets')
			messages.error(request, "Wrong Password")
			return redirect('/login/')
		except Exception as e:
			messages.error(request, "Something went wrong")
			return redirect('/register/')
	return render(request, "login.html")

# Register page for user
def register_page(request):
	if request.method == "POST":
		try:
			username = request.POST.get('username')
			password = request.POST.get('password')
			user_obj = User.objects.filter(username=username)
			if user_obj.exists():
				messages.error(request, "Username is taken")
				return redirect('/register/')
			user_obj = User.objects.create(username=username)
			user_obj.set_password(password)
			user_obj.save()
			messages.success(request, "Account created")
			return redirect('/login')
		except Exception as e:
			messages.error(request, "Something went wrong")
			return redirect('/register')
	return render(request, "register.html")

# Logout function
def custom_logout(request):
	logout(request)
	return redirect('login')

# Generate the Report
@login_required(login_url='/login/')
def report(request):
	if request.method == 'POST':
		data = request.POST
		name = data.get('name')
		amount = int(data.get('amount', 0))

		Asset.objects.create(
			name=name,
			amount=amount,
		)
		return redirect('report')

	queryset = Asset.objects.all()
	if request.GET.get('search'):
		queryset = queryset.filter(
			name__icontains=request.GET.get('search'))

	# Calculate the total sum
	total_sum = sum(asset.amount for asset in queryset)
	# Get the username
	username = request.user.username

	context = {'assets': queryset, 'total_sum': total_sum, 'username':username}
	return render(request, 'report.html', context)
