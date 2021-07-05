from rest_framework import serializers
from operator import itemgetter
import requests
import json


class PackageFinder:
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


class PackageValidator:
    def __init__(
        self,
        packages,
        PackageFinder,
        PackageInfo,
        error_message,
    ):
        self.packages = list(packages)
        self.package_finder = PackageFinder
        self.package_info = PackageInfo
        self.error_message = error_message

    def validate(self):
        packages = []
        for package in self.packages:
            package_finder = self.package_finder(
                package,
                self.error_message,
            )
            response = package_finder.get()
            release = package.get("version")

            package_info = self.package_info(
                response,
                release,
                self.error_message,
            )
            info = package_info.get()
            packages.append(info)
        return packages


class PackageUpdater:
    def __init__(self, current_list, received_list):
        self.current_list = sorted(current_list, key=itemgetter("name"))
        self.received_list = sorted(received_list, key=itemgetter("name"))

    def update(self):
        if not self.current_list:
            return self.received_list
        current_names = [package["name"] for package in self.current_list]
        for package in self.received_list:
            if package["name"] in current_names:
                self.current_list = [
                    item
                    for item in self.current_list
                    if item["name"] != package["name"]
                ]
            self.current_list.append(package)
        return sorted(self.current_list, key=itemgetter("name"))
