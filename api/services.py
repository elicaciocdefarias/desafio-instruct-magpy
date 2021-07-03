from rest_framework import serializers
import requests
import json


class PackageRequest:
    def __init__(self, package, error_message):
        self.package = package
        self.error_message = error_message

    def get(self):
        url = "https://pypi.python.org/pypi/%s/json" % self.package["name"]
        response = requests.get(url)
        try:
            return response.json()
        except json.JSONDecodeError:
            raise serializers.ValidationError({"error": self.error_message})


class PackageInfo:
    def __init__(self, response, release, error_message):
        self.release = release
        self.error_message = error_message
        self.name = response["info"]["name"]
        self.version = response["info"]["version"]
        self.releases = list(response["releases"].keys())

    def get(self):
        context = {}
        context["name"] = self.name
        if self.release is None:
            context["version"] = self.version
        elif self.release in self.releases:
            context["version"] = self.release
        else:
            raise serializers.ValidationError({"error": self.error_message})
        return context


class PackageValidate:
    def __init__(
        self,
        packages,
        PackageRequest,
        PackageInfo,
        error_message,
    ):
        self.packages = list(packages)
        self.package_request = PackageRequest
        self.package_info = PackageInfo
        self.error_message = error_message

    def validate(self):
        packages = []
        for package in self.packages:
            package_request = self.package_request(
                package,
                self.error_message,
            )
            response = package_request.get()
            release = package.get("version")

            package_info = self.package_info(
                response,
                release,
                self.error_message,
            )
            info = package_info.get()
            packages.append(info)
        return packages
