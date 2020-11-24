from home.models import ApplicationFeatures 


def index_page_permitted(request):
    app_feature = ApplicationFeatures.objects.filter(id=1).first()
    allowed = request.user.is_authenticated or (app_feature.signup is False)
    return allowed

def register_login_page_permitted():
    app_feature = ApplicationFeatures.objects.filter(id=1).first()
    allowed = app_feature.signup
    return allowed

def allow_login(request, user):
    app_feature = ApplicationFeatures.objects.filter(id=1).first()
    allowed = (app_feature.signup is True and user.is_active) or (app_feature.signup is False and user.is_superuser)
    # print("in allow login" , allowed)
    return allowed

def allow_register():
    app_feature = ApplicationFeatures.objects.filter(id=1).first()
    allowed = (app_feature.signup is True)
    return allowed