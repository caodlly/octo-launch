from rest_framework import mixins
from rest_framework import generics


class ListLookupField(mixins.ListModelMixin,
                      generics.RetrieveAPIView,
                      generics.GenericAPIView):

    lookup_field = 'pk'

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk is not None:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)


class LookUpMethod(ListLookupField, generics.DestroyAPIView, generics.UpdateAPIView):
    pass


class ListCreateMethod(generics.ListAPIView, generics.CreateAPIView):
    pass
