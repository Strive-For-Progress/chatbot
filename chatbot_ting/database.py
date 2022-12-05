import pymysql

db = pymysql.connect(host='mysql.cs.ccu.edu.tw',
                    user='xbt109u',
                    password='xbt109u',
                    database='xbt109u_appdb')


def all_projects(live = True):
    # 列出所有project、project的title、researches、PI、COPI 
    # (live=True:不包含過期(copi_end_time))，反之包含
    cursor = db.cursor(cursor=pymysql.cursors.DictCursor)
    
    sql = "SELECT a.id, a.project_title, a.user_id FROM specific_periods a "
    if live : sql += "WHERE NOW() < a.apply_copi_end_date "
    sql += "ORDER BY a.id"

    cursor.execute(sql)
    results = cursor.fetchall()

    for project in results: #添加researches、COPI
        project['research'] = specific_period_researches(project['id'])
        project['COPI']     = COPI_project(project['id'])
        
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

def specific_period_researches(specific_period_id = -1):
    # 列出project_id的researches
    # 不填specific_period_id回傳[]
    cursor = db.cursor(cursor=pymysql.cursors.DictCursor)
    sql = "SELECT a.name FROM researches a \
            JOIN specific_period_researches b \
            WHERE b.specific_period_id = %d\
                AND a.id = b.research_id" %(specific_period_id)

    cursor.execute(sql)
    results = cursor.fetchall()

    researches = []
    for research in results:
        researches.append(research['name'])

    return researches

def user_researches(user_id=-1):
    # 列出user_id的researches
    # 不填user_id回傳[]
    cursor = db.cursor(cursor=pymysql.cursors.DictCursor)
    sql = "SELECT a.name FROM researches a \
        JOIN user_researches b \
        WHERE b.user_id = %d AND a.id = b.research_id" % (user_id)
    cursor.execute(sql)
    results = cursor.fetchall()

    researches = []
    for research in results:
        researches.append(research['name'])

    return researches


def COPI_project(specific_period_id=-1):
    # 列出project_id的COPI(user)
    # 不填specific_period_id回傳[]
    cursor = db.cursor(cursor=pymysql.cursors.DictCursor)
    sql = "SELECT a.user_id FROM COPI_project a \
            WHERE a.specific_period_id = %d" %(specific_period_id)

    cursor.execute(sql)
    results = cursor.fetchall()

    COPIs = []
    for COPI in results:
        COPIs.append(COPI['user_id'])

    return COPIs

def projects_match(tags=all_researches()):
    #計算project的researches與tags符合的數量 (不包含過期(copi_end_time))
    #不填tags，直接用projects_match()，回傳project的tag數量
    #填[]，即projects_match(tags=[])，回傳{}
    results={}
    projects=all_projects(live=True)
    for project in projects:
        for research in project['research']:
            if research in tags:
                results[project['id']]= results.get(project['id'], 0) + 1 

    return results

def user_COPI_projects(user_id=-1,live=False):
    #列出所有此user_id為pi、copi的project 包含過期(copi_end_time)
    #不填回傳[]
    COPI_projects=[]

    projects=all_projects(live=live)
    for project in projects:
        if user_id == project['user_id'] or user_id in project['COPI']:
            COPI_projects.append(project['id'])
          
    return COPI_projects    

def not_user_COPI_projects(user_id=-1):
    #列出所有此user_id"並非"pi、copi的project 包含過期(copi_end_time)
    #不填回傳所有project_id
    not_COPI_projects = []

    projects=all_projects(live=False)
    for project in projects:
        if user_id != project['user_id'] and user_id not in project['COPI']:
            not_COPI_projects.append(project['id'])

    return not_COPI_projects

def some_projects(ids=[], user_id=-1, live=True):
    # 依照ids順序，列出指定project_id的project_id、project_title、researches、PI、COPI
    # (不包含user_id是PI、COPI的project)(live=True: 不包含過期(copi_end_time))
    # 不填回傳[]
    if not ids: return []    
    cursor = db.cursor(cursor=pymysql.cursors.DictCursor)

    copi_projects=user_COPI_projects(user_id=user_id)

    sql = f"SELECT a.id, a.project_title, a.user_id FROM specific_periods a \
            WHERE a.user_id != {user_id} "      #user_id非project_id發起人

    if len(ids) >= 2:                                       #project_id符合ids
        sql += f"AND a.id in {format(tuple(ids))} "        
    elif len(ids) == 1:                                     # tuple([1]) => (1,)
        sql += f"AND a.id = {ids[0]} "                      # element == 1 時不能用tuple

    if live:                                                # 過期？(copi_end_time)
        sql += f"AND NOW() < a.apply_copi_end_date "

    if len(copi_projects) == 1:                             # user_id非此project的PI、COPI
        sql += f"AND a.id != {copi_projects[0]} "           # element == 1 時不能用tuple
    elif copi_projects:
        sql += f"AND a.id not in {tuple(copi_projects)} "    

    if len(ids) >= 2 :                                      # order by ids
        sql += f"ORDER BY FIELD(a.id, {','.join(str(x) for x in ids)})"

    cursor.execute(sql)
    results = cursor.fetchall()

    for project in results:                                 #添加researches、COPI
        project['research'] = specific_period_researches(project['id'])
        project['COPI']     = COPI_project(project['id'])
        
    return results

if __name__ == "__main__":

    print("========================================")
    print(f"所有的projects(含過期)：")
    for project in all_projects(live=False): print(project)

    print("========================================")
    print(f"所有的researches：\n{all_researches()}")

    print("========================================")
    u_id=6  # 取user_6的資料    
    print(f"user_{u_id}的researches：\n{user_researches(user_id=u_id)}")
    
    print("========================================")
    p_id=2  # 取project_2的資料    
    print(f"project_{p_id}的researches：\n{specific_period_researches(specific_period_id=p_id)}")
    
    print("========================================")
    p_id=2
    print(f"project_{p_id}的PI、COPI：\n{COPI_project(specific_period_id=p_id)}")
    
    print("========================================")
    u_id=7
    print(f"user_{u_id}為PI、COPI的project：\n{user_COPI_projects(user_id=u_id)}")
    
    print("========================================")
    u_id=7
    print(f"user_{u_id}並非PI、COPI的project：\n{not_user_COPI_projects(user_id=u_id)}")
    
    print("========================================")
    tags=['web','DL','AI']
    print(f"所有project的researches與tags={tags}有幾項符合：({{project_id : match_num}})\n{projects_match(tags=tags)}")
    
    print("========================================")
    print("所有的projects：(不列出過期)")
    for project in all_projects(): print(project)
    
    print("========================================")
    ids=[4,2,3,1]
    u_id=7
    print(f"id 為 {ids} 且PI、COPI不為user_{u_id} 的projects：")
    print("(照順序)(不列出過期)")
    for project in some_projects(ids=ids,user_id=u_id): print(project)
    
    print("\n######################################################")
    print(" ===================== 以下拼裝 =====================")
    print("######################################################\n")
    u_id=7
    print(f"所有project的researches與tags=[user_({u_id})的偏好]")
    print(f"有幾項符合？({{project_id : match_num}})\n{projects_match(tags=user_researches(user_id=u_id))}")    
    
    print("========================================")
    u_id=7
    print(f"所有user_{u_id}非PI、COPI的project(詳細)：")
    for project in some_projects(ids=not_user_COPI_projects(user_id=u_id)): print(project)

    print("========================================")
    u_id=7
    orders = projects_match(tags=user_researches(user_id=u_id))
    orders = sorted(orders.items(), key=lambda kv : kv[1], reverse=True)
    ids = []
    for order in orders:
        ids.append(order[0])
    print(f"依據user_{u_id}偏好，選出user_{u_id}非PI、COPI的project：\n(order by 偏好_match_num)")
    for project in some_projects(ids=ids, user_id=u_id): print(project)
