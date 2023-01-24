import boto3
import pandas as pd
from io import BytesIO


def main():
    s3 = boto3.client('s3')
    client = boto3.client('comprehend')

    obj = s3.get_object(Bucket='scrape-results-webank', Key='scrape-result.xlsx')
    file_like_object = BytesIO(obj['Body'].read())
    df = pd.read_excel(file_like_object)
    df = df[['content','score']]
    print('Dataframe created')

    def sentiment_analysis(test):
        response = client.detect_sentiment(
            Text=test,
            LanguageCode='it'
        )
        return response
    
    sentiments = []

    for review in df['content']:
        sent = sentiment_analysis(review)
        sentiments.append(sent['Sentiment'])

    df['sentiment'] = sentiments
    print('Sentiment analysis completed')

    ## SAVE FILE DIRECTLY TO S3
    output = BytesIO()

    df.to_excel(output)
    output.seek(0)

    s3.upload_fileobj(output, 'analysis-results-webank', 'sentiment_analysis.xlsx')
    print('Analysis results saved to S3')


if __name__ == '__main__':
    main()


# def main():
#     s3 = boto3.client('s3')
#     path = 's3://scrape-results-webank/scrape_result.xlsx'

#     df = pd.read_excel(path)
#     df = df[['content','score']]
#     print(df.head())