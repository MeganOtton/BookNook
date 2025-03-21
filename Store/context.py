def device_type_context(request):
    print (request.session.get('device_type'))
    return {
        'device_type': request.session.get('device_type') 

    }