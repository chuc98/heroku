import requests, uuid, json

# Add your subscription key and endpoint
subscription_key = "24737e77bae44bac99ec8d68d259cace"
endpoint = "https://hackathonbrayam.cognitiveservices.azure.com/"

# Add your location, also known as region. The default is global.
# This is required if using a Cognitive Services resource.
def traductor(text):
    location = "southcentralus"

    path = '/translate'
    constructed_url = endpoint + path

    params = {
        'api-versi0on': '3.0',
        'from': 'esp',
        'to': ['en']
    }
    constructed_url = endpoint + path

    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    # You can pass more than one object in body.
    body = [{
        'text': text
    }]

    request = requests.post(constructed_url, params=params, headers=headers, json=body)
    response = request.json()

    print(json.dumps(response, sort_keys=True, ensure_ascii=False, indent=4, separators=(',', ': ')))
    return 1
    
traductor('Hola')