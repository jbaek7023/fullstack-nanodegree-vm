#Item Tournament
Common code for the Relational Databases and Full Stack Fundamentals courses. 

##Before Run
Install [Vagrant](https://www.vagrantup.com/) and [VirtualBox](https://www.virtualbox.org/)

##How to Run
1. download whole file

2. open terminal and navigate to the file

3. enter 'vagrant up' to power up on the virtual machine followed by 'vagrant ssh' (logs into the virtual machine)

3. enter 'psql' to run PostgreSQL server

4. enter '\i tournament.sql' to execute sql queries which create database and tables

5. open another terminal and navigate to the file

6. enter 'vagrant ssh' 

7. enter 'cd /vagrant/tournament'

8. To test, 'python tournament_test.py'

9. You see all the test pass

##the purpose of each file 
1. tournament.sql  - this file is used to set up your database schema (the table representation of your data structure).

2. tournament.py - this file is used to provide access to your database via a library of functions which can add, delete or query data in your database to another python program (a client program). Remember that when you define a function, it does not execute, it simply means the function is defined to run a specific set of instructions when called.

3. tournament_test.py - this is a client program which will use your functions written in the tournament.py module. We've written this client program to test your implementation of functions in tournament.py
