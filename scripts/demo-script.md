# Demo Script — Mini Banking Dashboard (20-30 phút)

## Phần 1: Mở đầu (2 phút)

"Em xin demo Mini Banking Dashboard — use case phổ biến trong banking sector.
App gồm 3 tier: Frontend, API, PostgreSQL, chạy trên OpenShift Local cluster
em setup trên laptop."

## Phần 2: Kiến trúc (2 phút)

- Show diagram trong instruction.txt hoặc slide
- Giải thích flow: Browser → nginx → FastAPI → PostgreSQL

## Phần 3: Deploy & Topology (5 phút)

- Mở OpenShift Console → Developer → Topology
- Show pods, services, route
- Click vào banking-api pod → YAML → show liveness/readiness probes

## Phần 4: Live app (3 phút)

- Mở Route URL
- Show dashboard, stat cards, transaction table
- Click "Generate Transaction" vài lần

## Phần 5: Monitoring (4 phút)

- Console → Observe → Metrics
- Show CPU/RAM per pod
- Workloads → Logs của banking-api

## Phần 6: Auto-scale (5 phút)

- Chạy: `bash scripts/load-test.sh <ROUTE_URL> 60`
- Console → watch banking-api pods scale 1 → N
- "Đây là lợi ích so với VM: không cần provision máy mới"

## Phần 7: Rolling update (5 phút)

- Đổi APP_THEME: blue → red trong deployment
- `oc apply -f openshift/02-backend-deployment.yaml`
- Refresh browser — header đổi màu, app không down
- "maxUnavailable: 0 đảm bảo zero downtime"

## Phần 8: CI/CD (3 phút, optional)

- Show GitHub Actions workflow
- Push commit → pipeline → rollout

## Phần 9: Business value (2 phút)

- Time to market, resilience, security (SCC, RBAC), hybrid cloud

## Phần 10: Q&A
