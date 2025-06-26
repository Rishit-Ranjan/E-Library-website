from flask import Flask, render_template, request
import pickle
import numpy as np

popular_df = pickle.load(open('C:/Users/rishi/OneDrive/Documents/The-Grey-Ink-main/project/popular.pkl', 'rb'))
pt = pickle.load(open('C:/Users/rishi/OneDrive/Documents/The-Grey-Ink-main/project/pt.pkl','rb'))
books = pickle.load(open('C:/Users/rishi/OneDrive/Documents/The-Grey-Ink-main/project/books.pkl','rb'))
similarity_scores = pickle.load(open('C:/Users/rishi/OneDrive/Documents/The-Grey-Ink-main/project/similarity_scores.pkl','rb'))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/trending')
def trending():
    return render_template('trending.html',
                           book_name = list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           votes=list(popular_df['num_ratings'].values),
                           rating=list(popular_df['avg_rating'].values)
                           )

@app.route('/category')
def category():
    return render_template('category.html')

@app.route('/recommend_books', methods = ["POST"])
def recommend_books():
    user_input = request.form.get('user_input')
    index = np.where(pt.index==user_input)
    similar_items = sorted(list(enumerate(similarity_scores[index])),key=lambda x:x[1],reverse=True) [1:5]
    
    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        
        data.append(item)
    print(data)  # Debugging output to check the recommendations
    return render_template('recommendation.html', data=data)

if __name__ == '__main__':
    app.run(debug= True)