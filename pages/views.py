from django.shortcuts import render, get_object_or_404
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Page
from .serializers import PageSerializer

# Vista 1: Lista completa de páginas
@api_view(['GET'])
def get_pages(request):
    paginas = Page.objects.all()
    serializer = PageSerializer(paginas, many=True)
    return Response(serializer.data)

# Vista 2: Detalle de una página por slug o id
@api_view(['GET'])
def get_page_detail(request, slug):
    try:
        if str(slug).isdigit():
            pagina = Page.objects.get(pk=slug)
        else:
            pagina = Page.objects.get(slug=slug)
        serializer = PageSerializer(pagina)
        return Response(serializer.data)
    except Page.DoesNotExist:
        return Response({'error': 'Página no encontrada'}, status=status.HTTP_404_NOT_FOUND)

class PageDetailView(generics.RetrieveAPIView):
    queryset = Page.objects.all()
    serializer_class = PageSerializer
    lookup_field = 'slug'  # O 'id' si prefieres buscar por ID

def sample(request, page_id, page_slug):

    page = get_object_or_404(Page, id=page_id)

    return render(request, "sample.html",{
        'page': page
    })