"""
Kubeflow Installation fixture module
"""

import subprocess
import tempfile
import time
import pytest
import os

from e2e.utils.config import configure_resource_fixture
from e2e.utils.constants import KUBEFLOW_VERSION
from e2e.utils.utils import wait_for,kubectl_delete, kubectl_delete_crd


def apply_kustomize(path):
    """
    Equivalent to:

    while ! kustomize build <PATH> | kubectl apply -f -; do echo "Retrying to apply resources"; sleep 30; done

    but creates a temporary file instead of piping.
    """
    with tempfile.NamedTemporaryFile() as tmp:
        build_retcode = subprocess.call(f"kustomize build {path} -o {tmp.name}".split())
        assert build_retcode == 0
        apply_retcode = subprocess.call(f"kubectl apply -f {tmp.name}".split())
        # to deal with runtime crds, give it another chance to build
        if apply_retcode == 1:
            time.sleep(30)
            apply_retcode = subprocess.call(f"kubectl apply -f {tmp.name}".split())
        assert apply_retcode == 0

def install_helm(chart_name, path):
    """
    Equivalent to:

    helm install <chart_name> <path>
    
    """

    with tempfile.NamedTemporaryFile() as tmp:
        install_retcode = subprocess.call(f"helm install {chart_name} {path}".split())
        assert install_retcode == 0

def delete_kustomize(path):
    """
    Equivalent to:

    kustomize build <PATH> | kubectl delete -f -

    but creates a temporary file instead of piping.
    """
    with tempfile.NamedTemporaryFile() as tmp:
        build_retcode = subprocess.call(f"kustomize build {path} -o {tmp.name}".split())
        assert build_retcode == 0
    
        delete_retcode = subprocess.call(f"kubectl delete -f {tmp.name}".split())

def uninstall_helm(chart_name, namespace = None):
    """
    Equivalent to:

    helm uninstall <chart_name>

    """
    if namespace: 
        uninstall_retcode = subprocess.call(f"helm uninstall {chart_name} -n {namespace}".split())
    else:
        uninstall_retcode = subprocess.call(f"helm uninstall {chart_name}".split())
    assert uninstall_retcode == 0


@pytest.fixture(scope="class")
def configure_manifests():
    pass


@pytest.fixture(scope="class")
def clone_upstream():
    upstream_path = "../../upstream"
    if not os.path.isdir(upstream_path):
        retcode = subprocess.call(
            f"git clone --branch {KUBEFLOW_VERSION} https://github.com/kubeflow/manifests.git ../../upstream".split()
        )
        assert retcode == 0
    else:
        print("upstream directory already exists, skipping clone ...")


@pytest.fixture(scope="class")
def installation(
    metadata, cluster, clone_upstream, configure_manifests, installation_path, installation_option, request
):
    """
    This fixture is created once for each test class.

    Before all tests are run, installs kubeflow using the manifest at `kustomize_path`
    if `kustomize_path` was not provided in the metadata.

    After all tests are run, uninstalls kubeflow using the manifest at `kustomize_path`
    if the flag `--keepsuccess` was not provided as a pytest argument.
    """

    def on_create():

        if (installation_option == 'kustomize'):
            wait_for(lambda: apply_kustomize(installation_path), timeout=20 * 60)
            time.sleep(5 * 60)  # wait a bit for all pods to be running
        # TODO: verify this programmatically
        if (installation_option == 'helm'):

            for helm_chart in installation_path:
                chart_path = helm_chart[0]
                chart_name = helm_chart[1]
                wait_for(lambda: install_helm(chart_name, chart_path), timeout=3 * 60)
                time.sleep(10)

        time.sleep(60)
        # wait a bit for all pods to be running

    def on_delete():
         # deleting the kubeflow deployment deletes the load balancer controller at the same time as ingress
            # the problem with this is the ingress managed load balacer does not get cleaned up as there is no controller 
        subprocess.call(f"kubectl delete ingress -n istio-system --all".split())
        subprocess.call(f"kubectl delete profile --all".split())
            # load balancer controller does not place a finalizer on the ingress and so deleting the attached load balancer is asynhronous
            # adding a random wait to allow controller to delete the load balancer
            # TODO: implement a better check
        time.sleep(2 * 60)
        if (installation_option == 'kustomize'):
            delete_kustomize(installation_path)
            kubectl_delete_crd("authrequests.dex.coreos.com")
            kubectl_delete_crd("connectors.dex.coreos.com")
            kubectl_delete_crd("devicerequests.dex.coreos.com")
            kubectl_delete_crd("devicetokens.dex.coreos.com")
            kubectl_delete_crd("oauth2clients.dex.coreos.com")
            kubectl_delete_crd("offlinesessionses.dex.coreos.com")
            kubectl_delete_crd("passwords.dex.coreos.com")
            kubectl_delete_crd("refreshtokens.dex.coreos.com")
            kubectl_delete_crd("signingkeies.dex.coreos.com")

        
        if (installation_option == 'helm'):
            installation_path.reverse()

            for helm_chart in installation_path:
                chart_name = helm_chart[1]
                uninstall_helm(chart_name)
                if os.path.isdir(f"{helm_chart[0]}/crds"):
                    print(f"deleting {chart_name} crds ...")
                    kubectl_delete(f"{helm_chart[0]}/crds")
                    if chart_name == "dex":
                        kubectl_delete_crd("authrequests.dex.coreos.com")
                        kubectl_delete_crd("connectors.dex.coreos.com")
                        kubectl_delete_crd("devicerequests.dex.coreos.com")
                        kubectl_delete_crd("devicetokens.dex.coreos.com")
                        kubectl_delete_crd("oauth2clients.dex.coreos.com")
                        kubectl_delete_crd("offlinesessionses.dex.coreos.com")
                        kubectl_delete_crd("passwords.dex.coreos.com")
                        kubectl_delete_crd("refreshtokens.dex.coreos.com")
                        kubectl_delete_crd("signingkeies.dex.coreos.com")




    configure_resource_fixture(
        metadata, request, installation_path, "installation_path", on_create, on_delete
    )
