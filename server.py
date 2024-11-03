from flask import Flask, render_template, request

app = Flask("Emotion Detector")

@app.route("/emotionDetector")
def sentiment_analyzer():
    '''
    gets text from html page
    and runs emotion detection using the code we wrote in emotion_detection.py
    '''

    text = request.args.get('textToAnalyze')
    response = emotion_detector(text)

    anger = response['anger']
    disgust = response['disgust']
    fear = response['fear']
    joy = response['joy']
    sadness = response['sadness']
    dominant_emotion = response['dominant_emotion']
    if dominant_emotion is None:
        return "API Failed, your text may be too short. Please Try Again."
    return f"For the given statement, the system response is 'anger': {anger}, " \
       f"'disgust': {disgust}, 'fear': {fear}, 'joy': {joy} and 'sadness': {sadness}. " \
       f"The dominant emotion is {dominant_emotion}."

    return response

@app.route("/")
def render_index_page():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)