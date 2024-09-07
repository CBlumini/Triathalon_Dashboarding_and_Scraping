# Triathlon Dashboarding
Welcome to my project for dashboarding results from triathlons. I built a scraper in Selenium to pull data off of the results website for races I was competing in while I was in the Bay Area. 

I then host the data as a simple excel spreadsheet on Github. This choice is driven by the lower usage of the application and the simplicity of hosting and manipulating the data in this way. I've experimented with hosting the data in an S3 bucket but for the purposes of this project it didn't offer any technical improvement. Future versions will use SQL for storing the data as more race get scraped and added.

Data is presented using the Dash framework which is based on Plotly. Feel free to use the sliders and text boxes to filter and view the data.

If you want to run the code clone the repository and run the the docker container in `docker_version_dashboard/project`. Build the file with `docker build -t <image name> .` and run with `docker run -d -p 8050:8050 <image name>`

