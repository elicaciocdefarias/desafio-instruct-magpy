import pytest
import json

from api.services import PackageInfo, PackageRequest, PackageValidate
from rest_framework import serializers


@pytest.fixture
def package_request():
    package = {
        "name": "cronos",
        "packages": [
            {"name": "Django"},
        ],
    }
    return PackageRequest(package, "error message")


class TestPackageRequest:
    def test__deve_retornar_uma_instancia_de_dicionario__quando_a_resposta_for_um_json_valido(
        self,
        mocker,
        package_request,
    ):
        def get(*args):
            return json.loads('{"key": "value"}')

        mocker.patch.object(
            package_request,
            "get",
            get,
        )

        result = package_request.get()
        assert isinstance(result, dict)

    def test__deve_lancar_excecao__quando_a_reposta_for_um_json_invalido(
        self,
        mocker,
        package_request,
    ):
        def get(*args):
            return json.loads('{"key", "value"}')

        mocker.patch.object(
            package_request,
            "get",
            get,
        )
        with pytest.raises(json.JSONDecodeError):
            package_request.get()


@pytest.fixture
def response():
    response = {
        "info": {
            "name": "Django",
            "version": "3.2.5",
        },
        "releases": {
            "3.2.3": [],
            "3.2.4": [],
            "3.2.5": [],
        },
    }
    return response


class TestPackageInfo:
    @pytest.mark.parametrize(
        "release, expected",
        [
            (None, dict),
            ("3.2.3", dict),
            ("3.2.4", dict),
            ("3.2.5", dict),
        ],
    )
    def test__deve_retorna_um_dicionario_com_informacoes_validas_sobre_um_pacote(
        self,
        response,
        release,
        expected,
    ):

        package_info = PackageInfo(response, release, "error message")
        result = package_info.get()
        assert isinstance(result, expected)

    @pytest.mark.parametrize(
        "release",
        [
            "3.2.6",
            "3.2.7",
            "3.2.8",
        ],
    )
    def test__deve_lancar_uma_excecao__quando_a_release_nao_estiver_contida_na_lista_de_releases(
        self,
        response,
        release,
    ):
        package_info = PackageInfo(response, release, "error message")
        with pytest.raises(serializers.ValidationError):
            package_info.get()


class TestPackageValidate:
    def test__deve_retornar_uma_lista_vazia__quando_receber_uma_lista_de_pacotes_vazia(
        self,
    ):
        package_validate = PackageValidate([], PackageRequest, PackageInfo, "error")
        packages = package_validate.validate()
        assert len(packages) == 0
