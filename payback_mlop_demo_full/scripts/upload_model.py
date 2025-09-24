import os, shutil
from google.cloud import storage
ARTIFACTS_DIR = os.environ.get('ARTIFACTS_DIR', 'artifacts')
GCS_BUCKET = os.environ.get('MODEL_GCS_BUCKET', None)
GCS_PREFIX = os.environ.get('MODEL_GCS_PREFIX', '')

def upload_to_local(src_path):
    os.makedirs(ARTIFACTS_DIR, exist_ok=True)
    dst = os.path.join(ARTIFACTS_DIR, os.path.basename(src_path))
    shutil.copy2(src_path, dst)
    print(f"Copied artifact to local artifacts dir: {dst}")

def upload_to_gcs(src_path, bucket_name, prefix=''):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    dest_blob = prefix + os.path.basename(src_path)
    blob = bucket.blob(dest_blob)
    blob.upload_from_filename(src_path)
    print(f"Uploaded {src_path} to gs://{bucket_name}/{dest_blob}")

def upload_artifact_if_configured(model_path, manifest_path=None):
    if GCS_BUCKET:
        try:
            upload_to_gcs(model_path, GCS_BUCKET, GCS_PREFIX)
            if manifest_path and os.path.exists(manifest_path):
                upload_to_gcs(manifest_path, GCS_BUCKET, GCS_PREFIX)
        except Exception as e:
            print(f"GCS upload failed: {e}")
    else:
        try:
            upload_to_local(model_path)
            if manifest_path and os.path.exists(manifest_path):
                upload_to_local(manifest_path)
        except Exception as e:
            print(f"Local artifact copy failed: {e}")
