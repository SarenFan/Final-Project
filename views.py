from django.shortcuts import render, get_object_or_404, redirect
from .models import Course, Lesson, Enrollment, Question, Choice, Submission

def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    # Grab the current enrollment for the user
    enrollment = Enrollment.objects.get(user=request.user, course=course)
    submission = Submission.objects.create(enrollment=enrollment)
    
    # Check selected choices
    for question in course.question_set.all():
        for choice in question.choice_set.all():
            choice_id = request.POST.get(f'choice_{choice.id}')
            if choice_id:
                selected_choice = Choice.objects.get(pk=choice_id)
                submission.choices.add(selected_choice)
    
    submission.save()
    return redirect('onlinecourse:show_exam_result', course_id=course.id, submission_id=submission.id)

def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)
    
    # Calculate the score
    total_questions = course.question_set.count()
    correct_answers = 0
    
    for question in course.question_set.all():
        selected_choices = submission.choices.filter(question=question)
        correct_choices = question.choice_set.filter(is_correct=True)
        
        # Check if the user selected exactly the correct choices
        if set(selected_choices) == set(correct_choices):
            correct_answers += 1
            
    score = int((correct_answers / total_questions) * 100) if total_questions > 0 else 0
    passed = score >= 80 # Assuming 80 is the passing grade
    
    context = {
        'course': course,
        'score': score,
        'passed': passed,
    }
    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)
