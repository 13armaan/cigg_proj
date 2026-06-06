from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse
import zipfile
import io
import os

from .models import Album
from .serializers import AlbumSerializer,AlbumListSerializer
from accounts.permissions import IsVerified, IsCoordinator, IsAdmin, IsAdminOrCoordinator

# albums/views.py
class AlbumViewSet(ModelViewSet):
    queryset = Album.objects.all().order_by("-created_at")

    def get_serializer_class(self):
        if self.action == "list":
            return AlbumListSerializer
        return AlbumSerializer

    def get_permissions(self):
        if self.action in ["create", "destroy"]:
            return [IsAdmin()]
        if self.action in ["update", "partial_update"]:
            return [IsAuthenticated(), IsAdminOrCoordinator()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=["get"], permission_classes=[IsAuthenticated, IsVerified])
    def download_all(self, request, pk=None):
        album = self.get_object()
        photos = album.photo_set.all()

        if not photos.exists():
            return HttpResponse("No photos in this album.", status=404)

        # Create an in-memory ZIP file
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            for photo in photos:
                if photo.original_img and os.path.exists(photo.original_img.path):
                    file_path = photo.original_img.path
                    file_name = os.path.basename(file_path)
                    zip_file.write(file_path, arcname=file_name)

        zip_buffer.seek(0)
        response = HttpResponse(zip_buffer, content_type="application/zip")
        response["Content-Disposition"] = f'attachment; filename="album_{album.album_id}_photos.zip"'
        return response