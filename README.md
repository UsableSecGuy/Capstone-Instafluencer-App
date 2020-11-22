# Instafluencer App

## Full Stack Nano - Capstone Project

Influencer Marketing has become a growing part of many marketing programs. The goal is to find someone with a decent-sized, highly engaged following on various social media platforms to share your product with their audience. The larger the following and higher the engagement, the more influencers will charge. Smaller businesses often have limited funds and focus on leveraging nano-influencers (1,000-10,000 followers). Smaller audiences can often mean higher engagement rates.

The goal of the Instafluencer App is to allow marketers to search for Instagram nano-influencers with high engagement raters. Marketers can use the Instafluencer App to search Instagram bios for hashtags related to their campaign. Influencers generally charge $10 per 1000 followers they have. The marketers we are targeting as users have budget of $20 per post. This means that all results should have a less than 2,500 followers in the [SearchMyBio.com](www.SearchMyBio.com) database.

Note: The number of followers an influencer currently has may differ from what they had when stored in the SearchMyBio.com database.

The Instafluencer application:

1. Searches its own or the SearchMyBio.com database for Instafluencers by hashtag with less than 2,500 followers.
2. Save lists of Instafluencers.
3. Present Instafluencers in order of highest engagement.


## About the Stack

There is a full backend (due to time, a frontend will be added at a later date). It is designed with some key functional areas:

### Backend

The `./backend` directory contains a completed Flask server with a written SQLAlchemy module, required endpoints, configure, and integrate Auth0 for authentication.

[View the README.md within ./backend for more details.](./backend/README.md)
