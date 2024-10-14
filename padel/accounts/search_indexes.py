from haystack import indexes
from accounts.models import ComplejoDePadel

class ComplejoDePadelIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    nombre_complejo = indexes.CharField(model_attr='nombre_complejo')
    tipo_instalacion = indexes.CharField(model_attr='tipo_instalacion')
    provincia = indexes.CharField(model_attr='provincia')
    ciudad = indexes.CharField(model_attr='ciudad')

    content_auto = indexes.EdgeNgramField(model_attr='nombre_complejo')
    

    def get_model(self):
        return ComplejoDePadel

    def index_queryset(self, using=None):
        return self.get_model().objects.all()