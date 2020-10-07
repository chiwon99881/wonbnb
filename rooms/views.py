from django.views.generic import ListView
from django.http import Http404
from django.shortcuts import render
from django.utils import timezone
from . import models as room_models


class HomeView(ListView):

    """ HomeView Definition """

    model = room_models.Room
    paginate_by = 10
    paginate_orphans = 5
    ordering = "created"
    template_name = "rooms/home.html"
    template_name_suffix = ""
    context_object_name = "rooms"

    # 모든 Class Based View 는 get_context_data를 가진다.
    # context에 기존에 있는 값들에 + now 라는 값을 추가해준다.
    # 만약 첫번째 줄에 super()구문을 쓰지 않는다면 기존에 부모 클래스인 ListView가 가지고 있는
    # 모든 데이터들이 날라가므로 반드시 첫 줄에 작성해줘야 한다.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        context["now"] = now
        return context


def room_detail(request, pk):
    try:
        room = room_models.Room.objects.get(pk=pk)
        return render(request, "rooms/detail.html", context={"room": room})
    except room_models.Room.DoesNotExist:
        raise Http404()
