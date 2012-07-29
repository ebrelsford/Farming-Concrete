def is_mobile(request):
    try:
        ua = request.META['HTTP_USER_AGENT'].lower()
    except KeyError:
        ua = ''
    return 'iphone' in ua or 'android' in ua
