import pymysql


def insert_team(team_name):
    # Function to insert the specified team
    try:
        con = pymysql.connect(user='root',
                              db='tickets',
                              charset='utf8mb4',
                              cursorclass=pymysql.cursors.DictCursor)
        cur = con.cursor()
        cur.execute("INSERT INTO team(team_name) values(%s)",
                    (team_name))  # SQL query to insert team
        con.commit()
        con.close()
        return "Successfully added \'" + team_name + "\'"
    except Exception as e:
        return str(e)


def remove_team(team_name):
    # Function to remove the specified team
    try:
        con = pymysql.connect(user='root',
                              db='tickets',
                              charset='utf8mb4',
                              cursorclass=pymysql.cursors.DictCursor)
        cur = con.cursor()
        # SQL query to remove the specified team
        cur.execute("DELETE from team where team_name=\"" + team_name + "\"")
        con.commit()
        con.close()
        return "Successfully removed \'" + team_name + "\'"
    except Exception as e:
        return str(e)


def insert_worker(worker_name, team):
    # Function to insert the specified worker with the specified team
    try:
        con = pymysql.connect(user='root',
                              db='tickets',
                              charset='utf8mb4',
                              cursorclass=pymysql.cursors.DictCursor)
        cur = con.cursor()
        cur.execute("SELECT * FROM team")
        data = cur.fetchall()
        teams = {}
        for dic in data:
            teams[dic['team_name']] = dic['id']
        cur.execute("INSERT INTO worker(worker_name, team_id) values(%s, %s)",
                    (worker_name, teams[team]))  # SQL query to insert the worker
        con.commit()
        con.close()
        return "Successfully added \'" + worker_name + "\' to \'" + team + "\'"
    except Exception as e:
        return str(e)


def remove_worker(worker_name, team):
    # Function to remove the specified worker
    try:
        con = pymysql.connect(user='root',
                              db='tickets',
                              charset='utf8mb4',
                              cursorclass=pymysql.cursors.DictCursor)
        cur = con.cursor()
        cur.execute("SELECT * FROM team")
        data = cur.fetchall()
        teams = {}
        for dic in data:
            teams[dic['team_name']] = dic['id']
        cur.execute("DELETE from worker WHERE worker_name=\"" + worker_name +
                    "\" and team_id=" + str(teams[team]))  # SQL query to remove the worker
        con.commit()
        con.close()
        return "Successfully removed \'" + worker_name + "\' from \'" + team + "\'"
    except Exception as e:
        return str(e)


def insert_product(product_name):
    # Function to insert the specified product
    try:
        con = pymysql.connect(user='root',
                              db='tickets',
                              charset='utf8mb4',
                              cursorclass=pymysql.cursors.DictCursor)
        cur = con.cursor()
        cur.execute("INSERT INTO product(product_name) values(%s)",
                    (product_name))  # SQL query to insert the product
        con.commit()
        con.close()
        return "Successfully added \'" + product_name + "\'"
    except Exception as e:
        return str(e)


def remove_product(product_name):
    # Function to remove the specified product
    try:
        con = pymysql.connect(user='root',
                              db='tickets',
                              charset='utf8mb4',
                              cursorclass=pymysql.cursors.DictCursor)
        cur = con.cursor()
        cur.execute("DELETE from product where product_name=\"" +
                    product_name + "\"")  # SQL query to remove the product
        con.commit()
        con.close()
        return "Successfully removed \'" + product_name + "\'"
    except Exception as e:
        return str(e)


def get_impact(issue_priority, issue_severity):
    # Function to return the impact value based on priority and severity
    if issue_priority == 1:
        if issue_severity == 1 or issue_severity == 2:
            return 1
        else:
            return 2
    elif issue_priority == 2:
        if issue_severity == 1 or issue_severity == 2:
            return 2
        else:
            return 3
    else:
        return 3


def insert_issue(team, worker, product, issue_type, issue_desc, issue_priority, issue_severity):
    # Function to insert the issue with the related values
    try:
        con = pymysql.connect(user='root',
                              db='tickets',
                              charset='utf8mb4',
                              cursorclass=pymysql.cursors.DictCursor)
        cur = con.cursor()
        cur.execute("SELECT * FROM team")
        data = cur.fetchall()
        teams = {}
        for dic in data:
            teams[dic['team_name']] = dic['id']
        cur.execute("SELECT * FROM product")
        data = cur.fetchall()
        products = {}
        for dic in data:
            products[dic['product_name']] = dic['id']
        cur.execute("SELECT id, worker_name FROM worker")
        data = cur.fetchall()
        workers = {}
        for dic in data:
            workers[dic['worker_name']] = dic['id']
        issue_impact = get_impact(issue_priority, issue_severity)
        cur.execute("INSERT INTO issue(team_id, product_id, issue_type, issue_description, issue_priority, issue_severity, issue_impact, worker_id) values(%s, %s, %s, %s, %s, %s, %s, %s)",
                    (teams[team], products[product], issue_type, issue_desc, issue_priority, issue_severity, issue_impact, workers[worker]))  # SQL query to insert the issues
        con.commit()
        con.close()
        return "Successfully added issue of type \'" + issue_type + "\'"
    except Exception as e:
        return str(e)


def team_names():
    # Function to get the team names
    try:
        con = pymysql.connect(user='root',
                              db='tickets',
                              charset='utf8mb4',
                              cursorclass=pymysql.cursors.DictCursor)
        cur = con.cursor()
        cur.execute("SELECT team_name FROM team")
        data = cur.fetchall()
        names = []
        if data:
            for dic in data:
                names.append(dic['team_name'])
        else:
            names = ['Placeholder']
        con.commit()
        con.close()
        return names
    except Exception as e:
        raise Exception(str(e))


def worker_names(team_name):
    # Function to get the worker names
    try:
        con = pymysql.connect(user='root',
                              db='tickets',
                              charset='utf8mb4',
                              cursorclass=pymysql.cursors.DictCursor)
        cur = con.cursor()
        cur.execute("SELECT * FROM team")
        data = cur.fetchall()
        teams = {}
        for dic in data:
            teams[dic['team_name']] = dic['id']
        cur.execute(
            "SELECT worker_name FROM worker WHERE team_id=" + str(teams[team_name]))
        data = cur.fetchall()
        names = []
        if data:
            for dic in data:
                names.append(dic['worker_name'])
        else:
            names = ['Placeholder']
        con.commit()
        con.close()
        return names
    except Exception as e:
        raise Exception(str(e))


def product_names():
    # Function to get the product names
    try:
        con = pymysql.connect(user='root',
                              db='tickets',
                              charset='utf8mb4',
                              cursorclass=pymysql.cursors.DictCursor)
        cur = con.cursor()
        cur.execute("SELECT product_name FROM product")
        data = cur.fetchall()
        names = []
        if data:
            for dic in data:
                names.append(dic['product_name'])
        else:
            names = ['Placeholder']
        con.commit()
        con.close()
        return names
    except Exception as e:
        raise Exception(str(e))


def relate_all():
    # Fucntion to provide the bsae view of the app
    try:
        con = pymysql.connect(user='root',
                              db='tickets',
                              charset='utf8mb4')
        cur = con.cursor()
        cur.execute("SELECT product_name, issue_type, issue_description, issue_priority, issue_severity, issue_impact, worker_name," +
                    " team_name FROM team, worker, issue, product WHERE team.id = issue.team_id AND product.id = issue.product_id AND worker.id = issue.worker_id;")  # SQL query to join the tables to get the necessary details
        data = cur.fetchall()
        con.close()
        return data
    except Exception as e:
        raise Exception(str(e))


def login_check(username, password):
    # Function to check the login details
    try:
        con = pymysql.connect(user='root',
                              db='tickets',
                              charset='utf8mb4',
                              cursorclass=pymysql.cursors.DictCursor)
        cur = con.cursor()
        cur.execute('SELECT usrname, password from admin')
        data = cur.fetchall()
        users = {}
        for dic in data:
            users[dic['usrname']] = dic['password']
        if users[username] == password:
            return True
        else:
            return False
    except Exception as e:
        return False
