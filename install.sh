# create environment
virtualenv -p python .

# activate it
source bin/activate

# upgrade pip
pip install --upgrade pip

# install dependencies
pip install pandas numpy matplotlib pillow wordcloud seaborn tabulate SQLAlchemy