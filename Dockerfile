FROM tp33/django:1.2

RUN pip install --upgrade pip \ 
	&& pip install requests