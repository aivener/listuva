FROM tp33/django-docker:1.3

RUN pip install --upgrade pip \ 
	&& pip install requests \ 
	&& pip install kafka-python
