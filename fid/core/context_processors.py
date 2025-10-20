def es_playero(request):
    if not request.user.is_authenticated:
        return {'es_playero': False}
    try:
        is_playero = request.user.groups.filter(name='playero').exists()
    except Exception:
        is_playero = False
    return {'es_playero': is_playero}
