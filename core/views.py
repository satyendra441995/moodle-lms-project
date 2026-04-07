from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .forms import CustomUserCreationForm, CourseForm, AssignmentForm, SubmissionGradeForm, StudentSubmissionForm
from .models import Course, Assignment, Submission

def index(request):
    if request.user.is_authenticated:
        if request.user.is_teacher:
            return redirect('teacher_dashboard')
        elif request.user.is_student:
            return redirect('student_dashboard')
        else:
            return render(request, 'core/index.html')
    return render(request, 'core/index.html')

def register(request):
    if request.user.is_authenticated:
        return redirect('index')
        
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome, {user.username}! Your account has been created.")
            return redirect('index')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'core/register.html', {'form': form})

@login_required
def teacher_dashboard(request):
    if not request.user.is_teacher:
        messages.error(request, "Access denied. Only teachers can view this page.")
        return redirect('index')
    courses = request.user.courses_taught.all()
    return render(request, 'core/teacher_dashboard.html', {'courses': courses})

@login_required
def create_course(request):
    if not request.user.is_teacher:
        return redirect('index')
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.teacher = request.user
            course.save()
            messages.success(request, "Course created successfully!")
            return redirect('teacher_dashboard')
    else:
        form = CourseForm()
    return render(request, 'core/create_course.html', {'form': form})

@login_required
def teacher_course_detail(request, course_id):
    if not request.user.is_teacher:
        return redirect('index')
    course = get_object_or_404(Course, id=course_id, teacher=request.user)
    assignments = course.assignments.all()
    return render(request, 'core/teacher_course_detail.html', {'course': course, 'assignments': assignments})

@login_required
def student_dashboard(request):
    if not request.user.is_student:
        messages.error(request, "Access denied. Only students can view this page.")
        return redirect('index')
    enrolled_courses = request.user.enrolled_courses.all()
    return render(request, 'core/student_dashboard.html', {'courses': enrolled_courses})

@login_required
def course_list(request):
    if not request.user.is_student:
        return redirect('index')
    courses = Course.objects.all()
    enrolled = request.user.enrolled_courses.values_list('id', flat=True)
    return render(request, 'core/course_list.html', {'courses': courses, 'enrolled': enrolled})

@login_required
def enroll_course(request, course_id):
    if not request.user.is_student:
        return redirect('index')
    course = get_object_or_404(Course, id=course_id)
    course.students.add(request.user)
    messages.success(request, f"Successfully enrolled in {course.title}!")
    return redirect('student_dashboard')

@login_required
def student_course_detail(request, course_id):
    if not request.user.is_student:
        return redirect('index')
    course = get_object_or_404(Course, id=course_id, students=request.user)
    assignments = course.assignments.all()
    # Find which ones are submitted
    user_submissions = Submission.objects.filter(student=request.user, assignment__course=course)
    submitted_assignment_ids = user_submissions.values_list('assignment_id', flat=True)
    
    return render(request, 'core/student_course_detail.html', {
        'course': course, 
        'assignments': assignments,
        'submitted_assignment_ids': submitted_assignment_ids,
        'submissions': {sub.assignment_id: sub for sub in user_submissions}
    })

@login_required
def submit_assignment(request, assignment_id):
    if not request.user.is_student:
        return redirect('index')
    assignment = get_object_or_404(Assignment, id=assignment_id, course__students=request.user)
    
    # Check if already submitted
    submission = Submission.objects.filter(assignment=assignment, student=request.user).first()
    
    if request.method == 'POST':
        form = StudentSubmissionForm(request.POST, request.FILES, instance=submission)
        if form.is_valid():
            sub = form.save(commit=False)
            sub.assignment = assignment
            sub.student = request.user
            sub.status = 'submitted' # or pending
            sub.save()
            messages.success(request, "Assignment submitted successfully!")
            return redirect('student_course_detail', course_id=assignment.course.id)
    else:
        form = StudentSubmissionForm(instance=submission)
        
    return render(request, 'core/submit_assignment.html', {'form': form, 'assignment': assignment, 'submission': submission})


@login_required
def create_assignment(request, course_id):
    if not request.user.is_teacher:
        return redirect('index')
    course = get_object_or_404(Course, id=course_id, teacher=request.user)
    if request.method == 'POST':
        form = AssignmentForm(request.POST, request.FILES)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.course = course
            assignment.save()
            messages.success(request, "Assignment created successfully!")
            return redirect('teacher_course_detail', course_id=course.id)
    else:
        form = AssignmentForm()
    return render(request, 'core/create_assignment.html', {'form': form, 'course': course})

@login_required
def grade_submissions(request, assignment_id):
    if not request.user.is_teacher:
        return redirect('index')
    assignment = get_object_or_404(Assignment, id=assignment_id, course__teacher=request.user)
    submissions = assignment.submissions.all()
    
    if request.method == 'POST':
        sub_id = request.POST.get('submission_id')
        submission = get_object_or_404(Submission, id=sub_id, assignment=assignment)
        form = SubmissionGradeForm(request.POST, instance=submission)
        if form.is_valid():
            sub = form.save(commit=False)
            sub.status = 'graded'
            sub.save()
            messages.success(request, f"Graded submission for {submission.student.username}")
            return redirect('grade_submissions', assignment_id=assignment.id)

    return render(request, 'core/grade_submissions.html', {'assignment': assignment, 'submissions': submissions})
