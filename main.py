from flask import Flask, request, Response
from transformers import pipeline
import waitress
import logging
import click
import json

logger = logging.getLogger(__name__)

logging.basicConfig(
    format = '%(levelname)s | %(asctime)s | %(message)s',
    datefmt = '%Y-%m-%dT%H:%M:%SZ'
    )

def deploy_model(
        model_id,
        host = '0.0.0.0',
        port = 2244
):
    
    app = Flask(__name__)

    logger.info('loading model')
    try:
        model = pipeline(model = model_id, trust_remote_code = True, device_map = 'auto')
        logger.info('model successfully loaded')
    except Exception as e:
        logger.exception(f'Error while loading model: {e}')

    @app.route('/predict', methods = ['POST'])
    def predict():
        try:
            data = request.get_json()
            to_predict = data['prompt']
            logger.info('data successfully retrieved from request')
        except Exception as e:
            logger.exception(f'Error while retrieving data: {e}')
            return Response(
                'Data appears to be incorrectly formatted',
                400
            )

        try:
            model_response = model(to_predict)[0]['generated_text']
            logger.info('model response successfully retrieved')
            model_response = {
                'choices' : [{'text' : model_response}]
            }
            logger.info('model response successfully formatted, returning')
            return json.dumps(model_response)
        except Exception as e:
            logger.exception(f'Error while retrieving model response: {e}')
            return Response(
                'Error in performing prediction',
                500
            )
        
    logger.info('Serving model')
    waitress.serve(
        app,
        host = host,
        port = port
    )

@click.command()
@click.argument('model')
def main(model):
    deploy_model(model)

if __name__ == '__main__':
    main()
