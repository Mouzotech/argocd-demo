# argocd-demo — GitOps en el homelab

Flujo completo: **push de código → GitHub Actions construye la imagen → ghcr.io →
ArgoCD la despliega en k3s** sin tocar el cluster a mano.

```
push a app/ ──► GitHub Actions ──► ghcr.io/mouzotech/argocd-demo:<sha>
                     │
                     └──► commit automático en manifests/ con el nuevo tag [skip ci]
                                │
                                ▼  (ArgoCD hace poll del repo)
                          ArgoCD (k3s) ──► rolling update ──► https://demo.xeon
```

## Estructura

| Ruta | Qué es |
|---|---|
| `app/app.py` | La app (página web con versión, color y nombre del pod) |
| `Dockerfile` | Imagen de la app |
| `manifests/` | Lo que ArgoCD vigila: Deployment + Service + Ingress (`demo.xeon`) |
| `.github/workflows/ci.yaml` | CI: build → push a ghcr → actualiza tag en manifests |
| `argocd/application.yaml` | Application de ArgoCD (se aplica una sola vez a mano) |

## Cómo hacer la demo

1. Edita `app/app.py` (cambia `MESSAGE`, `COLOR` o `VERSION`) y haz push a `main`.
2. Mira la pestaña **Actions**: build + push de la imagen (~1-2 min).
3. El workflow hace un commit en `manifests/deployment.yaml` con el nuevo tag.
4. ArgoCD (https://argocd.xeon) detecta el cambio y sincroniza solo.
5. Refresca https://demo.xeon → cambio visible.

Cambios solo de manifests (p. ej. `replicas`) no pasan por CI: ArgoCD los aplica directamente.
