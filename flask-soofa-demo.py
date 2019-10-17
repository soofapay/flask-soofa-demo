from decimal import Decimal

from flask import Flask, request, render_template, redirect, url_for
from soofa import Soofa, Transaction

TILL_NUMBER = "5005"
SECRET_KEY = "1zjmqsomeaxx8j8nqrn3t9oc1ee4ig"
app = Flask(__name__)


@app.route('/')
def home(response=None):
    return render_template('demo.html')


@app.route('/success/<response>')
def success(response):
    return render_template('demo.html', response=response)


@app.route('/payment', methods=['POST'])
def payment():
    if request.method == 'POST':
        tid = request.form["tid"]
        reference = request.form["reference"]
        amount = request.form["amount"]
        print("transaction id: "+ tid + " Transaction reference: " + reference + " Amount transacted: " + amount)
        soofa = Soofa(TILL_NUMBER, SECRET_KEY)
        if soofa.find(tid):
            transaction: Transaction = soofa.get_transaction()
            if Decimal(amount) < transaction.gross_amount:
                return redirect(url_for('success',
                                       response=f'Your payment of {transaction.receiver_currency}  {transaction.gross_amount} '
                                       f'is less than the expected {transaction.receiver_currency} '
                                       f'{amount}'))
            print(transaction.tid)
            print(transaction.status)
            print(transaction.get_time())
            return redirect(url_for('success', response="Transaction successful , transaction code " + transaction.tid))
        return redirect(url_for('success', response="Sorry, the transaction could not be completed"))
    else:
        return redirect(url_for('success', response="wrong request method"))


@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.get_json()
        transaction = Transaction(**data)
    except TypeError:
        return "invalid data"
    print(transaction.get_time())
    print(transaction.tid)
    print(transaction.receiver_currency, transaction.gross_amount)
    print(transaction.json())
    return "success"


if __name__ == '__main__':
    app.run(debug=True)
