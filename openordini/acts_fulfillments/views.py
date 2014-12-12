# Create your views here.

from open_municipio.acts.views import ActDetailView
from .models import Fascicolo

class FascicoloDetailView(ActDetailView):
    model = Fascicolo
