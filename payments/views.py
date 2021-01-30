# payments/views.py
import stripe
import json

from django.conf import settings # new
from django.http.response import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt # new
from django.views.generic.base import TemplateView

from accounts.models import User


class HomePageView(TemplateView):
    template_name = 'payments/home.html'


# new
@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)


@csrf_exempt
def create_checkout_session(request):
    if request.method == 'GET':
        domain_url = 'http://localhost:8000/payments/'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            # Create new Checkout Session for the order
            # Other optional params include:
            # [billing_address_collection] - to display billing address details on the page
            # [customer] - if you have an existing Stripe Customer ID
            # [payment_intent_data] - capture the payment later
            # [customer_email] - prefill the email input in the form
            # For full details see https://stripe.com/docs/api/checkout/sessions/create

            # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
            checkout_session = stripe.checkout.Session.create(
                client_reference_id=request.user.id if request.user.is_authenticated else None,
                customer_email=request.user.email if request.user.is_authenticated else None,
                success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'cancelled/',
                payment_method_types=['card'],
                mode='payment',
                line_items=[
                    {
                        'name': 'Ghostrr Credits',
                        'quantity': 1,
                        'currency': 'usd',
                        'amount': '2500',
                    }
                ]
            )
            print(dir(stripe.checkout.Session.create))
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})


class SuccessView(TemplateView):
    template_name = 'payments/cancelled.html'
    extra_context = {
        'title': 'Ghostrr Credit',
        'status_title': 'Payment Successful',
        'message': 'Your payment has been created successfully. When we verify the transfer your Ghostrr credits will be transferred to your account. It may take at least some minutes',
        'link_name': 'account',
        'link_text': 'My Account',
    }


class CancelledView(TemplateView):
    template_name = 'payments/cancelled.html'
    extra_context = {
        'title': 'Ghostrr Credit Payment Cancelled',
        'status_title': 'Payment Cancelled',
        'message': 'The payment process was interuppted and could not be completed successfully. Check the details of your payment if it was correct, you can try to buy again with the button below',
        'link_name': 'pricings',
        'link_text': 'Buy credits',
    }


@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        print("Payment was successful.")
        # print(request.body)
        # with open('payments/user_payments.json', 'w') as fric:
        #     datas = json.dumps(request.body.decode())
        #     fric.write(datas)
        # print('Json loaded succesfully')
        # TODO: run some custom code here

        # Get the client_reference_id and the product
        payment_json = json.loads(request.body.decode())
        client_reference_id = payment_json['data']['object']['client_reference_id']
        user = User.objects.get(pk=client_reference_id)
        user.profile.credit = user.profile.credit + 200
        user.profile.level = '1'
        user.profile.save()



    return HttpResponse(status=200)