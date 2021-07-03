import { check, group } from 'k6';
import { Httpx } from 'https://jslib.k6.io/httpx/0.0.3/index.js';

let session = new Httpx({
  baseURL: `${__ENV.API_BASE}api`,
  headers: { 'Content-Type': 'application/json' },
});

const responseToJson = (request) => {
  try {
    return JSON.parse(request.body);
  } catch (error) {
    return {};
  }
};

const shallowObjectCompare = (expected, received) => {
  return Object.keys(expected).every(k => expected[k] === received[k]);
}

export default () => {

  group("Cria projeto titan", () => {
    session.delete("/projects/titan/");  // <- limpa o ambiente antes do teste

    const titanData = {
      name: "titan",
      packages: [
        { name: "django-rest-swagger" },
        { name: "Django", version: "2.2.24" },
        { name: "psycopg2-binary", version: "2.9.1" }
      ]
    };
    const titan = session.post("/projects/", JSON.stringify(titanData));

    check(titan, {
      "Cria o projeto com sucesso": (r) => r.status === 201,
    });

    check(titan, {
      "O pacote Django continua com a versão especificada": (r) => {
        const data = responseToJson(r);
        const django = data.packages.find((p) => p.name === "Django");
        return django.version === "2.2.24";
      },
    });

    check(titan, {
      "O pacote django-rest-swagger usa a última versão disponível": (r) => {
        const data = responseToJson(r);
        const django = data.packages.find((p) => p.name === "django-rest-swagger");
        return django.version === "2.2.0";
      },
    });
  });
  group("Cria dois projetos com o mesmo nome", () => {
    session.delete("/projects/cronos/");

    const CronosData = {
      name: "cronos",
      packages: [
        { name: "Django" }
      ]
    };

    session.post("/projects/", JSON.stringify(CronosData));
    const cronos = session.post("/projects/", JSON.stringify(CronosData));

    check(cronos, {
      "Tentativa resulta em erro BAD REQUEST": (r) => r.status === 400,
    });

    check(cronos, {
      "Apresenta mensagem de erro": (r) => {
        const expected = '{"name":["project with this name already exists."]}';
        return r.body === expected
      },
    });
  });

  group("Cria projeto sem declarar a variavel packages", () => {
    session.delete("/projects/tanos/");

    const TanosData = {
      name: "tanos"
    };

    const tanos = session.post("/projects/", JSON.stringify(TanosData));
    check(tanos, {
      "Tentativa resulta em erro BAD REQUEST": (r) => r.status === 400,
    });

    check(tanos, {
      "Apresenta mensagem de erro": (r) => {
        const expected = '{"packages":["This field is required."]}';
        return r.body === expected;
      },
    });
  });

  group("Cria projeto com pacote inexistente", () => {
    session.delete("/projects/machine-head/");  // <- limpa o ambiente antes do teste

    const mhdData = {
      name: "machine-head",
      packages: [
        { name: "keras" },
        { name: "matplotlib" },
        { name: "pypypypypypypypypypypypypy" }
      ]
    };
    const mh = session.post("/projects/", JSON.stringify(mhdData));

    check(mh, {
      "Tentativa resulta em erro BAD REQUEST": (r) => r.status === 400,
    });

    check(mh, {
      "Apresenta mensagem de erro": (r) => {
        const data = responseToJson(r);
        const expected = { "error": "One or more packages doesn't exist" };
        return shallowObjectCompare(expected, data);
      },
    });
  });

  group("Cria projeto com versão de pacote inexistente", () => {
    session.delete("/projects/prometheus/");

    const prometheusData = {
      name: "prometheus",
      packages: [
        { name: "django-rest-swagger" },
        { name: "Django", version: "33.33.33" },
        { name: "psycopg2-binary", version: "2.9.1" }
      ]
    };
    const prometheus = session.post("/projects/", JSON.stringify(prometheusData));

    check(prometheus, {
      "Tentativa resulta em error BAD REQUEST": (r) => r.status === 400,
    });

    check(prometheus, {
      "Apresenta mensagem de erro": (r) => {
        const data = responseToJson(r);
        const expected = { "error": "One or more packages doesn't exist" };
        return shallowObjectCompare(expected, data);
      },
    });
  });
};
