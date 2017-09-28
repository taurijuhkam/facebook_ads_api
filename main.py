# -*- coding: utf-8 -*-

"""
The main module, containing the basic flow
"""
import os
import conf
from pprint import pprint as pp
from facebookads import FacebookAdsApi
from facebookads import FacebookSession
from facebookads.adobjects.adaccount import AdAccount
from facebookads.adobjects.adset import AdSet
from facebookads.adobjects.campaign import Campaign

session = FacebookSession(conf.MY_APP_ID, conf.MY_APP_SECRET, conf.MY_ACCESS_TOKEN)
api = FacebookAdsApi(session)

def get_image_files():
    """Returns a list of paths of all the images in the current directory
    
    Returns:
        list: absolute paths of images in current directory
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    images = [img for img in os.listdir(current_dir) if img[-3:] in ['jpg', 'png']]
    image_paths = [os.path.join(current_dir, img) for img in images]
    return image_paths


def main():
    pass

def stuff():


def create_campaign_test():
    """Testing out campaign creation
    """
    FacebookAdsApi.set_default_api(api)
    account = AdAccount('act_' + conf.AD_ACCOUNT_ID)
    # account_2 = AdAccount.get_my_account() # > First account associated with the user    
    # print(my_account)
    adsets = account.get_ad_sets(fields=[AdSet.Field.name])
    account.remote_read(fields=[AdAccount.Field.name])

    x = account.get_campaigns(fields=[Campaign.Field.name, Campaign.Field.status])

    campaign = Campaign(parent_id='act_' + conf.AD_ACCOUNT_ID)
    campaign.update({
        Campaign.Field.name: 'My Campaign',
        Campaign.Field.objective: Campaign.Objective.link_clicks,
    })

    campaign.remote_create(params={
        'status': Campaign.Status.paused,
    })



if __name__ == '__main__':
    main()
