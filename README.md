# onlinenn
The project for setting up and training of neural networks in the cloud with Keras library.
<h2>How to install in Linux</h2>
<p>1. Download the virtual environment directory (https://cloud.mail.ru/public/9e1g/jXGkprc6f) and put it in the root directory of project.</p>
<p>2. Instal redis-server: </p>
<pre>sudo apt-get install redis-server</pre>
<h2>How to run project in Linux</h2>
<p>1. Open terminal and run redis-server.</p>
<pre>redis-server</pre>
<p>2. Go to the root directory of project in new terminal and run celery.</p>
<pre>source venv/bin/activate</pre>
<pre>python manage.py celeryd</pre>
<p>3. Start django project in root directory of project in new terminal.</p>
<pre>source venv/bin/activate</pre>
<pre>python manage.py runserver</pre>
<p>4. In your browser go to http://127.0.0.1:8000/</p>
