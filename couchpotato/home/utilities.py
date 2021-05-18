from home.models import ApplicationFeatures 


def index_page_permitted(request):
    '''
    Description : 
    
    limit_user_signup is the feature added to prevent the create account option in the software. 

    if 
        user feature is present , 
        then it looks for authentication 
        and if logged in then load the index page
    else if 
        signup feature is not at all 
        present then load the index page
    '''
    app_feature = ApplicationFeatures.objects.filter(id=1).first()
    allowed = request.user.is_authenticated or (app_feature.signup is False)
    return allowed

def register_login_page_permitted():
    '''
    Description : 
    
    if 
        user feature is present , 
        then it looks for authentication 
        and if logged in then load the index page

    '''
    app_feature = ApplicationFeatures.objects.filter(id=1).first()
    allowed = app_feature.signup
    return allowed

def allow_login(request, user):
    '''
    Description : 
    
    check if the app allows login feature from index pafe. This is provided by admin
         

    '''
    app_feature = ApplicationFeatures.objects.filter(id=1).first()
    allowed = (app_feature.signup is True and user.is_active) or (app_feature.signup is False and user.is_superuser)
    return allowed

def allow_register():
    '''
    Description : 
    
    check if the app allows register feature from index pafe. This is provided by admin
         
    '''
    app_feature = ApplicationFeatures.objects.filter(id=1).first()
    allowed = (app_feature.signup is True and app_feature.limit_user_signup is False)
    return allowed