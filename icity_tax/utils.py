import requests
from icity_tax.settings import RECAPTCHA_PUBLIC_KEY


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def check_captcha(request):
    captcha_result = request.data['g-recaptcha-response']
    url = "https://www.google.com/recaptcha/api/siteverify"
    params = {
        'secret': RECAPTCHA_PUBLIC_KEY,
        'response': captcha_result,
        'remoteip': get_client_ip(request)
    }
    verify_result = requests.get(url, params=params, verify=True).json()
    if verify_result.get("success", False):
        return {
            'status': 401,
            'error': verify_result.get('error-codes', None) or "Unspecified error."
        }
    else:
        return {'status': 200}
