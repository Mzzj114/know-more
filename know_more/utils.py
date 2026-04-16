from django.utils.translation import get_language_from_request

def get_language(request):
    """Returns ether 'zh' or 'en'"""
    lang_code = get_language_from_request(request, check_path=True)
    print("language code is ", lang_code)
    # Convert 'zh-hans' or 'zh-hant' to 'zh'
    if lang_code.startswith('zh'):
        return 'zh'
    # Default to 'en' for any other language
    return 'en'