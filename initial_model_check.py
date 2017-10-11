# Model Check
# =======
#
# We're going to use our processed data files to attempt to make some
# predictions. First, I'll just see if running everything through a
# (cross-validated) random forest will actually return results.

# %%

import os
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV

import wcf


%matplotlib inline
print(f'WCF API version {wcf.__version__}')


# %%

def combine_dataframes(start_path):
    files = os.listdir(start_path)
    frames = []
    for f in files:
        filename = start_path / f
        frames.append(pd.read_csv(filename))
    return pd.concat(frames)


men_path = Path('data') / 'men'
women_path = Path('data') / 'women'

women_df = combine_dataframes(women_path)
print(women_df.shape)
women_df.head()

# %%

men_df = combine_dataframes(men_path)
print(men_df.shape)
men_df.head()

# %%

sns.pairplot(women_df[['score_diff',
                       'score_ends_diff',
                       'score_hammer_diff',
                       'steal_diff',
                       'steal_ends_diff',
                       'winning_team']],
             hue='winning_team')
plt.show()

# It looks like we can get some separability here, but that might just be a
# limitation of the plot. This plot also doesn't include the country code
# (Canada probably would get a boost in any classifier), and I am unsure about
# how some of the non-diff data could help out.
#
# What should happen is how well the model performs when given just the first
# end, then the first two ends, etc. Or something like that. I'll see what
# happens as I start testing stuff. I'll focus on just the women's games first.

# Initial model check
# ----------------------
# %%

data = pd.get_dummies(women_df).dropna()

holdout = data[data.year == 2017]
training = data[data.year != 2017]

params = {'n_estimators': [10, 25, 50],
          'max_depth': [2, 5, 10, None]}

X_train = training.drop(['winning_team', 'game_id', 'tourney_id'], axis=1)
y_train = training.winning_team
X_test = training.drop(['winning_team', 'game_id', 'tourney_id'], axis=1)
y_test = training.winning_team

reg = GridSearchCV(RandomForestClassifier(),
                   params,
                   cv=3)

reg.fit(X_train, y_train)
reg.score(X_test, y_test)

# %%

reg.best_estimator_

# %%

data_men = pd.get_dummies(men_df).dropna()
data_men['team_0_LAT'] = 0
data_men['team_1_LAT'] = 0

men_X = data_men[X_train.columns]
men_y = data_men.winning_team

reg.score(men_X, men_y)

# %%

importances = reg.best_estimator_.feature_importances_
std = np.std([tree.feature_importances_
              for tree in reg.best_estimator_.estimators_],
             axis=0)
indices = np.argsort(importances)[::-1]

# Print the feature ranking
print('Feature ranking:')
for i in range(X_train.shape[1]):
    name = X_train.columns[i]
    imp = importances[indices[i]]
    print(f'{i + 1:2d}: {name} ({imp:.4f})')

plt.figure()
plt.title("Feature importances")
plt.bar(range(X_train.shape[1]),
        importances[indices],
        color="r",
        yerr=std[indices],
        align="center")
plt.xticks(range(X_train.shape[1]), indices)
plt.xlim([-1, X_train.shape[1]])
plt.show()

# %%

X_train.columns[53]

# The team listing at the end of the feature importances somewhat makes sense,
# so it's nice to see that the model picks out some of the top teams
# automatically, which is cool. Our testing accuracy of 0.8 is pretty good. We
# can probably do better with some directed feature engineering (or maybe a
# different model), but it's good to see that I actually *can* build out a
# predicitive model for this.
#
# The feature interactions (end_number x score_diff x hammer, for instance),
# will probably increase how good my model could become. Instead of building
# out those interactions automatically, I'll build them explicitly.
