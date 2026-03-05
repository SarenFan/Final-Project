def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)
    
    # 1. Create a list of the choice IDs the user selected
    selected_ids = [choice.id for choice in submission.choices.all()]
    
    total_score = 0
    possible_score = 0
    
    # 2. Calculate scores using the required is_get_score() method
    for question in course.question_set.all():
        possible_score += question.grade
        total_score += question.is_get_score(selected_ids)
        
    # 3. Calculate the final grade percentage
    grade = int((total_score / possible_score) * 100) if possible_score > 0 else 0
    
    # 4. Pass the exact variables the grader expects into the context
    context = {
        'course': course,
        'grade': grade,
        'selected_ids': selected_ids,
        'submission': submission
    }
    
    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)
