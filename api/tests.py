import pytest
import json

from api.services import PackageInfo, PackageFinder, PackageValidator, PackageUpdater
from rest_framework import serializers


@pytest.fixture
def package_finder():
    package = {
        "name": "cronos",
        "packages": [
            {"name": "Django"},
        ],
    }
    return PackageFinder(package, "error message")


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


@pytest.fixture
def received_list():
    return [
        {
            "name": "Django",
            "version": "3.2.5",
        },
        {
            "name": "psycopg2-binary",
            "version": "2.9.1",
        },
    ]


class TestPackageFinder:
    def test__deve_retornar_uma_instancia_de_dicionario__quando_a_resposta_for_um_json_valido(
        self,
        mocker,
        package_finder,
    ):
        def get(*args):
            return json.loads('{"key": "value"}')

        mocker.patch.object(
            package_finder,
            "get",
            get,
        )

        result = package_finder.get()
        assert isinstance(result, dict)

    def test__deve_lancar_excecao__quando_a_reposta_for_um_json_invalido(
        self,
        mocker,
        package_finder,
    ):
        def get(*args):
            return json.loads('{"key", "value"}')

        mocker.patch.object(
            package_finder,
            "get",
            get,
        )
        with pytest.raises(json.JSONDecodeError):
            package_finder.get()


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


class TestPackageValidator:
    def test__deve_retornar_uma_lista_vazia__quando_receber_uma_lista_de_pacotes_vazia(
        self,
    ):
        package_validate = PackageValidator([], PackageFinder, PackageInfo, "error")
        packages = package_validate.validate()
        assert len(packages) == 0


class TestPackageUpdater:
    def test__deve_retornar_a_lista_que_foi_recebida__quando_a_lista_atual_estiver_vazia(
        self,
        received_list,
    ):

        current_list = []
        package_list = PackageUpdater(current_list, received_list)
        result = package_list.update()
        assert result == received_list

    def test__deve_adicionar_o_pacote_na_lista_atual__quando_ele_não_existir(
        self,
        received_list,
    ):
        current_list = [
            {
                "name": "Django",
                "version": "3.2.5",
            },
        ]
        package_list = PackageUpdater(current_list, received_list)
        result = package_list.update()
        assert result == received_list

    def test__deve_substituir_o_pacote_na_lista_atual__quando_a_versao_for_diferente_da_lista_recebida(
        self,
        received_list,
    ):
        current_list = [
            {
                "name": "Django",
                "version": "3.2.2",
            },
            {
                "name": "django-rest-swagger",
                "version": "2.2.0",
            },
        ]

        expected = [
            {
                "name": "Django",
                "version": "3.2.5",
            },
            {
                "name": "django-rest-swagger",
                "version": "2.2.0",
            },
            {
                "name": "psycopg2-binary",
                "version": "2.9.1",
            },
        ]
        package_updater = PackageUpdater(current_list, received_list)
        result = package_updater.update()
        assert result == expected
