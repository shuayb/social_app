def set_to_lower_case(request):
    data = request.data.copy()
    if data.get('email'):
        data['email'] = data.get('email').lower()
    return data
