from django.shortcuts import render
from .work import Sort_el
from .models import Person, Algorithm, Problem, Student, Teacher, Group, Order, Solving
from django.http import HttpResponseRedirect, HttpResponseNotFound, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from untitled.settings import BASE_DIR
import datetime
import sqlite3
from reportlab.pdfgen import canvas
from reportlab.pdfbase import ttfonts, pdfmetrics
from reportlab.lib.colors import red, black, green


ALL_TASKS = ['Сортировка пузырьком', 'Сортировка вставками']


def index(request):
    status = ""
    if request.user.is_authenticated:
        person = Person.objects.get(pe_id=int(request.user.username))
        status = person.pe_status
        return render(request, "index.html", {"status": status, "person": person})
    return render(request, "index.html", {"status": status})


def group_me(request):
    order = Order.objects.get(id=1).order_group
    if order[-1] == 'd':
        order = '-' + order[:-1]
    stu = Student.objects.filter(st_profile_id=int(request.user.username))[0].st_id
    group = Group.objects.filter(gr_students=stu).order_by(order)
    return render(request, "group_me.html", {"group": group})


def checkin(request):
    people = Person.objects.all()
    return render(request, "checkin.html", {"people": people})


def group_add(request):
    order = Order.objects.get(id=1).order_group
    if order[-1] == 'd':
        order = '-' + order[:-1]
    people = Person.objects.all()
    group = Group.objects.all().order_by(order)
    return render(request, "group_add.html", {"people": people, "group": group})


def creategroup(request):
    te_id = Teacher.objects.filter(te_profile_id=int(request.user.username))[0].te_id
    if request.method == "POST":
        tom = Group()
        tom.gr_name = request.POST.get("name")
        person = Teacher.objects.filter(te_id=te_id)
        tom.save()
        tom.gr_teachers.add(te_id)
        tom.save()
        return HttpResponseRedirect("/group_add/")


def solve(request, pr_id):
    tom = Solving()
    tom.so_problem = Problem.objects.get(pr_id=pr_id)
    tom.so_student = Student.objects.get(st_profile_id=int(request.user.username))
    tom.so_todaydate = datetime.datetime.now()
    tom.so_res = 0
    tom.save()
    obj = Sort_el()
    test_cr = None
    if Problem.objects.get(pr_id=pr_id).pr_algo.al_name == 'Сортировка пузырьком':
        test_cr = obj.create_test(obj.bubble_sort)
    elif Problem.objects.get(pr_id=pr_id).pr_algo.al_name == 'Сортировка выбором':
        test_cr = obj.create_test(obj.choice_sort)
    if test_cr is None:
        tom.so_res = 1
        tom.save()
        return HttpResponseRedirect('/'.join(request.path.split('/')[:-4]))

    # print(test_cr[0].data, test_cr[1].data)
    # print(test_cr[0].answer, test_cr[1].answer)
    dat = " ".join([str(el) for el in test_cr[0].data])
    first = test_cr[0]
    second = test_cr[1]
    return render(request, "solve.html", {"data": dat, "first": first, "second": second, "pr_id": pr_id})


def createsolving(request, pr_id):
    Pro = Problem.objects.get(pr_id=pr_id)
    Stu = Student.objects.get(st_profile_id=int(request.user.username))
    tom = Solving.objects.filter(so_problem=Pro, so_student=Stu)[0]

    if request.method == "POST":
        ans1 = request.POST.get("choice1")
        ans2 = request.POST.get("choice2")
        real_ans1 = request.POST.get("ffirst")
        real_ans2 = request.POST.get("fsecond")
        res = 0
        if ans1 == real_ans1:
            res += 5
        if ans2 == real_ans2:
            res += 5
        tom.so_res = res
        Stu.st_rate += res
        tom.save()
        Stu.save()
    return HttpResponseRedirect ('/'.join(request.path.split('/')[:-4]))


def report1(request):
    resp = HttpResponse(content_type='application/pdf')
    resp['Content_Disposition'] = 'attachment; filename="somefilename.pdf"'
    base = sqlite3.connect("db.sqlite3")
    cur = base.cursor()
    cur.execute("Select gr_name, count(Distinct student_id) AS 'Количество студентов', count(Distinct pr_id) as 'Количество заданий' from (algo_learn_problem A inner join algo_learn_group B on A.pr_group_id = B.gr_id) С inner join algo_learn_group_gr_students D on gr_id = group_id Group by gr_name Order By count(Distinct pr_id) DESC ")
    res = cur.fetchall()
    base.close()
    c = canvas.Canvas(resp)
    ob = ttfonts.TTFont('Arial', 'arial.ttf')
    pdfmetrics.registerFont(ob)
    wid = 700
    c.setTitle("Отчет")
    c.setFont("Arial", 30)
    c.setFillColor(red)
    c.drawString(170, 600, "Отчет по группам")
    c.showPage()
    for el in res:
        c.setFont("Arial", 15)
        c.setStrokeColorRGB(0.2, 0.6, 0.4)
        c.setFillColor(black)
        c.drawString(60, wid, "Название группы: ")
        c.setFillColor(red)
        c.drawString(400, wid, str(el[0]))
        c.setFillColor(black)
        c.drawString(60, wid-30, "Количество студентов в группе: ")
        c.setFillColor(green)
        c.drawString(400, wid-30, str(el[1]))
        c.setFillColor(black)
        c.drawString(60, wid-60, "Количество заданий в группе: ")
        c.setFillColor(green)
        c.drawString(400, wid-60, str(el[2]))
        c.line(0, wid-2, 600, wid-2)
        c.showPage()
    c.save()
    return resp


def report2(request):
    resp = HttpResponse(content_type='application/pdf')
    resp['Content_Disposition'] = 'attachment; filename="somefilename.pdf"'
    base = sqlite3.connect("db.sqlite3")
    cur = base.cursor()
    cur.execute('Select pe_name,  count(CASE WHEN so_res=0 THEN 1 ELSE NULL END),  count(CASE WHEN so_res=5 THEN 1 ELSE NULL END), count(CASE WHEN so_res=10 THEN 1 ELSE NULL END), st_rate from algo_learn_solving inner join algo_learn_student on st_id=so_student_id inner join algo_learn_person on st_profile_id=pe_id inner join algo_learn_problem on so_problem_id=pr_id inner join algo_learn_group on pr_group_id=gr_id Group by pe_name, st_rate')
    res = cur.fetchall()
    base.close()
    c = canvas.Canvas(resp)
    ob = ttfonts.TTFont('Arial', 'arial.ttf')
    pdfmetrics.registerFont(ob)
    wid = 700
    c.setTitle("Отчет")
    c.setFont("Arial", 30)
    c.setFillColor(red)
    c.drawString(170, 600, "Отчет по студентам")
    c.showPage()
    for el in res:
        c.setFont("Arial", 15)
        c.setStrokeColorRGB(0.2, 0.6, 0.4)
        c.setFillColor(black)
        c.drawString(60, wid, "Имя: ")
        c.setFillColor(red)
        c.drawString(400, wid, str(el[0]))
        c.setFillColor(black)
        c.drawString(60, wid-30, "Количество неправильных решений: ")
        c.setFillColor(green)
        c.drawString(400, wid-30, str(el[1]))
        c.setFillColor(black)
        c.drawString(60, wid-60, "Количество наполовину правильных решений: ")
        c.setFillColor(green)
        c.drawString(400, wid - 60, str(el[2]))
        c.setFillColor(black)
        c.drawString(60, wid - 90, "Количество правильных решений: ")
        c.setFillColor(green)
        c.drawString(400, wid - 90, str(el[3]))
        c.setFillColor(black)
        c.drawString(60, wid - 120, "Общий балл: ")

        c.setFillColor(green)
        c.drawString(400, wid-120, str(el[4]))
        c.line(0, wid-2, 600, wid-2)
        c.showPage()
    c.save()
    return resp


def arbitrary(request):
    pers = Person.objects.get(pe_id=int(request.user.username))
    base = sqlite3.connect("db.sqlite3")
    cur = base.cursor()
    res = None
    res_name = None
    if request.method == "POST":
        name = request.POST.get("name")
        try:
            cur.execute(name)
            res = cur.fetchall()
            desc = cur.description
            res_name = [desc[i][0] for i in range(len(desc))]
        except sqlite3.OperationalError:
            pass
        pers.pe_query = name
    base.close()
    pers.save()
    return render(request, 'arbitrary_q.html', {"person": pers, "res": res, "res_name": res_name})


def add(request, pe_id):
    gr_id = int(request.path.split('/')[3])
    group = Group.objects.get(gr_id=gr_id)
    person = Student.objects.get(st_profile_id=pe_id)
    group.gr_students.add(person)
    return HttpResponseRedirect('/'.join(request.path.split('/')[:-3])+'/')


def remove(request, pe_id):
    gr_id = int(request.path.split('/')[3])
    group = Group.objects.get(gr_id=gr_id)
    person = Student.objects.get(st_profile_id=pe_id)
    group.gr_students.remove(person)
    return HttpResponseRedirect('/'.join(request.path.split('/')[:-3])+'/')


def search_list(word, list):
    for el in list:
        if word in el:
            return True
    return False

def search_all_list(word_list, list):
    for el in word_list:
        if not search_list(el, list):
            return False
    return True

def search(request):
    people_string = []
    problem_string = []
    algo_string = []
    group_string = []
    res = False
    if request.method == "POST":
        sent = (request.POST.get("word")).split(' ')
        people = Person.objects.all()
        problems = Problem.objects.all()
        algos = Algorithm.objects.all()
        groups = Group.objects.all()
        for el in people:
            pers = [el.pe_name, el.pe_surname, el.pe_patronymic, el.pe_login, el.pe_email, el.pe_status, str(el.pe_birthdate)[:10], str(el.pe_todaydate)[:10]]
            if search_all_list(sent, pers):
                people_string += [pers]

        for el in algos:
            pers = [el.al_type, el.al_name, el.al_comment]
            if search_all_list(sent, pers):
                algo_string += [pers]

        for el in problems:
            pers = [el.pr_name, str(el.pr_checkdate)[:10]]
            if search_all_list(sent, pers):
                problem_string += [pers]

        for el in groups:
            pers = [el.gr_name]
            if search_all_list(sent, pers):
                group_string += [pers]
    if len(people_string):
        people_string = [['Имя', 'Фамилия', 'Отчество', 'Логин', 'Почта', 'Статус', 'Дата рождения','Дата Регистрации']] + people_string
    if len(algo_string):
        algo_string = [['Тип', 'Имя', 'Коммментарий']] + algo_string
    if len(group_string):
        group_string = [['Название']] + group_string
    if len(problem_string):
        problem_string = [['Название', 'Дата проверки']] + problem_string
    if len(people_string +problem_string + algo_string + group_string):
        res = True
    return render(request, "search.html", {"people_string": people_string, "problem_string": problem_string, "group_string": group_string, "algo_string": algo_string, "res": res})


def editgroup(request, gr_id):
    group = Group.objects.get(gr_id=gr_id)
    try:
        if request.method == "POST":
            group.gr_name = request.POST.get("name")
            group.save()
            return HttpResponseRedirect("/group_add/")
        else:
            return render(request, "group_edit.html", {"group": group})
    except group.DoesNotExist:
        return HttpResponseNotFound("<h2>Group not found</h2>")


def problems(request, gr_id):
    algo = Algorithm.objects.all()
    order = Order.objects.get(id=1).order_problem
    if order[-1] == 'd':
        order = '-' + order[:-1]
    name = Group.objects.get(gr_id=gr_id).gr_name
    pro = Problem.objects.filter(pr_group=gr_id).order_by(order)
    solv = Solving.objects.all()
    res = []
    for el in pro:
        find = Solving.objects.filter(so_problem=el, so_student=Student.objects.filter(st_profile_id=int(request.user.username))[0])
        if len(find) == 0:
            res += [-1]
        else:
            res += [find[0].so_res]
    return render(request, "problems.html", {"name": name, "problems": pro, "res": res, "todate": datetime.datetime.now(), "algo": algo})


def editgr_people(request, gr_id):
    order = Order.objects.get(id=1).order_person
    name = Group.objects.get(gr_id=gr_id).gr_name
    group = Student.objects.filter(group=gr_id)
    people = Student.objects.all()
    gr = []
    for pers in people:
        if pers not in group:
            gr += [pers]
    people = gr
    group_people = []
    for person in group:
        group_people += [Person.objects.get(pe_id=person.st_profile_id)]
    people_people = []
    for person in people:
        people_people += [Person.objects.get(pe_id=person.st_profile_id)]
    if order == "pe_surname":
        people_people.sort(key=lambda per: per.pe_surname, reverse=False)
        group_people.sort(key=lambda per: per.pe_surname, reverse=False)
    elif order == "pe_surnamed":
        people_people.sort(key=lambda per: per.pe_surname, reverse=True)
        group_people.sort(key=lambda per: per.pe_surname, reverse=True)
    elif order == "pe_name":
        people_people.sort(key=lambda per: per.pe_name, reverse=False)
        group_people.sort(key=lambda per: per.pe_name, reverse=False)
    elif order == "pe_named":
        people_people.sort(key=lambda per: per.pe_name, reverse=True)
        group_people.sort(key=lambda per: per.pe_name, reverse=True)
    elif order == "pe_todaydate":
        people_people.sort(key=lambda per: per.pe_todaydate, reverse=False)
        group_people.sort(key=lambda per: per.pe_todaydate, reverse=False)
    elif order == "pe_todaydated":
        people_people.sort(key=lambda per: per.pe_todaydate, reverse=True)
        group_people.sort(key=lambda per: per.pe_todaydate, reverse=True)
    elif order == "pe_login":
        people_people.sort(key=lambda per: per.pe_login, reverse=False)
        group_people.sort(key=lambda per: per.pe_login, reverse=False)
    elif order == "pe_logind":
        people_people.sort(key=lambda per: per.pe_login, reverse=True)
        group_people.sort(key=lambda per: per.pe_login, reverse=True)
    elif order == "pe_birthdate":
        people_people.sort(key=lambda per: per.pe_login, reverse=False)
        group_people.sort(key=lambda per: per.pe_login, reverse=False)
    elif order == "pe_birthdated":
        people_people.sort(key=lambda per: per.pe_login, reverse=True)
        group_people.sort(key=lambda per: per.pe_login, reverse=True)
    return render(request, "editgr_people.html", {"people": people_people, "group": group_people, "name": name})


def deletegroup(request, gr_id):
    try:
        group = Group.objects.get(gr_id=gr_id)
        group.delete()
        return HttpResponseRedirect("/group_add/")
    except group.DoesNotExist:
        return HttpResponseNotFound("<h2>Group not found</h2>")


def log_in(request):
    if request.method == "POST":
        log = request.POST.get("login")
        email = request.POST.get("email")
        password = request.POST.get("password")
        tom = Person.objects.filter(pe_login=log, pe_email=email, pe_password=password)
        if len(tom):
            user = authenticate(username=tom[0].pe_id, password=tom[0].pe_password)
            login(request, user)
    return HttpResponseRedirect("/")


def log_out(request):
    logout(request)
    return HttpResponseRedirect("/")


def create(request):
    if request.method == "POST":
        tom = Person()
        tom.pe_name = request.POST.get("name")
        tom.pe_surname = request.POST.get("surname")
        tom.pe_patronymic = request.POST.get("patronymic")
        tom.pe_birthdate = request.POST.get("birthdate")
        tom.pe_todaydate = datetime.datetime.now()
        tom.pe_login = request.POST.get("login")
        tom.pe_status = request.POST.get("status")
        tom.pe_password = request.POST.get("password")
        tom.pe_email = request.POST.get("email")
        tom.pe_admin = request.POST.get("admin")
        tom.save()
        if tom.pe_status == "Преподаватель":
            tommy = Teacher()
            tommy.te_profile = tom
            tommy.save()
        else:
            tommy = Student()
            tommy.st_profile = tom
            tommy.save()
        user = User.objects.create_user(tom.pe_id, tom.pe_email, tom.pe_password)
        user.first_name = tom.pe_name
        user.last_name = tom.pe_login
        user.save()
        return HttpResponseRedirect("/")


def edit(request, pe_id):
    try:
        person = Person.objects.get(pe_id=pe_id)
        user = User.objects.get(username=str(pe_id))
        if request.method == "POST":
            person.pe_name = request.POST.get("name")
            person.pe_surname = request.POST.get("surname")
            person.pe_patronymic = request.POST.get("patronymic")
            person.pe_birthdate = request.POST.get("birthdate")
            #person.todaydate = request.POST.get("todaydate")
            person.pe_login = request.POST.get("login")
            #person.status = request.POST.get("status")
            person.pe_password = request.POST.get("password")
            person.pe_email = request.POST.get("email")
            person.pe_admin = request.POST.get("admin")
            person.save()
            user.email = person.pe_email
            user.last_name = person.pe_login
            user.first_name = person.pe_name
            user.save()
            return HttpResponseRedirect("/")
        else:
            return render(request, "edit.html", {"person": person})
    except Person.DoesNotExist:
        return HttpResponseNotFound("<h2>Person not found</h2>")


def delete(request, pe_id):
    try:
        person = Person.objects.get(pe_id=pe_id)
        user = User.objects.get(username=str(pe_id))
        user.delete()
        person.delete()
        return HttpResponseRedirect("/")
    except Person.DoesNotExist:
        return HttpResponseNotFound("<h2>Person not found</h2>")


def algonew(request):
    order = Order.objects.get(id=1).order_algorithm
    if order[-1] == 'd':
        order = '-' + order[:-1]
    algo = Algorithm.objects.all().order_by(order)
    return render(request, "algonew.html", {"algo": algo})


def createtask(request):
    if request.method == "POST":
        tom = Problem()
        tom.pr_name = request.POST.get("name")
        tom.pr_checkdate = request.POST.get("checkdate")
        temp = request.POST.get("algoname").split(" ")[0]
        tom.pr_algo = Algorithm.objects.get(al_id=temp)
        task_name = Algorithm.objects.get(al_id=temp).al_name
        temp = request.POST.get("groupname").split(" ")[0]
        tom.pr_group = Group.objects.get(gr_id=temp)
        tom.save()
        return HttpResponseRedirect("/tasknew")


order_task = 'pr_name'


def tasknew(request):
    order = Order.objects.get(id=1).order_problem
    if order[-1] == 'd':
        order = '-' + order[:-1]
    algo = Algorithm.objects.all()
    task = Problem.objects.all().order_by(order)
    group = Group.objects.all()
    return render(request, "tasknew.html", {"algo": algo, "task": task, "group": group})


def edittask(request, pr_id):
    algo = Algorithm.objects.all()
    try:
        task = Problem.objects.get(pr_id=pr_id)
        if request.method == "POST":
            task.pr_name = request.POST.get("name")
            task.pr_checkdate = request.POST.get("checkdate")
            task.save()
            return HttpResponseRedirect("/tasknew")
        else:
            return render(request, "edittask.html", {"task": task,"algo": algo})
    except Person.DoesNotExist:
        return HttpResponseNotFound("<h2>Task not found</h2>")


def deletetask(request, pr_id):
    try:
        task = Problem.objects.get(pr_id=pr_id)
        task.delete()
        return HttpResponseRedirect("/tasknew")
    except Problem.DoesNotExist:
        return HttpResponseNotFound("<h2>Task not found</h2>")


def createalgo(request):
    if request.method == "POST":
        tom = Algorithm()
        tom.al_name = request.POST.get("name")
        tom.al_type = request.POST.get("type")
        tom.al_visualization = request.POST.get("visualization")
        tom.al_comment = request.POST.get("comment")
        tom.al_theory = request.POST.get("theory")
        tom.save()
    return HttpResponseRedirect("/algonew")


def editalgo(request, al_id):
    try:
        algo = Algorithm.objects.get(al_id=al_id)
        if request.method == "POST":
            algo.al_name = request.POST.get("name")
            algo.al_type = request.POST.get("type")
            algo.al_visualization = request.POST.get("visualization")
            algo.al_comment = request.POST.get("comment")
            algo.al_theory = request.POST.get("theory")
            algo.save()
            return HttpResponseRedirect("/algonew")
        else:
            return render(request, "editalgo.html", {"algo": algo})
    except Person.DoesNotExist:
        return HttpResponseNotFound("<h2>Person not found</h2>")


def deletealgo(request, al_id):
    try:
        algo = Algorithm.objects.get(al_id=al_id)
        algo.delete()
        return HttpResponseRedirect("/algonew")
    except Person.DoesNotExist:
        return HttpResponseNotFound("<h2>Person not found</h2>")


def order(request):
    order = Order.objects.get(id=1)
    ord = (request.path.split('/'))[-1]
    if ord[:2] == 'st':
        order.order_student = ord
    elif ord[:2] == 'pe':
        order.order_person = ord
    elif ord[:2] == 'pr':
        order.order_problem = ord
    elif ord[:2] == 'al':
        order.order_algorithm = ord
    elif ord[:2] == 'te':
        order.order_teacher = ord
    elif ord[:2] == 'gr':
        order.order_group = ord
    order.save()
    return HttpResponseRedirect('/'.join(request.path.split('/')[:-2]))