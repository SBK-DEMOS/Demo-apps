package main

import (
        "context"
        "os"
        "time"

        corev1 "k8s.io/api/core/v1"
        "k8s.io/apimachinery/pkg/api/errors"
        "k8s.io/apimachinery/pkg/runtime" 
        clientgoscheme "k8s.io/client-go/kubernetes/scheme"
        ctrl "sigs.k8s.io/controller-runtime"
        "sigs.k8s.io/controller-runtime/pkg/client"
        "sigs.k8s.io/controller-runtime/pkg/log/zap"
)

var (
        scheme   = runtime.NewScheme()
        setupLog = ctrl.Log.WithName("setup")
)

const (
        // LabelKey defines the key for the label to be applied to namespaces.
        LabelKey = "controller.example.com/managed"
        // LabelValue defines the value for the label.
        LabelValue = "true"
)

func init() {
        // Add the core Kubernetes scheme to the runtime scheme.
        _ = clientgoscheme.AddToScheme(scheme)

        // Add any other API groups you might need to watch here.
        // For this controller, only corev1 (Namespaces) is needed.
}

// NamespaceReconciler reconciles a Namespace object.
type NamespaceReconciler struct {
        client.Client
        Scheme *runtime.Scheme
}

// +kubebuilder:rbac:groups="",resources=namespaces,verbs=get;list;watch;update;patch
// +kubebuilder:rbac:groups="",resources=namespaces/status,verbs=get

// Reconcile is part of the main kubernetes reconciliation loop which aims to
// move the current state of the cluster closer to the desired state.
// It will be triggered by events on Namespace resources.
func (r *NamespaceReconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
        log := ctrl.Log.WithValues("namespace", req.NamespacedName)

        // Fetch the Namespace instance.
        namespace := &corev1.Namespace{}
        err := r.Get(ctx, req.NamespacedName, namespace)
        if err != nil {
                if errors.IsNotFound(err) {
                        // Request object not found, could have been deleted after reconcile request.
                        // Owned objects are automatically garbage collected. For additional cleanup logic,
                        // use finalizers. Return and don't requeue.
                        log.Info("Namespace resource not found. Ignoring since object must be deleted")
                        return ctrl.Result{}, nil
                }
                // Error reading the object - requeue the request.
                log.Error(err, "Failed to get Namespace")
                return ctrl.Result{}, err
        }

        // Check if the namespace already has the desired label with the correct value.
        if namespace.Labels == nil {
                namespace.Labels = make(map[string]string)
        }

        if namespace.Labels[LabelKey] == LabelValue {
                log.Info("Namespace already has the correct label", "label", LabelKey)
                return ctrl.Result{}, nil // Nothing to do.
        }

        // Add or update the label.
        namespace.Labels[LabelKey] = LabelValue
        err = r.Update(ctx, namespace)
        if err != nil {
                log.Error(err, "Failed to update Namespace with label")
                // If update fails, requeue the request after a short delay.
                return ctrl.Result{RequeueAfter: time.Second * 5}, err
        }

        log.Info("Successfully labeled Namespace", "label", LabelKey, "value", LabelValue)
        return ctrl.Result{}, nil // Reconcile complete.
}

// SetupWithManager sets up the controller with the Manager.
func (r *NamespaceReconciler) SetupWithManager(mgr ctrl.Manager) error {
        // Create a new controller managed by the manager.
        return ctrl.NewControllerManagedBy(mgr).
                For(&corev1.Namespace{}). // Watches for Namespace objects.
                Complete(r)                // Completes the controller setup with this reconciler.
}

func main() {
        // Set up the logger.
        ctrl.SetLogger(zap.New(zap.UseFlagOptions(&zap.Options{Development: true})))

        // Set up the manager.
        mgr, err := ctrl.NewManager(ctrl.GetConfigOrDie(), ctrl.Options{
                Scheme: scheme,
                // MetricsBindAddress: "0", // Disable metrics to avoid port conflicts in simple setups
                // LeaderElection:   false, // Disable leader election for single replica
                Logger: zap.New(zap.UseFlagOptions(&zap.Options{Development: true})),
        })
        if err != nil {
                setupLog.Error(err, "unable to start manager")
                os.Exit(1)
        }

        // Create and register the NamespaceReconciler.
        if err = (&NamespaceReconciler{
                Client: mgr.GetClient(),
                Scheme: mgr.GetScheme(),
        }).SetupWithManager(mgr); err != nil {
                setupLog.Error(err, "unable to create controller", "controller", "Namespace")
                os.Exit(1)
        }

        setupLog.Info("starting manager")
        if err := mgr.Start(ctrl.SetupSignalHandler()); err != nil {
                setupLog.Error(err, "problem running manager")
                os.Exit(1)
        }
}