from flask import Flask, render_template, request, jsonify, send_from_directory
import os

app = Flask(__name__)
# مسیر ذخیره فایل‌ها
UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__name__)), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/login', methods=['POST'])
def login():
    username = request.json.get('username')
    if not username:
        return jsonify({'error': 'نام کاربری الزامی است'}), 400
    
    # ساخت پوشه کاربر در صورت عدم وجود
    user_dir = os.path.join(UPLOAD_FOLDER, username)
    os.makedirs(user_dir, exist_ok=True)
    return jsonify({'success': True})

@app.route('/api/folders', methods=['GET'])
def get_folders():
    # لیست تمام پوشه‌ها (کاربران)
    folders = [f for f in os.listdir(UPLOAD_FOLDER) if os.path.isdir(os.path.join(UPLOAD_FOLDER, f))]
    return jsonify(folders)

@app.route('/api/files/<folder>', methods=['GET'])
def get_files(folder):
    folder_path = os.path.join(UPLOAD_FOLDER, folder)
    if not os.path.exists(folder_path):
        return jsonify([])
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    return jsonify(files)

@app.route('/api/upload/<folder>', methods=['POST'])
def upload(folder):
    # بررسی دسترسی (نام کاربری فرستاده شده در هدر باید با نام پوشه یکی باشد)
    if request.headers.get('X-Username') != folder:
        return jsonify({'error': 'شما فقط مجاز به آپلود در پوشه خودتان هستید'}), 403
        
    if 'file' not in request.files:
        return jsonify({'error': 'فایلی ارسال نشده است'}), 400
        
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'نام فایل خالی است'}), 400
        
    # جلوگیری از باگ‌های امنیتی مسیر فایل
    safe_filename = file.filename.replace('/', '').replace('\\', '')
    file.save(os.path.join(UPLOAD_FOLDER, folder, safe_filename))
    return jsonify({'success': True})

@app.route('/api/delete/<folder>/<filename>', methods=['DELETE'])
def delete_file(folder, filename):
    if request.headers.get('X-Username') != folder:
        return jsonify({'error': 'شما مجاز به حذف این فایل نیستید'}), 403
        
    file_path = os.path.join(UPLOAD_FOLDER, folder, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
    return jsonify({'success': True})

@app.route('/api/rename/<folder>', methods=['PUT'])
def rename_file(folder):
    if request.headers.get('X-Username') != folder:
        return jsonify({'error': 'شما مجاز به تغییر نام در این پوشه نیستید'}), 403
        
    data = request.json
    old_name = data.get('old_name')
    new_name = data.get('new_name').replace('/', '').replace('\\', '')
    
    old_path = os.path.join(UPLOAD_FOLDER, folder, old_name)
    new_path = os.path.join(UPLOAD_FOLDER, folder, new_name)
    
    if os.path.exists(old_path):
        os.rename(old_path, new_path)
        return jsonify({'success': True})
    return jsonify({'error': 'فایل پیدا نشد'}), 404

@app.route('/download/<folder>/<filename>')
def download(folder, filename):
    # دانلود برای همه آزاد است
    return send_from_directory(os.path.join(UPLOAD_FOLDER, folder), filename)

if __name__ == '__main__':
    # اجرا روی تمام آی‌پی‌های شبکه داخلی
    app.run(host='0.0.0.0', port=5151, debug=True)
