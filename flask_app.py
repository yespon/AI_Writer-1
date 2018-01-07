import os
import sys
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify, send_file
from werkzeug.utils import secure_filename

import endpoints

"""
*-------------------------------------------------------*
|                   Flask Sever Session                 |
*-------------------------------------------------------*
"""

app = Flask(__name__)
UPLOAD_DIR = 'data/'
ALLOWED_EXT = set(['txt'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXT


@app.route('/')
def ocr():
    return render_template('writer.html')


@app.route('/submit', methods=['POST'])
def submit():
    if len(request.files) > 0:

        file = request.files['file']
        doc_fn = secure_filename(file.filename)

        sys.stdout.write("\n--- Uploading Document File------------------------------------------\n")
        sys.stdout.write("\t{}\n".format(request))
        print(request)

        if file and allowed_file(file.filename):

            try:
                sys.stdout.write("\tUp loading...\n")

                # check its directory for uploading
                if not os.path.isdir(UPLOAD_DIR):
                    os.mkdir(UPLOAD_DIR)

                # remove all the previous processed document file
                for fname in os.listdir(UPLOAD_DIR):
                    path = os.path.join(UPLOAD_DIR, fname)
                    if os.path.isfile(path):
                        os.remove(path)

                # save the uploaded document on UPLOAD_DIR
                file.save(os.path.join(UPLOAD_DIR, doc_fn))
                sys.stdout.write("\tsave the document {}\n".format(doc_fn))

                sys.stdout.write("\tsuccessfully uploaded.\n")
                dst_file_path = os.path.join(UPLOAD_DIR, doc_fn)

                result_article = endpoints.main(dst_file_path=dst_file_path)

                sys.stdout.write("\n--- Finished1 -------------------------------------------------------\n")

                return jsonify(result=result_article)

            except Exception as e:
                str = '\tException: {}'.format(e)
                sys.stdout.write(str + "\n")
                return str

        else:
            str = "\tnot allowed file format {}.".format(doc_fn)
            sys.stdout.write(str + "\n")
            return str


if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=True,
        threaded=True,
    )
