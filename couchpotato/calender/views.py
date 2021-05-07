from django.shortcuts import render

# Create your views here.
from home.utilities import index_page_permitted


def index(request):
      
    # render function takes argument  - request
    # and return HTML as response
    try:
        if index_page_permitted(request):
            return render(request, "calender.html")
        else:
                return render(request, 'login.html')
    except:
        return render(request, '404.html')
 