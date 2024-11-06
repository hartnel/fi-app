from dal import autocomplete
from churchs.models import Church
from sectors.models import Sector

class SectorAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return Sector.objects.none()

        qs = Sector.objects.filter(numchild__lte=1)

        if self.q:
            qs = qs.filter(label__istartswith=self.q)

        return qs
    
    
class ChurchAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return Church.objects.none()

        qs = Church.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs