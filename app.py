from flask import Flask, render_template, request
from addons import clothes, places, seasons


app = Flask('MyApp')

season = ''
place = ''


@app.route('/start')
def start_page():
    return render_template('main.html')

@app.route('/show_clothes', methods=['POST'])
def show_clothes():
    season = request.form['season']
    place = request.form['place']
    tops = []
    bot = []
    for i in range(len(clothes)):
        if season in clothes[i]['season']:
            if place in clothes[i]['place']:
                if clothes[i]['top']:
                    tops.append([clothes[i]['name'], clothes[i]['special']])
                else:
                    bot.append([clothes[i]['name'], clothes[i]['special']])
    return render_template('show_clothes.html', season=season, place=place, tops=tops, bot=bot, id_season = season, id_place = place)




@app.route('/create_collection', methods=['POST'])
def create_collection():
    tops = request.form.getlist("tops")
    bots = request.form.getlist("bots")
    season = request.form['season']
    place = request.form['place']
    answer = make(tops, bots, season, place)
    return render_template('collection.html', collections=answer)



def make(tops, bots, season, place):
    
    answer = set()
    
    def F(i, choice):
        for j in range(i, len(clothes)):
            if all(item in clothes[j]['match'] for item in choice):
                if place in clothes[j]['place']:
                    if season in clothes[j]['season']:
                        F(i+1, choice + [clothes[j]['special']])
        if len(choice) <= 3:
            if (not(check) and  any(not(clothes[int(item)]['top']) for item in choice))\
                or (check and any(item in bots for item in choice)):
                answer.add(tuple(sorted(choice)))

    if len(tops) > 0 and len(bots) > 0:
        check = True
        for special in tops:
            F(0, [special])
    else:
        check = False
        for special in tops+bots:
            F(0, [special])
        
    collections = []

    for collection in sorted(answer, key=len):
        s = ' и '.join([clothes[int(special)]['name'] for special in collection])
        collections.append(s)
        
    return collections
                    

    



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)



