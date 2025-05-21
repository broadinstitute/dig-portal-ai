docker buildx build \
  --platform linux/amd64 \
  -t gcr.io/simage-main/portal-tools:latest \
  --push \
  --cache-to=type=registry,ref=gcr.io/simage-main/portal-tools:cache,mode=max \
  --cache-from=type=registry,ref=gcr.io/simage-main/portal-tools:cache \
  .