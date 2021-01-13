from google.cloud import storage

bucket_name = 'public-curtis'
prefix = 'argon/im1kdup_lb442_im5000'

storage_client = storage.Client()
bucket = storage_client.bucket(bucket_name)

blobs = storage_client.list_blobs(bucket_name, prefix=prefix)
cnt=0
for b in blobs:
    b.download_to_filename('./argonjson/'+str(cnt)+'.json')
    cnt+=1