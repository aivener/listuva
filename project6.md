##Performance Testing with JMeter

I tested a sequence of actions on our website through our local running of the application and through Digital Ocean. The actions involved, in sequence, logging in, viewing a category, going back to the home page, creating a new post, looking at the new post, and logging out. I tested various number of users on the application (results below). In order to confirm that the proper web page was visited, I created a text response assertion that checked that a certain phrase was one the resulting page. Interestingly, the Digital Ocean hosting of the application had more errors than our local version. I had assumed that the Digital Ocean hosting would handle more users since cloud hosting is designed to gracefully handle an increase and decrease of users. Both applications reached problems with 200 users, but the Digital Ocean hosting had more errors at 150 users as well. The error that occurred was “Non HTTP response message: Operation timed out”. The Digital Ocean hosting has a higher average time (in milliseconds) in all cases tested. 



