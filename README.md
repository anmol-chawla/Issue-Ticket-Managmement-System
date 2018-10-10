# Ticket Management System

## Overview 
This is a simple TkInter project written in python3 to create a viewable platform for the MySQL database. It allows addition and deletion to 
the various tables present in the database.

## Packages required
asn1crypto==0.24.0
cffi==1.11.5
cryptography==2.3.1
idna==2.7
pycparser==2.19
PyMySQL==0.9.2
six==1.11.0

## Database structure
The project consists of the following tables -
* admin : The table responsible for the login information             
* issue : The table containing the issues and their priorities
* product : The table containing the product names
* team : The table containing the team names
* worker : The table containing the worker names

### admin table structure 

| Field    | Type        | Null | Key | Default | Extra          |
|----------|-------------|------|-----|---------|----------------|
| id       | int(11)     | NO   | PRI | NULL    | auto_increment |
| usrname  | varchar(20) | NO   | UNI | NULL    |                |
| password | varchar(20) | YES  |     | NULL    |                |

### issue table structure

| Field             | Type         | Null | Key | Default | Extra          |
|-------------------|--------------|------|-----|---------|----------------|
| id                | int(11)      | NO   | PRI | NULL    | auto_increment |
| team_id           | int(11)      | YES  | MUL | NULL    |                |
| product_id        | int(11)      | YES  | MUL | NULL    |                |
| issue_type        | varchar(20)  | YES  |     | NULL    |                |
| issue_description | varchar(100) | YES  |     | NULL    |                |
| issue_priority    | int(11)      | YES  |     | NULL    |                |
| issue_severity    | int(11)      | YES  |     | NULL    |                |
| issue_impact      | int(11)      | YES  |     | NULL    |                |
| worker_id         | int(11)      | YES  | MUL | NULL    |                |

### product table structure

| Field        | Type         | Null | Key | Default | Extra          |
|--------------|--------------|------|-----|---------|----------------|
| id           | int(11)      | NO   | PRI | NULL    | auto_increment |
| product_name | varchar(100) | NO   |     | NULL    |                |

### team table structure

| Field     | Type         | Null | Key | Default | Extra          |
|-----------|--------------|------|-----|---------|----------------|
| id        | int(11)      | NO   | PRI | NULL    | auto_increment |
| team_name | varchar(100) | NO   | UNI | NULL    |                |

### worker table structure

| Field       | Type         | Null | Key | Default | Extra          |
|-------------|--------------|------|-----|---------|----------------|
| id          | int(11)      | NO   | PRI | NULL    | auto_increment |
| worker_name | varchar(100) | NO   |     | NULL    |                |
| team_id     | int(11)      | YES  | MUL | NULL    |                |
