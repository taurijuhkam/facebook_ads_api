### Environment setup
1. Installed virtualenv and virtualenv wrapper
2. workon facebook_ads_api
3. pip3 install -r requirements.txt


### Getting the required credentials
1. Register an app at https://developers.facebook.com/
2. Enable all migrations in the App's Settings--> Advanced--> Migrations page.
3. Turn on 'Require App Secret' in your app's Settings--> Advanced page.
4. From app dashboard, get APP_ID and APP_SECRET, add these to conf.py
5. For access token - [Graph API Explorer](https://developers.facebook.com/tools/explorer) seems to give a temporary solution. Somehow need to get a permanent one...


#### Development log 29.09
- Using JSON as a configuration file. Define some basic, most used parameters, then read in JSON and overwrite them as necessary.
- Might need to write a lookup-campaign_id-by-campaing-name function for easier access to existing campaigns
- It is not exactly easy to find something in Facebook developer documentation. Spent a good time trying to find what are the valid options for Campaign.Field.objective. Apparently you can set it by
Campaign.Field.objective = getattr(Campaign.Objective, '<OBJECTIVE NAME>') and do dir(Campaign.Objective) to view all possibilities. Common ones are e.g. conversions, link_clicks, reach
- 
