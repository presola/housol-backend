#!/usr/bin/env python

import coreapi
import coreschema
from rest_framework.schemas import ManualSchema
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .views import process_structure, get_struc


get_extra_fields = [
    coreapi.Field(
        "id",
        required=True,
        location="path",
        example="1",
        description='ID of structure',
        schema=coreschema.String()
    ),
]
post_extra_fields = [
    coreapi.Field(
        "id",
        required=True,
        location="path",
        example="1",
        description='ID of structure',
        schema=coreschema.String()
    ),
    coreapi.Field(
        "predict",
        required=True,
        location="form",
        example="false",
        description='For Prediction or Filtering',
        schema=coreschema.Boolean()
    ),
    coreapi.Field(
        "State",
        required=False,
        location="form",
        example="false",
        description='state to filter by',
        schema=coreschema.String()
    ),
    coreapi.Field(
        "Metro",
        required=True,
        location="form",
        description='metro to filter by',
        schema=coreschema.String()
    ),
    coreapi.Field(
        "RegionID",
        required=True,
        location="form",
        description='region id',
        schema=coreschema.String()
    ),
    coreapi.Field(
        "RegionType",
        required=True,
        location="form",
        description='region type',
        schema=coreschema.String()
    ),
    coreapi.Field(
        "start_date",
        required=True,
        location="form",
        description='start date',
        schema=coreschema.String()
    ),
    coreapi.Field(
        "end_date",
        required=True,
        location="form",
        description='end date',
        schema=coreschema.String()
    ),
]

class CustomIDSchema(ManualSchema):
    """
    Overrides `get_link()` to provide Custom Behavior X
    """
    def get_link(self, path, method, base_url):
        if method == 'POST':
            self._fields = post_extra_fields
        if method == 'GET':
            self._fields = get_extra_fields
        link = super().get_link(path, method, base_url)
        # Do something to customize link here...
        return link



class StructureViewSet(APIView):
    """
    get:
        Get all available structures
    """
    permission_classes = [IsAuthenticated]

    @csrf_exempt
    def get(self, request, *args, **kwargs):
        return get_struc(kwargs)


class StructureViewIDSet(APIView):
    permission_classes = [IsAuthenticated]
    schema = CustomIDSchema(fields=[])

    @csrf_exempt
    def get(self, request, *args, **kwargs):
        return get_struc(kwargs)

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        return process_structure(request, kwargs["id"])
