from dependencies import *

class MicrofinanceViewSet(mixins.ListModelMixin,
                          mixins.RetrieveModelMixin,
                          mixins.CreateModelMixin,
                          viewsets.GenericViewSet):

    queryset = Microfinance.objects.all()
    serializer_class = MicrofinanceSerializer
    permission_classes = [IsPersonnel]

    @transaction.atomic
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        created_by = request.user

        if not created_by.is_superuser:
            return Response({"status": "Vous n'avez pas les permissions nécessaires"}, status=403)

        serializer.save(created_by=created_by)
        return Response(serializer.data, status=201)

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return Microfinance.objects.all().order_by("-id")

        try:
            personnel = Personnel.objects.get(user=user)
        except Personnel.DoesNotExist:
            return Microfinance.objects.none()

        microfinance = personnel.agence.microfinance

        if user.has_perm("api.view_microfinance", microfinance):
            return Microfinance.objects.filter(nom=microfinance, is_deleted=False).order_by("-id")

        return Microfinance.objects.none()
