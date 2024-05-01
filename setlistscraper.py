{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {
    "tags": []
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "           Artist Date and Location                             Location Name  \\\n",
      "0  Morgan Wallen         Apr 5 2024  Lucas Oil Stadium, Indianapolis, IN, USA   \n",
      "\n",
      "  Start Time Tour Average Duration  \\\n",
      "0    9:30 PM                 4h 4m   \n",
      "\n",
      "                                               Songs  \n",
      "0  [Broadway Girls, Ain't That Some, I Wrote the ...  \n",
      "CSV file has been updated with the latest detailed data.\n"
     ]
    }
   ],
   "source": [
    "from selenium import webdriver\n",
    "from selenium.webdriver.chrome.service import Service\n",
    "from bs4 import BeautifulSoup\n",
    "import time\n",
    "import pandas as pd\n",
    "\n",
    "service = Service(executable_path='/Users/kater/Downloads/chromedriver-mac-x64/chromedriver')\n",
    "driver = webdriver.Chrome(service=service)\n",
    "\n",
    "def fetch_setlist_data(url):\n",
    "    driver.get(url)\n",
    "    time.sleep(5)  \n",
    "\n",
    "    soup = BeautifulSoup(driver.page_source, 'html.parser')\n",
    "\n",
    "    artist_element = soup.find(class_='setlistHeadline')\n",
    "    artist = artist_element.text.replace('Setlist', '').strip() if artist_element else \"Artist not found\"\n",
    "\n",
    "    date_location_element = soup.find('div', class_='dateBlock')\n",
    "    date_location = ' '.join(date_location_element.text.split()) if date_location_element else \"Date and location not found\"\n",
    "\n",
    "    location_name = soup.select_one('a[title^=\"More setlists from\"] > span').text.strip()\n",
    "    \n",
    "\n",
    "    start_time_element = soup.find('div', class_='mainTime', string=lambda t: \"PM\" in t or \"AM\" in t)\n",
    "    start_time = start_time_element.text.strip() if start_time_element else \"Start time not found\"\n",
    "    \n",
    "\n",
    "    tour_avg_duration_element = soup.find('div', class_='mainTime', string=lambda t: \"h\" in t and \"m\" in t)\n",
    "    tour_avg_duration = tour_avg_duration_element.text.strip() if tour_avg_duration_element else \"Tour duration not found\"\n",
    "\n",
    "    songs_elements = soup.find('ol', class_='songsList')\n",
    "    songs = []\n",
    "    if songs_elements:\n",
    "        for li in songs_elements.find_all('li', recursive=False):\n",
    "            song_part = li.find('div', class_='songPart')\n",
    "            if song_part:\n",
    "                song_title = song_part.text.strip()\n",
    "                songs.append(song_title)\n",
    "            else:\n",
    "                tape_part = li.find('div', class_='songTooltip')\n",
    "                if tape_part:\n",
    "                    tape_title = tape_part.text.strip()\n",
    "                    songs.append(tape_title)\n",
    "\n",
    "    data = {\n",
    "        'Artist': artist.split('\\n')[0],\n",
    "        'Date and Location': date_location,\n",
    "        'Location Name': location_name,\n",
    "        'Start Time': start_time,\n",
    "        'Tour Average Duration': tour_avg_duration,\n",
    "        'Songs': songs,\n",
    "    }\n",
    "    \n",
    "    return pd.DataFrame([data])\n",
    "\n",
    "\n",
    "\n",
    "url = 'https://www.setlist.fm/setlist/morgan-wallen/2024/lucas-oil-stadium-indianapolis-in-5bab1778.html'\n",
    "data_frame = fetch_setlist_data(url)\n",
    "print(data_frame)\n",
    "\n",
    "driver.quit()\n",
    "\n",
    "\n",
    "exploded_df = data_frame.explode('Songs')\n",
    "\n",
    "exploded_df.to_csv('setlist_data.csv', index=False)\n",
    "\n",
    "print(\"CSV file has been updated with the latest detailed data.\")\n",
    "\n"
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
