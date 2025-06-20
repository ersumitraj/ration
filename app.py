from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
import unicodedata
import os

app = Flask(__name__)
app.secret_key = 'shambhu123'
csv_file = 'data.csv'


def clean_column(name):
    return unicodedata.normalize("NFKC", name).replace('\u200b', '').strip()


def read_data():
    if not os.path.exists(csv_file):
        columns = ['Ref_Id', 'Date', 'वर्ग', 'आधार नंबर', 'नाम', 'मोबाईल न', 'Paid', 'Dues', 'Status']
        df = pd.DataFrame(columns=columns)
        df.to_csv(csv_file, index=False)
    df = pd.read_csv(csv_file, dtype=str, keep_default_na=False)
    df.columns = [clean_column(col) for col in df.columns]
    df.fillna('', inplace=True)
    df.insert(0, 'क्रम', range(1, len(df) + 1))
    return df


def save_data(df):
    df.drop(columns=['क्रम'], inplace=True, errors='ignore')
    df.to_csv(csv_file, index=False)


@app.route('/')
def home():
    return redirect(url_for('card_view'))


@app.route('/card')
def card_view():
    df = read_data()
    return render_template('card.html', data=df.to_dict(orient='records'))


@app.route('/mark_paid/<int:index>', methods=['POST'])
def mark_paid(index):
    df = read_data()
    if index < len(df):
        current_status = df.at[index, 'Status'] if 'Status' in df.columns else ''
        df.at[index, 'Status'] = 'Paid' if current_status != 'Paid' else 'Unpaid'
        save_data(df)
    return redirect(url_for('card_view'))


@app.route('/table')
def table_view():
    df = read_data()
    return render_template('table.html', data=df.to_dict(orient='records'), columns=df.columns)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
