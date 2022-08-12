
from e2e.utils.utils import print_banner
import argparse
from e2e.utils.utils import kubectl_delete, kubectl_delete_crd
from e2e.fixtures.installation import uninstall_helm, delete_kustomize
import os

##Kustomize paths
#level 1
cert_manager_kustomize_path = "../../upstream/common/cert-manager/cert-manager/base"
kubeflow_roles_kustomize_path = "../../upstream/common/kubeflow-roles/base"


#level 2
kubeflow_issuer_kustomize_path = "../../upstream/common/cert-manager/kubeflow-issuer/base"
istio_crd_kustomize_path = "../../upstream/common/istio-1-14/istio-crds/base"
istio_namespace_kustomize_path = "../../upstream/common/istio-1-14/istio-namespace/base"
istio_base_kustomize_path = "../../upstream/common/istio-1-14/istio-install/base"

#level 3
dex_kustomize_path = "../../upstream/common/dex/overlays/istio"
kubeflow_namespace_kustomize_path = "../../upstream/common/kubeflow-namespace/base"
cluster_local_gateway_kustomize_path = "../../upstream/common/istio-1-14/cluster-local-gateway/base"
knative_serving_kustomize_path = "../../upstream/common/knative/knative-serving/base"
knative_eventing_kustomize_path = "../../upstream/common/knative/knative-eventing/base"

#level 4
oidc_authservice_kustomize_path = "../../upstream/common/oidc-authservice/base"
kubeflow_istio_resources_kustomize_path = "../../upstream/common/istio-1-14/kubeflow-istio-resources/base"
kserve_kustomize_path = "../../awsconfigs/apps/kserve"
models_web_app_kustomize_path = "../../upstream/contrib/kserve/models-web-app/overlays/kubeflow"

#level 5
central_dashboard_kustomize_path = "../../upstream/apps/centraldashboard/upstream/overlays/kserve"

#pipelines
kubeflow_pipelines_kustomize_path = "../../upstream/apps/pipeline/upstream/env/cert-manager/platform-agnostic-multi-user"
#notebook
admission_webhook_kustomize_path = "../../upstream/apps/admission-webhook/upstream/overlays/cert-manager"
jupyter_web_app_kustomize_path = "../../awsconfigs/apps/jupyter-web-app"
notebook_controller_kustomize_path = "../../upstream/apps/jupyter/notebook-controller/upstream/overlays/kubeflow"
#volume-web-app
volumes_web_app_kustomize_path = "../../upstream/apps/volumes-web-app/upstream/overlays/istio"
#training-operator
training_operator_kustomize_path = "../../upstream/apps/training-operator/upstream/overlays/kubeflow"
#katib
katib_kustomize_path = "../../upstream/apps/katib/upstream/installs/katib-with-kubeflow"
#tensorboard
tensorboard_controller_kustomize_path = "../../upstream/apps/tensorboard/tensorboard-controller/upstream/overlays/kubeflow"
tensorboards_web_app_kustomize_path = "../../upstream/apps/tensorboard/tensorboards-web-app/upstream/overlays/istio"
#profiles and kfam
profiles_and_kfam_kustomize_path = "../../upstream/apps/profiles/upstream/overlays/kubeflow"
#user namespace
user_namespace_kustomize_path = "../../upstream/common/user-namespace/base"
#AWS Telemetry (Optional)
aws_telemetry_kustomize_path = "../../awsconfigs/common/aws-telemetry"




#level 1 
cert_manager_chart_path = "../../charts/common/cert-manager"
kubeflow_roles_chart_path = "../../charts/common/kubeflow-roles"
#level 2
kubeflow_issuer_chart_path = "../../charts/common/kubeflow-issuer"
istio_chart_path = "../../charts/common/istio-1-14"
#level 3
dex_chart_path = "../../charts/common/dex"
kubeflow_namespace_chart_path = "../../charts/common/kubeflow-namespace"
cluster_local_gateway_chart_path = "../../charts/common/cluster-local-gateway"
knative_serving_chart_path = "../../charts/common/knative-serving"
knative_eventing_chart_path = "../../charts/common/knative-eventing"
#level 4
oidc_authservice_chart_path = "../../charts/common/oidc-authservice"
kubeflow_istio_resources_chart_path = "../../charts/common/kubeflow-istio-resources"
kserve_chart_path = "../../charts/common/kserve"
models_web_app_chart_path = "../../charts/apps/models-web-app"
#level 5
central_dashboard_chart_path = "../../charts/apps/central-dashboard"
#pipeline
kubeflow_pipelines_chart_path = "../../charts/apps/kubeflow-pipelines"
#notebook
admission_webhook_chart_path = "../../charts/common/admission-webhook"
jupyter_web_app_chart_path = "../../charts/apps/jupyter-web-app"
notebook_controller_chart_path = "../../charts/apps/notebook-controller"
#volume-web-app
volumes_web_app_chart_path = "../../charts/apps/volumes-web-app"
#training-operator
training_operator_chart_path = "../../charts/apps/training-operator"
#katib
katib_chart_path = "../../charts/apps/katib"
#tensorboard
tensorboard_controller_chart_path = "../../charts/apps/tensorboard-controller"
tensorboards_web_app_chart_path = "../../charts/apps/tensorboards-web-app"
#profiles and kfam
profiles_and_kfam_chart_path = "../../charts/common/profiles-and-kfam"
#user namespace
user_namespace_chart_path = "../../charts/common/user-namespace"

def main():
    print_banner(f"You are uninstalling kubeflow with {args.installation_option}")
    
    delete_component("user-namespace",user_namespace_chart_path, user_namespace_kustomize_path)
    delete_component("profiles-and-kfam",profiles_and_kfam_chart_path, profiles_and_kfam_kustomize_path)
    delete_component("tensorboard-controller",tensorboard_controller_chart_path, tensorboard_controller_kustomize_path)
    delete_component("tensorboards-web-app",tensorboards_web_app_chart_path, tensorboards_web_app_kustomize_path)
    delete_component("katib",katib_chart_path,katib_kustomize_path)
    delete_component("training-operator",training_operator_chart_path,training_operator_kustomize_path)
    delete_component("volumes-web-app",volumes_web_app_chart_path,volumes_web_app_kustomize_path)
    delete_component("notebook-controller",notebook_controller_chart_path,notebook_controller_kustomize_path)
    delete_component("jupyter-web-app",jupyter_web_app_chart_path,jupyter_web_app_kustomize_path)
    delete_component("admission-webhook",admission_webhook_chart_path,admission_webhook_kustomize_path)
    delete_component("kubeflow-pipelines",kubeflow_pipelines_chart_path,kubeflow_pipelines_kustomize_path)
    delete_component("central-dashboard",central_dashboard_chart_path,central_dashboard_kustomize_path)
    delete_component("models-web-app",models_web_app_chart_path,models_web_app_kustomize_path)
    delete_component("kserve",kserve_chart_path,kserve_kustomize_path)
    delete_component("kubeflow-istio-resources",kubeflow_istio_resources_chart_path,kubeflow_istio_resources_kustomize_path)
    delete_component("oidc-authservice",oidc_authservice_chart_path,oidc_authservice_kustomize_path)
    delete_component("knative-eventing",knative_eventing_chart_path,knative_eventing_kustomize_path)
    delete_component("knative-serving",knative_serving_chart_path,knative_serving_kustomize_path)
    delete_component("cluster-local-gateway",cluster_local_gateway_chart_path,cluster_local_gateway_kustomize_path)
    delete_component("dex",dex_chart_path,dex_kustomize_path)
    delete_component("kubeflow-namespace", kubeflow_namespace_chart_path, kubeflow_namespace_kustomize_path)

    
    if INSTALLATION_OPTION == "helm":
        delete_component("istio-1-14",istio_chart_path)
    else:
        print(f"==========uninstallating Istio-1-14...==========")
        delete_component("Istio-base",kustomize_path=istio_base_kustomize_path)
        delete_component("Istio-namespace",kustomize_path=istio_namespace_kustomize_path)
        delete_component("Istio-crd",kustomize_path=istio_crd_kustomize_path)
    

    delete_component("kubeflow-issuer",kubeflow_issuer_chart_path,kubeflow_issuer_kustomize_path)
    delete_component("kubeflow-roles",kubeflow_roles_chart_path, kubeflow_roles_kustomize_path)
    delete_component("cert-manager",cert_manager_chart_path, cert_manager_kustomize_path, "cert-manager")
    
    
def delete_component(chart_name=None, chart_path=None, kustomize_path=None, namespace=None,):
    print(f"==========uninstallating {chart_name}...==========")
    if INSTALLATION_OPTION == 'helm':
        uninstall_helm(chart_name,namespace)
        if os.path.isdir(f"{chart_path}/crds"):
            print(f"deleting {chart_name} crds ...")
            kubectl_delete(f"{chart_path}/crds")
            #clear up implicit crd resources for Dex
    
    else:
        delete_kustomize(kustomize_path)
    
    if chart_name == "dex" or kustomize_path == dex_kustomize_path:
                kubectl_delete_crd("authrequests.dex.coreos.com")
                kubectl_delete_crd("connectors.dex.coreos.com")
                kubectl_delete_crd("devicerequests.dex.coreos.com")
                kubectl_delete_crd("devicetokens.dex.coreos.com")
                kubectl_delete_crd("oauth2clients.dex.coreos.com")
                kubectl_delete_crd("offlinesessionses.dex.coreos.com")
                kubectl_delete_crd("passwords.dex.coreos.com")
                kubectl_delete_crd("refreshtokens.dex.coreos.com")
                kubectl_delete_crd("signingkeies.dex.coreos.com")
        

    print(f"All {chart_name} resources are cleared!")




parser = argparse.ArgumentParser()
INSTALLATION_OPTION_DEFAULT="kustomize"
parser.add_argument(
    "--installation_option",
    type=str,
    default=INSTALLATION_OPTION_DEFAULT,
    help=f"Kubeflow Installation option (helm/kustomize), default is set to {INSTALLATION_OPTION_DEFAULT}",
    required=False,
)

args, _ = parser.parse_known_args()

if __name__ == "__main__":
    INSTALLATION_OPTION=args.installation_option
    main()