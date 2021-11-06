from django.core.checks import messages
from django.db.models.query_utils import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse, response , Http404
from .models import *
from .forms import NewTopicForm
# Create your views here.
def home(request):
    boards = Board.objects.all() #django model api
    return render(request, 'boards/home.html', { 'boards': boards}) #check template in boards app


def board_topics(request, id):
    # try:
    #     board = Board.objects.get(id=id)
    # except Board.DoesNotExist:
    #     raise Http404
    board = get_object_or_404(Board, id=id)
    topics = board.topics.all()
    return render(request, 'boards/topics.html',{'board':board, 'topics':topics})


def new_topic(request, id):
    board = get_object_or_404(Board, id=id)
    user = User.objects.first()  # User model has only admin user.
    
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False) # newtopicform.save() return topic we can get it without save with commit=false
            topic.board = board
            topic.user = user
            topic.save()


            post = Post.objects.create(
                message = form.cleaned_data.get('message'),
                topic  = topic,
                created_by = user
            )

            return redirect('board_topics', id = board.id)
    else:
        form = NewTopicForm()
    return render(request, 'boards/new_topic.html', {'board': board, 'form': form}) # pass board we need id to make url