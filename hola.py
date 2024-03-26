import openai
import urllib.request

# Set your API key here
openai.api_key = os.getenv("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")

def generate_image(prompt):
    response = openai.Image.create(
        prompt=prompt,
        n=1,  # Number of images to generate
        size="512x512"  # Size of the image
    )

    if "data" in response:
        for idx, obj in enumerate(response["data"]):
            filename = f'my_image_{idx}.jpg'
            urllib.request.urlretrieve(obj['url'], filename)
        print('Images have been downloaded and saved locally')
    else:
        print("Failed to generate images")

generate_image("A mathematician writing equations on a blackboard")

