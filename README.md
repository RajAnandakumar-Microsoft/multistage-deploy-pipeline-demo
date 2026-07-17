# Multi-Stage Deployment Pipeline (Sample)

A reusable **GitHub Actions** pipeline that builds a container image once and promotes it through
progressive **deployment waves** (Dev, Site, Additional Sites, Regional), with **manual approval
gates**, **post-deploy health checks**, and **automatic `helm rollback` on failure**.

## Two ways to run it

| Workflow | Deploys to | Needs | Use it for |
|----------|-----------|-------|-----------|
| `.github/workflows/demo-pipeline.yml` | An ephemeral **kind** cluster inside the runner | Nothing (runs entirely on GitHub) | Watching the full promotion + gates + rollback flow go green, no cloud |
| `.github/workflows/deploy-pipeline.yml` | **AKS** via Helm + OIDC | Azure (ACR, AKS, OIDC federation) | The real cloud deployment to lift into your environment |

## Layout

| Path | What it is |
|------|-----------|
| `app/` | Minimal hello-world web app (`/`, `/healthz`) plus Dockerfile. |
| `chart/` | Helm chart for the sample app, with one `values-<env>.yaml` per wave. |
| `.github/workflows/` | Orchestrators plus reusable per-wave deploy workflows (cloud and demo). |

## Quick start (demo, no cloud)

1. Push to `main`, or run **Demo Pipeline (kind, no cloud)** from the **Actions** tab.
2. Create four GitHub Environments (`dev`, `site`, `additional-sites`, `regional`) and add required
   reviewers so each wave pauses for approval.
3. Watch the image get built once and promoted through all four waves, approving each gate.

## Demo the rollback

Run **Demo Pipeline (kind, no cloud)** from the **Actions** tab and set **simulate_failure_wave** to a
wave (for example `dev`). That wave installs a healthy baseline, then a broken upgrade, so you watch the
health check fail, `helm rollback` restore the good version, and promotion stop. Leave it as `none` for a
normal green run.

## How it works

- **Build once, promote the same image.** The build job produces one image; every wave deploys that
  exact artifact, so what you validate in Dev is what reaches Regional.
- **Approval gates.** Each wave is bound to a GitHub Environment; required reviewers hold promotion
  until a human approves.
- **Health checks.** After each deploy, `kubectl rollout status` (backed by the chart readiness and
  liveness probes) confirms the wave is healthy before promotion continues.
- **Automatic rollback.** If a deploy or health check fails, the pipeline runs `helm rollback` to the
  last good revision and stops.

## Cloud version

`deploy-pipeline.yml` builds with `az acr build`, authenticates to Azure with **OIDC** (no long-lived
secrets), deploys to **AKS**, and adds an **Azure Monitor** health gate on top of the Kubernetes-native
checks. Set the `AZURE_*`, `ACR_*`, and per-wave cluster variables, then run it. It is manual-only in
this repo; add a `push` trigger in your environment.
