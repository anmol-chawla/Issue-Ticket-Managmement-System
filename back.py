import pymysql


def insert_team(team_name):
    try:
        con = pymysql.connect(user='root',
                              db='tickets',
                              charset='utf8mb4',
                              cursorclass=pymysql.cursors.DictCursor)
        cur = con.cursor()
        cur.execute("INSERT INTO team(team_name) values(%s)", (team_name))
        con.commit()
        con.close()
        return "Successfully added \'" + team_name + "\'"
    except Exception as e:
        return str(e)


def insert_worker(worker_name, team):
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
                    (worker_name, teams[team]))
        con.commit()
        con.close()
        return "Successfully added \'" + worker_name + "\' to \'" + team + "\'"
    except Exception as e:
        return str(e)


def insert_product(product_name):
     try:
        con = pymysql.connect(user='root',
                              db='tickets',
                              charset='utf8mb4',
                              cursorclass=pymysql.cursors.DictCursor)
        cur = con.cursor()
        cur.execute("INSERT INTO product(product_name) values(%s)",
                    (product_name))
        con.commit()
        con.close()
        return "Successfully added \'" + product_name + "\'"
     except Exception as e:
        return str(e)


def get_impact(issue_priority, issue_severity):
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

def insert_issue(team, product, issue_type, issue_desc, issue_priority, issue_severity):
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
        issue_impact = get_impact(issue_priority, issue_severity)
        cur.execute("INSERT INTO issue(team_id, product_id, issue_type, issue_description, issue_priority, issue_severity, issue_impact) values(%s, %s, %s, %s, %s, %s, %s)",
                    (teams[team], products[product], issue_type, issue_desc, issue_priority, issue_severity, issue_impact))
        con.commit()
        con.close()
        return "Successfully added issue of type \'" + issue_type + "\'"
    except Exception as e:
        return str(e)


def team_names():
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

def product_names():
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
    try:
        con = pymysql.connect(user='root',
                              db='tickets',
                              charset='utf8mb4')
        cur = con.cursor()
        cur.execute("SELECT product_name, issue_type, issue_description, issue_priority, issue_severity, issue_impact, worker_name," +\
                    " team_name FROM team, worker, issue, product WHERE team.id = issue.team_id AND product.id = issue.product_id;")
        data = cur.fetchall()
        con.close()
        return data
    except Exception as e:
        raise Exception(str(e))
