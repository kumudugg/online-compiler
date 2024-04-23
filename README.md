# Online compiler

#### Video Demo: 


#### Description

     A simple web application made by flask for run C, Python and SQL codes


    - You need to have python, gcc and sqlite3 installed. Cause I didn't include these. If I did, the size would be much larger
    - You need to have flask installed


    * Users can use this program without registering. But they can't save their codes.
    * The save button below text box is only shown after user logged in
    * The flash message will automatically hide after 2 seconds
    * I used seperate database for users to enter their commands. They can't access the main one.
    * The most challanging thing for me is that when user runs their code. That enterd code will disappered.
    * I use js for prevent this and also used ChatGPTs help.
    * Another challenging this was, When user save their codes, It doesen't showed indentation.
    * For this, I used txt.replace and in html, I used ("| safe") inside of that variable
    * I tried to use prism.js for syntax highlighting. But it's not working on textarea
    * Also, I used only one html page for 3 routings. (python, sql and c) and use jinja for pass variables
    * Thats why in these routs, there are dictonaries called variables.
    * And used lot of bootstrap.


    * Not included description about register, login and logout functions. It mostly same as CS50 previous project.


    For these three, I used python library called subprocess to run users commands

        In python, If request method is POST, getting given code from form and put it in to subprocess with "python3 -c". then, it will output result or error to the output.

        In C, It is exactly same as python. Only difference is that the program is save code file into temp folder and then executes it. That file automatically overwrite when user run commands.

        In sqlite, I created a another database for users to access. It only contain dummy values and users can do anything with it.

    The somewhat complex function is snippets, it checks 4 conditions instead of 2. 
    
        In first one, it checks request method is POST and ".method is delall." .method is a hidden fuction that I put in form to delete all the snippets user saved.

        In second one, It checks request method is POST and ".method is del. I used this for delete saved snipptes one by one.

        In third one check if request is post, It triggers when user click save button below the commands.


That's it.