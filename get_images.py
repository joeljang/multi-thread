import pandas as pd
import concurrent.futures
import time
import os
import urllib.request

#df = pd.read_csv('Argon434_imgurls.csv', delimiter='\t', header=None)
#df2 = pd.read_csv('argon_label_lst434.csv', delimiter=',', header=None)
df = pd.read_csv('Argon_missing8_imgurls.csv', delimiter='\t', header=None)
df2 = pd.read_csv('argon_label_lst_m8.csv', delimiter=',', header=None)

df.columns = ['label', 'ndid64', 'url']
df2.columns = ['label', 'label_code']

# Retrieve a single page and report the URL and contents
def load_url(url, timeout):
    with urllib.request.urlopen(url, timeout=timeout) as conn:
        return conn.read()

for index, row in df2.iterrows():
    label = row['label']
    label_code = row['label_code']
    temp_df = df.loc[df['label'] == label]
    print(f'The number of instances in {label, label_code}: {temp_df.shape}')
    img_urls = temp_df['url']

    #Getting the images with concurrent multi-thread
    os.mkdir('/data/public/rw/team-autolearn/argon434/train/'+label_code)
    t1 = time.perf_counter()
    imgcnt=0
    exceptcnt=0
    # We can use a with statement to ensure threads are cleaned up promptly
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Start the load operations and mark each future with its URL
        future_to_url = {executor.submit(load_url, url, 60): url for url in img_urls}
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                img_data = future.result()
                filename = '/data/public/rw/team-autolearn/argon434/train/'+label_code+'/'+label_code+'_'+str(imgcnt)+'.JPEG'
                with open(filename, 'wb') as handler:
                    handler.write(img_data)
                imgcnt+=1
            except Exception as exc:
                exceptcnt+=1
                #print('%r generated an exception: %s' % (url, exc))
    t2 = time.perf_counter()
    print(f'{index} Downloaded images: {imgcnt}, Exceptions: {exceptcnt}, Finished in {t2-t1} seconds')