from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, RetrieveDestroyAPIView


class PlayListView(ListCreateAPIView):
    pass


class PlayDetailView(RetrieveUpdateAPIView):
    pass


class AccentListView(ListCreateAPIView):
    pass


class AccentDetailView(RetrieveDestroyAPIView):
    pass
