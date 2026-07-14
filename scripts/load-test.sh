#!/usr/bin/env bash
# Load test script — triggers HPA scaling on OpenShift
# Usage: ./scripts/load-test.sh [URL] [DURATION_SEC]
# Example: ./scripts/load-test.sh http://banking-frontend-banking-demo.apps-crc.testing 60

URL="${1:-http://localhost:8080}"
DURATION="${2:-30}"

echo "Load testing: $URL/api/transactions/generate for ${DURATION}s"
echo "Watch pods scale: oc get pods -n banking-demo -w"

if command -v hey &> /dev/null; then
  hey -z "${DURATION}s" -c 20 -q 10 -m POST "${URL}/api/transactions/generate"
elif command -v ab &> /dev/null; then
  ab -k -n 3000 -c 10 -t "$DURATION" -p tmp/empty_body.txt -T "application/json" "${URL}/api/transactions/generate"
else
  echo "Install 'hey' or 'apache2-utils' (ab) for load testing."
  echo "Fallback: curl loop..."
  END=$((SECONDS + DURATION))
  while [ $SECONDS -lt $END ]; do
    curl -s -X POST "${URL}/api/transactions/generate" > /dev/null &
  done
  wait
fi

echo "Done."
