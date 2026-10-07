import json
import os
import urllib.request
import urllib.error
import boto3

s3 = boto3.client("s3")

GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-3.5-flash-lite")


def lambda_handler(event, context):

    print("Lambda started")

    # Get S3 information
    record = event["Records"][0]

    bucket = record["s3"]["bucket"]["name"]
    key = record["s3"]["object"]["key"]

    print(f"Input file: s3://{bucket}/{key}")

    # Download transcript
    response = s3.get_object(
        Bucket=bucket,
        Key=key
    )

    transcript_json = json.loads(
        response["Body"].read().decode("utf-8")
    )

    # Extract transcript
    transcript = extract_transcript(transcript_json)

    if not transcript:
        raise Exception("No transcript found in the JSON file.")

    print("Transcript successfully extracted.")

    # Generate summary
    summary = summarize_with_gemini(transcript)

    # Create output filename
    filename = os.path.basename(key)
    name = os.path.splitext(filename)[0]

    summary_key = f"Converted/{name}_summary.txt"

    # Save summary
    s3.put_object(
        Bucket=bucket,
        Key=summary_key,
        Body=summary.encode("utf-8"),
        ContentType="text/plain"
    )

    print(f"Summary saved to s3://{bucket}/{summary_key}")

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Meeting summary created successfully",
            "summary_location": f"s3://{bucket}/{summary_key}"
        })
    }


def extract_transcript(data):

    try:
        return data["results"]["transcripts"][0]["transcript"]

    except (KeyError, IndexError, TypeError):

        return ""


def summarize_with_gemini(transcript):

    prompt = f"""
You are an AI meeting assistant.

Analyze the following meeting transcript.

Create a professional meeting summary containing:

1. Overview
2. Key Points
3. Decisions Made
4. Action Items
5. Important Discussion Topics
6. Risks or Issues
7. Next Steps

For action items, include:
- Task
- Owner
- Deadline

Do NOT invent information.

If an owner or deadline was not mentioned,
write "Not specified."

If no decisions, risks, or next steps were identified,
write "None identified."

Keep the summary concise and professional.

MEETING TRANSCRIPT:

{transcript}
"""

    url = (
        "https://generativelanguage.googleapis.com/v1beta/"
        f"models/{GEMINI_MODEL}:generateContent"
        f"?key={GEMINI_API_KEY}"
    )

    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ],
        "generationConfig": {
            "maxOutputTokens": 3000
        }
    }

    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json"
        },
        method="POST"
    )

    try:

        with urllib.request.urlopen(request, timeout=60) as response:

            result = json.loads(
                response.read().decode("utf-8")
            )

        return result["candidates"][0]["content"]["parts"][0]["text"]

    except urllib.error.HTTPError as e:

        error = e.read().decode("utf-8")

        print("Gemini API error:")
        print(error)

        raise Exception(error)

        #TEST AT 10/07/2026 7:33PM
