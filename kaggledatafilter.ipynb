{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 10,
   "metadata": {
    "tags": []
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "\n",
      "Average audio features for ['Lil Uzi Vert']:\n",
      "duration_ms: 207275.37878787878\n",
      "acousticness: 0.14927866666666667\n",
      "danceability: 0.7649242424242425\n",
      "energy: 0.6211818181818182\n",
      "loudness: -6.462151515151514\n",
      "tempo: 141.65369696969697\n",
      "\n",
      "Average audio features for ['YoungBoy Never Broke Again']:\n",
      "duration_ms: 179109.97826086957\n",
      "acousticness: 0.16979695652173915\n",
      "danceability: 0.7117173913043477\n",
      "energy: 0.6666739130434783\n",
      "loudness: -5.831804347826086\n",
      "tempo: 155.35595652173913\n",
      "\n",
      "Average audio features for ['Drake']:\n",
      "duration_ms: 237069.54761904763\n",
      "acousticness: 0.2332688571428571\n",
      "danceability: 0.6415714285714286\n",
      "energy: 0.5798095238095238\n",
      "loudness: -7.814380952380953\n",
      "tempo: 150.56671428571428\n",
      "\n",
      "Average audio features for ['Kevin Gates']:\n",
      "duration_ms: 199430.7027027027\n",
      "acousticness: 0.14671486486486487\n",
      "danceability: 0.731891891891892\n",
      "energy: 0.6757027027027027\n",
      "loudness: -5.9787567567567566\n",
      "tempo: 140.31902702702703\n",
      "\n",
      "Average audio features for ['Mac Miller']:\n",
      "duration_ms: 222156.32432432432\n",
      "acousticness: 0.2578450810810811\n",
      "danceability: 0.571081081081081\n",
      "energy: 0.6681621621621621\n",
      "loudness: -6.886837837837839\n",
      "tempo: 151.5582162162162\n"
     ]
    }
   ],
   "source": [
    "import pandas as pd\n",
    "\n",
    "data = pd.read_csv('/Users/kater/Documents/DSCI510/kaggledata.csv')\n",
    "numeric_cols = ['duration_ms', 'acousticness', 'danceability', 'energy', 'loudness', 'tempo']\n",
    "data[numeric_cols] = data[numeric_cols].apply(pd.to_numeric, errors='coerce')\n",
    "\n",
    "condition = (data['year'].between(2010, 2020)) & (data['popularity'] != 0) & (data['explicit'] == 1) & (data['tempo'] >= 126)\n",
    "\n",
    "filtered_data = data[condition]\n",
    "\n",
    "filtered_data.to_csv('/Users/kater/Documents/DSCI510/filtered_spotify_data.csv', index=False)\n",
    "\n",
    "top_artists = filtered_data['artists'].value_counts().head(5).index\n",
    "\n",
    "for artist in top_artists:\n",
    "    artist_data = filtered_data[filtered_data['artists'] == artist]\n",
    "    print(f\"\\nAverage audio features for {artist}:\")\n",
    "    for col in numeric_cols:\n",
    "        average = artist_data[col].mean()\n",
    "        print(f\"{col}: {average}\")\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.11.5"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
