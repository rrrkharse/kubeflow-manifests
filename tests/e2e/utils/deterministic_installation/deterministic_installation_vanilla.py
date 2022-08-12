
from pickle import INST
from e2e.utils.utils import print_banner
import argparse
from e2e.utils.utils import kubectl_apply, kubectl_get_clusterrole, kubectl_wait_pods, kubectl_get_cronjob
from e2e.fixtures.installation import apply_kustomize, install_helm
import subprocess
import time

##Kustomize paths
#level 1
#cert-manager
cert_manager_kustomize_path = "../../upstream/common/cert-manager/cert-manager/base"
#kubeflow-roles
kubeflow_roles_kustomize_path = "../../upstream/common/kubeflow-roles/base"


#level 2
#kubeflow-issuer
kubeflow_issuer_kustomize_path = "../../upstream/common/cert-manager/kubeflow-issuer/base"
#istio
istio_crd_kustomize_path = "../../upstream/common/istio-1-14/istio-crds/base"
istio_namespace_kustomize_path = "../../upstream/common/istio-1-14/istio-namespace/base"
istio_base_kustomize_path = "../../upstream/common/istio-1-14/istio-install/base"

#level 3
#dex
dex_kustomize_path = "../../upstream/common/dex/overlays/istio"
#kubeflow-namespace
kubeflow_namespace_kustomize_path = "../../upstream/common/kubeflow-namespace/base"
#cluster-local-gateway
cluster_local_gateway_kustomize_path = "../../upstream/common/istio-1-14/cluster-local-gateway/base"
#knative
#knative_serving_kustomize_path = "../../upstream/common/knative/knative-serving/base"
knative_serving_kustomize_path = "../../upstream/common/knative/knative-serving/overlays/gateways"
knative_eventing_kustomize_path = "../../upstream/common/knative/knative-eventing/base"

#level 4
#oidc-authservice
oidc_authservice_kustomize_path = "../../upstream/common/oidc-authservice/base"
#kubeflow-istio-resources
kubeflow_istio_resources_kustomize_path = "../../upstream/common/istio-1-14/kubeflow-istio-resources/base"
#kserve
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




## Helm paths
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
#AWS Telemetry (Optional)
aws_telemetry_chart_path = "../../charts/common/aws-telemetry"

def main():
    print_banner(f"You are installing kubeflow with {args.installation_option}")
    build_certManager()
    
    if INSTALLATION_OPTION == "helm":
        print("==========Installing Kubeflow-Roles==========")
        install_helm("kubeflow-roles", kubeflow_roles_chart_path)
        print("==========Installing Kubeflow-Issuer==========")
        install_helm("kubeflow-issuer", kubeflow_issuer_chart_path)
    else:
        print("==========Installing Kubeflow-Roles==========")
        apply_kustomize(kubeflow_roles_kustomize_path)
        print("==========Installing Kubeflow-Issuer==========")
        apply_kustomize(kubeflow_issuer_kustomize_path)
   
    build_istio()
    build_dex()
    
    print("==========Installing Kubeflow-Namespace==========")
    
    
    if INSTALLATION_OPTION == "helm":
        install_helm("kubeflow-namespace", kubeflow_namespace_chart_path)
    else:
        apply_kustomize(kubeflow_namespace_kustomize_path)
    

    build_clusterLocalGateway()
    build_knativeServing()
    build_knativeEventing()
    build_oidcAuthService()
    print("==========Installing Kubeflow-Istio-Resources==========")
    
    
    if INSTALLATION_OPTION == "helm":
        install_helm("kubeflow-istio-resources", kubeflow_istio_resources_chart_path)
    else:
        apply_kustomize(kubeflow_istio_resources_kustomize_path)
    
    build_kserve()
    build_models_web_app()
    build_centralDashboard()
    build_kubeflowPipelines()
    build_notebook()
    build_volumesWebApp()
    build_trainingOperator()
    build_katib()
    build_tensorBoard()
    build_profile()
    if AWS_TELEMETRY == "enable":
        build_aws_telemetry()

def build_aws_telemetry():
    print("==========Installing AWS-Telemtry==========")
    if INSTALLATION_OPTION == "helm":
        install_helm("aws-telemtry", aws_telemetry_chart_path)
    else:
        #kustomize
        apply_kustomize(aws_telemetry_kustomize_path)
    retcode = kubectl_get_cronjob("aws-kubeflow-telemetry","kubeflow")
    assert retcode == 0
    print ("aws-telemetry is running!")
    

def build_certManager():
    print("==========Installing Cert-Manager==========")
    if INSTALLATION_OPTION == "helm":
        cmd = f"helm install cert-manager {cert_manager_chart_path} \
        --namespace cert-manager \
        --create-namespace \
        --set installCRDs=true".split()
        build_retcode = subprocess.call(cmd)
        assert build_retcode == 0
    else:
        #kustomize
        apply_kustomize(cert_manager_kustomize_path)

    print("Waiting for Cert-manager to be ready ...")
    retcode = kubectl_wait_pods(pods = 'cert-manager, webhook, cainjector',namespace='cert-manager',timeout=120)
    assert retcode == 0
    print("All cert-manager pods are running!")
    

def build_istio():
    print("==========Installing Istio==========")
    if INSTALLATION_OPTION == "helm":
        install_helm("istio-1-14", istio_chart_path)
    else:
        #kustomize
        apply_kustomize(istio_crd_kustomize_path)
        apply_kustomize(istio_namespace_kustomize_path)
        apply_kustomize(istio_base_kustomize_path)
    print("Waiting for istio to be ready ...")
    retcode = kubectl_wait_pods(pods='istio-ingressgateway, istiod', namespace='istio-system', timeout=120)
    assert retcode == 0
    print("All istio pods are running!")

def build_dex():
    print("==========Installing Dex==========")
    if INSTALLATION_OPTION == "helm":
        install_helm("dex", dex_chart_path)
    else:
        apply_kustomize(dex_kustomize_path)
    print("Waiting for dex to be ready ...")
    retcode = kubectl_wait_pods(pods='dex', namespace='auth', timeout=120)
    assert retcode == 0
    print("All dex pods are running!")

def build_clusterLocalGateway():
    print("==========Installing Cluster-local-gateway==========")
    if INSTALLATION_OPTION == "helm":
        install_helm("cluster-local-gateway", cluster_local_gateway_chart_path)
    else:
        apply_kustomize(cluster_local_gateway_kustomize_path)
    print("Waiting for cluster-local-gateway pods to be ready ...")
    retcode = kubectl_wait_pods(pods='cluster-local-gateway', namespace='istio-system', timeout=120)
    assert retcode == 0
    print("All cluster-local-gateway pods are running!")

def build_knativeServing():
    print("==========Installing Knative-Serving==========")
    if INSTALLATION_OPTION == "helm":
        install_helm("knative-serving", knative_serving_chart_path)
    else:
        apply_kustomize(knative_serving_kustomize_path)
    print("Waiting for knative-serving pods to be ready ...")
    retcode = kubectl_wait_pods(pods='activator, autoscaler, controller, istio-webhook, networking-istio, webhook', namespace='knative-serving', timeout=120)
    assert retcode == 0
    print("All knative-serving pods are running!")

def build_knativeEventing():
    print("==========Installing Knative-Eventing==========")
    if INSTALLATION_OPTION=="helm":
        install_helm("knative-eventing", knative_eventing_chart_path)
    else:
        apply_kustomize(knative_eventing_kustomize_path)
    print("Waiting for knative-eventing pods to be ready ...")
    retcode = kubectl_wait_pods(pods='eventing-controller, eventing-webhook', namespace='knative-eventing', timeout=120)
    assert retcode == 0
    print("All knative-eventing pods are running!")

def build_oidcAuthService():
    print("==========Installing OIDC-Authservice==========")
    if INSTALLATION_OPTION == "helm":
        install_helm("oidc-authservice", oidc_authservice_chart_path)
    else:
        apply_kustomize(oidc_authservice_kustomize_path)
    print("Waiting for oidc-authservice pods to be ready ...")
    retcode = kubectl_wait_pods(pods='authservice', namespace='istio-system', timeout=120)
    assert retcode == 0
    print("All oidc-authservice pods are running!")

def build_kserve():
    print("==========Installing Kserve==========")
    if INSTALLATION_OPTION == "helm":
        install_helm("kserve", kserve_chart_path)
    else:
        apply_kustomize(kserve_kustomize_path)
    print("Waiting for kserve pods to be ready ...")
    retcode = kubectl_wait_pods(pods='kserve', namespace='kubeflow', timeout=120)
    assert retcode == 0
    print("All kserve pods are running!")

def build_models_web_app():
    print("==========Installing Models-Web-Apps==========")
    
    if INSTALLATION_OPTION == "helm":
        install_helm("models-web-app", models_web_app_chart_path)
    else:
        apply_kustomize(models_web_app_kustomize_path)
    
    print("Waiting for models-web-app pods to be ready ...")
    retcode = kubectl_wait_pods(pods='kserve-models-web-app', namespace='kubeflow', timeout=120, identifier="kustomize.component")
    assert retcode == 0
    print("All kserve-models-web-app pods are running!")

def build_centralDashboard():
    print("==========Installing Central-Dashboard==========")
    if INSTALLATION_OPTION == "helm":
        install_helm("central-dashboard", central_dashboard_chart_path)
    else:
        apply_kustomize(central_dashboard_kustomize_path)
    print("Waiting for central-dashboard pods to be ready ...")
    retcode = kubectl_wait_pods(pods='centraldashboard', namespace='kubeflow', timeout=120)
    assert retcode == 0
    print("All central-dashboard pods are running!")

def build_kubeflowPipelines():
    print("==========Installing Kubeflow-Pipelines==========")
    if INSTALLATION_OPTION == "helm":
        install_helm("kubeflow-pipelines", kubeflow_pipelines_chart_path)
    else:
        apply_kustomize(kubeflow_pipelines_kustomize_path)
    print("Waiting for kubeflow-pipelines pods to be ready ...")
    retcode = kubectl_wait_pods(pods='cache-server, kubeflow-pipelines-profile-controller, \
                                      metacontroller, metadata-envoy-deployment, metadata-grpc-deployment, \
                                      metadata-writer, minio, ml-pipeline, ml-pipeline-persistenceagent, \
                                      ml-pipeline-scheduleworkflow, ml-pipeline-ui, ml-pipeline-viewer-crd, \
                                      ml-pipeline-visualizationserver, mysql, workflow-controller', 
                                 namespace='kubeflow', timeout=120)
    assert retcode == 0
    print("All kubeflow-pipelines pods are running!")

def build_notebook():
    print("==========Installing Notebook==========")
    ##admission-webhook
    if INSTALLATION_OPTION == "helm":
        install_helm("admission-webhook", admission_webhook_chart_path)
    else:
        apply_kustomize(admission_webhook_kustomize_path)
    print("Waiting for admission-webhook pods to be ready ...")
    retcode = kubectl_wait_pods(pods='poddefaults', namespace='kubeflow', timeout=120)
    assert retcode == 0
    ##notebook-controller
    if INSTALLATION_OPTION == "helm":
        install_helm("notebook-controller", notebook_controller_chart_path)
    else:
        apply_kustomize(notebook_controller_kustomize_path)
    print("Waiting for notebook-controller pods to be ready ...")
    retcode = kubectl_wait_pods(pods='notebook-controller', namespace='kubeflow', timeout=120)
    assert retcode == 0
    ##jupyter-web-app
    if INSTALLATION_OPTION == "helm":
        install_helm("jupyter-web-app", jupyter_web_app_chart_path)
    else:
        apply_kustomize(jupyter_web_app_kustomize_path)
    print("Waiting for jupyter-web-app pods to be ready ...")
    retcode = kubectl_wait_pods(pods='jupyter-web-app', namespace='kubeflow', timeout=120)
    assert retcode == 0
    print("All notebook pods are running!")

def build_volumesWebApp():
    print("==========Installing Volumes-web-app==========")
    if INSTALLATION_OPTION == "helm":
        install_helm("volumes-web-app", volumes_web_app_chart_path)
    else:
        apply_kustomize(volumes_web_app_kustomize_path)
    print("Waiting for volumes-web-app pods to be ready ...")
    retcode = kubectl_wait_pods(pods='volumes-web-app', namespace='kubeflow', timeout=120)
    assert retcode == 0
    print("All volumes-web-app pods are running!")

def build_tensorBoard():
    print("==========Installing Tensor-Board==========")
    ##tensorboard-controller
    if INSTALLATION_OPTION == "helm":
        install_helm("tensorboard-controller", tensorboard_controller_chart_path)
    else:
        apply_kustomize(tensorboard_controller_kustomize_path)
    print("Waiting for tensorboard-controller pods to be ready ...")
    retcode = kubectl_wait_pods(pods='tensorboard-controller', namespace='kubeflow', timeout=120)
    assert retcode == 0
    ##tensorboards-web-app
    if INSTALLATION_OPTION == "helm":
        install_helm("tensorboards-web-app", tensorboards_web_app_chart_path)
    else:
        apply_kustomize(tensorboards_web_app_kustomize_path)
    print("Waiting for tensorboards-web-app pods to be ready ...")
    retcode = kubectl_wait_pods(pods='tensorboards-web-app', namespace='kubeflow', timeout=120)
    assert retcode == 0
    print("All tensorboard pods are running!")

def build_trainingOperator():
    print("==========Installing Training-Operator==========")
    if INSTALLATION_OPTION == "helm":
        install_helm("training-operator", training_operator_chart_path)
    else:
        apply_kustomize(training_operator_kustomize_path)
    print("Waiting for training-operator pods to be ready ...")
    retcode = kubectl_wait_pods(pods='kubeflow-training-operator', namespace='kubeflow', timeout=120, identifier='control-plane')
    assert retcode == 0
    print("All training-operator pods are running!")

def build_katib():
    print("==========Installing Katib==========")
    if INSTALLATION_OPTION == "helm":
        install_helm("katib",katib_chart_path)
    else:
        apply_kustomize(katib_kustomize_path)
    print("Waiting for katib pods to be ready ...")
    retcode = kubectl_wait_pods(pods='controller, db-manager, \
                                      mysql, ui', 
                                namespace='kubeflow', timeout=150,identifier='katib.kubeflow.org/component')
    assert retcode == 0
    print("All katib pods are running!")

def build_profile():
    print("==========Installing Profiles==========")
    ##profile-and-kfam
    
    if INSTALLATION_OPTION == "helm":
        install_helm("profiles-and-kfam", profiles_and_kfam_chart_path)
    else:
        apply_kustomize(profiles_and_kfam_kustomize_path)
    print("Waiting for profiles-and-kfam pods to be ready ...")
    retcode = kubectl_wait_pods(pods='profiles', namespace='kubeflow', timeout=120, identifier='kustomize.component')
    assert retcode == 0
    
    ##user_namespace
    if INSTALLATION_OPTION == "helm":
        install_helm("user-namespace", user_namespace_chart_path)
    else:
        apply_kustomize(user_namespace_kustomize_path)
    print("Waiting for user-namespace pods to be ready ...")
    ##It needs some time for the pod to show up before validating
    time.sleep(15)
    retcode = kubectl_wait_pods(pods='ml-pipeline-ui-artifact, ml-pipeline-visualizationserver', namespace='kubeflow-user-example-com', timeout=120)
    assert retcode == 0
    print("All user-profile pods are running!")


parser = argparse.ArgumentParser()
INSTALLATION_OPTION_DEFAULT="kustomize"
parser.add_argument(
    "--installation_option",
    type=str,
    default=INSTALLATION_OPTION_DEFAULT,
    help=f"Kubeflow Installation option (helm/kustomize), default is set to {INSTALLATION_OPTION_DEFAULT}",
    required=False,
)
AWS_TELEMETRY_DEFAULT="enable"
parser.add_argument(
    "--aws_telemetry",
    type=str,
    default=AWS_TELEMETRY_DEFAULT,
    help=f"Usage tracking (enable/disable), default is set to {AWS_TELEMETRY_DEFAULT}",
    required=False,
)

args, _ = parser.parse_known_args()

if __name__ == "__main__":
    INSTALLATION_OPTION=args.installation_option
    AWS_TELEMETRY=args.aws_telemetry
    main()