from django.shortcuts import render
from django.views.generic import View
from django.shortcuts import render
from django.http import HttpResponseRedirect

#def index(request):
#    HttpResponse("Hello, world. You're at the polls index.")

class map(View):
    """docstring for map."""

    def __init__(self, arg):
        super(map, self).__init__()
        self.arg = arg

class map_View(View):
    initial={'kay':'value'}
    #form_class=Paciente_Form
    template_name = 'mezzanine_gasStation_map/map.html'

    def get(self, request, *args, **kwargs):
        #var1 = self.kwargs['var1']
        return render(request, self.template_name)
