from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import Question, Choice
from django.urls import reverse

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list' : latest_question_list}
    #return HttpResponse('Hello')
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
    #question = Question.objects.get(pk=question_id)
    
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/detail.html", {'question' : question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id) 
    try:
        print("choice id " + request.POST['choice'])
        # request.POST['choice']는 name값을 찾아서 id값을 반환한다.
        select_choice = question.choice_set.get(pk=request.POST['choice'])
        #request.POST['choice'] 가 없으면 KeyError를 반환한다.
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question':question,
            'error_message':"You didn't select a choice"
        })
    else:
        select_choice.votes += 1
        select_choice.save()
        # 다른웹언어처럼 변경이 정상적으로 되면 html파일로 바로 가는 것이 아니라 
        # url로 redirect해준다. 이것은 웹개발 권장사항이다.
        # 그렇다면 redirect시에 /<int:question_id>/results/ 이런 주소가 나와야 하는데
        # 접근 방식은 namespace방식인 polls:results이다.
        # 보통 html에서는 {% url 'polls:results' question.id %} 이렇게 호출한다.
        # views에서는 reverse함수를 사용해서 접근하면서 param을 넘긴다.
        # ex) /polls/3/results/
        # 중요 : args의 인수에는 ,가 들어가지 않으면 string, ,가 들어가면 int로 인식
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question' : question})