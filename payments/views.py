from django.shortcuts import render
import uuid
import requests
from django.contrib.auth.decorators import login_required
from students.models import StudentProfile
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
# Create your views here.
from django.http import HttpResponse, JsonResponse
from .models import Fee, Payment, FeeAmount
from .forms import PaymentForm
from students.models import StudentProfile
import random
import string
from django.template.loader import get_template
from paystackapi.paystack import Paystack
from paystackapi.transaction import Transaction
import qrcode
import base64
from django.contrib.sites.shortcuts import get_current_site
from io import BytesIO
from django.conf import settings
from students.decorators import *






@login_required
def index(request):
    return render(request, 'payments/payment.html')

# def verify_reciept(request, reference):
#     payment = get_object_or_404(Payment, reference=reference)
#     student = payment.user.studentprofile
#     context = {
#         'payment': payment,
#         'student': student,
#     }
#     return render(request, 'payments/verify-reciept.html', context)


def generate_qr_code(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    return img

# def render_to_pdf(template_src, context_dict):
#     template = get_template(template_src)
#     html = template.render(context_dict)
#     result = HttpResponse(content_type='application/pdf')
#     result['Content-Disposition'] = 'attachment; filename="Payment-reciept.pdf"'
#     pisa_status = pisa.CreatePDF(html, dest=result)
#     if pisa_status.err:
#         return HttpResponse('We had some errors <pre>' + html + '</pre>')
#     return result

# def reciept2pdf(request, reference):
#     payment = get_object_or_404(Payment, reference=reference)
#     student = get_object_or_404(StudentProfile, user=payment.user)
#     matric = student.user.username
#     date = payment.timestamp
#     current_site = get_current_site(request)
#     site_url = current_site.domain

#     qr_data = f"http://{site_url}/payments/verify-reciept/{payment.reference}"
#     qr_code_img = generate_qr_code(qr_data)
    
#     buffer = BytesIO()
#     qr_code_img.save(buffer, format='PNG')
#     qr_code_data = base64.b64encode(buffer.getvalue()).decode('utf-8')
    
#     if not qr_code_data:
#         print("QR code data generation failed")
    
    
#     context = {
#         'payment': payment,
#         'date': date,
#         'student': student,
#         'qrcode': qr_code_data,
#         'matric': matric,
#     }
#     return render_to_pdf('payments/reciept.html', context)


# def verify_reciept(request, reference):
#     payment = get_object_or_404(Payment, reference=reference)
#     student = payment.user.studentprofile
#     context = {
#         'payment': payment,
#         'student': student,
#     }
#     return render(request, 'payments/verify-reciept.html', context)


def print_reciept(request, reference):
    payment = get_object_or_404(Payment, reference=reference)
    student = get_object_or_404(StudentProfile, user=payment.user)
    matric = student.user.username
    date = payment.timestamp
    current_site = get_current_site(request)
    site_url = current_site.domain

    qr_data = f"http://{site_url}/payments/reciept2pdf/{payment.reference}"
    qr_code_img = generate_qr_code(qr_data)
    
    buffer = BytesIO()
    qr_code_img.save(buffer, format='PNG')
    qr_code_data = base64.b64encode(buffer.getvalue()).decode('utf-8')
    
    if not qr_code_data:
        print("QR code data generation failed")
    
    
    context = {
        'payment': payment,
        'date': date,
        'student': student,
        'qrcode': qr_code_data,
        'matric': matric,
    }
    return render(request, 'payments/reciept.html', context)



paystack = Paystack(secret_key=settings.PAYSTACK_SECRET_KEY)


def generate_reference():
    return str(uuid.uuid4())


def get_levels(request):
    fee_id = request.GET.get('fee_id')
    levels = FeeAmount.objects.filter(fee_id=fee_id).values_list('level_id', 'level__level')
    level_dict = {level_id: level_name for level_id, level_name in levels}
    print(level_dict)
    return JsonResponse(level_dict)

def get_amount(request):
    fee_id = request.GET.get('fee_id')
    level_id = request.GET.get('level_id')
    try:
        amount = FeeAmount.objects.get(fee_id=fee_id, level_id=level_id).amount
        feeamount = FeeAmount.objects.get(fee_id=fee_id, level_id=level_id)
        return JsonResponse({'amount': amount})
    except FeeAmount.DoesNotExist:
        return JsonResponse({'amount': 'Not found'})




@login_required
# @profile_completed_required
def initialize_payment(request):
    fees = Fee.objects.all()
    print(f"fee is {fees}")
    current_site = get_current_site(request)
    site_url = current_site.domain
    print(site_url)
    reciepts = Payment.objects.filter(user=request.user)
    if request.method == 'POST':
        fee_id = request.POST.get('fee')
        level_id = request.POST.get('level')  # Get the selected level ID
        print(f"fee id {fee_id} - level id {level_id}")
        try:
            fee = Fee.objects.get(pk=fee_id)
            level = Level.objects.get(pk=level_id) 
            feeamount = FeeAmount.objects.get(fee=fee, level=level)
            print(feeamount.amount)
        
            reference = generate_reference()
            print(f"refrence is {reference}")
            payment = Payment.objects.create(
                user=request.user,
                fee=feeamount,
                reference=reference
            )
            callback_url = request.build_absolute_uri(reverse('payments:verify_payment', args=[reference]))

            response = Transaction.initialize(
                reference=reference,
                amount=int(feeamount.amount * 100),  # Paystack amount is in kobo
                email=request.user.studentprofile.inst_email,
                callback_url=callback_url,
                logo='https://logodix.com/logo/1931260.png',  # Replace with your logo URL

            )
            if response['status']:
                return redirect(response['data']['authorization_url'])
            else:
                payment.delete()
        except (Fee.DoesNotExist, Level.DoesNotExist, FeeAmount.DoesNotExist):
            messages.error(request, "Invalid fee or level selection.")
    # else:
    #     form = PaymentForm()
    return render(request, 'payments/initialize_payment.html', {
                                                                'fees': fees,
                                                                'reciepts': reciepts,
                                                                    })


@login_required
def verify_payment(request, reference):
    payment = get_object_or_404(Payment, reference=reference)
    response = Transaction.verify(reference=reference)
    if response['status'] and response['data']['status'] == 'success':
        payment.verified = True
        payment.save()
        messages.success(request, "Payment verified successfully.")
        print("seccess")
    else:
        messages.error(request, "Payment verification failed.")
        print("error")
    return redirect('payments:initialize_payment')







# def verify_payment(request, ref):
#     try:
#         fee = Fee(request)
#         payment = Payments.objects.get(ref=ref)
#         verified = payment.verify_payment()

#         if verified:
#             last_order = Order.ob