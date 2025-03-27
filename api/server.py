from flask import Flask, jsonify, request
import pandas as pd

app = Flask(__name__)

class OperadorasService:
    def __init__(self, csv_path):
        self.df = pd.read_csv(csv_path, sep=';', encoding='utf-8')
    
    def search(self, term):
        if not term:
            return []
        
        return self.df[
            self.df.apply(lambda row: row.astype(str).str.contains(term, case=False).any(), axis=1)
        ].to_dict('records')

operadoras_service = OperadorasService('static/operadoras.csv')

@app.route('/api/operadoras', methods=['GET'])
def search_operadoras():
    term = request.args.get('q', '')
    results = operadoras_service.search(term)
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)