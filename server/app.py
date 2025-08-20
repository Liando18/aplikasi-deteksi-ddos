from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/hello', methods=['GET'])
def hello():
    return jsonify({"message": "Hello World"})

@app.route('/api/detection', methods=['POST'])
def detection():
    try:
        data = request.json  

        print("📥 Data diterima dari Server")
        if isinstance(data, list):
            for item in data:
                timestamp = item.get("datetime", "-")
                label = item.get("label", "-")
                print(f"{timestamp} | Status : {label}")
        else:  
            timestamp = data.get("datetime", "-")
            label = data.get("label", "-")
            print(f"{timestamp} | Status : {label}")

        return jsonify({
            "status": "success",
            "received_records": len(data) if isinstance(data, list) else 1
        }), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
