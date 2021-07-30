from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Question, Choice


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now()).exclude(
            choice__choice_text__isnull=True).order_by('-pub_date')[:10]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        excludes any questions that aren't published yet
        :return: object filtered
        """
        # return Question.objects.filter(pub_date__lte=timezone.now()).exclude(
        #     choice__choice_text__isnull=True) chcac tego uzyc trzeba najpierw wejsc na strone index i tam dodac
        # warunek ze jesli question nie ma chocies to wtedy nie przekierowywac

        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
        print(selected_choice)
        print(selected_choice.votes)

    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[0:5]
#     context = {
#         'latest_question_list': latest_question_list,
#     }
#     return render(request, 'polls/index.html', context)
#
#class DetailView(generic.DetailView):
    # model = Question
    # template_name = 'polls/detail.html'
# def detail(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     print(f'wyswietl question {question}')
#     return render(request, 'polls/detail.html', {'question': question})
#
# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/results.html', {'question': question})
#

# Article.objects.filter(reporter__full_name__startswith='John')
# from django.db.models import Q
# Q(question__startswith='Wh
# Q(question__startswith='Who') | Q(question__startswith='What')
# Poll.objects.get(
#     Q(pub_date=date(2005, 5, 2)) | Q(pub_date=date(2005, 5, 6)),
#     question__startswith='Who',
# )
#
# Entry.objects.filter(
# ...     headline__startswith='What'
# ... ).exclude(
# ...     pub_date__gte=datetime.date.today()

# Blog.objects.filter(entry__headline__contains='Lennon', entry__pub_date__year=2008)
# Blog.objects.exclude(
#     entry__headline__contains='Lennon',
#     entry__pub_date__year=2008,
# )
