from dal import autocomplete
from sectors.models import Sector

class SectorAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return Sector.objects.none()

        qs = Sector.objects.filter(numchild=0)

        if self.q:
            qs = qs.filter(label__istartswith=self.q)

        return qs