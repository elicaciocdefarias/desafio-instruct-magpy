from api.services import PackageRequest, PackageInfo, PackageValidate
from rest_framework import serializers
from .models import PackageRelease, Project

from copy import deepcopy
from rest_framework.views import exception_handler

PACKAGE_DOES_NOT_EXISTS = "One or more packages doesn't exist"


def packages_exception_handler(exc, context):
    response = exception_handler(exc, context)
    error_message = response.data.get("packages")
    if "packages" in response.data and error_message[0] == PACKAGE_DOES_NOT_EXISTS:
        data = deepcopy(response.data)
        data.pop("packages")
        data["error"] = PACKAGE_DOES_NOT_EXISTS
        response.data = data
    return response


class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackageRelease
        fields = ["name", "version"]
        extra_kwargs = {"version": {"required": False}}


class ProjectSerializer(serializers.ModelSerializer):
    packages = PackageSerializer(many=True)

    class Meta:
        model = Project
        fields = ["name", "packages"]

    def create(self, validated_data):
        packages = validated_data.pop("packages")
        package_validate = PackageValidate(
            packages,
            PackageRequest,
            PackageInfo,
            PACKAGE_DOES_NOT_EXISTS,
        )
        validated_packages = package_validate.validate()
        project = Project.objects.create(**validated_data)
        for package in validated_packages:
            PackageRelease.objects.create(project=project, **package)
        return project
