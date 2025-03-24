def device_type_context(request):
    return {
        'device_type': request.session.get('device_type') 

    }