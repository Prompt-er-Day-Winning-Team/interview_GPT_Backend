from lda import TopicAnalyzer
from flask import Flask, request, jsonify

app = Flask(__name__)

analyzer = TopicAnalyzer()

@app.route('/analyze', methods=['GET', 'POST'])
def analyze():
    if request.method == 'GET':
        return "GET 요청을 받았습니다. POST 요청을 사용하세요."
    elif request.method == 'POST':
        try:
            data = request.json
            documents = data.get('documents')
            if documents:
                topics = analyzer.analyze_text(documents)
                return jsonify({"topics": topics})
            else:
                return jsonify({"error": "문서가 제공되지 않았습니다."})
        except Exception as e:
            return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
