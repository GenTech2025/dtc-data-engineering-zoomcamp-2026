### Setting up GCP Service Account with Kestra

```bash
# When executed from kestra directory
echo SECRET_GCP_SERVICE_ACCOUNT=$(cat ../../module_1/terraform-gcp/keys/creds.json | base64 -w 0) >> .env_encoded
```
