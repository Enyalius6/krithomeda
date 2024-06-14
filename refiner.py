from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Load the places data from CSV into a pandas DataFrame
places_data = pd.read_csv('places_data.csv')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    # Retrieve user preferences from the form
    checkbox_fields = [
        'isHistorical', 'isArchitectural', 'isRomantic', 'isFamilyFriendly',
        'isSpiritual', 'isCultural', 'isPeaceful', 'isBeachDestination',
        'isRelaxing', 'isPartyDestination', 'isTrekking', 'isAdventure',
        'isScenic', 'isPhysical', 'isWildlife', 'isSafari', 'isPhotography',
        'isBoatRide', 'isReligious', 'isHillStation', 'isArchaeological',
        'isDesert', 'isSnorkeling', 'isScubaDiving', 'isCulinary',
        'isColonial', 'isBirdwatching', 'isSunsetView'
    ]
    
    preferences = {field: 0 for field in checkbox_fields}
    
    # Get list of checked checkboxes and update preferences
    checked_values = request.form.getlist('preferences')
    for value in checked_values:
        if value in preferences:
            preferences[value] = 1

    # Calculate recommendation scores for each place based on user preferences
    scores = []
    for index, row in places_data.iterrows():
        score = 0
        for field in checkbox_fields:
            if row[field] == preferences[field]:
                score += 1
        scores.append(score)

    # Add scores to places_data as a new column
    places_data['score'] = scores

    # Sort places by score in descending order and select top 5
    recommended_places = places_data.sort_values(by='score', ascending=False).head(5)['Place'].tolist()

    return render_template('recommendations.html', recommended_places=recommended_places)

if __name__ == '__main__':
    app.run(debug=True)
