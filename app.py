from flask import Flask, request, redirect, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import hashlib

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']  = 'postgresql://postgres:password@db/db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class URLMapping(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    short_url = db.Column(db.String(6), unique=True, nullable=False)
    long_url = db.Column(db.String, nullable=False)

    def __init__(self, short_url, long_url):
        self.short_url = short_url
        self.long_url = long_url

# # 在应用上下文中创建数据库表
# with app.app_context():
#     db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/hello')
def hello():
    return 'hello!'

@app.route('/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()
    if 'long_url' not in data:
        return jsonify({"error": "Missing long_url parameter"}), 400
    
    long_url = data['long_url']
    
    # 使用 SHA256 哈希算法生成短网址
    short_url = hashlib.sha256(long_url.encode()).hexdigest()[:6]
    
    # 检查短网址是否已存在
    existing_url = URLMapping.query.filter_by(short_url=short_url).first()
    if existing_url:
        if existing_url.long_url != long_url:
            return jsonify({"error": "Short URL collision"}), 409
        return jsonify({"short_url": short_url}), 200
    
    # 存储新的短网址和长网址映射
    new_mapping = URLMapping(short_url, long_url)
    db.session.add(new_mapping)
    db.session.commit()
    
    return jsonify({"short_url": short_url}), 201

@app.route('/<short_url>', methods=['GET'])
def redirect_to_long_url(short_url):
    url_mapping = URLMapping.query.filter_by(short_url=short_url).first()
    if not url_mapping:
        return jsonify({"error": "Short URL not found"}), 404
    
    return redirect(url_mapping.long_url)

if __name__ == '__main__':
    app.run(debug=True)
