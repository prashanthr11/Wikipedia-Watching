# Wikipedia Watching
- [Introduction](#introduction)
- [Requirements](#requirements)
- [Running the code](#running-our-code)
- [Conclusion](#conclusion)
## Introduction

In this project, we are going to track the real time updates on [Wikipedia](https://www.wikipedia.org/).

## Requirements
> To run this file we required [sseclient](https://pypi.org/project/sseclient/) module.
- Run the below command in terminal to install sseclient module in python.
```
pip install sseclient
```
or just run the below command in terminal
```
pip install -r requirements.txt
```
# Running our code
- If you want to run the code on [Jupyter Notebooks](https://jupyter.org/try). Just copy paste the [main.py](main.py) in the notebook and just run the code.
> **Note:** Before running the code make sure that you installed [sseclient](https://pypi.org/project/sseclient/) package. In case, If you are installed, [click here](#requirements) to out the command to install the package.
- ## Running on Terminal
- Just open the Terminal, and navigate to the directory, where main.py belongs and just run the below command.
```
python main.py
```

- ## Running on IDE's
- Copy main.py and paste it in your IDE and run the code.
```
python main.py
```
# Conclusion
- In this project, we are generating the reports for domains as well as users updates. In other words, we keep track of how many pages in domains and who is updating and how many edits the user has been made for each minute. In the above program, I'm assuming that I have generated report for 60 seconds and keep track of previous 5 minutes. At every minute, I have generated both domains and users report. Feel free to change the values, and play with them. 
