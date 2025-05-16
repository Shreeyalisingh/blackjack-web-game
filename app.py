from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def deal_card():
    cards = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11]
    return random.choice(cards)

def calculate_score(cards):
    if sum(cards) == 21 and len(cards) == 2:
        return 0
    if 11 in cards and sum(cards) > 21:
        cards.remove(11)
        cards.append(1)
    return sum(cards)

def compare(user_score, dealer_score):
    if user_score == dealer_score:
        return "Draw 🙃"
    elif dealer_score == 0:
        return "Lose, opponent has Blackjack 😱"
    elif user_score == 0:
        return "Win with a Blackjack 😎"
    elif user_score > 21:
        return "You went over. You lose 😭"
    elif dealer_score > 21:
        return "Opponent went over. You win 😁"
    elif user_score > dealer_score:
        return "You win 😃"
    else:
        return "You lose 😤"

@app.route('/')
def index():
    session['user_cards'] = [deal_card(), deal_card()]
    session['dealer_cards'] = [deal_card(), deal_card()]
    return redirect(url_for('game'))

@app.route('/game', methods=['GET', 'POST'])
def game():
    user_cards = session['user_cards']
    dealer_cards = session['dealer_cards']

    if request.method == 'POST':
        if request.form['action'] == 'Hit':
            user_cards.append(deal_card())
            session['user_cards'] = user_cards
        elif request.form['action'] == 'Stand':
            while calculate_score(dealer_cards) < 17:
                dealer_cards.append(deal_card())
            session['dealer_cards'] = dealer_cards
            return redirect(url_for('result'))

    user_score = calculate_score(user_cards)
    if user_score > 21 or user_score == 0:
        return redirect(url_for('result'))

    return render_template('game.html', user_cards=user_cards, dealer_card=dealer_cards[0], user_score=user_score)

@app.route('/result')
def result():
    user_cards = session['user_cards']
    dealer_cards = session['dealer_cards']
    user_score = calculate_score(user_cards)
    dealer_score = calculate_score(dealer_cards)

    result = compare(user_score, dealer_score)

    return render_template('result.html', user_cards=user_cards, dealer_cards=dealer_cards,
                           user_score=user_score, dealer_score=dealer_score, result=result)

if __name__ == '__main__':
    app.run(debug=True)
