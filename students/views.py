from django.shortcuts import render, get_list_or_404, get_object_or_404,redirect
from . models import *
from .decorators import *
# from.forms import *
from datetime import date
from django.http import JsonResponse
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives, EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.encoding import force_bytes, force_str
from django.utils.crypto import get_random_string
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, logout, login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import StudentProfileForm, ProfilePictureForm, RegisterForm, LoginForm, PasswordResetForm
# views.py
from django.http import HttpResponse
from django.template.loader import get_template
import string
import random
from django.contrib.auth.hashers import make_password


# Create your views here.

@login_required
@profile_completed_required
def index(request):
    studentprofile = request.user.studentprofile
    #  try:
    #     profile = request.user.studentprofile
    # except StudentProfile.DoesNotExist:
    #     profile = StudentProfile(user=request.user)

    print(f"your student profile is {studentprofile}")

    context = {
        
        'student': studentprofile
    }
    return render(request, 'students/students.html', context)



# def render_to_pdf(template_src, context_dict):
#     template = get_template(template_src)
#     html = template.render(context_dict)
#     result = HttpResponse(content_type='application/pdf')
#     result['Content-Disposition'] = 'attachment; filename="user_profile.pdf"'
#     pisa_status = pisa.CreatePDF(html, dest=result)
#     if pisa_status.err:
#         return HttpResponse('We had some errors <pre>' + html + '</pre>')
#     return result


# # @profile_completed_required
# def user_profile_pdf(request):
#     today = date.today() 
#     user_profile = get_object_or_404(StudentProfile, user=request.user)
#     context = {
#         'student': user_profile,
#         'today': today,
#     }
#     return render_to_pdf('app/profilepdf.html', context)




# def get_departments(request):
#     faculty_id = request.GET.get('faculty_id')
#     departments = Department.objects.filter(faculty_id=faculty_id).values_list('id', 'name')
#     department_dict = {dept_id: dept_name for dept_id, dept_name in departments}
#     return JsonResponse(department_dict)


# EDIT USER INFORMATION
# def edit_details(request):
#     try:
#         profile = request.user.studentprofile
#     except StudentProfile.DoesNotExist:
#         profile = StudentProfile(user=request.user)

#     if request.method == 'POST':
#         form = StudentProfileForm(request.POST, instance=profile)

#         if form.is_valid():
#             form.save()
            
#             messages.success(request, "Profile updated successfully.")
#             return redirect('students:reset-info')  # Adjust to your actual profile page URL name
#         else:
#             messages.error(request, "Please correct the errors below.")
#     else:
#         form = StudentProfileForm(instance=profile)
#         # profile_picture_form = ProfilePictureForm()    
#     return render(request, "students/edit-details.html", {
#         'form': form,
#         'profile': profile,
#         'pic_form': ProfilePictureForm,
#         })
#     # return render(request, "students/edit-details.html", context)


def get_departments(request):
    faculty_id = request.GET.get('faculty_id')
    departments = Department.objects.filter(faculty_id=faculty_id).values_list('id', 'name')
    department_dict = {dept_id: dept_name for dept_id, dept_name in departments}
    return JsonResponse(department_dict)

def edit_details(request):
    profile = get_object_or_404(StudentProfile, user=request.user)
    faculties = Faculty.objects.all()  
    levels = Level.objects.all()  
    selected_faculty_id = profile.faculty.id if profile.faculty else None

    # Fetch departments related to the selected faculty
    if selected_faculty_id:
        departments = Department.objects.filter(faculty=profile.faculty)
    else:
        departments = []

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        other_names = request.POST.get('other_names')
        admission_year_id = request.POST.get('admission_year')
        faculty_id = request.POST.get('faculty')
        department_id = request.POST.get('department')
        phone_number = request.POST.get('phone_number')
        state = request.POST.get('state')
        nationality = request.POST.get('nationality')
        gender = request.POST.get('Gender')
        inst_email = request.POST.get('inst_email')

        try:
            admission_year = Level.objects.get(pk=admission_year_id)
            faculty = Faculty.objects.get(pk=faculty_id)
            department = Department.objects.get(pk=department_id)

            profile.first_name = first_name
            profile.last_name = last_name
            profile.other_names = other_names
            profile.matric_no = profile.user.username
            profile.admission_year = admission_year
            profile.faculty = faculty
            profile.department = department
            profile.phone_number = phone_number
            profile.state = state
            profile.nationality = nationality
            profile.Gender = gender  # Set the Gender attribute
            profile.user.email = inst_email
            profile.inst_email = inst_email
            profile.account_completed = True
            profile.email_verified = True
            profile.save()

            messages.success(request, "Profile updated successfully.")
            return redirect('students:reset-info')
        except (Level.DoesNotExist, Faculty.DoesNotExist, Department.DoesNotExist):
            messages.error(request, "Invalid selection for admission year, faculty, or department.")
   

    return render(request, "students/edit-details.html", {
        'pic_form': ProfilePictureForm,
        'profile': profile,
        'faculties': faculties,
        'levels': levels,
        'selected_faculty_id': selected_faculty_id,
        'departments': departments, 

    })


def edit_profilepicture(request):
    try:
        profile = request.user.studentprofile
    except StudentProfile.DoesNotExist:
        profile = StudentProfile(user=request.user)

    if request.method == 'POST':
        profile_picture_form = ProfilePictureForm(request.POST, request.FILES, instance=profile)

        if profile_picture_form.is_valid():
            profile_picture_form.save()
            messages.success(request, "Profile picture updated successfully.")
            return redirect('students:reset-info')  # Adjust to your actual profile page URL name
        else:
            messages.error(request, "Please correct the errors below.")
    return redirect("student:reset-info")



# EDIT USER PASSWORD
@login_required
@profile_completed_required
def change_password(request):
    if request.method == "POST":
        try:
            old_password = request.POST.get('old_password')
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')

            print(f"your pass is {new_password} and {confirm_password}")

            if new_password != confirm_password:
                print("passwords do not match.")
                messages.error(request, " passwords do not match.")
                return redirect('students:reset-password')

            user = request.user
            if not user.check_password(old_password):
                messages.error(request, "Old password is incorrect.")
                return redirect('students:reset-password')

            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)  # Keeps the user logged in after password change
            messages.success(request, "Your password has been updated successfully.")
            print("success")
            return redirect('students:reset-password')
        except Exception as e:
            print(f"passsword update error is {e}")
            # messages.error(request, "An error occured!.")
    return render(request, "students/change-password.html")




def generate_random_password(length=6):  # Set the default length to 6
    # Generate a random string of digits only
    digits = string.digits 
    return ''.join(random.choice(digits) for i in range(length))



@auth_user_should_not_access
def register_user(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            matric = form.cleaned_data['matric']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']

            # Create the user
            user = User.objects.create_user(username=matric, email=email, password=password)
            user.save()

            messages.success(request, "Your account has been created successfully. You can now log in.")
            return redirect('students:login_user')  # Adjust this to your login URL
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = RegisterForm()


    return render(request, 'app/register.html', {'form': RegisterForm})



# LOGIN PAGE
@auth_user_should_not_access
def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            matric = form.cleaned_data['matric']
            password = form.cleaned_data['password']
            user = authenticate(request, username=matric, password=password)
            if user is not None:
                login(request, user)
                return redirect('students:index')  # Redirect to the desired page after login
            else:
                messages.error(request, "Invalid username or password.")

                form.add_error(None, 'Invalid username or password')
    else:
        form = LoginForm()

    context = {
        'form': form,
    }
    return render(request, 'app/login_user.html', context)



@auth_user_should_not_access
def forget_password(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                
                # Generate a new random password
                new_password = generate_random_password()
                print(new_password)
                
                # Set the new password for the user
                
                # Email content
                mail_subject = 'Password Reset Request'
                
                # Create the HTML message using a template
                html_message = render_to_string('app/password_reset_email.html', {
                    'username': user.username,
                    'new_password': new_password,
                })
                
                # Create the plain text message from the HTML content
                plain_message = strip_tags(html_message)

                # Send the email
                email = EmailMultiAlternatives(
                    subject=mail_subject,
                    body=plain_message,
                    from_email=None,  # Uses the EMAIL_HOST_USER defined in settings.py
                    to=[user.email],
                )
                
                # Attach the HTML content to the email
                email.attach_alternative(html_message, "text/html")
                email.send()
                print(f"email sent")
                user.set_password(new_password)
                user.save()
                print("password set")
                
                
                messages.success(request, "A new password has been sent to your email.")
                return redirect('students:login_user')
            except Exception as e:
                print(f"your error is {e}")
                form.add_error('email', "No account is associated with this email address.")
                messages.error(request, "Invalid email address")
    else:
        form = PasswordResetForm()

    return render(request, 'app/forget_password.html', {'form': form})



@login_required
def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('students:login_user')  