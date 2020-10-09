# FlaskEwatson

## About

This project represents the sensor box code linked to the 2Imprezs website developed by SDU.

## Dev information

- [Setting up Dev enviroment](https://github.com/han-SDU/FlaskEwatson/wiki/Setting-up-Dev-enviroment)
- [Flask documentation](https://flask.palletsprojects.com/en/1.1.x/)

# IMPORTANT

At the time i am writing this the sensor box has NOT been build yet and hence i will leave some instructions on how to assemble the final code.

- I can not stress enough that the rPi need to be configured to allows mariadb event schedulers. It is not enoughto set this once inside the shell, it must be configured outside see [here](https://stackoverflow.com/questions/20112395/how-to-set-global-event-scheduler-on-even-if-mysql-is-restarted). The entire solution **WILL** crash if this is not done correctly.

- If you want get fancy with it we can remote update the code with [this](https://github.com/Dachshund77/SensorBoxWrapper). Just make sure it run befroe starting the flask and sensor services.

- You will need a deployment server to serve the server (mainServer.py). You can read more aobut that [here](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-18-04)
