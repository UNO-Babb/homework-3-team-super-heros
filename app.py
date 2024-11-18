from flask import Flask, render_template, redirect, url_for, session
import random
import csv

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed to use sessions

@app.route('/')
def index():
    # Initialize game state if it doesn't exist in session
    if 'player1_wins' not in session:
        session['player1_wins'] = 0
        session['player2_wins'] = 0
        session['turn'] = 1  # 1 for Player 1, 2 for Player 2
        session['winner'] = None  # Round winner

    return render_template(
        'index.html',
        player1_wins=session['player1_wins'],
        player2_wins=session['player2_wins'],
        turn=session['turn'],
        winner=session['winner']
    )

@app.route('/roll')
def roll():
    # Roll two dice and calculate the sum
    dice_roll = random.randint(1, 6) + random.randint(1, 6)
    
    # Check if the roll is 11
    if dice_roll == 11:
        # Update win count for the player who rolled an 11
        if session['turn'] == 1:
            session['player1_wins'] += 1
            session['winner'] = "Player 1"
        else:
            session['player2_wins'] += 1
            session['winner'] = "Player 2"
    else:
        # Switch turns if no one wins this roll
        session['turn'] = 2 if session['turn'] == 1 else 1
        session['winner'] = None  # No winner this roll

    return redirect(url_for('index'))

@app.route('/reset')
def reset():
    # Reset the game, but keep the win counts
    session['turn'] = 1
    session['winner'] = None
    return redirect(url_for('index'))

@app.route('/new_game')
def new_game():
    # Clear the session completely to start a new game
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
