# Messenger web application

## Essay

Five flaws from [OWASP 2017 top ten list](https://owasp.org/www-project-top-ten/) and how to fix them.

Installation instruction are omitted because Django framework is used as instructed in course and project description.

### Link
[Messenger git hub repository]()

### FLAW 1 - A01:2017-Injection / A03:2021-Injection
1. Source: [views.py line 28]()
user_filter_id = User.objects.raw(f"SELECT id, username FROM auth_user WHERE username='{str(filter_username)}' ORDER BY id")[0].id
2. Description: SQL injection vulnerability. Any maliculous username can be used for injections.
3. How to fix: Change raw SQL handling to ORM by changing affected lines to:
user_filter_id = User.objects.filter(username=filter_username)[0].id

### FLAW 2 - A07:2017-Cross-Site Scripting (XSS) / A03:2021-Injection
1. Source: [views.py line 65]()
def profile(request, user_id):
    current_user = User.objects.get(id=int(user_id.split()[0]))
    html_str = '<link rel="shortcut icon" href="/static/images/favicon.png"/>\n'
    html_str = html_str + f"Showing page for user_id: {user_id}\n"
    html_str = html_str + f'<p>Username = {current_user.username} \
                            <p>First Name = {current_user.first_name} \
                            <p>Last Name = {current_user.last_name}'
    return HttpResponse(html_str)
2. Description: Unsanitazed user input is being parsed as html
3. How to fix: Change function profile in views.py:
def profile(request):
    current_user = request.user
    user_data = {"username": current_user.username,
                "first_name": current_user.first_name,
                 "last_name": current_user.last_name}
    return render(request, 'messenger/profile.html', context=user_data)

Introduce [profile.html]() template:
        Showing page for user_id: {{user_id}}
        <p>
        Username: {{ user.username }}
        <p>
        First Name: {{ user.first_name }}
        <p>
        Last Name: {{ user.last_name }}

Change [index.html line 47]():
User profile: <a href="profile/{{user.id}}">{{user.username}}</a>
to
User profile: <a href="profile">{{user.username}}</a>

Change [urls.py line 36]():
    path('profile/<str:user_id>', messenger_views.profile, name="profile"),
to
    path('profile/', messenger_views.profile, name="profile"),

### FLAW 3 - A06:2016-Security Misconfiguration / A05:2021-Security Misconfiguration
1. Source: [setting.py line 28]()
DEBUG = True
2. Description: Debug mode is left on in setting.py
3. How to fix: Change the affected line to:
DEBUG = False

### FLAW 4 A05:2017-Broken Access Control / A01:2021-Broken Acces Control
1. Source: [views.py line 65]()
2. Description: Access to user data is not done secure way but as GET parameter which can be altered by anybody to see any user profile
3. How to fix: Using request.user to get current user to show only current logged in user profile as instructed in FLAW 2 section.

### FLAW 5 A03:2017-Sensitive Data Exposure / A02:2021-Cryptographic Failures or A04:2021-Insecure Design
1. Source: [setting.py line 28]()
2. Description: Sensitive data leakage as secret key is stored in github repository
3. How to fix: Remove the line and replace with:
    with open('/etc/secret_key.txt') as f:
        SECRET_KEY = f.read().strip()
or
    import os
    SECRET_KEY = os.environ['SECRET_KEY']
Do not keep secret_key.txt in the github repository

### FLAW 6
1. Source: Everywhere
2. Description: HTTPS not enabled
3. How to fix: In production server enable in setting.py
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True


## Notes for developer how to start and run a Django project

[Writing your first Django app, part 1](https://docs.djangoproject.com/en/3.1/intro/tutorial01/)

1. In project folder "django-admin startproject config" where config can be any folder name.

2. In project folder "python manage.py startapp messenger" where messenger is any app name.

3. In folder 'messenger' views.py def index(request) handles index page

4. Create messenger/urls.py and other editing and definitely editing settings.py

5. python manage.py migrate

6. edit messenger/models.py models

7. python manage.py makemigrations messenger