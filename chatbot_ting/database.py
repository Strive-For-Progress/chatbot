import pymysql

db = pymysql.connect(host='mysql.cs.ccu.edu.tw',
                    user='xbt109u',
                    password='xbt109u',
                    database='xbt109u_appdb')

def tagToProjects(tags=[],neg_tags=[],user_id=-1,live=True,limit=5):
    # 依據tags內容(match越多越優先)，列出user_id非PI、COPI的project
    # 不填user則直接依tags計算 
    # tags不填 回傳[] , neg_tags不填 依tags計算
    # limit不填預設5

    if(len(tags) == 0): return []
    else: tags_text =  '"' + '","'.join(tags) + '"'

    if(limit <= 0): limit = 5 

    if live: live_text = "AND NOW() < sp.apply_copi_end_date "
    else: live_text = ""

    if(len(neg_tags) == 0): neg_tags_text = ""
    else:
        neg_tags_text = (
            "WHERE "
            "match_table.id NOT IN ( "
                "SELECT sp.id "
                "FROM specific_periods sp "
                "JOIN researches r "
                "JOIN specific_period_researches spr "
                "WHERE "
        ) 
        neg_tags_text += 'r.name IN ("' + '","'.join(neg_tags) + '") '        
        neg_tags_text += (
                    "AND r.id = spr.research_id AND spr.specific_period_id = sp.id "
                    "GROUP BY sp.id "
            ") "
        )

    cursor = db.cursor(cursor=pymysql.cursors.DictCursor)    
    sql=(
        "SELECT sp.id, sp.project_title, GROUP_CONCAT(r.name ORDER BY r.id ASC) AS researches "
        "FROM specific_periods sp "
        "JOIN ( "
                "SELECT sp.id, COUNT(distinct r.id) AS match_num "
                "FROM researches r "
                "INNER JOIN specific_period_researches spr "
                "INNER JOIN specific_periods sp "
                "INNER JOIN users u "
                
                "WHERE "
                    f"r.name IN ({tags_text}) "
                    "AND r.id = spr.research_id AND spr.specific_period_id = sp.id "
                    f"{live_text}"
                    "AND u.id = sp.user_id "
                    f"AND u.id != {user_id} AND {user_id} NOT IN (SELECT user_id FROM COPI_project CO WHERE CO.specific_period_id = sp.id) "
                
                "GROUP BY sp.id " 
                ") match_table ON match_table.id = sp.id "
        "JOIN specific_period_researches spr ON spr.specific_period_id = sp.id "
        "JOIN researches r ON spr.research_id = r.id "
        f"{neg_tags_text}"
        "GROUP BY sp.id "
        "ORDER BY match_num DESC "
        f"LIMIT 0, {limit} "
    )

    cursor.execute(sql)
    results = cursor.fetchall()

    return results

def user_prefer_project(user_id=-1,live=True,limit=5):
    # 依據user_id偏好(match越多越優先)，列出user_id非PI、COPI的project
    # user不填 ，回傳{} 
    # (live=True:不包含過期(copi_end_time))，反之包含
    # limit不填預設5

    if(user_id < 0): return {}

    if(limit < 0): limit = 5

    if live: live_text = "AND NOW() < sp.apply_copi_end_date "
    else: live_text = ""

    cursor = db.cursor(cursor=pymysql.cursors.DictCursor)    
    sql=(
        "SELECT sp.id, sp.project_title, GROUP_CONCAT(r.name ORDER BY r.id ASC) AS researches "
        "FROM specific_periods sp "
        "JOIN ( "
                "SELECT sp.id, COUNT(distinct r.id) AS match_num "
                "FROM researches r "
                "INNER JOIN specific_period_researches spr "
                "INNER JOIN specific_periods sp "
                "INNER JOIN users u "
                
                "WHERE "
                    "r.name IN (SELECT r.name "
                            "FROM researches r "
                            "JOIN user_researches ur ON ur.research_id = r.id "
                            "JOIN users u ON u.id = ur.user_id "
                            f"WHERE u.id = {user_id} "
                            ") "
                    "AND r.id = spr.research_id AND spr.specific_period_id = sp.id "
                    f"{live_text}"
                    "AND u.id = sp.user_id "
                    f"AND u.id != {user_id} AND {user_id} NOT IN (SELECT user_id FROM COPI_project CO WHERE CO.specific_period_id = sp.id) "
                
                "GROUP BY sp.id "                 
                ") match_num ON match_num.id = sp.id "
        "JOIN specific_period_researches spr ON spr.specific_period_id = sp.id "
        "JOIN researches r ON spr.research_id = r.id "
        "GROUP BY sp.id "
        "ORDER BY match_num DESC "
        f"LIMIT 0, {limit} "
    )

    cursor.execute(sql)
    results = cursor.fetchall()

    return results

def all_projects(live = True,limit=5):
    # 列出所有project、project的id、title、researches
    # (live=True:不包含過期(copi_end_time))，反之包含
    # limit不填預設5

    if live: live_text = "AND NOW() < sp.apply_copi_end_date "
    else: live_text = ""

    if(limit < 0): limit = 5

    cursor = db.cursor(cursor=pymysql.cursors.DictCursor)
    sql = (
            "SELECT sp.id, sp.project_title "
                ", GROUP_CONCAT(c.name ORDER BY c.id) AS researches "
            "FROM specific_periods sp "
            "JOIN specific_period_researches spr ON spr.specific_period_id = sp.id "
            "JOIN researches c ON c.id = spr.research_id "
            f"{live_text}"
            "GROUP BY sp.id "
            "ORDER BY sp.id "
            f"LIMIT 0,{limit} "
        )

    cursor.execute(sql)
    results = cursor.fetchall()

    return results

def all_researches():
    # 列出所有researches
    cursor = db.cursor(cursor=pymysql.cursors.DictCursor)
    sql = "SELECT name FROM researches"

    cursor.execute(sql)
    results = cursor.fetchall()

    researches = []
    for research in results:
        researches.append(research['name'])

    return researches

def user_researches(user_id=-1):
    # 列出user_id的researches
    if(user_id < 0): return [] # 不填user_id回傳[]

    cursor = db.cursor(cursor=pymysql.cursors.DictCursor)
    sql = (
        "SELECT r.name FROM researches r "
        "JOIN user_researches ur "
        f"WHERE ur.user_id = {user_id} AND r.id = ur.research_id "
        "ORDER BY ur.id"
    )
    cursor.execute(sql)
    results = cursor.fetchall()

    researches = []
    for research in results:
        researches.append(research['name'])

    return researches

def specific_period_researches(specific_period_id = -1):
    # 列出project_id的researches
    if(specific_period_id < 0): return []    # 不填specific_period_id回傳[]

    cursor = db.cursor(cursor=pymysql.cursors.DictCursor)
    sql = (
        "SELECT r.name FROM researches r "
        "JOIN specific_period_researches spr "
        f"WHERE spr.specific_period_id = {specific_period_id} "
            "AND r.id = spr.research_id "
        "ORDER BY r.id"
    )
    cursor.execute(sql)
    results = cursor.fetchall()

    researches = []
    for research in results:
        researches.append(research['name'])

    return researches

def latest_projects(limit=5,live=True):
    # 列出所有project、project的id、title、researches(照時間)
    # (live=True:不包含過期(copi_end_time))，反之包含 
    # limit不填預設5

    if live: live_text = "AND NOW() < sp.apply_copi_end_date "
    else: live_text = ""

    if(limit <= 0): limit = 5

    cursor = db.cursor(cursor=pymysql.cursors.DictCursor)
    sql = (
            "SELECT sp.id, sp.project_title "
                ", GROUP_CONCAT(c.name ORDER BY c.id) AS researches "
            "FROM specific_periods sp "
            "JOIN specific_period_researches spr ON spr.specific_period_id = sp.id "
            "JOIN researches c ON c.id = spr.research_id "
            f"{live_text}"
            "GROUP BY sp.id "
            "ORDER BY sp.start_date DESC "
            f"LIMIT 0,{limit} "
        )

    cursor.execute(sql)
    results = cursor.fetchall()

    return results


if __name__ == "__main__":
    print("===================================")    
    for project in tagToProjects(tags=['C++','AI','DL'],neg_tags=['web'],user_id=-1,live=True): print(project)
    print("===================================")
    for project in user_prefer_project(user_id=7, limit=2): print(project)
    print("===================================")
    for project in all_projects(live=False,limit=2): print(project)
    print("===================================")
    print(all_researches())
    print("===================================")
    print(user_researches(user_id=6))
    print("===================================")
    print(specific_period_researches(specific_period_id=3))
    print("===================================")    
    print(all_researches())
    print("===================================")    
    for project in latest_projects(limit=2): print(project)
    
