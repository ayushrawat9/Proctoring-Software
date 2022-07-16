from django.shortcuts import render
from django.http import HttpResponseRedirect

from .forms import QAUploadForm
import logging
from coolname import generate_slug
import pandas as pd
from .models import *
from students.models import *
from accounts.models import *


def index(request):
    return render(request, "teachers/home.html")


def create_test_objective(request):
    if request.method == 'POST':
        form = QAUploadForm(request.POST, request.FILES)
        if form.is_valid():
            logging.info(form.cleaned_data)

            test_id = generate_slug(2)
            test_id = test_id.replace("-","_")
            filestream = form.cleaned_data.get('doc')
            filestream.seek(0)
            df = pd.read_csv(filestream)
            fields = ['question_id', 'question', 'option_a', 'option_b', 'option_c', 'option_d', 'ans', 'marks']
            df = pd.DataFrame(df, columns=fields)

            for row in df.index:
                test_obj = TestObjective()
                test_obj.test_id = test_id
                test_obj.question_id = df['question_id'][row]
                test_obj.question = df['question'][row]
                test_obj.option_a = df['option_a'][row]
                test_obj.option_b = df['option_b'][row]
                test_obj.option_c = df['option_c'][row]
                test_obj.option_d = df['option_d'][row]
                test_obj.ans = df['ans'][row]
                test_obj.marks = df['marks'][row]
                test_obj.save()

            test_teacher_join = TeacherTestJoin()
            test_teacher_join.test_id = test_id
            test_teacher_join.teacher_id = request.user.username
            test_teacher_join.save()

            test_information = TestInformation()
            test_information.test_id = test_id
            test_information.type = "Objective"
            test_information.subject = form.cleaned_data.get('subject')
            test_information.topic = form.cleaned_data.get('topic')
            test_information.start_date = form.cleaned_data.get('start_date')
            test_information.start_time = form.cleaned_data.get('start_time')
            test_information.end_date = form.cleaned_data.get('end_date')
            test_information.end_time = form.cleaned_data.get('end_time')
            test_information.duration = form.cleaned_data.get('duration')
            test_information.neg_mark = form.cleaned_data.get('neg_mark')
            test_information.password = form.cleaned_data.get('password')
            test_information.proctor_type = form.cleaned_data.get('proctor_type')
            test_information.save()

            return HttpResponseRedirect('/teachers')
        else:
            return render(request, "teachers/create-test-obj.html", {'form': form.as_p()})

    form = QAUploadForm()
    return render(request, "teachers/create-test-obj.html", {'form': form.as_p()})


def create_test_subjective(request):
    if request.method == 'POST':
        form = QAUploadForm(request.POST, request.FILES)
        if form.is_valid():
            logging.info(form.cleaned_data)

            test_id = generate_slug(1)
            filestream = form.cleaned_data.get('doc')
            filestream.seek(0)
            df = pd.read_csv(filestream)
            fields = ['question_id', 'question', 'marks']
            df = pd.DataFrame(df, columns=fields)

            for row in df.index:
                test_obj = TestSubjective()
                test_obj.test_id = test_id
                test_obj.question_id = df['question_id'][row]
                test_obj.question = df['question'][row]
                test_obj.marks = df['marks'][row]
                test_obj.save()

            test_teacher_join = TeacherTestJoin()
            test_teacher_join.test_id = test_id
            test_teacher_join.teacher_id = request.user.username
            test_teacher_join.save()

            test_information = TestInformation()
            test_information.type = "Subjective"
            test_information.test_id = test_id
            test_information.subject = form.cleaned_data.get('subject')
            test_information.topic = form.cleaned_data.get('topic')
            test_information.start_date = form.cleaned_data.get('start_date')
            test_information.start_time = form.cleaned_data.get('start_time')
            test_information.end_date = form.cleaned_data.get('end_date')
            test_information.end_time = form.cleaned_data.get('end_time')
            test_information.duration = form.cleaned_data.get('duration')
            test_information.neg_mark = form.cleaned_data.get('neg_mark')
            test_information.password = form.cleaned_data.get('password')
            test_information.proctor_type = form.cleaned_data.get('proctor_type')
            test_information.save()

            return HttpResponseRedirect('/teachers')
        else:
            return render(request, "teachers/create-test-subj.html", {'form': form.as_p()})

    form = QAUploadForm()
    return render(request, "teachers/create-test-subj.html", {'form': form.as_p()})


def view_question(request):
    tests = TeacherTestJoin.objects.filter(teacher_id=request.user.username)
    if request.method == 'POST':
        logging.debug(f"fetching questions for test_id {request.POST}")
        test_id = request.POST['test_id']
        test = TestInformation.objects.filter(test_id=test_id)
        test_type = test[0].type
        if test_type == "Subjective":
            questions = TestSubjective.objects.filter(test_id=test_id)
            context = {"tests": tests, "questions": questions, "type": "Subjective"}
        if test_type == "Objective":
            questions = TestObjective.objects.filter(test_id=test_id)
            context = {"tests": tests, "questions": questions, "type": "Objective"}
        return render(request, "teachers/view-questions.html", context=context)

    context = {"tests": tests}
    return render(request, "teachers/view-questions.html", context=context)


def view_tests_logs(request):
    tests = TeacherTestJoin.objects.filter(teacher_id=request.user.username)
    students = UserProfile.objects.filter(role="student")
    if request.method == 'POST':
        test_id = request.POST['test_id']
        student_id = request.POST['student_id']
        proctoring_logs = ProctoringLog.objects.filter(test_id=test_id, student_id=student_id).order_by("-timestamp")
        context = {"proctoring_logs": proctoring_logs, "tests": tests, "students": students}
        return render(request, "teachers/view-proctor-logs.html", context=context)

    context = {"tests": tests, "students": students}
    return render(request, "teachers/view-proctor-logs.html", context=context)


def view_live_tests_logs(request):
    tests = TeacherTestJoin.objects.filter(teacher_id=request.user.username)

    if request.method == 'POST':
        test_id = request.POST['test_id']
        context = {"tests": tests, "room_name": test_id}
        return render(request, "teachers/view-live-proctor-logs.html", context=context)

    context = {"tests": tests}
    return render(request, 'teachers/view-live-proctor-logs.html', context=context)
