# Troubleshooting

Common issues and solutions for DClaw Video.

## Quick Diagnostics

```bash
# Check app pods
kubectl get pods -n dclaw-video

# Check logs
kubectl logs -n dclaw-video deployment/dclaw-video-backend

# Check database
kubectl get clusters -n dclaw-video
```

## Sections

- [Common Issues](./common-issues)
- [FAQ](./faq)
