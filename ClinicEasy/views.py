def service_details(request, name):
    return render(request, 'service_details.html', {
        'service': name
    })