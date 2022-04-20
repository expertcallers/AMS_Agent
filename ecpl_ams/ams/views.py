from datetime import datetime, date, timedelta
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.shortcuts import render, redirect
from .models import *
import calendar
from django.http import HttpResponse
from django.db.models import Q, Sum
from django.apps import apps

# Create your views here.
Profile = apps.get_model('mapping', 'Profile')
agent_list = ['Client Relationship Officer', 'MIS Executive', 'Patrolling officer',
              'Data Analyst', 'Business Development Executive', 'Content Developer',
              'Junior Developer', 'Web Developer', 'Trainee Developer', 'Jr Dev', 'CRO',
              ]


def loginPage(request):  # Test1
    logout(request)
    form = AuthenticationForm()
    data = {'form': form}
    return render(request, 'login.html', data)


def logoutView(request):  # Test1
    logout(request)
    return redirect('/ams/')


def loginAndRedirect(request):  # Test1
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if request.user.profile.pc == False:
                return redirect('/ams/change-password')
            else:
                return redirect('/ams/agent-dashboard')
        else:
            form = AuthenticationForm()
            messages.info(request, 'Invalid Credentials')
            data = {'form': form}
            return render(request, 'login.html', data)
    else:
        logout(request)
        form = AuthenticationForm()
        data = {'form': form}
        return render(request, 'login.html', data)


@login_required
def change_password(request):  # Test1
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            user = request.user
            user.profile.pc = True
            user.save()
            user.profile.save()
            logout(request)
            return redirect('/ams/')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change-password.html', {'form': form})


@login_required
def agentDashBoard(request):  # Test1
    if request.user.profile.emp_desi in agent_list:
        emp_id = request.user.profile.emp_id
        emp = Profile.objects.get(emp_id=emp_id)
        # Leave status
        leave_hist = LeaveTable.objects.filter(Q(emp_id=emp_id), Q(leave_type__in=['SL', 'PL', 'ML'])).order_by(
            '-id')[:5]
        # Month view
        month_days = []
        todays_date = date.today()
        year = todays_date.year
        month = todays_date.month
        a, num_days = calendar.monthrange(year, month)
        start_date = date(year, month, 1)
        end_date = date(year, month, num_days)
        delta = timedelta(days=1)
        while start_date <= end_date:
            month_days.append(start_date.strftime("%Y-%m-%d"))
            start_date += delta
        month_cal = []
        for i in month_days:
            dict = {}
            try:
                st = EcplCalander.objects.get(Q(date=i), Q(emp_id=emp_id)).att_actual
            except EcplCalander.DoesNotExist:
                st = 'Unmarked'
            dict['dt'] = i
            dict['st'] = st
            month_cal.append(dict)
        data = {'emp': emp, 'leave_hist': leave_hist, 'month_cal': month_cal}
        return render(request, 'agent-dashboard-new.html', data)
    else:
        return redirect('http://hrms.ecpl.com/ams/login')


@login_required
def uploadImageToDB(request):  # Test1
    if request.method == 'POST':
        user_image = request.FILES['user-img']
        id = request.POST['id']
        prof = Profile.objects.get(id=id)
        prof.img = user_image
        prof.save()
        return redirect('/ams/agent-dashboard')
    else:
        pass


@login_required
def agentSettings(request):  # Test1
    emp_id = request.user.profile.emp_id
    emp = Profile.objects.get(emp_id=emp_id)
    form = PasswordChangeForm(request.user)
    data = {'emp': emp, 'form': form}
    return render(request, 'agent-settings.html', data)


@login_required
def applyLeave(request):  # Test1
    if request.method == 'POST':
        emp_name = request.POST["emp_name"]
        emp_id = request.POST["emp_id"]
        prof = Profile.objects.get(emp_id=emp_id)
        emp_desi = prof.emp_desi
        emp_process = prof.emp_process
        emp_rm1_id = prof.emp_rm1_id
        emp_rm2_id = prof.emp_rm2_id
        emp_rm3_id = prof.emp_rm3_id
        emp_rm1 = prof.emp_rm1
        emp_rm2 = prof.emp_rm2
        emp_rm3 = prof.emp_rm3
        leave_type = request.POST["type"]
        start_date = request.POST["startdate"]
        end_date = request.POST["enddate"]
        no_days = request.POST["leave_days"]
        agent_reason = request.POST["reason"]
        unique_id = request.POST['csrfmiddlewaretoken']

        leaves = LeaveTable.objects.filter(emp_id=emp_id)
        leave_dates_list = []
        for i in leaves:
            while i.start_date <= i.end_date:
                leave_dates_list.append(i.start_date)
                i.start_date += timedelta(days=1)
        new_leave_dates = []
        list_start_date = date.fromisoformat(start_date)  # To Convert type of start_date from string to date
        list_end_date = date.fromisoformat(end_date)  # To Convert type of end_date from string to date
        while list_start_date <= list_end_date:
            new_leave_dates.append(list_start_date)
            list_start_date += timedelta(days=1)

        common_dates = set(leave_dates_list) & set(new_leave_dates)
        if common_dates:
            messages.error(request, "Leaves have already been applied for selected date(s).")
            return redirect('/ams/ams-apply_leave')
        else:
            e = LeaveTable()
            e.unique_id = unique_id
            e.applied_date = date.today()
            e.leave_type = leave_type
            e.start_date = start_date
            e.end_date = end_date
            e.no_days = no_days
            e.agent_reason = agent_reason
            e.emp_name = emp_name
            e.emp_id = emp_id
            e.emp_desi = emp_desi
            e.emp_process = emp_process
            e.emp_rm1 = emp_rm1
            e.emp_rm2 = emp_rm2
            e.emp_rm3 = emp_rm3
            e.emp_rm1_id = emp_rm1_id
            e.emp_rm2_id = emp_rm2_id
            e.emp_rm3_id = emp_rm3_id
            rm1_desi = Profile.objects.get(emp_id=emp_rm1_id).emp_desi

            e.save()
            leave_balance = EmployeeLeaveBalance.objects.get(emp_id=emp_id)
            if leave_type == 'PL':
                leave_balance.pl_balance -= int(no_days)
                leave_balance.save()
            elif leave_type == 'SL':
                leave_balance.sl_balance -= int(no_days)
                leave_balance.save()
            return redirect('/ams/ams-apply_leave')
    else:
        emp_id = request.user.profile.emp_id
        emp = Profile.objects.get(emp_id=emp_id)
        leave = LeaveTable.objects.filter(emp_id=emp_id)

        try:
            Profile.objects.get(emp_id=emp_id, doj=None)
            doj = date(2020, 1, 1)
            today = date.today()
            probation = (today - doj).days
        except Profile.DoesNotExist:
            if emp.doj == None:
                doj = date(2020, 1, 1)
            else:
                doj = emp.doj
            today = date.today()
            probation = (today - doj).days
        try:
            leave_balance = EmployeeLeaveBalance.objects.get(emp_id=emp_id)
        except EmployeeLeaveBalance.DoesNotExist:
            leave_balance = {'sl_balance': 0, 'pl_balance': 0}
        leave_his = leaveHistory.objects.filter(emp_id=emp_id).values('date', 'transaction',
                                                                      'leave_type', 'total').annotate(
            no_days=Sum('no_days'))
        data = {'emp': emp, 'leave': leave, 'leave_balance': leave_balance, 'probation': probation,
                'leave_his': leave_his}
        return render(request, 'apply-leave.html', data)


@login_required
def addAttendance(request):
    month = 4
    year = 2022
    start_date = date(year, month, 1)
    last = calendar.monthrange(year, month)[1]
    last_date = date(year, month, last)
    delta = last_date - start_date
    date_list = []
    for i in range(delta.days + 1):
        day = start_date + timedelta(days=i)
        date_list.append(day)
    profile = Profile.objects.filter(agent_status='Active')
    for i in date_list:
        for j in profile:
            ec_cal = EcplCalander.objects.filter(emp_id=j.emp_id, date=i).count()
            if ec_cal < 1:
                cal = EcplCalander.objects.create(date=i, emp_id=j.emp_id, att_actual='Unmarked', emp_name=j.emp_name,
                                                  emp_desi=j.emp_desi,
                                                  team=j.emp_process, team_id=j.emp_process_id, rm1=j.emp_rm1,
                                                  rm2=j.emp_rm2, rm3=j.emp_rm3, rm1_id=j.emp_rm1_id,
                                                  rm2_id=j.emp_rm2_id, rm3_id=j.emp_rm3_id)
                cal.save()
    return redirect('/ams/agent-dashboard')


@login_required
def SLProofSubmit(request):  # Test1
    if request.method == 'POST':
        id = request.POST['id']
        proof = request.FILES['proof']
        leave = LeaveTable.objects.get(id=id)
        last_date = leave.end_date
        timee = (date.today() - last_date).days
        if timee <= 2:
            leave.proof = proof
            leave.save()
            return redirect('/ams/ams-apply_leave')
        else:
            messages.info(request, "The time has exceeded cannot upload now :)")
            return redirect('/ams/ams-apply_leave')


@login_required
def applyEscalation(request):  # Test1
    if request.method == "POST":
        id = request.POST["id"]
        reason = request.POST['reason']
        e = LeaveTable.objects.get(id=id)
        e.escalation = True
        e.escalation_reason = reason
        e.save()
        emp_id = e.emp_id
        no_days = e.no_days
        type = e.leave_type
        a = EmployeeLeaveBalance.objects.get(emp_id=emp_id)
        if type == "PL":
            a.pl_balance = a.pl_balance - no_days
        else:
            a.sl_balance = a.sl_balance - no_days
        a.save()
        messages.info(request, "Leave Escalated Successfully!")
        return redirect('/ams/ams-apply_leave')
    else:
        pass
