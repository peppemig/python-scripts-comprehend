from google_play_scraper import app
from google_play_scraper import Sort, reviews
import boto3
import pandas as pd
import numpy as np
from io import BytesIO

def main():
    s3 = boto3.client('s3')

    result, continuation_token = reviews(
    'com.opentecheng.android.webank',
    lang='it',
    country='it',
    sort=Sort.NEWEST,
    count=20)
    print('Scraping done')

    df = pd.DataFrame(np.array(result),columns=['review'])
    df = df.join(pd.DataFrame(df.pop('review').tolist()))
    print('Dataframe created')

    # df.to_excel('scrape_result.xlsx')
    # s3.upload_file('scrape_result.xlsx','scrape-results-webank','scrape_result.xlsx')
    ## SAVE FILE DIRECTLY TO S3

    output = BytesIO()
    df.to_excel(output)
    output.seek(0)
    s3.upload_fileobj(output, 'scrape-results-webank', 'scrape-result.xlsx')
    print('Scraping results saved to S3')


if __name__ == '__main__':
    main()