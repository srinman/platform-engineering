import os
import requests
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

_SA_TOKEN_PATH = "/var/run/secrets/kubernetes.io/serviceaccount/token"
_SA_CA_PATH = "/var/run/secrets/kubernetes.io/serviceaccount/ca.crt"

_K8S_HOST = (
    f"https://{os.environ['KUBERNETES_SERVICE_HOST']}"
    f":{os.environ['KUBERNETES_SERVICE_PORT']}"
)
_APP1_NS = os.environ.get("APP1_NAMESPACE", "app1")


# ─── K8s helpers ─────────────────────────────────────────────────────────────

def _token() -> str:
    with open(_SA_TOKEN_PATH) as fh:
        return fh.read().strip()


def _headers(extra: dict | None = None) -> dict:
    h = {"Authorization": f"Bearer {_token()}"}
    if extra:
        h.update(extra)
    return h


def _get(path: str) -> dict:
    resp = requests.get(
        f"{_K8S_HOST}{path}",
        headers=_headers(),
        verify=_SA_CA_PATH,
        timeout=10,
    )
    resp.raise_for_status()
    return resp.json()


def _post(path: str, body: dict) -> dict:
    resp = requests.post(
        f"{_K8S_HOST}{path}",
        headers=_headers({"Content-Type": "application/json"}),
        json=body,
        verify=_SA_CA_PATH,
        timeout=10,
    )
    resp.raise_for_status()
    return resp.json()


def _delete(path: str) -> dict:
    resp = requests.delete(
        f"{_K8S_HOST}{path}",
        headers=_headers(),
        verify=_SA_CA_PATH,
        timeout=10,
    )
    resp.raise_for_status()
    return resp.json()


# ─── UI ──────────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html", namespace=_APP1_NS)


# ─── CostOptimizedApp ────────────────────────────────────────────────────────

@app.route("/api/costoptimizedapps", methods=["GET"])
def list_cost_apps():
    data = _get(f"/apis/kro.run/v1alpha1/namespaces/{_APP1_NS}/costoptimizedapps")
    items = [
        {
            "name": i["metadata"]["name"],
            "image": i["spec"].get("image", ""),
            "port": i["spec"].get("port", ""),
            "state": i.get("status", {}).get("state", "—"),
        }
        for i in data.get("items", [])
    ]
    return jsonify(items)


@app.route("/api/costoptimizedapps", methods=["POST"])
def create_cost_app():
    body = request.get_json(force=True)
    name = body.get("name", "").strip()
    if not name:
        return jsonify({"error": "name is required"}), 400

    manifest = {
        "apiVersion": "kro.run/v1alpha1",
        "kind": "CostOptimizedApp",
        "metadata": {"name": name, "namespace": _APP1_NS},
        "spec": {
            "image": body.get("image", "nginx:1.27"),
            "port": int(body.get("port", 80)),
        },
    }
    result = _post(
        f"/apis/kro.run/v1alpha1/namespaces/{_APP1_NS}/costoptimizedapps",
        manifest,
    )
    return jsonify({"name": result["metadata"]["name"]}), 201


@app.route("/api/costoptimizedapps/<name>", methods=["DELETE"])
def delete_cost_app(name: str):
    _delete(f"/apis/kro.run/v1alpha1/namespaces/{_APP1_NS}/costoptimizedapps/{name}")
    return jsonify({"deleted": name})


# ─── HighlyAvailableApp ──────────────────────────────────────────────────────

@app.route("/api/highlyavailableapps", methods=["GET"])
def list_ha_apps():
    data = _get(f"/apis/kro.run/v1alpha1/namespaces/{_APP1_NS}/highlyavailableapps")
    items = [
        {
            "name": i["metadata"]["name"],
            "image": i["spec"].get("image", ""),
            "port": i["spec"].get("port", ""),
            "state": i.get("status", {}).get("state", "—"),
        }
        for i in data.get("items", [])
    ]
    return jsonify(items)


@app.route("/api/highlyavailableapps", methods=["POST"])
def create_ha_app():
    body = request.get_json(force=True)
    name = body.get("name", "").strip()
    if not name:
        return jsonify({"error": "name is required"}), 400

    manifest = {
        "apiVersion": "kro.run/v1alpha1",
        "kind": "HighlyAvailableApp",
        "metadata": {"name": name, "namespace": _APP1_NS},
        "spec": {
            "image": body.get("image", "nginx:1.27"),
            "port": int(body.get("port", 80)),
        },
    }
    result = _post(
        f"/apis/kro.run/v1alpha1/namespaces/{_APP1_NS}/highlyavailableapps",
        manifest,
    )
    return jsonify({"name": result["metadata"]["name"]}), 201


@app.route("/api/highlyavailableapps/<name>", methods=["DELETE"])
def delete_ha_app(name: str):
    _delete(f"/apis/kro.run/v1alpha1/namespaces/{_APP1_NS}/highlyavailableapps/{name}")
    return jsonify({"deleted": name})


# ─── Read-only views into app1 ───────────────────────────────────────────────

@app.route("/api/pods", methods=["GET"])
def list_pods():
    data = _get(f"/api/v1/namespaces/{_APP1_NS}/pods")
    items = [
        {
            "name": i["metadata"]["name"],
            "phase": i["status"].get("phase", "—"),
            "node": i["spec"].get("nodeName", "—"),
            "ready": f"{sum(c.get('ready', False) for c in i['status'].get('containerStatuses', []))}"
                     f"/{len(i['spec'].get('containers', []))}",
        }
        for i in data.get("items", [])
    ]
    return jsonify(items)


@app.route("/api/deployments", methods=["GET"])
def list_deployments():
    data = _get(f"/apis/apps/v1/namespaces/{_APP1_NS}/deployments")
    items = [
        {
            "name": i["metadata"]["name"],
            "desired": i["spec"].get("replicas", 0),
            "ready": i["status"].get("readyReplicas", 0),
            "available": i["status"].get("availableReplicas", 0),
        }
        for i in data.get("items", [])
    ]
    return jsonify(items)


@app.route("/api/services", methods=["GET"])
def list_services():
    data = _get(f"/api/v1/namespaces/{_APP1_NS}/services")
    items = [
        {
            "name": i["metadata"]["name"],
            "type": i["spec"].get("type", "—"),
            "cluster_ip": i["spec"].get("clusterIP", "—"),
            "ports": ", ".join(
                f"{p.get('port')}/{p.get('protocol', 'TCP')}"
                for p in i["spec"].get("ports", [])
            ),
        }
        for i in data.get("items", [])
    ]
    return jsonify(items)


@app.route("/api/pdbs", methods=["GET"])
def list_pdbs():
    data = _get(f"/apis/policy/v1/namespaces/{_APP1_NS}/poddisruptionbudgets")
    items = [
        {
            "name": i["metadata"]["name"],
            "min_available": i["spec"].get("minAvailable", "—"),
            "disruptions_allowed": i["status"].get("disruptionsAllowed", "—"),
            "current_healthy": i["status"].get("currentHealthy", "—"),
        }
        for i in data.get("items", [])
    ]
    return jsonify(items)


# ─── Error handlers ──────────────────────────────────────────────────────────

@app.errorhandler(requests.HTTPError)
def handle_k8s_error(exc: requests.HTTPError):
    status = exc.response.status_code if exc.response is not None else 500
    try:
        detail = exc.response.json()
    except Exception:
        detail = str(exc)
    return jsonify({"error": detail}), status


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
