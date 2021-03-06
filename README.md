# Messenger web application

### Link
[Messenger git hub repository](https://github.com/ivaeisaenen/CyberSecurityBaseProjectI.git)

Maybe consider reading at git hub for nices formatting?

## Essay

Five flaws from [OWASP 2017 top ten list](https://owasp.org/www-project-top-ten/) and how to fix them. The 2017 list is used but also 2021 name is mentioned in addition of 2017.

Detailed installation instruction are omitted because Django framework is used as instructed in course and project description, but generally should install Django framework and then run:
```python
python manage.py migrate
```
and
```python
python manage.py runserver
```

## Preface

Generally it seems really hard to do insecure design using Django framework but also might be really difficult to find out security flaws as so much is done by Django framework behind the scenes

### FLAW 1 - A01:2017-Injection / A03:2021-Injection
1. Source: [views.py line 30](https://github.com/ivaeisaenen/CyberSecurityBaseProjectI/blob/c666851fafbe2b2c5d6c83741c580d01a0168212/messenger/views.py#L30)
```python
user_filter_id = User.objects.raw(f"SELECT id, username FROM auth_user WHERE username='{str(filter_username)}' ORDER BY id")[0].id
```
2. Description: SQL injection vulnerability. Any malicious username can be used for injections. SQL injections are dangerous as this can lead data alterations including total data destruction and cleverly altered data. Extreme cases there can be added users with admin privileges or other harmful additions which can go totally unnoticed. Total data destruction is at leas usually noticed.
3. How to fix: Change raw SQL handling to ORM by changing affected lines to:
```python
user_filter_id = User.objects.filter(username=filter_username)[0].id
```
### FLAW 2 - A07:2017-Cross-Site Scripting (XSS) / A03:2021-Injection
1. Source: [views.py line 68](https://github.com/ivaeisaenen/CyberSecurityBaseProjectI/blob/c666851fafbe2b2c5d6c83741c580d01a0168212/messenger/views.py#L68)
```python
def profile(request, user_id):
    current_user = User.objects.get(id=int(user_id.split()[0]))
    html_str = '<link rel="shortcut icon" href="/static/images/favicon.png"/>\n'
    html_str = html_str + f"Showing page for user_id: {user_id}\n"
    html_str = html_str + f'<p>Username = {current_user.username} \
                            <p>First Name = {current_user.first_name} \
                            <p>Last Name = {current_user.last_name}'
    return HttpResponse(html_str)
```
2. Description: Unsanitazed user input is being parsed as html
3. How to fix: Change function profile in views.py:
```python
def profile(request):
    current_user = request.user
    user_data = {"username": current_user.username,
                "first_name": current_user.first_name,
                 "last_name": current_user.last_name}
    return render(request, 'messenger/profile.html', context=user_data)
```
Introduce [profile.html]() template:
```html
        Showing page for user_id: {{user_id}}
        <p>
        Username: {{ user.username }}
        <p>
        First Name: {{ user.first_name }}
        <p>
        Last Name: {{ user.last_name }}
```
Change [index.html line 47]():
```html
User profile: <a href="profile/{{user.id}}">{{user.username}}</a>
```
to
```html
User profile: <a href="profile">{{user.username}}</a>
```

Change [urls.py line 36]():
```python
    path('profile/<str:user_id>', messenger_views.profile, name="profile"),
```
to
```python
    path('profile/', messenger_views.profile, name="profile"),
```

### FLAW 3 - A06:2016-Security Misconfiguration / A05:2021-Security Misconfiguration
1. Source: [setting.py line 28](https://github.com/ivaeisaenen/CyberSecurityBaseProjectI/blob/c666851fafbe2b2c5d6c83741c580d01a0168212/cyber3/settings.py#L28)
```python
DEBUG = True
```
2. Description: Debug mode is left on in setting.py. Enabling debug mode greatly increases risk of sensitive data leakage as [Django debug](https://docs.djangoproject.com/en/dev/ref/settings/#debug) informations says "Never deploy a site into production with DEBUG turned on" even they promise they do their best to obscure secure information.
3. How to fix: Change the affected line in setting.py file to following:
```python
DEBUG = False
```

### FLAW 4 A05:2017-Broken Access Control / A01:2021-Broken Access Control
1. Source: [views.py line 62](https://github.com/ivaeisaenen/CyberSecurityBaseProjectI/blob/c666851fafbe2b2c5d6c83741c580d01a0168212/messenger/views.py#L62)
2. Description: Access to user data is not done secure way but as GET parameter which can be altered by anybody to see any user profile:
```python
current_user = User.objects.get(id=int(user_id.split()[0])).
```
There is also ```@csrf_exempt``` decorator for filter_messages_by_users function which should be removed and proper ```{% csrf_token %}``` introduced in the index.html for the given form.

3. How to fix: Using request.user to get current user to show only current logged in user profile as instructed in FLAW 2 section. Generally authentication or confidential data inputs should not be handled using GET commands and authentication should be verified with CSRF token.

### FLAW 5 A03:2017-Sensitive Data Exposure / A02:2021-Cryptographic Failures or A04:2021-Insecure Design
1. Source: [setting.py line 23](https://github.com/ivaeisaenen/CyberSecurityBaseProjectI/blob/c666851fafbe2b2c5d6c83741c580d01a0168212/cyber3/settings.py#L23)
2. Description: Sensitive data leakage as secret key is stored in github repository
3. How to fix:
Remove the line and replace with:
```python
    with open('/etc/secret_key.txt') as f:
        SECRET_KEY = f.read().strip()
```
or
```python
    import os
    SECRET_KEY = os.environ['SECRET_KEY']
```
Do not keep secret_key.txt in the github repository

### FLAW 6 A03:2017-Sensitive Data Exposure / A02:2021-Cryptographic Failures or A04:2021-Insecure Design
1. Source: Everywhere
2. Description: HTTPS not enabled
3. How to fix: In production server enable in setting.py
```python
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
```

### FLAW 7 - A10:2017-Insufficient Logging&Monitoring
1. Source: setting.py and views.py
2. Description:
3. How to fix: As the [Django documentation about logging](https://docs.djangoproject.com/en/4.0/topics/logging/) points out that there is need to add following to setting.py:
```python
import os
LOGGING = {
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
```

Also views.py should be added:
```python
import logging
logger = logging.getLogger('owasp_logger')
```
Then also log interesting events such as maybe successful or/and failed user logins:
```python
    logger.debug(f"Some string telling something happened for username: {user.username}")
```