def es_playero(request):
    """
    Devuelve {'es_playero': True/False} para usar en templates.
    Evita errores si user no está autenticado o no tiene cliente.
    """
    if not request.user.is_authenticated:
        return {'es_playero': False}
    try:
        # Si usás grupo "playero" (recomendado) o el flag en cliente, adaptá:
        # option A: por grupo
        is_playero = request.user.groups.filter(name='playero').exists()
        # option B: por campo en cliente:
        # is_playero = getattr(getattr(request.user, 'cliente', None), 'is_playero', False)
    except Exception:
        is_playero = False
    return {'es_playero': is_playero}
