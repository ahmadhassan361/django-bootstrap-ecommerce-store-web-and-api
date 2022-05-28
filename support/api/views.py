from rest_framework.response import Response
from .. import models
from . import serializer
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import AllowAny

@api_view(['GET'])
@permission_classes([AllowAny])
def get_faq(request):
    faq = models.FAQ.objects.all()
    serialized_faq = serializer.FAQSerializer(faq,many=True)
    return Response(serialized_faq.data)
